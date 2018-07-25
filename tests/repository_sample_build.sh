#!/usr/bin/env bash

# git_commit AUTHOR_NAME AUTHOR_EMAIL COMMIT_DATE COMMIT_MSG
function git_commit {
    GIT_COMMITTER_NAME="${1}" GIT_COMMITTER_EMAIL="${2}" GIT_COMMITTER_DATE="${3}" git commit --allow-empty-message --author "${1} <${2}>" --date "${3}" -m "${4}"
}

PROJECT_DIR=sample-01

BILBO_NAME="Bilbo Baggins"
BILBO_MAIL="bilbo.baggins@shire.net"

# git_bilbo COMMIT_DATE COMMIT_MSG
function git_bilbo_commit {
    git_commit "${BILBO_NAME}" "${BILBO_MAIL}" "${1}" "${2}"
}

FRODO_NAME="Frodo Baggins"
FRODO_MAIL="frodo.baggins@shire.net"

# git_frodo COMMIT_DATE COMMIT_MSG
function git_frodo_commit {
    git_commit "${FRODO_NAME}" "${FRODO_MAIL}" "${1}" "${2}"
}

MERRY_NAME="Meriadoc Brandybuck"
MERRY_MAIL="merry@gmail.com"

# git_merry COMMIT_DATE COMMIT_MSG
function git_merry_commit {
    git_commit "${MERRY_NAME}" "${MERRY_MAIL}" "${1}" "${2}"
}

PIPPIN_NAME="Peregrin Took"
PIPPIN_MAIL="pippin@outlook.com"

# git_pippin COMMIT_DATE COMMIT_MSG
function git_pippin_commit {
    git_commit "${PIPPIN_NAME}" "${PIPPIN_MAIL}" "${1}" "${2}"
}

SAM_NAME="Samwise Gamgee"
SAM_MAIL="samwise.gamgee@shire.net"

# git_sam COMMIT_DATE COMMIT_MSG
function git_sam_commit {
    git_commit "${SAM_NAME}" "${SAM_MAIL}" "${1}" "${2}"
}

##### Check if repository exists #####
if [ -d "$PROJECT_DIR" ]; then
    echo "error: repository '${PROJECT_DIR}' already exists!"
    exit 1
fi

##### Repository creation #####
mkdir ${PROJECT_DIR}
cd ${PROJECT_DIR}
git init .

##### Initial commit (README) #####
cat > README <<EOF
This is a README file for the project!

Authors:
Bilbo Baggins <bilbo.baggins@shire.net>
Frodo Baggins <frodo.baggins@shire.net>
Meriadoc Brandybuck <merry@gmail.com>
Peregrin Took <pippin@outlook.com>
Samwise Gamgee <samwise.gamgee@shire.net>
EOF

# Adding the files to commit
git add README

# git_frodo_commit COMMIT_DATE COMMIT_MSG
git_frodo_commit "Sat, 17 Oct 2015 16:37:13" "Initial commit"

##### Commit (library interface) #####
mkdir include

cat > include/trie.h <<EOF
#ifndef TRIE_H
#define TRIE_H

/* Default number of the number of children in trie node */
#define TRIE_CHILDREN         4

/* Mark the end of the data-structure */
#define TRIE_NOT_LAST         -1

/* Tries data-structure definition */
struct trie;
typedef struct
{
  int symb;
  ssize_t last;
  struct trie *next;
} child_t;

typedef struct
{
  unsigned int children_size;
  unsigned int children_count;
  struct child *  children;
} trie_t;

/* Create a new trie node */
trie_t *trie_allocate (void);

/* Free the memory of the whole trie */
void trie_free (trie_t *);

/* Add a new word in the trie */
void trie_add_word (trie_t *, const char *, size_t, ssize_t);

/* Search the trie for a word */
ssize_t trie_search (trie_t *, const char *, size_t);

/* Search the trie for a given prefix */
trie_t * trie_check_prefix (trie_t *, const char *, size_t, ssize_t *);

/* Display the content of the trie */
void trie_print (trie_t *);

#endif /* TRIE_H */
EOF

# Adding the files to commit
git add include/trie.h

# git_commit COMMIT_DATE COMMIT_MSG
git_frodo_commit "Sun, 18 Oct 2015 12:40:22" "Setting the interface of the trie data-structure"

##### Commit (mask implementation) #####
mkdir src

cat > src/trie.c <<EOF
#include "trie.h"

#include <stdio.h>
#include <stdlib.h>

#include <assert.h>
#include <string.h>

/* Default number of the number of children in trie node */
#define TRIE_CHILDREN         4

/* Private definition of the data-structure */
typedef struct
{
  int symb;
  ssize_t last;
  trie_t *next;
} child_t;

struct trie_t
{
  unsigned int children_size;
  unsigned int children_count;
  child_t *children;
};
EOF

cat > patch.diff <<EOF
diff --git a/include/trie.h b/include/trie.h
index b5f44e6..22b6990 100644
--- a/include/trie.h
+++ b/include/trie.h
@@ -1,30 +1,17 @@
 #ifndef TRIE_H
 #define TRIE_H
 
-/* Default number of the number of children in trie node */
-#define TRIE_CHILDREN         4
+#include <stddef.h>
+#include <sys/types.h>
 
 /* Mark the end of the data-structure */
 #define TRIE_NOT_LAST         -1
 
-/* Tries data-structure definition */
-struct trie;
-typedef struct
-{
-  int symb;
-  ssize_t last;
-  struct trie *next;
-} child_t;
-
-typedef struct
-{
-  unsigned int children_size;
-  unsigned int children_count;
-  struct child *  children;
-} trie_t;
+/* Tries data-structure forward definition */
+typedef struct trie_t trie_t;
 
 /* Create a new trie node */
-trie_t *trie_allocate (void);
+trie_t *trie_alloc (void);
 
 /* Free the memory of the whole trie */
 void trie_free (trie_t *);
@@ -36,7 +23,7 @@ void trie_add_word (trie_t *, const char *, size_t, ssize_t);
 ssize_t trie_search (trie_t *, const char *, size_t);
 
 /* Search the trie for a given prefix */
-trie_t * trie_check_prefix (trie_t *, const char *, size_t, ssize_t *);
+trie_t *trie_check_prefix (trie_t *, const char *, size_t, ssize_t *);
 
 /* Display the content of the trie */
 void trie_print (trie_t *);
EOF

git apply patch.diff
rm -f patch.diff

git add include/trie.h src/trie.c

git_bilbo_commit "Mon, 19 Oct 2015 09:23:36" "Mask the implementation of the trie data-structure in the .c file"

##### Commit (build-system) #####

cat > Makefile <<EOF
# Commands
MAKE=make

# Special rules and targets
.PHONY:	all clean help

# Rules and targets
all:
	@cd src/ && \$(MAKE)
	@cp -f src/trie.so .

clean:
	@cd src/ && \$(MAKE) clean
	@rm -f trie.so *~

help:
	@echo "Usage:"
	@echo "  make [all]\t\tBuild the library"
	@echo "  make clean\t\tRemove all files generated by make"
	@echo "  make help\t\tDisplay this help"
EOF

cat > src/Makefile <<EOF
CFLAGS=-Wall -Wextra -std=c11 -g -O2
CPPFLAGS=-I../include
LDFLAGS=

.PHONY:	all clean help

all: trie.so

trie.so: trie.o
	\$(CC) \$(CFLAGS) -shared -o \$@ \$< \$(LDFLAGS)

trie.o: trie.c ../include/trie.h
	\$(CC) \$(CFLAGS) \$(CPPFLAGS) -c \$< 

clean:
	@rm -f *~ *.o trie.so

help:
	@echo "Usage:"
	@echo "  make [all]\t\tBuild the library"
	@echo "  make clean\t\tRemove all files generated by make"
	@echo "  make help\t\tDisplay this help"
EOF

git add Makefile src/Makefile

git_bilbo_commit "Mon, 19 Oct 2015 10:23:36" "Adding a decent minimal build-system"

##### Commit (function trie_alloc()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 3c86a1a..48bd5ac 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -23,3 +23,14 @@ struct trie_t
   unsigned int children_count;
   child_t *children;
 };
+
+trie_t *
+trie_alloc ()
+{
+  trie_t *trie= malloc(sizeof (trie_t));
+  child_t *child = malloc(TRIE_CHILDREN * sizeof (child_t));
+  trie->children_size =TRIE_CHILDREN;
+  trie->children_count = 0;
+  trie->children = child;
+  return (trie);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_merry_commit "Mon, 19 Oct 2015 10:23:36" ""

##### Commit (adding comments and reformating) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 48bd5ac..6e2cb13 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -24,13 +24,19 @@ struct trie_t
   child_t *children;
 };
 
+
+/* Allocate a new empty trie */
 trie_t *
-trie_alloc ()
+trie_alloc (void)
 {
-  trie_t *trie= malloc(sizeof (trie_t));
-  child_t *child = malloc(TRIE_CHILDREN * sizeof (child_t));
-  trie->children_size =TRIE_CHILDREN;
+  /* Allocate the trie data-structure */
+  trie_t *trie = malloc (sizeof (trie_t));
+  child_t *child = malloc (TRIE_CHILDREN * sizeof (child_t));
+
+  /* Initializing the trie data-structure */
+  trie->children_size = TRIE_CHILDREN;
   trie->children_count = 0;
   trie->children = child;
-  return (trie);
+
+  return trie;
 }
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_frodo_commit "Mon, 19 Oct 2015 10:54:48" "Adding comments and reformating a bit"

##### Commit (Checking return code of malloc()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 6e2cb13..f1c8783 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -29,9 +29,18 @@ struct trie_t
 trie_t *
 trie_alloc (void)
 {
-  /* Allocate the trie data-structure */
+  /* Allocate trie data-structure */
   trie_t *trie = malloc (sizeof (trie_t));
+  if (!trie)
+    return NULL;
+
+  /* Allocate child data-structure */
   child_t *child = malloc (TRIE_CHILDREN * sizeof (child_t));
+  if (!child)
+    {
+      free (trie);
+      return NULL;
+    }
 
   /* Initializing the trie data-structure */
   trie->children_size = TRIE_CHILDREN;
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Mon, 19 Oct 2015 11:15:26" "Checking return code of malloc()"

##### Commit (function trie_free())) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index f1c8783..87b1aee 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -49,3 +49,12 @@ trie_alloc (void)
 
   return trie;
 }
+
+void
+trie_free (trie_t trie)
+{
+  int i;
+  for (i = 0; i < trie->children_count; i++)
+    trie_free (trie->children[i].next);
+  free (trie);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_merry_commit "Mon, 19 Oct 2015 15:15:26" ""

##### Commit (Fixing typo in trie_free() signature) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 87b1aee..8acb3e8 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -51,7 +51,7 @@ trie_alloc (void)
 }
 
 void
-trie_free (trie_t trie)
+trie_free (trie_t *trie)
 {
   int i;
   for (i = 0; i < trie->children_count; i++)
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_merry_commit "Mon, 19 Oct 2015 15:18:53" "Sorry!"

##### Commit (Reformating to conform to C11 standard) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 8acb3e8..eeff82f 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -53,8 +53,7 @@ trie_alloc (void)
 void
 trie_free (trie_t *trie)
 {
-  int i;
-  for (i = 0; i < trie->children_count; i++)
+  for (size_t i = 0; i < trie->children_count; ++i)
     trie_free (trie->children[i].next);
   free (trie);
 }
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_frodo_commit "Mon, 19 Oct 2015 15:46:20" "Better conformance to C11 standard (Merry, be more cautious when you commit code!!!)"

##### Commit (Free trie->children) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index eeff82f..f6bb510 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -55,5 +55,9 @@ trie_free (trie_t *trie)
 {
   for (size_t i = 0; i < trie->children_count; ++i)
     trie_free (trie->children[i].next);
+
+  if (trie->children)
+    free (trie->children);
+
   free (trie);
 }
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Mon, 19 Oct 2015 17:03:32" "Fixing memory leak in trie_free()"

##### Commit (Check if trie == NULL) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index f6bb510..717c130 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -24,7 +24,6 @@ struct trie_t
   child_t *children;
 };
 
-
 /* Allocate a new empty trie */
 trie_t *
 trie_alloc (void)
@@ -53,6 +52,9 @@ trie_alloc (void)
 void
 trie_free (trie_t *trie)
 {
+  if (!trie)
+    return;
+
   for (size_t i = 0; i < trie->children_count; ++i)
     trie_free (trie->children[i].next);

EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Mon, 19 Oct 2015 17:07:18" "Handle the trie == NULL case in trie_free()"

##### Branching (Creating a branch to store trie_print()) #####

git checkout -b trie_print

##### Commit (trie_print()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 717c130..eba0daa 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -24,6 +24,7 @@ struct trie_t
   child_t *children;
 };
 
+
 /* Allocate a new empty trie */
 trie_t *
 trie_alloc (void)
@@ -63,3 +64,25 @@ trie_free (trie_t *trie)
 
   free (trie);
 }
+
+/* Private function to recursively print the trie */
+static void
+_trie_print_rec (trie_t *t, int level)
+{
+  if (!t)
+    return;
+
+  for (size_t i = 0; i < t->children_count; i++)
+    {
+      printf ("%c %s\n", (char) t->children[i].symb,
+             t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
+      _trie_print_rec (t->children[i].next, level + 1);
+    }
+}
+
+/* Wrapper for print */
+void
+trie_print (trie_t *t)
+{
+  _trie_print_rec (t, 0);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_sam_commit "Mon, 19 Oct 2015 17:08:58" "function trie_print()"

##### Commit (Added a tabification) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index eba0daa..306444f 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -65,6 +65,12 @@ trie_free (trie_t *trie)
   free (trie);
 }
 
+#define tab(n)                              \\
+  do {                                      \\
+       for (size_t __i = 0; __i < n; ++__i) \\
+         printf ("  ");                     \\
+} while (0)
+
 /* Private function to recursively print the trie */
 static void
 _trie_print_rec (trie_t *t, int level)
@@ -74,6 +80,7 @@ _trie_print_rec (trie_t *t, int level)
 
   for (size_t i = 0; i < t->children_count; i++)
     {
+      tab (level);
       printf ("%c %s\n", (char) t->children[i].symb,
              t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
       _trie_print_rec (t->children[i].next, level + 1);
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Tue, 20 Oct 2015 10:24:08" "Added a tabification to trie_print()"

##### Commit (fixing a warning from the compiler) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 90f94c5..bb8d84d 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -65,10 +65,10 @@ trie_free (trie_t *trie)
   free (trie);
 }
 
-#define tab(n)                              \\
-  do {                                      \\
-       for (size_t __i = 0; __i < n; ++__i) \\
-         printf ("  ");                     \\
+#define tab(n)                           \\
+  do {                                   \\
+       for (int __i = 0; __i < n; ++__i) \\
+         printf ("  ");                  \\
 } while (0)
 
 /* Private function to recursively print the trie */
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Tue, 20 Oct 2015 10:27:44" "Fixed a warning of the compiler"

##### Back to master (meanwhile...) #####

git checkout master

##### Commit (function trie_search_child()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 717c130..75924d9 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -63,3 +63,29 @@ trie_free (trie_t *trie)
 
   free (trie);
 }
+
+/* Helper for bsearch and qsort */
+static int
+cmp_children (const void *k1, const void *k2)
+{
+  child_t *c1 = (child_t *) k1;
+  child_t *c2 = (child_t *) k2;
+  return c1->symb - c2->symb;
+}
+
+/* Search for a symbol in a children of a certain trie.
+ * Uses binary search as the children are kept sorted */
+child_t *
+trie_search_child (trie_t *trie, int symb)
+{
+  child_t s;
+
+  if (trie->children_count == 0)
+    return NULL;
+
+  s.symb = symb;
+  return
+    (child_t *) bsearch (&s,
+                        trie->children, trie->children_count,
+                        sizeof (child_t), cmp_children);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_frodo_commit  "Mon, 19 Oct 2015 18:49:22" "function trie_search_child"

##### Commit (Reformating for C11 standard) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index c38b6dc..459d91a 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -66,17 +66,16 @@ trie_free (trie_t *trie)
 
 /* Search for a symbol in a children of a certain trie.
  * Uses binary search as the children are kept sorted */
-child_t *
+static child_t *
 trie_search_child (trie_t *trie, int symb)
 {
-  child_t s;
-
   if (trie->children_count == 0)
     return NULL;
 
-  s.symb = symb;
+  child_t s = { .symb = symb };
+
   return
     (child_t *) bsearch (&s,
-                        trie->children, trie->children_count,
-                        sizeof (child_t), cmp_children);
+                        trie->children, trie->children_count,
+                        sizeof (child_t), cmp_children);
 }
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit  "Tue, 20 Oct 2015 09:17:13" "Tag as 'static' and better conformance to C11 standards"

##### Merging trie_print to master (with conflict) #####

git merge trie_print

##### Solving the conflict #####

cat > src/trie.c <<EOF
#include "trie.h"

#include <stdio.h>
#include <stdlib.h>

#include <assert.h>
#include <string.h>

/* Default number of the number of children in trie node */
#define TRIE_CHILDREN         4

/* Private definition of the data-structure */
typedef struct
{
  int symb;
  ssize_t last;
  trie_t *next;
} child_t;

struct trie_t
{
  unsigned int children_size;
  unsigned int children_count;
  child_t *children;
};


/* Allocate a new empty trie */
trie_t *
trie_alloc (void)
{
  /* Allocate trie data-structure */
  trie_t *trie = malloc (sizeof (trie_t));
  if (!trie)
    return NULL;

  /* Allocate child data-structure */
  child_t *child = malloc (TRIE_CHILDREN * sizeof (child_t));
  if (!child)
    {
      free (trie);
      return NULL;
    }

  /* Initializing the trie data-structure */
  trie->children_size = TRIE_CHILDREN;
  trie->children_count = 0;
  trie->children = child;

  return trie;
}

void
trie_free (trie_t *trie)
{
  if (!trie)
    return;

  for (size_t i = 0; i < trie->children_count; ++i)
    trie_free (trie->children[i].next);

  if (trie->children)
    free (trie->children);

  free (trie);
}

/* Helper for bsearch and qsort */
static int
cmp_children (const void *k1, const void *k2)
{
  child_t *c1 = (child_t *) k1;
  child_t *c2 = (child_t *) k2;
  return c1->symb - c2->symb;
}

/* Search for a symbol in a children of a certain trie.
 * Uses binary search as the children are kept sorted */
static child_t *
trie_search_child (trie_t *trie, int symb)
{
  if (trie->children_count == 0)
    return NULL;

  child_t s = { .symb = symb };

  return
    (child_t *) bsearch (&s,
			 trie->children, trie->children_count,
			 sizeof (child_t), cmp_children);
}

#define tab(n)                           \\
  do {                                   \\
       for (int __i = 0; __i < n; ++__i) \\
         printf ("  ");                  \\
} while (0)

/* Private function to recursively print the trie */
static void
_trie_print_rec (trie_t *t, int level)
{
  if (!t)
    return;

  for (size_t i = 0; i < t->children_count; i++)
    {
      tab (level);
      printf ("%c %s\n", (char) t->children[i].symb,
             t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
      _trie_print_rec (t->children[i].next, level + 1);
    }
}

/* Wrapper for print */
void
trie_print (trie_t *t)
{
  _trie_print_rec (t, 0);
}
EOF

git add src/trie.c

git_bilbo_commit "Tue, 20 Oct 2015 16:39:11" "Merging the trie_print() function in master"

##### Commit (fixing a few things in the code) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 25c84e4..5493a2e 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -41,6 +41,7 @@ trie_alloc (void)
       free (trie);
       return NULL;
     }
+  memset (child, 0, TRIE_CHILDREN * sizeof (child_t));
 
   /* Initializing the trie data-structure */
   trie->children_size = TRIE_CHILDREN;
@@ -66,7 +67,7 @@ trie_free (trie_t *trie)
 }
 
 /* Helper for bsearch and qsort */
-static int
+static inline int
 cmp_children (const void *k1, const void *k2)
 {
   child_t *c1 = (child_t *) k1;
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_frodo_commit "Wed, 21 Oct 2015 09:32:24" "Fixed initialization of child memory to zero and declaring cmp_children() as inlined"

###### Branch (test) #####

git checkout -b test

##### Commit (Starting the test branch) #####

mkdir test

cat > test/trie_test.c <<EOF
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <assert.h>
#include <string.h>

#include <trie.h>


int
main (int argc, char *argv[])
{
  /* Intializing the data-base */
  trie_t *t = trie_alloc ();

  trie_free (t);

  return EXIT_SUCCESS;
}
EOF

cat > test/Makefile <<EOF
CFLAGS=-Wall -Wextra -std=c11 -g -O2
CPPFLAGS=-I../include
LDFLAGS=

.PHONY:	all clean help

all: trie_test

../src/trie.o:
	cd ../src && make

trie_test: trie_test.c ../src/trie.o
	\$(CC) \$(CFLAGS) \$(CPPFLAGS) -o \$@ \$^ \$(LDFLAGS)

clean:
	@rm -f *~ *.o trie_test

help:
	@echo "Usage:"
	@echo "  make [all]\t\tBuild the tests"
	@echo "  make clean\t\tRemove all files generated by make"
	@echo "  make help\t\tDisplay this help"
EOF

cat > patch.diff <<EOF
# Commands
MAKE=make

# Special rules and targets
.PHONY:	all check clean help

# Rules and targets
all:
	@cd src/ && \$(MAKE)
	@cp -f src/trie.so .

check: all
	@cd test && \$(MAKE)

clean:
	@cd src/ && \$(MAKE) clean
	@cd test/ && \$(MAKE) clean
	@rm -f trie.so *~

help:
	@echo "Usage:"
	@echo "  make [all]\t\tBuild the library"
	@echo "  make check\t\tRun all the tests"
	@echo "  make clean\t\tRemove all files generated by make"
	@echo "  make help\t\tDisplay this help"
EOF

git add Makefile test/Makefile test/trie_test.c

git_sam_commit "Wed, 21 Oct 2015 11:57:43" "Test framework started"
