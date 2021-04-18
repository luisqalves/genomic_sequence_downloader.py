import argparse
import os


def check_target_gene_annotation_status():
    id = os.popen('esearch -db gene -query "'+args.target_gene_name +
                  '[GENE] AND '+current_species+'[Organism]" -sort "Relevance" | esummary | xtract -pattern DocumentSummary -element Id').read().split('\n')[0].replace('\n', '')
    if len(id) > 0:
        download_via_existent_gene_annotation(id)
    else:
        download_via_synteny_conservation()


def download_via_existent_gene_annotation(id):
    species_common_name = os.popen(
        'esummary -db gene -id '+id+' | xtract -pattern DocumentSummary -element CommonName').read().replace('\n', '')
    data = os.popen('esummary -db gene -id '+id +
                    ' | xtract -pattern DocumentSummary -if LocationHist -block LocationHistType -element ChrAccVer ChrStart ChrStop AssemblyAccVer').read().split('\t')
    if data == ['']:
        data = os.popen('esummary -db gene -id '+id +
                        ' | xtract -pattern DocumentSummary -if GenomicInfo -block GenomicInfoType -element ChrAccVer ChrStart ChrStop AssemblyAccVer').read().split('\t')
    if data == ['']:
        download_via_synteny_conservation()
        return 0
    print(args.target_gene_name+" annotation has been found.\nDownloading the genomic sequence underlying " +
          args.target_gene_name+" annotation...")
    genomic_ID = data[0]
    start = int(data[1])
    stop = int(data[2])
    assembly_ID = data[3].replace('\n', '')
    if start < stop:
        start = start-2000
        stop = stop+2000
    else:
        start = start+2000
        stop = stop-2000
    start = str(start)
    stop = str(stop)
    sequence = os.popen('efetch -db nuccore -id '+data[0]+' -chr_start ' +
                        start+' -chr_stop '+stop+' -format fasta').read().split('\n')
    sequences_output_file.write('>'+current_species+'\n')
    for i in range(len(sequence)):
        if i > 0:
            sequences_output_file.write(sequence[i])
    sequences_output_file.write('\n')
    sequences_data_file.write(str(species_counter)+','+args.target_gene_name+','+current_species+',' +
                              species_common_name+','+genomic_ID+','+start+','+stop+','+assembly_ID+',Annotated Gene-Based Method'+'\n')
    print("Done.")


def download_via_synteny_conservation():
    print(current_species+" genome does not present annotation for the "+args.target_gene_name +
          " gene.\nDownloading through the synteny conservation-based method...")
    upstream_flanking_genes = [args.first_upstream_gene_name,
                               args.second_upstream_gene_name, args.third_upstream_gene_name]
    while(len(upstream_flanking_genes) > 0):
        upstream_gene_name = upstream_flanking_genes[0]
        upstream_gene_data = os.popen('esearch -db gene -query "'+upstream_gene_name +
                                      '[GENE] AND '+current_species+'[Organism]" -sort "Relevance" | esummary | xtract -pattern DocumentSummary -element Id Name').read().split('\n')[0].split('\t')
        if upstream_gene_data != ['']:
            upstream_gene_name = upstream_gene_data[1].upper()
            print('Selected Upstream Flanking Gene: '+upstream_gene_name)
            break
        upstream_flanking_genes.remove(upstream_flanking_genes[0])
        if len(upstream_flanking_genes) == 0:
            print("Failed. At least one of the "+args.target_gene_name +
                  " flanking genes is not annotated in this species genome.")
            sequences_data_file.write(str(species_counter)+','+current_species+", Failed.  At least one of the " +
                                      args._target_gene_name+" flanking genes is not annotated in this species genome.\n")
            return 0
    downstream_flanking_genes = [args.first_downstream_gene_name,
                                 args.second_downstream_gene_name, args.third_downstream_gene_name]
    while(len(downstream_flanking_genes) > 0):
        downstream_gene_name = downstream_flanking_genes[0]
        downstream_gene_data = os.popen('esearch -db gene -query "'+downstream_gene_name +
                                        '[GENE] AND '+current_species+'[Organism]" -sort "Relevance" | esummary | xtract -pattern DocumentSummary -element Id Name').read().split('\n')[0].split('\t')
        if downstream_gene_data != ['']:
            downstream_gene_name = downstream_gene_data[1].upper()
            print('Selected Downstream Flanking Gene: '+downstream_gene_name)
            break
        downstream_flanking_genes.remove(downstream_flanking_genes[0])
        print(downstream_gene_name+" annotation not found.")
        if len(downstream_flanking_genes) == 0:
            print("Failed. At least one of the "+args.target_gene_name +
                  " flanking genes is not annotated in this species genome.")
            sequences_data_file.write(str(species_counter)+','+current_species+", Failed.  At least one of the " +
                                      args.target_gene_name+" flanking genes is not annotated in this species genome.\n")
            return 0
    upstream_gene_id = upstream_gene_data[0]
    downstream_gene_id = downstream_gene_data[0]
    species_common_name = os.popen('esummary -db gene -id '+downstream_gene_id +
                                   ' | xtract -pattern DocumentSummary -element CommonName').read()
    downstream_gene_coordinates = os.popen('esummary -db gene -id '+downstream_gene_id +
                                           ' | xtract -pattern DocumentSummary -if LocationHist -block LocationHistType -element ChrAccVer ChrStart ChrStop').read().split('\t')
    if downstream_gene_coordinates == ['']:
        downstream_gene_coordinates = os.popen('esummary -db gene -id '+downstream_gene_id +
                                               ' | xtract -pattern DocumentSummary -if GenomicInfo -block GenomicInfoType -element ChrAccVer ChrStart ChrStop').read().split('\t')
    if downstream_gene_coordinates == ['']:
        print("Failed. At least one of the "+gene_name +
              " flanking genes is not annotated in this species genome.")
        sequences_data_file.write(str(species_counter)+','+current_species+", Failed.  At least one of the " +
                                  gene_name+" flanking genes is not annotated in this species genome.\n")
        return 0
    downstream_gene_stop = downstream_gene_coordinates[2].replace('\n', '')
    upstream_gene_coordinates = os.popen('esummary -db gene -id '+upstream_gene_id +
                                         ' | xtract -pattern DocumentSummary -if LocationHist -block LocationHistType -element ChrAccVer ChrStart ChrStop').read().split('\t')
    if upstream_gene_coordinates == ['']:
        upstream_gene_coordinates = os.popen('esummary -db gene -id '+upstream_gene_id +
                                             ' | xtract -pattern DocumentSummary -if GenomicInfo -block GenomicInfoType -element ChrAccVer ChrStart ChrStop').read().split('\t')
    if upstream_gene_coordinates == ['']:
        print("Failed. At least one of the "+args.target_gene_name +
              " flanking genes is not annotated in this species genome.")
        sequences_data_file.write(str(species_counter)+','+current_species+', Failed.  At least one of the ' +
                                  args.target_gene_name+" flanking genes is not annotated in this species genome.\n")
        return 0
    upstream_sequence_id = upstream_gene_coordinates[0]
    downstream_sequence_id = downstream_gene_coordinates[0]
    upstream_gene_start = upstream_gene_coordinates[1].replace('\n', '')
    if downstream_sequence_id == upstream_sequence_id:
        assembly_ID = os.popen('esummary -db gene -id '+downstream_gene_id +
                               ' | xtract -pattern DocumentSummary -if LocationHist -block LocationHistType -element AssemblyAccVer').read().replace('\n', '').split('\t')[0]
        if assembly_ID == ['']:
            assembly_ID = os.popen('esummary -db gene -id '+downstream_gene_id +
                                   ' | xtract -pattern DocumentSummary -if GenomicInfo -block GenomicInfoType -element AssemblyAccVer').read().replace('\n', '').split('\t')[0]
        sequence = os.popen('efetch -db nuccore -id '+downstream_sequence_id+' -chr_start ' +
                            downstream_gene_stop+' -chr_stop '+upstream_gene_start+' -format fasta').read().split('\n')
        sequences_output_file.write('>'+current_species+'\n')
        for i in range(len(sequence)):
            if i > 0:
                sequences_output_file.write(sequence[i])
        sequences_output_file.write('\n')
        sequences_data_file.write(str(species_counter)+','+args.target_gene_name+','+current_species+','+species_common_name.replace('\n', '')+','+downstream_sequence_id +
                                  ','+downstream_gene_stop+','+upstream_gene_start+','+assembly_ID+',Synteny Conservation-Based Method'+'\n')
        print("Done.")
    else:
        print("Failed. Annotated "+args.target_gene_name +
              " flanking genes are not located on the same genomic sequence.")
        sequences_data_file.write(str(species_counter)+','+current_species+", Failed. Annotated "+args.target_gene_name +
                                  " flanking genes are not located on the same genomic sequence.\n")


parser = argparse.ArgumentParser()
parser.add_argument('target_gene_name', metavar='-target_gene_name', type=str,
                    help='Target Gene Name')
parser.add_argument('first_downstream_gene_name', metavar='-1st_downstream_flanking_gene_name',
                    type=str, help='1st Downstream Flanking Gene Name')
parser.add_argument('second_downstream_gene_name', metavar='-2nd_downstream_flanking_gene_name',
                    type=str, help='2nd Downstream Flanking Gene Name')
parser.add_argument('third_downstream_gene_name', metavar='-3rd_downstream_flanking_gene_name',
                    type=str, help='3rd Downstream Flanking Gene Name')
parser.add_argument('first_upstream_gene_name', metavar='-1st_upstream_flanking_gene_name',
                    type=str, help='1st Upstream Flanking Gene Name')
parser.add_argument('second_upstream_gene_name', metavar='-2nd_upstream_flanking_gene_name',
                    type=str, help='2nd Upstream Flanking Gene Name')
parser.add_argument('third_upstream_gene_name', metavar='-3rd_upstream_flanking_gene_name',
                    type=str, help='3rd Upstream Flanking Gene Name')
parser.add_argument('target_species_list_file_path', metavar='-target_species_list_file_path',
                    type=str, help='Target Species List File Path (.txt)')
parser.add_argument('sequences_content_output_file_path', metavar='-sequences_content_output_file_path',
                    type=str, help='Output Sequence Content File Path (FASTA)')
parser.add_argument('sequences_data_output_file_path', metavar='-sequences_data_output_file_path',
                    type=str, help='Output Sequence Data File Path (.csv)')
args = parser.parse_args()

print('Genomic Sequence Downloader Script\n')

species_counter = 0
species_list_file = open(args.target_species_list_file_path, 'r')
sequences_output_file = open(args.sequences_content_output_file_path, 'w')
sequences_data_file = open(args.sequences_data_output_file_path, 'w')

for current_species in species_list_file:
    species_counter += 1
    current_species = current_species.replace(
        '\n', '').replace('_', ' ').strip()
    print('['+str(species_counter)+' - '+current_species+']')
    check_target_gene_annotation_status()
    print('\n')

species_list_file.close()
sequences_output_file.close()
sequences_data_file.close()
