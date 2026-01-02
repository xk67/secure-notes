from notes.serializers import NoteSerializer, NoteContentSerializer, NoteCreateSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from notes.models import Note
from django.http import  Http404
from uuid import UUID

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_notes(request):

    user = request.user
    notes_user = user.notes.all()
    notes_all = Note.objects.filter(private=False).exclude(owner=user)
    notes = notes_user | notes_all

    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_note(request, uuid):

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
def create_note(request):

    serializer = NoteCreateSerializer(data=request.data, context={"user": request.user})

    if serializer.is_valid():
        note = serializer.save()
        return Response({"uuid": note.uuid}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
