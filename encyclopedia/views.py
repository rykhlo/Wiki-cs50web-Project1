from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

from markdown2 import Markdown



class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
    # if request.method == "POST":  #when the user submits data
    #     form = NewTaskForm(request.POST) #save the submitted data inside of form 
    #     if form.is_valid(): #check if the format of the task is valid
    #         task = form.cleaned_data["task"]
    #         request.session["tasks"] += [task] #tasks.append(task)
    #         return HttpResponseRedirect(reverse("tasks:index"))
    #     else:
    #         return render(request, "tasks/add.html", {
    #             "form" : form  #render the same add.html but with form that the user submitted
    #         })
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_input = form.cleaned_data["search"]
            if search_input in util.list_entries():
                page = util.get_entry(search_input)
                page_converted = Markdown().convert(page)
                content = {
                    "title" : search_input,
                    "page" : page_converted,
                    "form" : form,
                }
                return HttpResponseRedirect(f"wiki/{search_input}")
            
            #generate a list of search matches
            search_matches = [] 
            for entry in util.list_entries():
                if search_input.lower() in entry.lower():
                    search_matches.append(entry)

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
        content = {
            "title" : title,
            "page" : page_converted,
            "form" : SearchForm(),
        }
        return render(request, "encyclopedia/entry.html", content)

    else: #TODO
        return 

