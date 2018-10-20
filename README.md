# Soybean_WGS_Collection Pipeline
k-genome pipeline submission </br>

한국농촌진흥청에서 soybean genotype chip을 이용하여 작성한 총 222점의 콩 유전형 자료를 바탕으로 뼈대가 될 matrix를 작성하고 유전형 profile을 기반으로한 빠른 분석을 위해 해당 matrix를 python scikit-learn의 pca 차원 축소기능을 활용하여 20개의 주성분으로 이루어진 222 samples X 20 PCA matrix를 작성하였다. 이때 훈련된 주성분 가중치는 파일로 저장하고 이후 수집되는 유전형 vector를 주성분으로 변환하는데 사용되었다. </br>
여기에 다양한 연구에 의해 생성된 Soybean WGS 데이터를 NCBI SRA를 통해 추가로 수집하고 얻은 raw data를 활용해 vcf 파일을 생성 이렇게 작성된 genotype을 PCA 가중치를 통해 20 PCA vector로 하는 작업을 거쳤다. 신규로 만들어진 PCA vector는 기반 matrix와 병합한뒤 직관적인 정보확인 및 공유를 위해 Django (https://www.djangoproject.com/ ) 와 D3.js (https://d3js.org/) 를 통해 웹 기반 군집분석 및 시각화를 수행하였다. 이를 통해 Query SRA ID입력에 의해 자동으로 genotype matrix를 작성가능하게 되었다.

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
Pythozomev12.1(Gmax_275_v2.0.fa)</br>
bwa index 작업 필요 </br>

# command line 
$ python3 vcf_genome.py [SRR_ID] [ref file location] </br>
$ python3 vcf_genome_test.py [SRR_ID] [ref_file_location] [vcf_grep_loacation]
