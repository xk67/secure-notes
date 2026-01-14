from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from notes.models import Note
from notes.forms import NoteForm, NoteSearchForm, NoteDeleteForm
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ValidationError
from notes.utils import markdown2html_safe, sanitize_title
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST, require_GET

@login_required
def create_note(request):
    note_url = None
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.title = sanitize_title(form.cleaned_data['title'])
            note.content = markdown2html_safe(form.cleaned_data['content'])
            note.save()
            note_url = request.build_absolute_uri(reverse("notes:view_note", kwargs={"uuid": note.uuid}))
            form = NoteForm()
    else:
        form = NoteForm()

    return render(request, "notes/create_note.html", {"form": form, "note_url": note_url})

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
def view_note(request, uuid):

    try:
        note = Note.objects.get(uuid=uuid)
    except (Note.DoesNotExist, ValidationError):
        raise Http404()

    if request.method == "POST":
        if note.owner != request.user:
            raise Http404()

        form = NoteDeleteForm(request.POST)
        if form.is_valid():
            note.delete()
            return redirect("notes:list_notes")
    else:
        form = NoteDeleteForm()

    context = {
        "note_title": note.title,
        "note_content": mark_safe(note.content),
        "form": form,
        "is_owner": note.owner == request.user
    }

    return render(request, "notes/view_note.html", context)

@login_required
@require_GET
def search_note(request):

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

@login_required
@require_POST
def preview_note(request):
    markdown = request.POST.get('markdown') or ''
    return HttpResponse(markdown2html_safe(markdown).encode())
