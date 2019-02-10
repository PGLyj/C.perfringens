import sys, os
import pandas as pd
import numpy as np
import glob
import pickle
from functools import reduce
from sklearn.decomposition import PCA
from sklearn.externals import joblib

fastq = sys.argv[1]
ref_location = sys.argv[2]

#변환과정
os.system('bwa mem -t 20 %s %s_1.fastq %s_2.fastq -o ./Downloads/%s.sam'%(ref_location,fastq, fastq, fastq))
os.system('samtools fixmate -O bam ./Downloads/%s.sam ./Downloads/%s.bam'%(fastq, fastq))
os.system('sambamba sort -t  40 -o ./Downloads/%s.sort.bam ./Downloads/%s.bam --tmpdir ./Downloads/tmp'%(fastq, fastq))
#os.system('rm %s_*.fastq'%(fastq))
os.system('bcftools mpileup -Ob -o ./Downloads/%s.bcf -f %s ./Downloads/%s.sort.bam'%(fastq, ref_location, fastq))
os.system('bcftools call -vmO z -o ./vcf_files/%s.vcf.gz ./Downloads/%s.bcf'%(fastq, fastq))
os.system('zcat ./vcf_files/%s.vcf.gz | grep -v \'##\' > ./vcf_files/%s.vcf.grep'%(fastq,fastq))

ncbi_sample         = pd.read_csv('./vcf_files/%s.vcf.grep'%(fastq), sep = '\t')
ncbi_sample.columns = ncbi_sample.columns[0:9].tolist() + [fastq]
m_snp               = ncbi_sample['INFO'].apply(lambda x : x.split(';')[0] != 'INDEL')
ncbi_sample_snp     = ncbi_sample[m_snp]

def matrix_REF(x):
    allele = np.array([x['REF']] + x['ALT'].split(','))
    gt_list_REF = x[c_gt]
    def change_REF(i):
        try:
            ix = list(map(int,i.split(':')[0].split('/')[1]))
            return ''.join(allele[ix])
        except ValueError:
            return 'N'
    return [change_REF(i) for i in gt_list_REF]

c_gt_REF    = ncbi_sample_snp.columns[9:]
gt_list_REF = ncbi_sample_snp.apply(matrix_REF,axis=1)
gt_list_REF = np.stack(gt_list_REF)

snp_INFO = pd.DataFrame(gt_list_REF, index=ncbi_sample_snp['#CHROM'], columns = [fastq])
snp_INFO['POS'] = np.array(ncbi_sample_snp['POS'])

snp_INFO.to_csv('%s.csv'%fastq)

def matrix(x):
    allele  = np.array([x['REF']] + x['ALT'].split(','))
    gt_list = x[c_gt]
    def change(i):
        try:
            ix = list(map(int,i.split(':')[0].split('/')))
            return ''.join(allele[ix])
        except ValueError:
            return 'NN'
    return [change(i) for i in gt_list]

c_gt    = ncbi_sample_snp.columns[9:]
gt_list = ncbi_sample_snp.apply(matrix,axis=1)
gt_list = np.stack(gt_list)

#pos 지정 => index 맞추기 작업
pos         = np.add(np.add(ncbi_sample_snp['#CHROM'],'_'),ncbi_sample_snp['POS'].astype(str)).values
ncbi_gt_mat = pd.DataFrame(gt_list, index=pos, columns = [fastq])

#standard_mat = pd.read_csv('./Kor_Soybean.csv')
#selected_pos = standard_mat['pos'].values
#dic_fill = dict(zip(standard_mat['pos'],standard_mat['Gmax_275_ref']))
dic_fill = pickle.load(open("./pk_files/pos.pk", "rb"))

selected_pos            = np.array(list(dic_fill.keys()))
df_ncbi_gt_mat_selected = ncbi_gt_mat.loc[selected_pos].T.fillna(value=dic_fill).T

def seq_convert(x):
    dicN    = {'A':'1','T':'2','G':'3','C':'4','N':'0'}
    gt      = list(x)
    gt.sort()
    result  = ''.join([dicN[i] for i in x])
    return int(result,5)

seq_convert_vec = np.vectorize(seq_convert)
ncbi_seq_vec    = seq_convert_vec(np.stack(df_ncbi_gt_mat_selected.values))
df_ncbi_vec     = pd.DataFrame(ncbi_seq_vec, columns=df_ncbi_gt_mat_selected.columns)

#pca 
pca             = joblib.load('./pk_files/c_perfringens.pca .pkl')
add_data        = pca.transform(df_ncbi_vec.T)
add_mat         = pd.DataFrame(add_data, index= [fastq])
add_mat.columns = [str(x) for x in add_mat.columns]
add_mat         = add_mat.reset_index()

pre_mat_pca = pd.read_pickle('./pk_files/standard_pca_mat.pk')
add_mat.to_pickle('./mat_list/%s.pk'%(fastq))

matrix_list     = glob.glob('./mat_list/*')
df_list         = [pd.read_pickle(x) for x in matrix_list]
add_total_mat   = reduce(lambda a,b : a.append(b), df_list)
output_mat      = pre_mat_pca.append(add_total_mat)
output_mat.to_csv('./django_vcf/static/output_pca_mat.csv', index=False)