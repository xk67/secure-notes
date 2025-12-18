from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "private"]

class NoteSearchForm(forms.Form):
    q = forms.CharField(
          required=True,
          max_length=32,
          label="Search",
      )
