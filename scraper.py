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


from hubster.models import GithubUser
from hubster.serializers import GithubRepoSerializerWithId, GithubUserSerializer

USER_URL_BASE = "https://api.github.com/users"
USER_REPO_TEMPLATE = Template("https://api.github.com/user/$user/repos")


async def scrapeUsers(session: aiohttp.ClientSession, startId: int = None) -> None:
    if not startId:
        maxId = GithubUser.objects.values("id").order_by("-id").first()
        startId = maxId.get("id")  # In case the

    queryArgs = {"since": startId} if startId else {}

    usersUrl = furl(USER_URL_BASE).add(queryArgs).url
    async with session.get(usersUrl) as resp:
        # print(resp.status)
        users = json.loads(await resp.text())
        for i, user in enumerate(users):
            print(i)
            githubUser = GithubUserSerializer(data=user)
            print(githubUser.is_valid())
            print(githubUser.errors)
            print(githubUser.validated_data)
            print("\n\n")


async def scrape(
    session: aiohttp.ClientSession,
    concurrency: int,
    buffer: int,
    quantity: int,
    startId: int = None,
) -> None:
    await scrapeUsers(session, startId)


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
        "-b",
        "--buffer",
        action="store",
        dest="buffer",
        default=20,
        type=int,
        help="Number of items to queue before writing to the database",
    )
    parser.add_argument(
        "-q",
        "--quantity",
        action="store",
        dest="quantity",
        default=3,
        type=int,
        help="Total number of users to scrape before quitting",
    )
    parser.add_argument(
        "-s",
        "--start",
        action="store",
        dest="quantity",
        type=int,
        help="User ID to start scraping repos from (exclusive), e.g., 46 will start scraping at 47. By default, it will start from the max ID in the database.",
    )

    args = vars(parser.parse_args())

    conn = aiohttp.TCPConnector(limit=3)
    async with aiohttp.ClientSession(connector=conn, loop=loop) as session:
        await scrape(session, **args)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

