#!/usr/bin/env python
"""
Transforms Heroku-style database URLs into shell environment variables.
"""

import click

SCHEMES = (
    "postgresql",
    "postgres",
    "postgis",
    "psql",
)


@click.command()
@click.argument("database_url")
@click.option("--prefix", default="PG")
def main(database_url, prefix):
    from os.path import basename
    from sys import argv

    try:
        from urllib.parse import urlparse
    except ImportError:
        from urlparse import urlparse

    def psql_envs(conn):
        env_map = {
            "user": f"{prefix}USER",
            "pass": f"{prefix}PASSWORD",
            "host": f"{prefix}HOST",
            "port": f"{prefix}PORT",
            "db": f"{prefix}DATABASE",
        }
        return dict((env_map[k], v) for k, v in conn.items() if v)

    def to_envs(url):
        assert url.scheme in SCHEMES, "unsupported URL scheme: %s" % url.scheme
        conn = {
            "user": url.username,
            "pass": url.password,
            "host": url.hostname,
            "port": url.port,
            "db": url.path[1:],
        }
        return psql_envs(conn)

    def format_envs(envs):
        return "\n".join("%s=%s" % (k, v) for k, v in envs.items())

    def _exit_with_usage():
        print("usage: %s <url>" % basename(argv[0]))
        exit(1)

    try:
        url = argv[1]
    except IndexError:
        _exit_with_usage()
    print(format_envs(to_envs(urlparse(url))))


if __name__ == "__main__":
    main.main()
