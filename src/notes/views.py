from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.http import HttpResponse, Http404
from .serializers import NoteSerializer, NoteContentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import markdown
from uuid import UUID
from rest_framework.generics import get_object_or_404

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
    notes_all = Note.objects.filter(private=False).exclude(owner=user)

    context = {
        "notes_user": notes_user,
        "notes_all": notes_all
    }

    return render(request, "notes/list_notes.html", context)

@login_required
def show_note(request, uuid):

    try:
        html = markdown.markdown(Note.objects.get(uuid=uuid).content)
    except:
        raise Http404()    

    return HttpResponse(html) 

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def api_list_notes(request):

    if request.method == "GET":
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_get_note(request, uuid):
    
    try:
        UUID(uuid, version=4)
    except ValueError:
        raise Http404() 

    try:
        note = Note.objects.get(uuid=uuid)
    except Note.DoesNotExist:
        raise Http404("Not found.")

    serializer = NoteContentSerializer(note)
    return Response(serializer.data)