import random

from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

from markdown2 import Markdown


class SearchForm(forms.Form):
    search = forms.CharField(label="Search",
        widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class CreateForm(forms.Form):
    title = forms.CharField(label="Title",
        widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Enter the page's content"}))

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_input = form.cleaned_data["search"]

            #check if search input matches to one of the entries 
            if search_input in util.list_entries():
                page = util.get_entry(search_input)
                page_converted = Markdown().convert(page)
                return HttpResponseRedirect(f"wiki/{search_input}")
            
            #generate a list of search matches
            search_matches = [] 
            for entry in util.list_entries():
                if search_input.lower() in entry.lower():
                    search_matches.append(entry)
            
            #check if there are no found pages
            if not search_matches:
                contex = {
                    "error_message" : f"Search: No results for [{search_input}] were found",
                    "form" : SearchForm(),
                }
                return render(request, "encyclopedia/error.html", contex)

            #render the page displaying the search results    
            return render(request, "encyclopedia/search.html", {
                "entries" : search_matches,
                "form" : SearchForm(),
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm(),
    })


def entry(request, title):
    if title in util.list_entries():
        page = util.get_entry(title)
        page_converted = Markdown().convert(page)
        contex = {
            "title" : title,
            "page" : page_converted,
            "form" : SearchForm(),
        }
        return render(request, "encyclopedia/entry.html", contex)

    else:
        contex = {
            "error_message" : f"Error: Requested page [{title}] is not found",
            "form" : SearchForm(),
        }
        return render(request, "encyclopedia/error.html", contex)

def create(request):
    
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data["title"]
            form_text = form.cleaned_data["text"]
            form_text_converted = Markdown().convert(form_text)

            #check if encyclopedia entry already exists 
            if form_title in util.list_entries():
                contex = {
                    "error_message" : f"Error: Page with title [{form_title}] already exists",
                    "form" : SearchForm(),
                }
                return render(request, "encyclopedia/error.html", contex)

            util.save_entry(form_title, form_text_converted)
            return HttpResponseRedirect(reverse("encyclopedia:index") + f"wiki/{form_title}")


    return render(request, "encyclopedia/create.html", {
        "entries": util.list_entries(),
        "form" : SearchForm(),
        "CreateForm" : CreateForm(),
    })

def random_page(request):
    random_page = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:index") + f"wiki/{random_page}")
