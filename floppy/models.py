from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.db.models import Q
from floppy.snapshot import NoteOriginator
from django.shortcuts import get_object_or_404


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, null=True)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(default=timezone.now, blank=True)
    deleted = models.BooleanField(default=False)

    @staticmethod
    def create(owner, title, content):
        note = Note.objects.create(owner=owner, title=title, content=content)
        caretaker = NoteCareTaker(note=note)
        note.save()
        caretaker.save()

        return note

    def edit(self, title, content):
        NoteOriginator.take_snapshot(note=self)

        self.title = title
        self.content = content
        self.date_modified = timezone.now()
        self.save()

    def move_to_trash(self):
        self.deleted = True
        self.save()

    def restore(self):
        self.deleted = False
        self.save()

    def revert(self, memento_id):
        care_taker = Note.get_care_taker(note=self)
        memento = get_object_or_404(
            NoteMemento.objects.filter(id=memento_id, care_taker=care_taker)
        )
        NoteOriginator.take_snapshot(note=self)
        self.title = memento.title
        self.content = memento.content
        self.date_modified = timezone.now()
        if self.deleted == True:
            self.deleted = False
        self.save()
        memento.delete()

    def deletememento(self, memento_id):
        care_taker = Note.get_care_taker(note=self)
        memento = get_object_or_404(
            NoteMemento.objects.filter(id=memento_id, care_taker=care_taker)
        )
        memento.delete()

    @staticmethod
    def get_user_notes(user):
        return (
            Note.objects.filter(owner=user, deleted=False)
            .order_by("date_modified")
            .reverse()
        )

    @staticmethod
    def get_deleted_notes(user):
        return (
            Note.objects.filter(owner=user, deleted=True)
            .order_by("date_modified")
            .reverse()
        )

    @staticmethod
    def get_care_taker(note):
        care_taker = None
        try:
            care_taker = NoteCareTaker.objects.get(note=note)
        except:
            care_taker = NoteCareTaker(note=note)
            care_taker.save()

        return care_taker

    @staticmethod
    def get_older_versions(user, note_id):
        note = get_object_or_404(Note.objects.filter(id=note_id, owner=user))
        care_taker = Note.get_care_taker(note)
        memento_list = (
            NoteMemento.objects.filter(care_taker=care_taker)
            .order_by("date_created")
            .reverse()
        )

        return memento_list

    @staticmethod
    def search(user, query):
        return Note.objects.filter(
            Q(owner=user)
            & Q(deleted=False)
            & (Q(title__icontains=query) | Q(content__icontains=query))
        )

    def __str__(self):
        str = ""
        if self.title != "":
            str = str + "Title: " + self.title + " | "
        str = str + "Content: " + self.content
        return str


class NoteCareTaker(models.Model):
    note = models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def add(self, memento):
        memento.care_taker = self
        memento.save()


class NoteMemento(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)
    care_taker = models.ForeignKey(NoteCareTaker, on_delete=models.CASCADE)
