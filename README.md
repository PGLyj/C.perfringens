# Soybean_WGS_Collection Pipeline
k-genome pipeline submission </br>

# dependency

aspera fastq-dump 2.9.2 -SRATOOLS </br>
bwa 0.7.17-r1188 </br>
samtools 1.9 </br>
sambamba 0.6.7 </br>
bcftools 1.9 </br>
selenium 3.14.1 </br>
numpy -1.15.2 </br>
CHROMEDRIVER 2.43 linux 64 </br>
sklearn 0.19.2 </br>
pandas 0.22.0 </br>

# reference files
Pythozomev12.1(Gmax_275_v2.0.fa)

# command line 
$ python3 vcf_genome.py [SRR_ID] [ref file location] </br>
$ python3 vcf_genome_test.py [SRR_ID] [ref_file_location] [vcf_grep_loacation]
