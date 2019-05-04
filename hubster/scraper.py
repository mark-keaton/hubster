import argparse


def main() -> None:
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
        default=100,
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

    print(parser.parse_args(["--concurrency", "33"]))


if __name__ == "__main__":
    main()

