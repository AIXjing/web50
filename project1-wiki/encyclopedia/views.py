from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django.shortcuts import render
from django import forms
from django.urls import reverse
import random

from . import util

# a class to create a new form
class NewItem(forms.Form):
    title =  forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.Textarea(), label='')

# a class to edit content
class EditItem(forms.Form):
    edit = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if (entry):
        text = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": text
        })
    else:
        return HttpResponse("The page is not found!") 
        
def search(request):
    if 'q' in request.GET:
        m = (request.GET['q']).lower()
        searched_results = []
        for entry in util.list_entries():
            if m in entry.lower():
                searched_results.append(entry)
            
        if searched_results:
            return render(request, "encyclopedia/search.html", {
                "filtered_entries": searched_results,
            })
        # if no result is found, return the Home page
        else:
            return index(request)
    else:
        return index(request)


# Create a new wiki page
def new(request):
    if request.method == "POST":
        form = NewItem(request.POST)
        if form.is_valid():
            title = (form.cleaned_data["title"]).capitalize()
            # check if the title exists 
            # if it exists, throw an error page 
            for entry in util.list_entries():
                if title == entry:
                    return render(request, "encyclopedia/error01.html")

            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            url = reverse('entry', kwargs = {'title':title})
            return HttpResponseRedirect(url)
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
                "form": NewItem()
            })

# Edit a page
# @refer to: https://forum.djangoproject.com/t/django-form-is-adding-extra-spaces-everytime-content-is-edited/3986
def edit(request, title):
    if request.method == "GET":
        # show previous value on the page
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit": EditItem(initial={
                'edit': util.get_entry(title)
                })
        })
    else:
        # only content was changed
        edited_content = EditItem(request.POST)
        if edited_content.is_valid():
            content = edited_content.cleaned_data['edit']
            util.save_entry(title, content)
        return entry(request, title)

# redirect to a random page
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    
    return render(request, "encyclopedia/entry.html", {
            "title": random_entry,
            "entry": markdown2.markdown(util.get_entry(random_entry))
            })
    