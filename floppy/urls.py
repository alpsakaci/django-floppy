from . import views
from django.urls import include, path
from rest_framework import routers
from floppy import views

router = routers.DefaultRouter()
router.register(r"notes", views.NoteViewSet, basename="note")

urlpatterns = [
    path("", views.index, name="floppyindex"),
    path("newnote/", views.new, name="newnote"),
    path("editnote/<int:note_id>/", views.edit, name="editnote"),
    path("movetotrash/<int:note_id>/", views.movetotrash, name="movetotrash"),
    path("deletenote/<int:note_id>/", views.delete, name="deletenote"),
    path("restore/<int:note_id>/", views.restore, name="restorenote"),
    path("browseversions/<int:note_id>/", views.browseversions, name="browseversions"),
    path("revertnote/<int:note_id>/<int:memento_id>/", views.revert, name="revertnote"),
    path("deletememento/<int:note_id>/<int:memento_id>/", views.deletememento, name="deletememento"),
    path("searchnote/", views.search, name="searchnote"),
    path("trash/", views.trash, name="trash"),
    path("api/", include(router.urls)),
]
