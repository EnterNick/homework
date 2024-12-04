from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, TemplateView
import json
from django.http.response import HttpResponseNotFound, HttpResponse

from scr.apps.forms.forms import VoteForm

polls = [
    {
        'id': 1,
        'question': 'Какой ваш любимый цвет?',
        'choices': ['Красный', 'Зеленый', 'Синий']
    },
    {
        'id': 2,
        'question': 'Какое ваше любимое животное?',
        'choices': ['Кот', 'Собака', 'Птица']
    }
]


def index(request):
    return render(request, 'forms/forms.html', {'polls': polls})


class OneFormsView(FormView):
    template_name = 'forms/index.html'
    form_class = VoteForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        try:
            return {**kwargs, 'data': next(filter(lambda x: x['id'] == self.kwargs['pk'], polls))}
        except StopIteration:
            return kwargs

    def post(self, request, pk=None, **kwargs):
        votes = json.loads(request.COOKIES.get('votes', '{}'))
        votes[str(pk)] = votes.get(str(pk), {})
        votes[str(pk)][request.POST.get('choice')] = votes[str(pk)].get(request.POST.get('choice'), 0) + 1
        response = redirect('results', pk=pk)
        response.set_cookie('votes', json.dumps(votes), max_age=3600 * 24 * 30)
        return response


class ResultsView(View):
    def get(self, request, pk):
        n = request.COOKIES.get('votes')
        print(n)
        return HttpResponse(json.dumps(json.loads(n), ensure_ascii=False))
