# Soybean_WGS_Collection Pipeline
k-genome pipeline submission </br>


 최근 Next generation sequencer(NGS) 기술의 발달로 Sequencing 비용이 저렴해지고 모델 생물체들에 대한 수백만 개의 Single Nucleotide Polymorphism(SNP)를 발견함에 따라 유전체를 기반으로 하는 개체의 profiling이 가능해졌다. 나아가 유전자 가위 기술의 발달은 유전체학을 통해 발견한 유용 후보유전자들의 직접적 도입을 가능하게 하여 기후변화에 의한 적응성 품종 개발, 소비자 맞춤형 품종 개발, 해외 작물 생산 전초기지 맞춤형 품종 개발을 가속화 할 수 있게 되었다. 이러한 미래 기술의 시작점인 유전체학 발전의 가속화를 위해서는 Whole Genome Sequence(WGS) 데이터를 효율적으로 수집하고 분석하는 것이 중요한데, 폭발적으로 증가하고 있는 WGS 데이터량에 비해 실험연구자, 육종가, 타분야 융합 연구자들이 쉽게 접근하여 사용할 수 있는 데이터 형태는 아직 개발되지 않았으며 이를 목적에 맞게 수집, 관리 할 수 있는 플랫폼 개발 역시 부족하다. 대표적인 WGS 결과 파일로서 Variant Call Format(VCF)는 SNP 및 Insertion/Deletion(InDel)과 같은 변이 정보들을 저장하기 위한 생물정보학 텍스트 파일 포맷이며 연구자가 WGS 실험 분석 서비스를 받을 경우 주로 제공 받는 파일 포맷이다. 따라서 VCF 파일과 NCBI에 존재하는 원데이터들을 활용한 데이터 수집 전략을 확보 할 수 있다면 향후 유전체 빅데이터를 이용한 분석이 원활해 질 것으로 보인다. 본 연구에서는 NCBI에 존재하는 Soybean WGS를 효율적으로 수집하고 정리하기 위해 NCBI ID 로 부터 VCF 파일을 생성하고 기존의 genotype matrix에 병합하여 분석하는 파이프라인을 개발하였다. 작성된 genotype matrix를 주성분 분석 및 군집 분석 방법을 통해 cultivar 간의 관계를 분석하고 알려진 cultivar들의 관계와 비교하여 만들어진 genotype matrix의 유효성을 검증한다. 분석을 통해 작성된 유전체 빅데이터를 기반으로 농업 생산량 예측 모델, 미확인 샘플 확인, 유전체를 통한 농작물 이력 추적, 수출입 검역을 위한 유전체 기반 금지 동식물 혼입 판단 등 다양한 목적을 위해 역할 할 수 있을 것으로 기대된다.

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
django 

# reference files
Phytozome v12.1(Gmax_275_v2.0.fa) https://phytozome.jgi.doe.gov/pz/portal.html# </br>
bwa index 작업 필요 </br>

# command line 
$ python3 vcf_genome.py [SRR_ID] [ref file location] </br>
$ python3 vcf_input.py [Cultivar] [vcf_location]

# test vcf files

https://drive.google.com/drive/folders/1EVvClvQZ0wYHQ2S_5M5Od-nRPuK1IKye?usp=sharing </br>

file_list : 
1. SRR2206271.vcf.gz | Santa_Rosa
2. SRR5479930.vcf.gz | WJK-PRC-46
