from django.urls import path

from .views import *

urlpatterns = [
    path('', main),
    path('notes/<int:note_id>/delete', delete_note),
    path('notes/<int:note_id>/archive', archive_note),
    path('notes/<int:note_id>/publish', publish_note),
    path('notes/<int:note_id>/edit', edit_note),
    path('notes/<int:note_id>', note_detail),
    path('notes/archive', archive_notes),
    path('test', TestPage.as_view()),
    path('stat', stat),
    path('bootstrap', bootstrap),
]

