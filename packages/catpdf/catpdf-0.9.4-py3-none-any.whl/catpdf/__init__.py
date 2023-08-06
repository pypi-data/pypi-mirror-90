"""conCATenate one or more source PDF files (or pieces of) into a target PDF file

syntax of positional arguments:

    <source>   ::= [<path>/]<file>.pdf[:<choice>]
    <choice>   ::= <interval>[,<interval>]*
    <interval> ::= <index>[-<index>]
    <index>    ::= <integer>|n
    <integer>  ::= 1..9[0..9]*
    
    <target>   ::= [<path>/]<file>.pdf

explanation:

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

examples:

    $ catpdf a.pdf b.pdf c.pdf # concatenate a.pdf and b.pdf into c.pdf

    $ catpdf -y a.pdf b.pdf a.pdf # append b.pdf at end of a.pdf

    $ catpdf a.pdf:1-10,95-n b.pdf:50-40 c.pdf # concatenate a.pdf (first 10 pages and from page 95 until the end of file) and b.pdf (from page 50 backwards until page 40) into c.pdf

    $ catpdf sdr-?.pdf sdr.pdf # concatenate sdr-a.pdf sdr-b.pdf and sdr-c.pdf and ... into sdr.pdf"""

__version__ = "0.9.4"

__requires__ = ["libfunx >=0.9.4", "pdfrw >=0.4"]

from libfunx import syntax_error

def choice2first_last(choice):
    """translate a choice string into a list of (first, last) couples
pages are numbered from 1 to n
n is translated into 0, it will be substituted py number of pages
>>> choice2first_last("23,23-34,55-22,23-n,n-34,n,n-n")
[(23, 23), (23, 34), (55, 22), (23, 0), (0, 34), (0, 0), (0, 0)]"""
    status = 0; first_last = []
    for jchar, char in enumerate(choice + ","):
        if status == 0:
            if "1" <= char <= "9":
                first = ord(char) - 48; status = 1
            elif char == "n":
                first = 0; status = 2
            else:
                syntax_error(choice, jchar)
        elif status == 1:
            if "0" <= char <= "9":
                first = first * 10 + ord(char) - 48 # 48 == ord("0")
            elif char == "-":
                status = 3
            elif char == ",":
                first_last.append((first, first)); status = 0
            else:
                syntax_error(choice, jchar)
        elif status == 2:
            if char == "-":
                status = 3
            elif char == ",":
                first_last.append((first, first)); status = 0
            else:
                syntax_error(choice, jchar)
        elif status == 3:
            if "1" <= char <= "9":
                last = ord(char) - 48; status = 4
            elif char == "n":
                last = 0; status = 5
            else:
                syntax_error(choice, jchar)
        elif status == 4:
            if "0" <= char <= "9":
                last = last * 10 + ord(char) - 48 # 48 == ord("0")
            elif char == ",":
                first_last.append((first, last)); status = 0
            else:
                syntax_error(choice, jchar)
        elif status == 5:
            if char == ",":
                first_last.append((first, last)); status = 0
            else:
                syntax_error(choice, jchar)
    if status != 0:
        syntax_error(choice, jchar)
    return first_last

