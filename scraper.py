#!/usr/bin/env python

### Start: Initialize Django
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hubster.settings")
django.setup()
### End Initialize Django

import argparse
import asyncio
import io
import json
from string import Template

import aiohttp
from furl import furl
from rest_framework.parsers import JSONParser
from typing import Any, Dict, List, Optional


from hubster.models import GithubUser, GithubRepo, License
from hubster.serializers import GithubRepoSerializerWithId, GithubUserSerializer

USER_URL_BASE = "https://api.github.com/users"
USER_REPO_TEMPLATE = Template("https://api.github.com/users/$user/repos")


def build_license_dict() -> Dict[str, int]:
    licenses = License.objects.values("id", "key")
    return {license["key"]: license["id"] for license in licenses}


def flatten(t: list) -> list:
    return [item for sublist in t for item in sublist]


async def save_repo(
    license_dict: Dict[str, int], user_id: int, repo_json: dict = {}
) -> None:
    license_key = repo_json.get("license", {}).get("key", "")
    license_id = license_dict.get(license_key)
    repo_json["owner"] = user_id
    repo_json["license"] = license_id
    githubRepo = GithubRepoSerializerWithId(data=repo_json)
    if githubRepo.is_valid():
        repo = githubRepo.save()
    else:
        print("Unable to save repo!")
        print(f"Errors: {githubRepo.errors}")
        print(f"Data was {githubRepo.validated_data}")
        print("\n\n")


async def scrapeUserRepos(
    session: aiohttp.ClientSession, license_dict: Dict[str, int], user_json: dict
) -> List[Any]:
    github_user = GithubUserSerializer(data=user_json)
    tasks: List = []
    if github_user.is_valid():
        user = github_user.save()
        reposUrl = USER_REPO_TEMPLATE.substitute({"user": user.login})
        async with session.get(reposUrl) as resp:
            repos = json.loads(await resp.text())
            print(f"repos: {repos}")
            tasks.extend(
                [
                    asyncio.create_task(save_repo(license_dict, user.id, repo))
                    for repo in repos
                ]
            )
    else:
        print("Unable to save user!")
        print(f"Errors: {github_user.errors}")
        print(f"Data was {github_user.validated_data}")
        print("\n\n")

    return tasks


async def scrapeUsers(
    session: aiohttp.ClientSession,
    license_dict: Dict[str, int],
    quantity: int,
    start_id: Optional[int] = None,
) -> List[Any]:
    if not start_id:
        maxId = GithubUser.objects.values("id").order_by("-id").first()
        startId = maxId.get("id") if maxId else None

    queryArgs = {"since": startId} if start_id else {}

    usersUrl = furl(USER_URL_BASE).add(queryArgs).url
    async with session.get(usersUrl) as resp:
        users = json.loads(await resp.text())
        return flatten(
            [
                await scrapeUserRepos(session, license_dict, user)
                for user in users[:quantity]
            ]
        )


async def scrape(
    session: aiohttp.ClientSession, quantity: int, start_id: Optional[int] = None
) -> None:
    license_dict = build_license_dict()
    await asyncio.gather(scrapeUsers(session, license_dict, quantity, start_id))


async def main(loop: asyncio.AbstractEventLoop) -> None:
    parser = argparse.ArgumentParser(description="Hubster Github scraper")

    parser.add_argument(
        "-c",
        "--concurrency",
        action="store",
        dest="concurrency",
        default=5,
        type=int,
        help="Number of concurrent connections to scrape with",
    )
    parser.add_argument(
        "-q",
        "--quantity",
        action="store",
        dest="quantity",
        default=1,
        type=int,
        help="Total number of users to scrape before quitting",
    )
    parser.add_argument(
        "-s",
        "--start",
        action="store",
        dest="start_id",
        type=int,
        help="User ID to start scraping repos from (exclusive), e.g., 46 will start scraping at 47. By default, it will start from the max ID in the database.",
    )

    parsed = parser.parse_args()

    conn = aiohttp.TCPConnector(limit=parsed.concurrency)
    auth = aiohttp.BasicAuth(
        login=os.environ.get("GITHUB_LOGIN"), password=os.environ.get("GITHUB_PASSWORD")
    )
    async with aiohttp.ClientSession(connector=conn, loop=loop, auth=auth) as session:
        await scrape(
            session=session, quantity=parsed.quantity, start_id=parsed.start_id
        )


if __name__ == "__main__":
    GithubUser.objects.all().delete()
    GithubRepo.objects.all().delete()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

