from datetime import datetime

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)

from .models import Note
from .serializers import NoteSerializer
from .forms import NoteForm, SearchForm


class NoteViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    )

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request):
        queryset = Note.objects.filter(owner=request.user)
        serializer = NoteSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Note.objects.filter(owner=request.user)
        note = get_object_or_404(queryset, pk=pk)
        serializer = NoteSerializer(note)

        return Response(serializer.data)


@login_required(login_url="/admin/login")
def index(request):
    notes = Note.get_user_notes(request.user)
    form = SearchForm()
    context = {"notes": notes, "search_form": form}

    return render(request, "floppy/index.html", context)


@login_required(login_url="/admin/login")
def new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            Note.create(owner=request.user, title=title, content=content)

            return redirect(index)
    else:
        form = NoteForm()
        context = {"form": form}

    return render(request, "floppy/new.html", context)


@login_required(login_url="/admin/login")
def edit(request, note_id):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = get_object_or_404(
                Note.objects.filter(id=note_id, owner=request.user)
            )
            note.edit(form.cleaned_data["title"], form.cleaned_data["content"])

            return redirect(index)
    else:
        note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
        form = NoteForm(initial={"title": note.title, "content": note.content})
        context = {"form": form, "note": note}

    return render(request, "floppy/edit.html", context)


@login_required(login_url="/admin/login")
def movetotrash(request, note_id):
    note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
    note.move_to_trash()

    return redirect(index)


@login_required(login_url="/admin/login")
def delete(request, note_id):
    note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
    note.delete()

    return redirect(index)


@login_required(login_url="/admin/login")
def restore(request, note_id):
    note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
    note.restore()

    return redirect(index)


@login_required(login_url="/admin/login")
def browseversions(request, note_id):
    note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
    older_versions = Note.get_older_versions(request.user, note_id)
    context = {"note": note, "older_versions": older_versions}

    return render(request, "floppy/versions.html", context)


@login_required(login_url="/admin/login")
def revert(request, note_id, memento_id):
    note = get_object_or_404(Note.objects.filter(id=note_id, owner=request.user))
    note.revert(memento_id)

    return redirect(index)


@login_required(login_url="/admin/login")
def search(request):
    form = SearchForm(request.POST)
    search_result = []
    if request.method == "POST":
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_result = Note.search(request.user, query)
            context = {
                "notes": search_result,
                "search_form": form,
                "search_result": len(search_result),
            }
            return render(request, "floppy/index.html", context)

    return redirect(index)


@login_required(login_url="/admin/login")
def trash(request):
    deleted_notes = Note.get_deleted_notes(request.user)
    form = SearchForm()
    context = {"notes": deleted_notes}

    return render(request, "floppy/index.html", context)
