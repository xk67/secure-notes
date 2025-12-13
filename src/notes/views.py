from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
import markdown

@login_required
def note(request):

    return render(request, "notes/index.html")

@login_required
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
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

    return render(request, "notes/create.html", context)

@login_required
def list_notes(request):

    user = request.user
    notes_user = user.notes.all()
    for note in notes_user:
        print(note.uuid)
    notes_all = Note.objects.filter(private=False).exclude(owner=user)

    context = {
        "notes_user": notes_user,
        "notes_all": notes_all
    }

    return render(request, "notes/list_notes.html", context)