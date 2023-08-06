"""SWAP PDF pages after scan of a two-sided sheet pack through a one-sided feeder.

Let's have a two-sided sheet pack we want scan through a one-sided feeder. Then:

    - we open the scan utility, say simple-scan aka Document Scanner
    - we click the "All Pages From Feeder" option
    - we scan all odd pages
    - then we turn upside down the pack and we put it again in the feeder
    - we scan all even pages
    - finally we save our pages in a file, say 'Scanned Document.pdf'

Now 'Scanned Document.pdf' contains odd pages in ascending order, followed by even pages in
descending order.

For instance, say our sheets are 4, so our pages are 8, so 'Scanned Document.pdf' contains
the pages:

    1 3 5 7 8 6 4 2
    
We issue at terminal:

    $ swapdf 'Scanned Document.pdf' mydoc.pdf

(Of course we need quotation marks because the blank in the file name)

Now mydoc.pdf contains the pages:

    1 2 3 4 5 6 7 8

in the right order."""

__version__ = "0.9.7"

__requires__ = ["pdfrw","libfunx"]
