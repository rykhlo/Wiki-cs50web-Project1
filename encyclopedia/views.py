from django.shortcuts import render

from . import util

from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
})

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = Markdown().convert(page)
        content = {
            "title" : title,
            "page" : page_converted,
        }
        return render(request, "encyclopedia/entry.html", content)

    else: #TODO
        return 


