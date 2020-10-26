from . import views
from django.urls import include, path
from rest_framework import routers
from floppy import views

router = routers.DefaultRouter()
router.register(r'notes', views.NoteViewSet, basename='note')

urlpatterns = [
    path('', views.index, name='floppyindex'),
    path('newnote/', views.new, name='newnote'),
    path('editnote/<int:note_id>/', views.edit, name='editnote'),
    path('deletenote/<int:note_id>/', views.delete, name='deletenote'),
    path('searchnote/', views.search, name='searchnote'),
    path('api/', include(router.urls)),
]
