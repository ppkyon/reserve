from view import HeadView, HeadListView

from question.models import HeadQuestion, HeadQuestionItem, HeadQuestionItemChoice

import random

class IndexView(HeadListView):
    template_name = 'head/question/index.html'
    title = '回答フォーム管理'
    model = HeadQuestion
    search_target = ['title', 'name', 'description']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(HeadView):
    template_name = 'head/question/edit.html'
    title = '回答フォーム管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['random'] = random.randint(10000000,99999999)

        context['question'] = HeadQuestion.objects.filter(display_id=self.request.GET.get("id")).first()
        if context['question']:
            context['question'].item = get_question_item_data(context['question'])
        else:
            context['question'] = HeadQuestion.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['question']:
                context['question'].item = get_question_item_data(context['question'])
                context['question'].display_id = ''
                context['question'].name = context['question'].name + ' コピー'
        return context



def get_question_item_data(question):
    question_item_list = HeadQuestionItem.objects.filter(question=question).order_by('number').all()
    for question_index, question_item in enumerate(question_item_list):
        question_item_list[question_index].random = random.randint(10000000,99999999)
        question_item_list[question_index].choice = HeadQuestionItemChoice.objects.filter(question_item=question_item).order_by('number').all()
        for question_choice_index, question_choice_item in enumerate(question_item_list[question_index].choice):
            question_item_list[question_index].choice[question_choice_index].random = random.randint(10000000,99999999)
    return question_item_list