from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Questions, Answers
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.db.models import Q


def search(request):
    query = request.GET.get("q", "")
    if query:
        queryset = Q(title__icontains=query) | Q(content__icontains=query)
        results = Questions.objects.filter(queryset).distinct()
    else:
        results = []
    return render(request, "qa_app/search.html", {"results": results, "query": query})


class QuestionListView(ListView):
    model = Questions
    template_name = "qa_app/home.html"
    questions = Questions.objects.all()
    context_object_name = "questions"
    ordering = ["-created_date"]

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context.update(
            {"answers_list": Answers.objects.all(), "users_list": User.objects.all(),}
        )
        return context


class QuestionDetailView(DetailView):
    model = Questions

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        self.object.qst_views = F("qst_views") + 1
        self.object.save()

        question_id = self.kwargs["pk"]
        context["question"] = self.object
        context["answer_list"] = self.object.answers_set.all()
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Questions

    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.asker = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Questions

    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.asker = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.asker:
            return True
        return False


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Questions
    success_url = "/"

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.asker:
            return True
        return False


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answers

    fields = ["answer_text"]
    # template_name = "qa_app/questions_detail.html"

    def form_valid(self, form):
        form.instance.question_id = self.kwargs["pk"]
        form.instance.replier = self.request.user
        return super().form_valid(form)

    def get_success_url(self):

        return reverse("questions-detail", kwargs={"pk": self.object.question_id})


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answers

    fields = ["answer_text"]

    def form_valid(self, form):
        form.instance.replier = self.request.user
        return super().form_valid(form)

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.replier:
            return True
        return False

    def get_success_url(self):
        return reverse("questions-detail", kwargs={"pk": self.object.question.id})


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answers

    def get_success_url(self):
        return reverse("questions-detail", kwargs={"pk": self.object.question.id})

    def test_func(self):
        answer = self.get_object()
        if self.request.user == answer.replier:
            return True
        return False
