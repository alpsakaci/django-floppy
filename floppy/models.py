from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import datetime  
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

CHANGE = 1
DELETION = 2

ACTION_FLAG_CHOICES = (
    (CHANGE, _('Change')),
    (DELETION, _('Deletion')),
)

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        str = ""
        if (self.title != ""):
            str = str + "Title: " + self.title + " | "
        str = str + "Content: " + self.content
        return str

class NoteLog(models.Model):
    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )
    action_flag = models.PositiveSmallIntegerField(_('action flag'), choices=ACTION_FLAG_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = RichTextField()
    change_title = models.CharField(max_length=50, blank=True, null=True)
    change_content = RichTextField(blank=True, null=True)

    def init_log(self, note, action_flag):
        self.action_flag = action_flag
        self.owner = note.owner
        self.title = note.title
        self.content = note.content

    def set_log(self, note):
        if (self.action_flag != 2):
            self.change_title = note.title
            self.change_content = note.content

    def __str__(self):
        str = ""
        if (self.title != ""):
            str = str + "Title: " + self.title + " | "
        str = str + "Content: " + self.content
        return str