#!/usr/bin/env python
"""Check MySQL seconds behind master for Nagios-like monitoring."""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from argparse import ArgumentParser
import sys

try:
    from MySQLdb import connect
except ImportError:
    pass


DESCRIPTION = "Check MySQL seconds behind master for Nagios-like monitoring."


def get_slave_status(host, user, passwd, port):
    """Returns a dictionary of the 'SHOW SLAVE STATUS;' command output."""
    try:
        conn = connect(user=user, passwd=passwd, host=host, port=port)
    except NameError:
        print("Failed to import MySQLdb. Is mysqlclient installed?")
        sys.exit(3)
    except BaseException:  # pylint: disable=broad-except
        print("Failed to connect.")
        sys.exit(3)
    cur = conn.cursor()
    cur.execute("""SHOW SLAVE STATUS;""")
    keys = [desc[0] for desc in cur.description]
    values = cur.fetchone()
    return dict(zip(keys, values))


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "-u", "--user", help="Login username", required=True, nargs="?"
    )
    parser.add_argument(
        "-p", "--password", help="Login password", required=True, nargs="?"
    )
    parser.add_argument(
        "--host", help="Login host", nargs="?", default="localhost"
    )
    parser.add_argument(
        "--port", help="Login port", nargs=1, type=int, default=3306
    )
    parser.add_argument(
        "warning_threshold",
        help="Warning threshold (defaults to 60)",
        default=60,
        type=int,
        nargs="?",
    )
    parser.add_argument(
        "critical_threshold",
        help="Critical threshold (defualts to 300)",
        default=300,
        type=int,
        nargs="?",
    )
    args = parser.parse_args()
    status = get_slave_status(
        host=args.host, user=args.user, passwd=args.password, port=args.port
    )
    if (
        "Slave_IO_Running" not in status
        or "Slave_SQL_Running" not in status
        or status["Slave_IO_Running"] != "Yes"
        or status["Slave_SQL_Running"] != "Yes"
    ):
        print("Replication is turned off.")
        sys.exit(0)
    lag = status["Seconds_Behind_Master"]
    if lag > args.critical_threshold:
        print("Seconds behind master is above the critical threshold.")
        sys.exit(2)
    elif lag > args.warning_threshold:
        print("Seconds behind master is above the warning threshold.")
        sys.exit(1)
    else:
        print("Seconds behind master is below the warning threshold.")
        sys.exit(0)


if __name__ == "__main__":
    main()
