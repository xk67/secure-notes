from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "private"]
        widgets = {
            'content': forms.Textarea(attrs={
                'id': 'md-textarea',
                'placeholder': 'Enter your markdown here...',
            })
        }

class NoteSearchForm(forms.Form):
    q = forms.CharField(
          required=True,
          max_length=32,
          label="Search",
          widget=forms.TextInput(attrs={'placeholder': 'Enter note title'})
      )

class NoteDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label='Check if you want to delete this note',
        required=True
    )
