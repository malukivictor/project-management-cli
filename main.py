import argparse
import sys

from models import User
from utils import storage


def add_user(args):
    print("Added user:", User.create(args.name, args.email))
    return True


def list_users(args):
    for user in User.all():
        print(user)


def build_parser():
    parser = argparse.ArgumentParser(prog="main.py", description="Project tracker")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    p = sub.add_parser("add-user", help="create a user")
    p.add_argument("--name", required=True, help="user's name")
    p.add_argument("--email", default="", help="user's email (optional)")
    p.set_defaults(func=add_user)

    p = sub.add_parser("list-users", help="list all users")
    p.set_defaults(func=list_users)

    return parser


def main():
    args = build_parser().parse_args()
    storage.load()
    try:
        if args.func(args):
            storage.save()
    except ValueError as e:
        print("Error:", e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())