from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notes.models import Note
from notes.forms import NoteForm, NoteSearchForm
from django.http import HttpResponse, Http404
from django.db.models import Q
from notes.utils import markdown2html_safe

@login_required
def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            form.save()
            html = markdown2html_safe(form.cleaned_data['content'])
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
    notes_all = Note.objects.filter(private=False).exclude(owner=user)

    context = {
        "notes_user": notes_user,
        "notes_all": notes_all
    }

    return render(request, "notes/list_notes.html", context)

@login_required
def show_note(request, uuid):

    try:
        html = markdown2html_safe(Note.objects.get(uuid=uuid).content)
    except:
        raise Http404()

    return HttpResponse(html)

@login_required
def search_note(request):
    if request.method == "GET":

        form = NoteSearchForm(request.GET)

        q = ""
        notes =  Note.objects.none()
        if form.is_valid():
            q = form.cleaned_data['q']

            notes = Note.objects.filter(
                    (Q(owner=request.user) | Q(private=False)) &
                    Q(title__icontains=q)
                ).distinct()

        context = {'form': form, 'notes': notes, 'query': q}

        return render(request, 'notes/search_note.html', context)
