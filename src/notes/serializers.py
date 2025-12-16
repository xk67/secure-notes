from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ["owner", "title", "content", "private", "uuid"]
        #read_only_fields = ["id", "created_at"]