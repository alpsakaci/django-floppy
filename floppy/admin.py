from django.contrib import admin
from .models import Note
from .forms import NoteForm

class NoteAdmin(admin.ModelAdmin):
    form = NoteForm

admin.site.register(Note, NoteAdmin)
