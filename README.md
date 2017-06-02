# Python Scripts
A collection of Assorted python scripts for Bioinformatics purposes

## the 'Batch-Entrez_nucleotide.py' script
So you want to automatically retrieve a bunch of nucleotide sequences from NCBI. Of course there's [Bio.Entrez](http://biopython.org/DIST/docs/api/Bio.Entrez-module.html), but they kindly ask to [minimize the number of requests](https://www.ncbi.nlm.nih.gov/books/NBK25497/#ui-ncbiinpagenav-heading-8) and I happen to find myself in a situation where I have a bunch of text files, each of which contains the accession numbers for orthologue genes across several species. 

Which brings us to [batch Entrez](https://www.ncbi.nlm.nih.gov/sites/batchentrez). This portal allows to upload such textfiles and will select the corresponding records for you. Rather than doing this manually for the 80+ files I have, I came up with this script which, from a folder, takes all files and submits them one by one to Entrez and saves the query results as FASTA.

There's probably a better way to do this, but I'm not (yet) the python wizzard I'd like to be. And probably, since you're reading this, neither are you.
