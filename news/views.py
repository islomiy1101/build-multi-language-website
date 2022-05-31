from django.shortcuts import render,get_object_or_404
from .models import Article
def article_detail(request,slug):
    data=get_object_or_404(Article,slug=slug)
    context={
        'data':data
    }
    return render(request,'news/article_detail.html',context)
