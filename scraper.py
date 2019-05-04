#!/usr/bin/env python

import aiohttp
import argparse
import asyncio
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hubster.settings")
django.setup()

from hubster.serializers import GithubRepoSerializerWithId


async def scrape(concurrency, buffer, quantity) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.github.com/events") as resp:
            print(resp.status)
            print(await resp.text())


async def main() -> None:
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
        default=100,
        type=int,
        help="Total number of repos to scrape before quitting",
    )

    args = vars(parser.parse_args())
    await scrape(**args)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

