#!/usr/bin/env python3

import argparse
import ast
import subprocess
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
    query = int(input("> "))
    if (query <= 0) or (query > n):
        raise ValueError
    return query


def __query_string__(prompt):
    return input(prompt)


def __alias_author__(authors, name, alias):
    for k, v in authors.items():
        if v == name:
            authors[k] = alias
    authors[name] = alias


def __list_authors__(authors):
    for auth, renm in authors.items():
        sys.stdout.write("- " + str(auth))
        if (renm != auth):
            sys.stdout.write(" -> " + str(renm))
        print("")

    print("")


def __input_rename__(authors):
    print("Select an author : ")
    itms = list(authors.items())
    for i, opt in enumerate(itms):
        print(str(i+1) + ") " + str(opt[0]))
    print("")
    query = __query_number__(len(itms))
    name = __query_string__("Name : ")
    __alias_author__(authors, itms[query-1][0], name)
    print("")


def __input_merge__(authors):
    print("Select an author to be merged : ")
    itms = list(authors.items())
    for i, opt in enumerate(itms):
        print(str(i+1) + ") " + str(opt[0]))
    print("")
    query_from = __query_number__(len(authors))
    print("Select an author to merge to : ")
    for i, opt in enumerate(itms):
        print(str(i+1) + ") " + str(opt[0]))
    print("")
    query_to = __query_number__(len(authors))
    if query_to == query_from:
        return
    __alias_author__(authors, itms[query_from-1][0], itms[query_to-1][0])
    print("")


def __initialize_authors__(repository):
    config_cmd = subprocess.Popen(["git", "-C", repository.location,
                                   "config", "inspector.aliases"],
                                  bufsize=1, stdout=subprocess.PIPE)
    config = config_cmd.stdout.readlines()
    config_cmd.wait()
    config_cmd.stdout.close()

    if config:
        if len(config) > 1:
            raise "Invalid config"
        dict = ast.literal_eval(config[0].decode("utf-8", "replace").strip())
        return dict
    else:
        return { a: a for a in repository.authors() }


def __finalize__(authors, repository):
    config_cmd = subprocess.Popen(["git", "-C", repository.location,
                                   "config", "inspector.aliases", str(authors)],
                                  bufsize=1, stdout=subprocess.PIPE)
    config_cmd.wait()
    config_cmd.stdout.close()

    sys.exit(0)


def main():
    opts = __parse_arguments__()
    repo = gitinspector.__get_validated_git_repos__([opts.repository])[0]
    authors = __initialize_authors__(repo)
    print("Managing options for repository " + str(repo.name) + " opts=" + str(opts) + "\n")

    while True:
        try:
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
        except ValueError:
            print("That's not a valid option !\n")
        except EOFError:
            print("")
            sys.exit(0)



if __name__ == "__main__":
    main()
