from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from personal.models import Sentence, NameForm




def index(request):
    return render(request,'personal/home.html')

def contact(request):
    return render(request,'personal/index.html')

def prediction(request):
    #print(MODEL.summary())
    Text = request.POST.get('Text',False)
    print(Text)
    Sentenceex = Sentence(str(Text))
    predct = Sentenceex.predection()
    #put(self, request, pk):
    print("Prediction is :",float(predct))#Sentence preparation
    ## POST request
   # model = mlmodel()
    #model.Text = Text
    #model.prediction = float(predct)
    #response = requests.post('/predictions/', data=model)

    return render(request, 'personal/home.html', {'prediction':  round(float(predct), 2) * 100})
