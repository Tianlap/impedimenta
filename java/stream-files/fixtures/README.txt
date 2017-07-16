There are several levels of directories contained herein. This helps test
whether getFiles() correctly recurses.

There are several files with the same name or similar names at several levels
within the directory tree. This helps test whether a dumb filename handling
scheme is used.

There are a total of ten *.txt files in this directory, either directly or
indirectly. This helps test the performance of serial vs parallel performance.
(It would also be cool to see the effect on performance when there are hundreds,
thousands, etc of files.)
