from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.
#goruntu veya metod olusturmak için kullanılır 
#ornegin index metodunu cagirdiğimida bize bu metodla ilişkili olan index.html sayfasını getirecek 
#localhost:
#http://127.0.0.1:8000/index

def index(request):
    return render(request,'pages/index.html')
def about(request):
    return render(request,'pages/about.html')






