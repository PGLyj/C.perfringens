from django.shortcuts import render
from django import forms

# Create your views here.
def index(request):
    #DBex    = DBmodel.objects.order_by('?')[0:2] # 렌덤으로 클레스를 가져온다.

    if request.method=='POST':


            return render(request, 'django_vcf/index.html',{'csvf':'output_pca_mat.csv'})

    else:
        return render(request, 'django_vcf/index.html',{'csvf':'output_pca_mat.csv'})
