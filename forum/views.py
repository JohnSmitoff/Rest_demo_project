from django.shortcuts import render
from rest_framework.views import APIView
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Count
from deep_collector.core import DeepCollector

# Create your views here.


class QuestionList(APIView):
    def get(self, request):
        qusetions = Question.objects.all()

        serializer = QuestionSerializer(qusetions, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionListWithAnswers(APIView):
    def get(self, request):
        questions_with_answers = Question.objects.annotate(answer_len=Count('answers')).filter(answer_len__gt=0)

        print(questions_with_answers)
        serializer = QuestionSerializer(questions_with_answers, many=True)

        return Response(serializer.data)


class QuestionDetails(APIView):
    def get_object(self, pk):
        try:
            question = Question.objects.get(pk=pk)
            return question
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, question_id):
        question = self.get_object(pk=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, question_id):
        question = self.get_object(pk=question_id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = self.get_object(pk=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerDetail(APIView):
    def get_object(self, pk):
        try:
            answer = Answer.objects.get(pk=pk)
            return answer
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, question_id, answer_id):
        full_request_url = request.build_absolute_uri()
        try:
            question = Question.objects.get(pk=question_id)

            if "dislike" in full_request_url:
                answer = self.get_object(pk=answer_id)
                answer.dislikes += 1
                answer.save()
                serializer = AnswerSerializer(answer)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            elif "like" in full_request_url:
                answer = self.get_object(pk=answer_id)
                answer.likes += 1
                answer.save()
                serializer = AnswerSerializer(answer)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                answer = self.get_object(pk=answer_id)
                serializer = AnswerSerializer(answer)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Question.DoesNotExist:

            return Response("No such a question", status=status.HTTP_404_NOT_FOUND)
