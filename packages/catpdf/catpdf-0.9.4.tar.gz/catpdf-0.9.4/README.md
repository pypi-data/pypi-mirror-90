###USAGE
```
    catpdf [-h] [-V] [-v] [-y] [-n] [-o] [-q] source [source ...] target
```

conCATenate one or more source PDF files (or pieces of) into a target PDF file

syntax of positional arguments:
```
    <source>   ::= [<path>/]<file>.pdf[:<choice>]
    <choice>   ::= <interval>[,<interval>]*
    <interval> ::= <index>[-<index>]
    <index>    ::= <integer>|n
    <integer>  ::= 1..9[0..9]*

    <target>   ::= [<path>/]<file>.pdf
```
explanation:
```
    each source is made by:

        an optional path followed by '/'
        a file name followed by a mandatory '.pdf' extension
        an optional choice preceded by ':' (default: ':1-n')

    the choice is a comma-separated list of one or more intervals

    each interval is made by:

        an index of a single page
        or two indexes separated by '-' (meaning first and last page)

    each index is:

        a positive integer constant (leading zeros not allowed)
        or a single lowercase 'n' letter (meaning the number of pages in source file)

    the target is made by:

        an optional path followed by '/'
        a file name followed by a mandatory '.pdf' extension
```
examples:
```
    $ catpdf a.pdf b.pdf c.pdf # concatenate a.pdf and b.pdf into c.pdf

    $ catpdf -y a.pdf b.pdf a.pdf # append b.pdf at end of a.pdf

    $ catpdf a.pdf:1-10,95-n b.pdf:50-40 c.pdf # concatenate a.pdf (first 10 pages and from page 95 until the end of file) and b.pdf (from page 50 backwards until page 40) into c.pdf

    $ catpdf sdr-?.pdf sdr.pdf # concatenate sdr-a.pdf sdr-b.pdf and sdr-c.pdf and ... into sdr.pdf
```
###POSITIONAL ARGUMENTS
```
  source         one or more source files (each with choice or not), followed
                 by...
  target         ...one target file

```
###OPTIONAL ARGUMENTS
```
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
  -v, --verbose  show what happens
  -y, --yes      overwrite existing target file (default: ask)
  -n, --no       don't overwrite existing target file (default: ask)
  -o, --open     at end open the target file for check and print (default:
                 ask)
  -q, --quit     at end don't open the target file for check and print
                 (default: ask)
```
