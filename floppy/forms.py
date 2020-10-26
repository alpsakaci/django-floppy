from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Note

class NoteForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=20, widget=forms.TextInput(attrs={'class': "form-control mb-3"}), required=False)
    content = forms.CharField(label='', widget=CKEditorWidget())

    class Meta:
        model = Note
        fields = ['title', 'content']

class SearchForm(forms.Form):
    query = forms.CharField(label='', widget=forms.TextInput(attrs={'class': "form-control mb-3", 'placeholder':"Search Note"}))
