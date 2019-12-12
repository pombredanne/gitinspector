#!/usr/bin/env bash

# git_commit AUTHOR_NAME AUTHOR_EMAIL COMMIT_DATE COMMIT_MSG
function git_commit {
    GIT_COMMITTER_NAME="${1}" GIT_COMMITTER_EMAIL="${2}" GIT_COMMITTER_DATE="${3}" git commit --allow-empty-message --author "${1} <${2}>" --date "${3}" -m "${4}"
}

PROJECT_DIR=trie-repository

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

###### Branch (test) #####

git checkout -b test

##### Commit (Start populate test branch) #####

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

###### Getting back to master #####

git checkout master

##### Commit (function trie_add_word()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 5493a2e..6fdc018 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -119,3 +119,53 @@ trie_print (trie_t *t)
 {
   _trie_print_rec (t, 0);
 }
+
+/* Add a word to the trie */
+void
+trie_add_word (trie_t *trie, const char *word, size_t length, ssize_t info)
+{
+  assert (trie != NULL);
+
+  trie_t *nxt = NULL;
+  child_t *child = trie_search_child (trie, word[0]);
+
+  if (child)
+    {
+      if (length == 1)
+	child->last = info;
+      if (length > 1 && child->next == NULL)
+	child->next = trie_alloc ();
+
+      nxt = child->next;
+    }
+  else
+    {
+      if (trie->children_count >= trie->children_size)
+	{
+	  trie->children_size *= 2;
+	  trie->children = realloc (trie->children,
+				    trie->children_size * sizeof (child_t));
+	}
+
+      trie->children[trie->children_count].symb = word[0];
+      if (length > 1)
+	{
+	  trie->children[trie->children_count].next = trie_alloc ();
+	  trie->children[trie->children_count].last = TRIE_NOT_LAST;
+	}
+      else
+	{
+	  trie->children[trie->children_count].next = NULL;
+	  trie->children[trie->children_count].last = info;
+	}
+
+      nxt = trie->children[trie->children_count].next;
+      trie->children_count++;
+
+      qsort (trie->children, trie->children_count,
+	     sizeof (child_t), cmp_children);
+    }
+
+  if (length > 1)
+    trie_add_word (nxt, &word[1], length - 1, info);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Fri, 23 Oct 2015 17:37:43" "function trie_add_word()"

###### Branch (test) #####

git checkout test

##### Commit (test trie_add_word() and trie_print()) #####

cat > patch.diff <<EOF
diff --git a/test/trie_test.c b/test/trie_test.c
index 6a310ec..b9b9889 100644
--- a/test/trie_test.c
+++ b/test/trie_test.c
@@ -7,12 +7,29 @@
 
 #include <trie.h>
 
+#define add_word(t, word)  trie_add_word (t, word, strlen (word), 1)
+
 int
 main (int argc, char *argv[])
 {
   /* Intializing the data-base */
   trie_t *t = trie_alloc ();
 
+  add_word (t, "+");
+  add_word (t, "++");
+  add_word (t, "+=");
+  add_word (t, "+++");
+  add_word (t, "-+-");
+  add_word (t, "+=+");
+  add_word (t, "=+=");
+  add_word (t, "===");
+  add_word (t, "---");
+  add_word (t, "+-+");
+
+  printf ("Printing all the database.\n");
+  trie_print (t);
+
+  /* Freeing memory */
   trie_free (t);
 
   return EXIT_SUCCESS;
EOF

git apply patch.diff
rm -f patch.diff

git add test/trie_test.c

git_sam_commit "Mon, 26 Oct 2015 10:17:55" "Testing trie_add_word() and trie_print()"

###### Merge (master + test) #####

git checkout master
git merge --no-commit test
git_sam_commit "Mon, 26 Oct 2015 10:23:07" "Merge branch 'test'"

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

git_sam_commit "Mon, 26 Oct 2015 11:32:24" "Fixed initialization of child memory to zero and declaring cmp_children() as inlined"

###### Commit (function trie_search()) ######

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 6fdc018..2046e08 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -169,3 +169,23 @@ trie_add_word (trie_t *trie, const char *word, size_t length, ssize_t info)
   if (length > 1)
     trie_add_word (nxt, &word[1], length - 1, info);
 }
+
+/* Search for word in trie. Returns true/false */
+ssize_t
+trie_search (trie_t *trie, const char *word, size_t length)
+{
+  assert (length > 0);
+
+  if (trie == NULL)
+    return TRIE_NOT_LAST;
+
+  child_t *child = trie_search_child (trie, word[0]);
+
+  if (!child)
+    return TRIE_NOT_LAST;
+
+  if (length == 1)
+    return child->last;
+  else
+    return trie_search (child->next, &word[1], length - 1);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_frodo_commit "Tue, 27 Oct 2015 10:13:52" "function trie_search()"

##### Commit (function trie_check_prefix()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 2046e08..dc80fd7 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -189,3 +189,33 @@ trie_search (trie_t *trie, const char *word, size_t length)
   else
     return trie_search (child->next, &word[1], length - 1);
 }
+
+/* Search for a prefix in the trie. Returns a position in the trie. */
+trie_t *
+trie_check_prefix (trie_t *trie, const char *word, size_t length, ssize_t * last)
+{
+  child_t *child;
+
+  assert (length > 0);
+  if (trie == NULL)
+    {
+      *last = TRIE_NOT_LAST;
+      return NULL;
+    }
+
+  child = trie_search_child (trie, word[0]);
+
+  if (!child)
+    {
+      *last = TRIE_NOT_LAST;
+      return NULL;
+    }
+
+  if (length == 1)
+    {
+      *last = child->last;
+      return child->next;
+    }
+  else
+    return trie_check_prefix (child->next, &word[1], length - 1, last);
+}
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Tue, 27 Oct 2015 11:45:32" "function trie_check_prefix()"

##### Commit (rework on the code of trie_check_prefix()) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index dc80fd7..d3ac02b 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -194,28 +194,25 @@ trie_search (trie_t *trie, const char *word, size_t length)
 trie_t *
 trie_check_prefix (trie_t *trie, const char *word, size_t length, ssize_t * last)
 {
-  child_t *child;
-
   assert (length > 0);
+
   if (trie == NULL)
-    {
-      *last = TRIE_NOT_LAST;
-      return NULL;
-    }
+    goto error;
 
-  child = trie_search_child (trie, word[0]);
+  child_t *child = trie_search_child (trie, word[0]);
 
   if (!child)
-    {
-      *last = TRIE_NOT_LAST;
-      return NULL;
-    }
+    goto error;
 
   if (length == 1)
     {
       *last = child->last;
       return child->next;
     }
-  else
-    return trie_check_prefix (child->next, &word[1], length - 1, last);
+
+  return trie_check_prefix (child->next, &word[1], length - 1, last);
+
+ error:
+  *last = TRIE_NOT_LAST;
+  return NULL;
 }
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_bilbo_commit "Tue, 27 Oct 2015 15:19:17" "rework on trie_check_prefix()"

##### Commit (test cases for the whole library) #####

cat > patch.diff <<EOF
diff --git a/test/Makefile b/test/Makefile
index ad42086..4a0ceda 100644
--- a/test/Makefile
+++ b/test/Makefile
@@ -4,16 +4,19 @@ LDFLAGS=
 
 .PHONY:	all clean help
 
-all: trie_test
+all: trie_test-01 trie_test-02
 
 ../src/trie.o:
 	cd ../src && make
 
-trie_test: trie_test.c ../src/trie.o
+trie_test-01: trie_test-01.c ../src/trie.o
+	\$(CC) \$(CFLAGS) \$(CPPFLAGS) -o \$@ \$^ \$(LDFLAGS)
+
+trie_test-02: trie_test-02.c ../src/trie.o
 	\$(CC) \$(CFLAGS) \$(CPPFLAGS) -o \$@ \$^ \$(LDFLAGS)
 
 clean:
-	@rm -f *~ *.o trie_test
+	@rm -f *~ *.o trie_test-01 trie_test-02
 
 help:
 	@echo "Usage:"
diff --git a/test/trie_test.c b/test/trie_test-01.c
similarity index 52%
rename from test/trie_test.c
rename to test/trie_test-01.c
index b9b9889..0bfbe01 100644
--- a/test/trie_test.c
+++ b/test/trie_test-01.c
@@ -12,6 +12,8 @@
 int
 main (int argc, char *argv[])
 {
+  assert (argc > 1);
+
   /* Intializing the data-base */
   trie_t *t = trie_alloc ();
 
@@ -29,6 +31,23 @@ main (int argc, char *argv[])
   printf ("Printing all the database.\n");
   trie_print (t);
 
+  /* Searching the data-base */
+  bool check_search = true, check_prefix_search = false;
+  if (check_search)
+    printf ("searching '%s' in the database -- %s\n",
+	    argv[1], trie_search (t, argv[1],
+				  strlen (argv[1])) !=
+	    TRIE_NOT_LAST ? "yes" : "no");
+  else if (check_prefix_search)
+    {
+      trie_t *res;
+      ssize_t last;
+      res = trie_check_prefix (t, argv[1], strlen (argv[1]), &last);
+      printf ("checking prefix for '%s' in database last: %s, follows:\n",
+	      argv[1], last != TRIE_NOT_LAST ? "yes" : "no");
+      trie_print (res);
+    }
+
   /* Freeing memory */
   trie_free (t);
 
diff --git a/test/trie_test-02.c b/test/trie_test-02.c
new file mode 100644
index 0000000..0060767
--- /dev/null
+++ b/test/trie_test-02.c
@@ -0,0 +1,40 @@
+#include <stdio.h>
+#include <stdlib.h>
+#include <unistd.h>
+
+#include <libgen.h>
+#include <string.h>
+
+#include <trie.h>
+
+/* We want to attach to every word in the trie data-base */
+typedef enum  {
+  type_a, type_b
+} word_type_t;
+
+int main (int argc, char *argv[])
+{
+  int ret = EXIT_SUCCESS;
+  ssize_t res;
+
+  trie_t * dict = trie_alloc ();
+  if (argc <= 1)
+    {
+      fprintf (stderr, "usage: %s word to find\n", basename(argv[0]));
+      exit(EXIT_FAILURE);
+    }
+
+  trie_add_word (dict, "hello", strlen ("hello"), (ssize_t) type_a);
+  trie_add_word (dict, "hell", strlen ("hell"), (ssize_t) type_b);
+
+  printf ("Printing the trie.\n");
+  trie_print (dict);
+
+  res = trie_search (dict, argv[1], strlen (argv[1]));
+  printf ("searching '%s' in the database -- %s\n", argv[1],
+	  res != TRIE_NOT_LAST ?
+	  (word_type_t) res == type_a ? "yes, type A" : "yes, type B" : "no");
+
+  trie_free (dict);
+  return ret;
+}
EOF

git apply patch.diff
rm -f patch.diff

git add test/Makefile test/trie_test-01.c test/trie_test-02.c

git_sam_commit "Wed, 28 Oct 2015 12:09:56" "Adding more complete test cases"

##### Commit (remove unnecessary file test/trie_test.c) #####

git rm test/trie_test.c

git_sam_commit "Wed, 28 Oct 2015 12:17:23" "Forgot to remove test/trie_test.c"

##### Commit (pippin tries to fake some activity) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index d3ac02b..7bda122 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -52,7 +52,7 @@ trie_alloc (void)
 }
 
 void
-trie_free (trie_t *trie)
+trie_free (trie_t * trie)
 {
   if (!trie)
     return;
@@ -78,12 +78,12 @@ cmp_children (const void *k1, const void *k2)
 /* Search for a symbol in a children of a certain trie.
  * Uses binary search as the children are kept sorted */
 static child_t *
-trie_search_child (trie_t *trie, int symb)
+trie_search_child (trie_t * trie, int symb)
 {
   if (trie->children_count == 0)
     return NULL;
 
-  child_t s = { .symb = symb };
+  child_t s = {.symb = symb };
 
   return
     (child_t *) bsearch (&s,
@@ -99,7 +99,7 @@ trie_search_child (trie_t *trie, int symb)
 
 /* Private function to recursively print the trie */
 static void
-_trie_print_rec (trie_t *t, int level)
+_trie_print_rec (trie_t * t, int level)
 {
   if (!t)
     return;
@@ -108,21 +108,21 @@ _trie_print_rec (trie_t *t, int level)
     {
       tab (level);
       printf ("%c %s\n", (char) t->children[i].symb,
-             t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
+	      t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
       _trie_print_rec (t->children[i].next, level + 1);
     }
 }
 
 /* Wrapper for print */
 void
-trie_print (trie_t *t)
+trie_print (trie_t * t)
 {
   _trie_print_rec (t, 0);
 }
 
 /* Add a word to the trie */
 void
-trie_add_word (trie_t *trie, const char *word, size_t length, ssize_t info)
+trie_add_word (trie_t * trie, const char *word, size_t length, ssize_t info)
 {
   assert (trie != NULL);
 
@@ -172,7 +172,7 @@ trie_add_word (trie_t *trie, const char *word, size_t length, ssize_t info)
 
 /* Search for word in trie. Returns true/false */
 ssize_t
-trie_search (trie_t *trie, const char *word, size_t length)
+trie_search (trie_t * trie, const char *word, size_t length)
 {
   assert (length > 0);
 
@@ -192,7 +192,8 @@ trie_search (trie_t *trie, const char *word, size_t length)
 
 /* Search for a prefix in the trie. Returns a position in the trie. */
 trie_t *
-trie_check_prefix (trie_t *trie, const char *word, size_t length, ssize_t * last)
+trie_check_prefix (trie_t * trie, const char *word, size_t length,
+		   ssize_t * last)
 {
   assert (length > 0);
 
@@ -212,7 +213,7 @@ trie_check_prefix (trie_t *trie, const char *word, size_t length, ssize_t * last
 
   return trie_check_prefix (child->next, &word[1], length - 1, last);
 
- error:
+error:
   *last = TRIE_NOT_LAST;
   return NULL;
 }
diff --git a/test/trie_test-02.c b/test/trie_test-02.c
index 0060767..73d7915 100644
--- a/test/trie_test-02.c
+++ b/test/trie_test-02.c
@@ -8,20 +8,22 @@
 #include <trie.h>
 
 /* We want to attach to every word in the trie data-base */
-typedef enum  {
+typedef enum
+{
   type_a, type_b
 } word_type_t;
 
-int main (int argc, char *argv[])
+int
+main (int argc, char *argv[])
 {
   int ret = EXIT_SUCCESS;
   ssize_t res;
 
-  trie_t * dict = trie_alloc ();
+  trie_t *dict = trie_alloc ();
   if (argc <= 1)
     {
-      fprintf (stderr, "usage: %s word to find\n", basename(argv[0]));
-      exit(EXIT_FAILURE);
+      fprintf (stderr, "usage: %s word to find\n", basename (argv[0]));
+      exit (EXIT_FAILURE);
     }
 
   trie_add_word (dict, "hello", strlen ("hello"), (ssize_t) type_a);
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c test/trie_test-02.c

git_pippin_commit "Sun, 1 Nov 2015 01:57:17" "Reformating the code"

##### Commit (useless variable renaming) #####

cat > patch.diff <<EOF
diff --git a/src/trie.c b/src/trie.c
index 7bda122..3e0f319 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -6,8 +6,8 @@
 #include <assert.h>
 #include <string.h>
 
-/* Default number of the number of children in trie node */
-#define TRIE_CHILDREN         4
+/* Default number of the number of childs in trie node */
+#define TRIE_CHILDS         4
 
 /* Private definition of the data-structure */
 typedef struct
@@ -19,9 +19,9 @@ typedef struct
 
 struct trie_t
 {
-  unsigned int children_size;
-  unsigned int children_count;
-  child_t *children;
+  unsigned int childs_size;
+  unsigned int childs_count;
+  child_t *childs;
 };
 
 
@@ -35,18 +35,18 @@ trie_alloc (void)
     return NULL;
 
   /* Allocate child data-structure */
-  child_t *child = malloc (TRIE_CHILDREN * sizeof (child_t));
+  child_t *child = malloc (TRIE_CHILDS * sizeof (child_t));
   if (!child)
     {
       free (trie);
       return NULL;
     }
-  memset (child, 0, TRIE_CHILDREN * sizeof (child_t));
+  memset (child, 0, TRIE_CHILDS * sizeof (child_t));
 
   /* Initializing the trie data-structure */
-  trie->children_size = TRIE_CHILDREN;
-  trie->children_count = 0;
-  trie->children = child;
+  trie->childs_size = TRIE_CHILDS;
+  trie->childs_count = 0;
+  trie->childs = child;
 
   return trie;
 }
@@ -57,38 +57,38 @@ trie_free (trie_t * trie)
   if (!trie)
     return;
 
-  for (size_t i = 0; i < trie->children_count; ++i)
-    trie_free (trie->children[i].next);
+  for (size_t i = 0; i < trie->childs_count; ++i)
+    trie_free (trie->childs[i].next);
 
-  if (trie->children)
-    free (trie->children);
+  if (trie->childs)
+    free (trie->childs);
 
   free (trie);
 }
 
 /* Helper for bsearch and qsort */
 static inline int
-cmp_children (const void *k1, const void *k2)
+cmp_childs (const void *k1, const void *k2)
 {
   child_t *c1 = (child_t *) k1;
   child_t *c2 = (child_t *) k2;
   return c1->symb - c2->symb;
 }
 
-/* Search for a symbol in a children of a certain trie.
- * Uses binary search as the children are kept sorted */
+/* Search for a symbol in a childs of a certain trie.
+ * Uses binary search as the childs are kept sorted */
 static child_t *
 trie_search_child (trie_t * trie, int symb)
 {
-  if (trie->children_count == 0)
+  if (trie->childs_count == 0)
     return NULL;
 
   child_t s = {.symb = symb };
 
   return
     (child_t *) bsearch (&s,
-			 trie->children, trie->children_count,
-			 sizeof (child_t), cmp_children);
+			 trie->childs, trie->childs_count,
+			 sizeof (child_t), cmp_childs);
 }
 
 #define tab(n)                           \\
@@ -104,12 +104,12 @@ _trie_print_rec (trie_t * t, int level)
   if (!t)
     return;
 
-  for (size_t i = 0; i < t->children_count; i++)
+  for (size_t i = 0; i < t->childs_count; i++)
     {
       tab (level);
-      printf ("%c %s\\n", (char) t->children[i].symb,
-	      t->children[i].last != TRIE_NOT_LAST ? "[last]" : "");
-      _trie_print_rec (t->children[i].next, level + 1);
+      printf ("%c %s\\n", (char) t->childs[i].symb,
+	      t->childs[i].last != TRIE_NOT_LAST ? "[last]" : "");
+      _trie_print_rec (t->childs[i].next, level + 1);
     }
 }
 
@@ -140,30 +140,30 @@ trie_add_word (trie_t * trie, const char *word, size_t length, ssize_t info)
     }
   else
     {
-      if (trie->children_count >= trie->children_size)
+      if (trie->childs_count >= trie->childs_size)
 	{
-	  trie->children_size *= 2;
-	  trie->children = realloc (trie->children,
-				    trie->children_size * sizeof (child_t));
+	  trie->childs_size *= 2;
+	  trie->childs = realloc (trie->childs,
+				    trie->childs_size * sizeof (child_t));
 	}
 
-      trie->children[trie->children_count].symb = word[0];
+      trie->childs[trie->childs_count].symb = word[0];
       if (length > 1)
 	{
-	  trie->children[trie->children_count].next = trie_alloc ();
-	  trie->children[trie->children_count].last = TRIE_NOT_LAST;
+	  trie->childs[trie->childs_count].next = trie_alloc ();
+	  trie->childs[trie->childs_count].last = TRIE_NOT_LAST;
 	}
       else
 	{
-	  trie->children[trie->children_count].next = NULL;
-	  trie->children[trie->children_count].last = info;
+	  trie->childs[trie->childs_count].next = NULL;
+	  trie->childs[trie->childs_count].last = info;
 	}
 
-      nxt = trie->children[trie->children_count].next;
-      trie->children_count++;
+      nxt = trie->childs[trie->childs_count].next;
+      trie->childs_count++;
 
-      qsort (trie->children, trie->children_count,
-	     sizeof (child_t), cmp_children);
+      qsort (trie->childs, trie->childs_count,
+	     sizeof (child_t), cmp_childs);
     }
 
   if (length > 1)
EOF

git apply patch.diff
rm -f patch.diff

git add src/trie.c

git_pippin_commit "Sun, 1 Nov 2015 02:04:22" "Refactoring code"


##### Commit (adding licensing) #####

cat > patch.diff <<EOF
diff --git a/include/trie.h b/include/trie.h
index 22b6990..e0cb878 100644
--- a/include/trie.h
+++ b/include/trie.h
@@ -1,3 +1,20 @@
+/*
+ * This file is part of the trie library.
+ *
+ * The trie library is free software: you can redistribute it and/or
+ * modify it under the terms of the GNU General Public License as
+ * published by the Free Software Foundation, either version 3 of the
+ * License, or at your option) any later version.
+ *
+ * The trie library is distributed in the hope that it will be useful,
+ * but WITHOUT ANY WARRANTY; without even the implied warranty of
+ * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
+ * General Public License for more details.
+ *
+ * You should have received a copy of the GNU General Public License
+ * along with the trie library. If not, see http://www.gnu.org/licenses/.
+ */
+
 #ifndef TRIE_H
 #define TRIE_H
 
diff --git a/src/trie.c b/src/trie.c
index 3e0f319..b9f2f18 100644
--- a/src/trie.c
+++ b/src/trie.c
@@ -1,3 +1,20 @@
+/*
+ * This file is part of the trie library.
+ *
+ * The trie library is free software: you can redistribute it and/or
+ * modify it under the terms of the GNU General Public License as
+ * published by the Free Software Foundation, either version 3 of the
+ * License, or at your option) any later version.
+ *
+ * The trie library is distributed in the hope that it will be useful,
+ * but WITHOUT ANY WARRANTY; without even the implied warranty of
+ * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
+ * General Public License for more details.
+ *
+ * You should have received a copy of the GNU General Public License
+ * along with the trie library. If not, see http://www.gnu.org/licenses/.
+ */
+
 #include "trie.h"
 
 #include <stdio.h>
diff --git a/test/trie_test-01.c b/test/trie_test-01.c
index 0bfbe01..7688ccf 100644
--- a/test/trie_test-01.c
+++ b/test/trie_test-01.c
@@ -1,3 +1,20 @@
+/*
+ * This file is part of the trie library.
+ *
+ * The trie library is free software: you can redistribute it and/or
+ * modify it under the terms of the GNU General Public License as
+ * published by the Free Software Foundation, either version 3 of the
+ * License, or at your option) any later version.
+ *
+ * The trie library is distributed in the hope that it will be useful,
+ * but WITHOUT ANY WARRANTY; without even the implied warranty of
+ * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
+ * General Public License for more details.
+ *
+ * You should have received a copy of the GNU General Public License
+ * along with the trie library. If not, see http://www.gnu.org/licenses/.
+ */
+
 #include <stdbool.h>
 #include <stdio.h>
 #include <stdlib.h>
diff --git a/test/trie_test-02.c b/test/trie_test-02.c
index 73d7915..a13f5e9 100644
--- a/test/trie_test-02.c
+++ b/test/trie_test-02.c
@@ -1,3 +1,20 @@
+/*
+ * This file is part of the trie library.
+ *
+ * The trie library is free software: you can redistribute it and/or
+ * modify it under the terms of the GNU General Public License as
+ * published by the Free Software Foundation, either version 3 of the
+ * License, or at your option) any later version.
+ *
+ * The trie library is distributed in the hope that it will be useful,
+ * but WITHOUT ANY WARRANTY; without even the implied warranty of
+ * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
+ * General Public License for more details.
+ *
+ * You should have received a copy of the GNU General Public License
+ * along with the trie library. If not, see http://www.gnu.org/licenses/.
+ */
+
 #include <stdio.h>
 #include <stdlib.h>
 #include <unistd.h>
EOF

git apply patch.diff
rm -f patch.diff

git add include/trie.h src/trie.c test/trie_test-01.c test/trie_test-02.c

git_pippin_commit "Sun, 1 Nov 2015 02:17:37" "Adding code licensing"
