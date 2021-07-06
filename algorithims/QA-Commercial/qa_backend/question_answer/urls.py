import qa_backend.question_answer.views as question_answer_views
from django.urls import path, include

urlpatterns = [
    path("ping", question_answer_views.ping),
    path("search", question_answer_views.search_request),
]
