from django.contrib import admin
from .models import Note, NoteCareTaker, NoteMemento
from .forms import NoteForm


class NoteAdmin(admin.ModelAdmin):
    form = NoteForm


admin.site.register(Note, NoteAdmin)
admin.site.register(NoteCareTaker)
admin.site.register(NoteMemento)
