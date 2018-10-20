import sys, os
import pandas as pd
import numpy as np
import glob
import pickle
from functools import reduce
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#ID 받는 부분
SRR_ID = sys.argv[1]
ref_location = sys.argv[2]
vcf_grep_location = sys.argv[3]

#vcf
#os.system('zcat ./vcf_files/%s.vcf.gz | grep -v \'##\' > ./vcf_files/%s.vcf.grep'%(SRR_ID,SRR_ID))

#web scrap
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path='/bin/chromedriver', chrome_options=options)
driver.get('https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=' + SRR_ID)
element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="id-common-fields"]/div/div[27]/em')))

try:
    div_selector = driver.find_element_by_css_selector('div').text
    cultivar = div_selector.split('cultivar')[1].split('\n')[1]
    col_name = cultivar
except IndexError:
    col_name = SRR_ID

#data arrange

ncbi_sample = pd.read_csv('%s'%vcf_grep_location, sep = '\t')

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
ncbi_gt_mat = pd.DataFrame(gt_list, index=pos, columns=[col_name])


#standard_mat = pd.read_csv('./Kor_Soybean.csv')
#selected_pos = standard_mat['pos'].values
#dic_fill = dict(zip(standard_mat['pos'],standard_mat['Gmax_275_ref']))
dic_fill = pickle.load(open("./pk_files/pos_ref.pk", "rb"))
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
add_mat = pd.DataFrame(add_data, index= [col_name])
add_mat.columns = [str(x) for x in add_mat.columns]
add_mat = add_mat.reset_index()

#matrix 병합
pre_mat_pca = pd.read_pickle('./pk_files/standard_pca_mat.pk')
add_mat.to_pickle('./mat_list/%s.pk'%SRR_ID)
matrix_list = glob.glob('./mat_list/*')
df_list = [pd.read_pickle(x) for x in matrix_list]
add_total_mat = reduce(lambda a,b : a.append(b), df_list)
output_mat = pre_mat_pca.append(add_total_mat)
output_mat.to_csv('./django_vcf/static/output_pca_mat.csv', index=False)

#runserver
os.system('python3 manage.py runserver')
