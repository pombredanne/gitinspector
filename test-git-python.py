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
print("Last five commits : ")
for i in range(0,5):
    print("{0} ({1} <{2}>)".format(commits[i],
                                    commits[i].author.name,
                                    commits[i].author.email))
    print("{0} : {1}".format(commits[i].committed_datetime,
                             commits[i].message.strip()))
    for f in commits[i].stats.files:
        print("- {0} ({1})".format(f.ljust(45), commits[i].stats.files[f]))

# Gitinspector commits contain :
# - sha
# - author
# - email
# - timestamp (used to sort commits)
# - date      (used in the TimelineData)
# - filediffs (basically a list of [name, insertions, deletions])

tree = repo.heads.master.commit.tree
# print(tree.trees) # subdirectories
# print(tree.blobs) # simple files
all_files = list(tree.traverse())
print("Number of files in repository : {0}".format(len(all_files)))
# for f in all_files:
#     print(f.path)

file = tree[0]
print("Displaying blames on '{0}' : ".format(file.path))
blames = repo.blame(repo.head, file.path)
blame_authors = set([ b[0].author for b in blames])
for a in blame_authors:
    lines = sum([ len(b[1]) for b in blames if b[0].author == a ])
    print("{0} : {1}".format(str(a).ljust(20),lines))

# Gitinspector blames contain
# - author
# - file
# - rows
# - skew (computed in blame.py for code average age)
# - comments (computed in blame.py for comment lines)
