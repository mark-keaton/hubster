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
from pathlib import Path
from string import Template

import aiohttp
from furl import furl
from typing import Any, Dict, List, Optional


from hubster.models import GithubUser, GithubRepo, License
from hubster.serializers import (
    GithubRepoSerializerWithId,
    GithubUserSerializer,
    LicenseSerializer,
)

USER_URL_BASE = "https://api.github.com/users"
USER_REPO_TEMPLATE = Template("https://api.github.com/users/$user/repos")


def build_license_dict() -> Dict[str, int]:
    licenses = License.objects.all()
    if len(licenses) != 13:
        licenses.delete()
        with Path("licenses.json").open() as infile:
            license_list = json.loads(infile.read())
            for license in license_list:
                serializer = LicenseSerializer(data=license)
                serializer.is_valid()
                serializer.save()

    licenses = License.objects.values("id", "key")
    return {license["key"]: license["id"] for license in licenses}


def flatten(t: list) -> list:
    return [item for sublist in t for item in sublist]


async def save_repo(
    license_dict: Dict[str, int], user_id: int, repo_json: dict = {}
) -> None:
    license = repo_json.get("license")
    license_key = license.get("key", "no-license") if license else "no-license"
    license_id = license_dict.get(license_key, 13)  # Default to no-license selected
    repo_json["owner"] = user_id
    repo_json["license"] = license_id
    github_repo = GithubRepoSerializerWithId(data=repo_json, partial=True)
    if github_repo.is_valid():
        repo = github_repo.save()
    else:
        error_dict = {key: repo_json[key] for key in github_repo.errors}
        print("Unable to save repo!")
        print(f"Errors: {github_repo.errors}")
        print(f"Invalid data: {error_dict}")
        print("\n")


async def scrapeUserRepos(
    session: aiohttp.ClientSession, license_dict: Dict[str, int], user_json: dict
) -> List[Any]:
    github_user = GithubUserSerializer(data=user_json)
    tasks: List = []
    if github_user.is_valid():
        user = github_user.save()
        repos_url = USER_REPO_TEMPLATE.substitute({"user": user.login})
        while True:
            async with session.get(repos_url) as resp:
                if not resp.links.get("next") or not resp.links.get("next").get("url"):
                    break
                repos = json.loads(await resp.text())
                tasks.extend(
                    [
                        asyncio.create_task(save_repo(license_dict, user.id, repo))
                        for repo in repos
                    ]
                )
            repos_url = resp.links.get("next").get("url")
    else:
        print("Unable to save user!")
        print(f"Errors: {github_user.errors}")
        print(f"Data was {github_user.validated_data}")
        print("\n")

    return tasks


async def scrapeUsers(
    session: aiohttp.ClientSession,
    license_dict: Dict[str, int],
    quantity: int,
    start_id: Optional[int] = None,
) -> List[Any]:
    if not start_id:
        max_id = GithubUser.objects.values("id").order_by("-id").first()
        start_id = max_id.get("id") if max_id else None

    query_args = {"since": start_id} if start_id else {}

    users_url = furl(USER_URL_BASE).add(query_args).url
    async with session.get(users_url) as resp:
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
        default=2,
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

