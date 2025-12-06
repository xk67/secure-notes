from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm
import markdown

def index(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            html = markdown.markdown(form.cleaned_data['content'])
            #return redirect("notes:index")
    else:
        form = NoteForm()
        html = None

    context = {
        "form": form,
        "html": html
    }

    return render(request, "notes/index.html", context)