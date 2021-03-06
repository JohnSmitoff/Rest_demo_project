from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path("^questions/$", views.QuestionList.as_view(), name="questions"),
    re_path(
        "^questions/(?P<question_id>\d+)/$",
        views.QuestionDetails.as_view(),
        name="question-details",
    ),
    re_path(
        "^questions/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/$",
        views.AnswerDetail.as_view(),
        name="answer-detail",
    ),
    re_path(
        "^only_questions_with_answers/$", views.QuestionListWithAnswers.as_view(), name="questions_with_answers"
    ),
]
