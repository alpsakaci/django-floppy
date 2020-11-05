from datetime import datetime

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from .models import Note, NoteLog
from .serializers import NoteSerializer
from .forms import NoteForm, SearchForm

class NoteViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def list(self, request):
        queryset = Note.objects.filter(owner = request.user)
        serializer = NoteSerializer(queryset, many = True)

        return Response(serializer.data)

    def retrieve(self, request, pk = None):
        queryset = Note.objects.filter(owner = request.user)
        note = get_object_or_404(queryset, pk = pk)
        serializer = NoteSerializer(note)

        return Response(serializer.data)

@login_required(login_url='/admin/login')
def index(request):
    notes = Note.objects.filter(owner = request.user).order_by('date_modified').reverse()
    form = SearchForm()
    context = {'notes': notes, 'search_form': form}

    return render(request, 'floppy/index.html', context)

@login_required(login_url='/admin/login')
def new(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            new_note = Note(owner=request.user, title=title, content=content)
            new_note.save()

            return redirect(index)
    else:
        form = NoteForm()
        context = {'form': form}

    return render(request, 'floppy/new.html', context)

@login_required(login_url='/admin/login')
def edit(request, note_id):
    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note = get_object_or_404(Note.objects.filter(id=note_id))
            notelog = NoteLog()
            notelog.init_log(note, 1)

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            note.title = title
            note.content = content
            note.date_modified = datetime.now()
            
            note.save()
            notelog.set_log(note)
            notelog.save()

            return redirect(index)
    else:
        note = get_object_or_404(Note.objects.filter(id=note_id))
        form = NoteForm(initial={'title':note.title, 'content':note.content})
        context = {'form': form, 'note':note}

    return render(request, 'floppy/edit.html', context)

@login_required(login_url='/admin/login')
def delete(request, note_id):
    note = get_object_or_404(Note.objects.filter(id=note_id))
    notelog = NoteLog()
    notelog.init_log(note, 2)
    notelog.save()
    note.delete()

    return redirect(index)

@login_required(login_url='/admin/login')
def search(request):
    form = SearchForm(request.POST)
    search_result = []
    if request.method == 'POST':
        if form.is_valid():
            query = form.cleaned_data['query']
            search_result = Note.objects.filter(Q(owner=request.user) & (Q(title__icontains=query) | Q(content__icontains=query)))
            context = {'notes': search_result, 'search_form': form, 'search_result': len(search_result)}
            return render(request, 'floppy/index.html', context)

    return redirect(index)
