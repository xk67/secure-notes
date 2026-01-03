from rest_framework import serializers
from .models import Note
from .utils import markdown2html_safe

class NoteSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = ["owner", "title", "content", "uuid"]
        #read_only_fields = ["id", "created_at"]

class NoteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["content"]
        read_only_fields = ["content"]

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "content", "private"]

    def create(self, validated_data):
        user = self.context["user"]
        validated_data['content'] = markdown2html_safe(validated_data['content'])
        return Note.objects.create(owner=user, **validated_data)
