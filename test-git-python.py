#!/usr/bin/env python3

import git
import sys

if (len(sys.argv) != 2):
    print("Usage : {0} <repository>".format(sys.argv[0]))
    sys.exit(1)
repo = git.Repo(sys.argv[1])
commits = list(repo.iter_commits('--all'))

print("Repository : {0}".format(repo))
print("Commits : {0}".format(len(commits)))
print("Last ten commits : ")
for i in range(0,10):
    print("{0} ({1}) : {2}".format(commits[i],
                                   commits[i].author,
                                   commits[i].message.strip()))
    for f in commits[i].stats.files:
        print("- {0} ({1}".format(f, commits[i].stats.files[f]))

tree = repo.heads.master.commit.tree
# print(tree.trees) # subdirectories
# print(tree.blobs) # simple files
all_files = list(tree.traverse())
for f in all_files:
    print(f.path)

file = tree['gitinspector/gitinspector.py']
blames = repo.blame(repo.head, file.path)
for b in blames:
    commit = b[0]
    code = b[1][0]
    print("{0}\t{1}".format(str(commit.author).ljust(20),code))
