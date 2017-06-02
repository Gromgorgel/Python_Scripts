# Python Scripts
A collection of assorted python scripts for Bioinformatics purposes

## the 'Batch-Entrez_nucleotide.py' script
So you want to automatically retrieve a bunch of nucleotide sequences from NCBI. Of course there's [Bio.Entrez](http://biopython.org/DIST/docs/api/Bio.Entrez-module.html), but they kindly ask to [minimize the number of requests](https://www.ncbi.nlm.nih.gov/books/NBK25497/#ui-ncbiinpagenav-heading-8) and I happen to find myself in a situation where I have a bunch of text files, each of which contains the accession numbers for orthologue genes across several species. 

Which brings us to [batch Entrez](https://www.ncbi.nlm.nih.gov/sites/batchentrez). This portal allows to upload exactly such text files (no coincidence) and will select the corresponding records for you. Rather than doing this manually for the 80+ files I have, I came up with this script which, from a folder, takes all files and submits them one by one to Entrez and saves the query results as FASTA.

The script contains quite a few `time.sleep()` commands sprinkled throughout the code in order to give the server the necessary time to respond (amount of sleep time has been experimentally optimized to a certain degree). However, some of the requests will still fail, so I've wrapped the entire procedure in a loop that'll keep trying to get the failed requests (you can set a maximum number of tries, currently `maxiter = 5`).

There's probably a better way to do this, but I'm not (yet) the python wizzard I'd like to be. And probably, since you're reading this, neither are you.
