from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    QuestionListView,
    QuestionDetailView,
    QuestionCreateView,
    QuestionUpdateView,
    QuestionDeleteView,
    AnswerCreateView,
    AnswerUpdateView,
    AnswerDeleteView,
)

urlpatterns = [
    path("", QuestionListView.as_view(), name="home"),
    path("questions/<int:pk>/", QuestionDetailView.as_view(), name="questions-detail"),
    path("questions/new/", QuestionCreateView.as_view(), name="questions-create"),
    path(
        "questions/<int:pk>/update/",
        QuestionUpdateView.as_view(),
        name="questions-update",
    ),
    path(
        "questions/<int:pk>/delete/",
        QuestionDeleteView.as_view(),
        name="questions-delete",
    ),
    path(
        "questions/<int:pk>/answers/",
        AnswerCreateView.as_view(),
        name="answers-create",
    ),
    path(
        "questions/<int:pk>/answers/<int:answer.id>/",
        AnswerUpdateView.as_view(),
        name="answers-update",
    ),
    path(
        "questions/<int:pk>/answers/<int:answer.id>/delete",
        AnswerDeleteView.as_view(),
        name="answers-delete",
    ),
    path("search/", views.search, name="search"),
]
