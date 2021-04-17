# genomic_sequence_downloader.py

<br>

`genomic_sequence_downloader.py` is a Python script that allows for downloading portions of genomic sequences underlying a given target gene annotation across multiple species with annotated genomes available at NCBI (FASTA format).

<br>

### Dependencies

+ Python 3
+ NCBI Entrez Programming Utilities 

<br>

### Usage 

`genomic_sequence_downloader.py` requires a set of 10 arguments: 
+ the name of the target gene (-target_gene_name); 
+ the names of three downstream and upstream target gene flanking genes, so that in the absence of the target gene annotation in a given species genome, the script automatically downloads the most likely genomic sequence region for the target gene to be physically located (according to the principle of synteny conservation across evolution);
+ the input path to a .txt file containing the list of the species of interest (scientific name, separated by lines) (-target_species_list_file_path);
+ the output path to a .fasta file that will contain  each species corresponding downloaded sequence (-sequences_content_output_file_path); 
+ the output path to a .csv file that will contain metadata regarding each downloaded sequence, including, among others, from left to right, the scientific and common name of the correponding species, the corresponding genomic sequence ID, the coordinates of the corresponding genomic sequence ID that define the genomic portion that was extracted, the ID of the corresponding genome assembly, and the used method for defining the extracted sequence (either the Annotated Gene-Based Method or the Synteny Conservation-Based Method).

<br>

	usage: genomic_downloader.py
                             -target_gene_name
                             -1st_downstream_flanking_gene_name
                             -2nd_downstream_flanking_gene_name
                             -3rd_downstream_flanking_gene_name
                             -1st_upstream_flanking_gene_name
                             -2nd_upstream_flanking_gene_name
                             -3rd_upstream_flanking_gene_name
                             -target_species_list_file_path
                             -sequences_content_output_file_path
                             -sequences_data_output_file_path

<br>

### Example

Download the script available at `script/genomic_sequence_downloader.py`. Try the following:

	python3 genomic_downloader.py RAG1 TRAF6 PRRR5L COMMD9 IFTAP LRRC4C API5 input_species.txt sequences_output.fasta sequences_data.csv
			
Using as `input` the above-mentioned arguments, the script will generate as `output` the same two files (sequences_output.fasta sequences_data.csv) found at the 'example' folder.

<br>

>**Enjoy it!**
