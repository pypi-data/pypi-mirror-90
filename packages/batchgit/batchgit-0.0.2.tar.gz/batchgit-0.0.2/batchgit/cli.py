#!/usr/bin/env python3

import argparse
import git
import os
import sys
import yaml

exit_code = 0

def config_home():
    return os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config')


def read_repo_paths():
    config_file = os.path.join(config_home(), 'batchgit', 'config.yaml')
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
            return config["repos"]
    except:
        print("Failed to read", config_file, file=sys.stderr)
        exit(1)


def show_status():
    for path in read_repo_paths():
        try:
            repo = git.Repo(path)
            if repo.is_dirty(untracked_files=True):
                print(path, "(dirty)")
                for item in repo.index.diff(None):
                    print("  *\t", item.a_path)
                for item in repo.untracked_files:
                    print("\t", item)
            else:
                print(path, "(clean)")
        except:
            print(path, "(error)", file=sys.stderr)
            exit_code = 1


def pull():
    for path in read_repo_paths():
        try:
            repo = git.Repo(path)
            g = repo.git
            g.pull()
            print("Finished processing: ", path)
        except:
            print("Error processing: ", path, file=sys.stderr)
            exit_code = 1


def push():
    for path in read_repo_paths():
        try:
            repo = git.Repo(path)
            g = repo.git
            g.push()
            print("Finished processing: ", path)
        except:
            print("Error processing: ", path, file=sys.stderr)
            exit_code = 1


def main():
    argp = argparse.ArgumentParser(description="Manage multiple git repos")
    argp.add_argument("command", nargs="?", help="action to take", default="help")
    args = argp.parse_args()
    action = {"status": show_status, "pull": pull, "push": push}.get(
        args.command, argp.print_help
    )
    action()
    exit(exit_code)


if __name__ == "__main__":
    main()
