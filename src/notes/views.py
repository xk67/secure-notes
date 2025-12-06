from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm

def index(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.data)
            return redirect("notes:index")
    else:
        form = NoteForm()

    context = {
        "form": form,
    }

    return render(request, "notes/index.html", context)