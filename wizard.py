#!/usr/bin/env python3

import argparse
import os
import sys

from gitinspector import gitinspector


class Task(object):
    def __init__(self, str, action):
        self.str = str
        self.action = action

    def act(self):
        self.action()

def __parse_arguments__():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=_("Prepare the analysis of REPOSITORY."))
    parser.add_argument('repository', metavar='REPOSITORY', type=str,
                        help=_('the address of a repository to be analyzed'))

    namespace = parser.parse_args()
    return namespace


def __query_number__(n):
    try:
        query = int(input("> "))
        if (query <= 0) or (query > n):
            raise ValueError
        return query
    except ValueError:
        print("That's not a valid option !\n")
        __query_number__(n)
    except EOFError:
        print("")
        sys.exit(0)


def __query_string__(prompt):
    return input(prompt)


def __list_authors__(authors):
    for (auth, renm) in authors:
        sys.stdout.write("- " + str(auth))
        if (renm != auth):
            sys.stdout.write(" -> " + str(renm))
        print("")

    print("")


def __input_rename__(authors):
    print("Select an author : ")
    for i, opt in enumerate(authors):
        print(str(i+1) + ") " + str(authors[i][1]))
    print("")
    query = __query_number__(len(authors))
    name = __query_string__("Name : ")
    authors[query-1] = (authors[query-1][0], name)
    print("")


def __input_merge__(authors):
    print("Select an author to be merged : ")
    for i, opt in enumerate(authors):
        print(str(i+1) + ") " + str(authors[i][1]))
    print("")
    query_from = __query_number__(len(authors))
    print("Select an author to merge to : ")
    for i, opt in enumerate(authors):
        print(str(i+1) + ") " + str(authors[i][1]))
    print("")
    query_to = __query_number__(len(authors))
    if query_to == query_from:
        return
    authors[query_from-1] = (authors[query_from-1][0], authors[query_to-1][0])
    print("")


def __finalize__(authors, repository):
    mailmap_file = os.path.join(repository.location, ".mailmap")
    with open(mailmap_file, "w") as f:
        for (auth, renm) in authors:
            f.write(str(auth) + " " + str(renm) + "\n")
        sys.exit(0)

def main():
    opts = __parse_arguments__()
    repo = gitinspector.__get_validated_git_repos__([opts.repository])[0]
    authors = [(a,a) for a in repo.authors()]
    print("Managing options for repository " + str(repo.name) + " opts=" + str(opts) + "\n")

    while True:
        tasks = [
            Task("List authors", lambda: __list_authors__(authors)),
            Task("Rename an author", lambda: __input_rename__(authors)),
            Task("Merge two authors", lambda: __input_merge__(authors)),
            Task("Dump config and exit", lambda: __finalize__(authors, repo)),
        ]
        for i, opt in enumerate(tasks):
            print(str(i+1) + ") " + opt.str)
        print("")
        query = __query_number__(len(tasks))
        print(str(query))
        print("")
        # os.system('clear')
        tasks[query-1].act()


if __name__ == "__main__":
    main()
