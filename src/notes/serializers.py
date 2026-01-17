from rest_framework import serializers
from .models import Note
from .utils import markdown2html_safe, sanitize_title

class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ["title", "content", "uuid", "owner"]

    def get_owner(self, obj):
        return obj.owner.username

class NoteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["content"]

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", "content", "private"]

    def create(self, validated_data):
        user = self.context["user"]
        validated_data['title'] = sanitize_title(validated_data['title'])
        validated_data['content'] = markdown2html_safe(validated_data['content'])
        return Note.objects.create(owner=user, **validated_data)
