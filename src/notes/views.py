from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm, NoteSearchForm
from django.http import HttpResponse, Http404
from .serializers import NoteSerializer, NoteContentSerializer, NoteCreateSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import markdown
from uuid import UUID

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_list_notes(request):

    user = request.user
    notes_user = user.notes.all()
    notes_all = Note.objects.filter(private=False).exclude(owner=user)
    notes = notes_user | notes_all

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

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_note(request):

    serializer = NoteCreateSerializer(data=request.data, context={"user": request.user})

    if serializer.is_valid():
        note = serializer.save()
        return Response({"uuid": note.uuid}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
