import sys, os
import pandas as pd
import numpy as np
import glob
import pickle
from functools import reduce
from sklearn.decomposition import PCA
from sklearn.externals import joblib


#ID 받는 부분
Cultivar = sys.argv[1]
vcf_location = sys.argv[1]

#vcf
os.system('zcat %s | grep -v \'##\' > ./%s.vcf.grep'%(vcf_location,Cultivar))

#data arrange

ncbi_sample = pd.read_csv('./%s.vcf.grep'%Cultivar, sep = '\t')

m_snp = ncbi_sample['INFO'].apply(lambda x : x.split(';')[0] != 'INDEL')
ncbi_sample_snp = ncbi_sample[m_snp]

#genotype list 만들기
def matrix(x):
    allele = np.array([x['REF']] + x['ALT'].split(','))
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
pos = np.add(np.add(ncbi_sample_snp['#CHROM'],'_'),ncbi_sample_snp['POS'].astype(str)).values
ncbi_gt_mat = pd.DataFrame(gt_list, index=pos, columns=[Cultivar])


#standard_mat = pd.read_csv('./Kor_Soybean.csv')
#selected_pos = standard_mat['pos'].values
#dic_fill = dict(zip(standard_mat['pos'],standard_mat['Gmax_275_ref']))
dic_fill = pickle.load(open("./pk_files/pos_ref.pk", "rb"))
selected_pos = np.array(list(dic_fill.keys()))
df_ncbi_gt_mat_selected = ncbi_gt_mat.loc[selected_pos].T.fillna(value=dic_fill).T

#gt 수치화 작업
def seq_convert(x):
    dicN = {'A':'1','T':'2','G':'3','C':'4','N':'0'}
    gt = list(x)
    gt.sort()
    result = ''.join([dicN[i] for i in x])
    return int(result,5)
seq_convert_vec = np.vectorize(seq_convert)
ncbi_seq_vec = seq_convert_vec(np.stack(df_ncbi_gt_mat_selected.values))
df_ncbi_vec = pd.DataFrame(ncbi_seq_vec, columns=df_ncbi_gt_mat_selected.columns)

#pca 
pca = joblib.load('./pk_files/vcf2genome.pca.pkl')
add_data = pca.transform(df_ncbi_vec.T)
add_mat = pd.DataFrame(add_data, index= [Cultivar])
add_mat.columns = [str(x) for x in add_mat.columns]
add_mat = add_mat.reset_index()

#matrix 병합
pre_mat_pca = pd.read_pickle('./pk_files/standard_pca_mat.pk')
add_mat.to_pickle('./mat_list/%s.pk'%Cultivar)
matrix_list = glob.glob('./mat_list/*')
df_list = [pd.read_pickle(x) for x in matrix_list]
add_total_mat = reduce(lambda a,b : a.append(b), df_list)
output_mat = pre_mat_pca.append(add_total_mat)
output_mat.to_csv('./django_vcf/static/output_pca_mat.csv', index=False)

#runserver
os.system('python3 manage.py runserver')
