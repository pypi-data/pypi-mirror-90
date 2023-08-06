#!/usr/bin/env python
"""
Transforms database URLs into shell environment variables.
"""
import click


@click.command()
@click.argument("database_url")
@click.option("--prefix", default="PG")
@click.option("--export", is_flag=True)
@click.option("--engine", is_flag=True)
def main(database_url, prefix, export, engine):
    from urllib.parse import urlparse

    def to_envs(url):
        result = [
            ("HOST", url.hostname),
            ("PORT", url.port),
            ("USER", url.username),
            ("PASSWORD", url.password),
            ("DATABASE", url.path[1:]),
        ]
        if engine:
            result.insert(0, ("ENGINE", url.scheme))
        return tuple(result)

    if export:
        prefix = f"export {prefix}"

    urlparse(database_url)

    for k, v in to_envs(urlparse(database_url)):
        if not v:
            continue
        print(f"{prefix}{k}={v}")


if __name__ == "__main__":
    main.main()
