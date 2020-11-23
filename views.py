from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
import random

from . import util

md = Markdown()

class NewPageForm(forms.Form):
    title = forms.CharField(initial="",label='Page Title',widget=forms.TextInput(
        attrs={'size':'60','maxlength':'70'} ))
    mkCode = forms.CharField(initial="",label='Markdown Code',widget=forms.Textarea)



class SearchForm(forms.Form):
    q = forms.CharField(label='search', max_length=100, widget=forms.TextInput(
        attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}))

def editPage(request,name):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            print(name.lower())
            print(form.cleaned_data["title"].lower())
            if form.cleaned_data["title"].lower() == name.lower():
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["mkCode"])
                messages.success(request, 'The page has been successfully edited!')
                return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                'form':SearchForm()
    })
            else:
                messages.warning(request, 'The page title cant be changed')
    else:
        data={'title':name,'mkCode':util.get_entry(name)}
        form = NewPageForm(data)
    return render(request, 'encyclopedia/create.html', {
        'form':SearchForm(),
        'CreatePageForm': form,
        'editcheck': name
        })
    

def newPage(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            titleList = util.list_entries()
            smallTitleList=[]
            for x in titleList:
                smallTitleList.append(x.lower())
            if form.cleaned_data["title"].lower() not in smallTitleList:
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["mkCode"])
                messages.success(request, 'A page has been successfully created! You can add another.')
                form = NewPageForm()
            else:
                messages.warning(request, 'The page title already exists')
    else:
        form = NewPageForm()

    return render(request, 'encyclopedia/create.html', {
        'form':SearchForm(),
        'CreatePageForm': form,
        'editcheck':'duh'
        })

def randomPage(request):
    entries= util.list_entries()
    length = len(entries)
    number=random.randint(0, length-1)
    return render(request,"encyclopedia/page.html",{
        "entries":md.convert(util.get_entry(entries[number])),
        "title":entries[number],
        'form':SearchForm()
        }) 




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form':SearchForm()
    })

def get_search(request):
    searchVar = request.GET['q']
    count = 0
    entries=[]
    if util.get_entry(searchVar) == None:
        for entry in  util.list_entries():
            if searchVar.lower() in entry.lower():
                entries.append(entry)
                count+=1
        if count > 0 :
            return render(request,"encyclopedia/search.html",{
            "results":entries,
            'form':SearchForm(),
            'type':'one'
            }) 

        else:
            return render(request,"encyclopedia/search.html",{
            "results":'None',
            'form':SearchForm(),
            'type':'two'
            }) 
    else:
        return render(request,"encyclopedia/search.html",{
        "results":md.convert(util.get_entry(searchVar)),
        'form':SearchForm(),
        'type':'three'
        })

def query(request,name):
    if util.get_entry(name) == None:
       return render(request,"encyclopedia/page.html",{
        "entries":'None',
        "title":name,
        'form':SearchForm()
        }) 
    else:
        return render(request,"encyclopedia/page.html",{
            "entries":md.convert(util.get_entry(name)),
            "title":name,
            'form':SearchForm()
        })

