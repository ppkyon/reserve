from django.shortcuts import redirect

from view import HeadView, HeadListView

from template.models import HeadTemplateText, HeadTemplateGreeting

class IndexView(HeadView):
    def get(self, request, **kwargs):
        return redirect('/head/template/text/')

class TextView(HeadListView):
    template_name = 'head/template/text/index.html'
    title = 'テキストメッセージ管理'
    model = HeadTemplateText
    search_target = ['name', 'head_template_text_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class TextEditView(HeadView):
    template_name = 'head/template/text/edit.html'
    title = 'テキストメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateText.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = HeadTemplateText.objects.filter(display_id=self.request.GET.get("copy")).first()
            context['template'].display_id = ''
            context['template'].name = context['template'].name + ' コピー'
        return context

class VideoView(HeadView):
    template_name = 'head/template/video/index.html'
    title = '動画メッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class VideoEditView(HeadView):
    template_name = 'head/template/video/edit.html'
    title = '動画メッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichMessageView(HeadView):
    template_name = 'head/template/richmessage/index.html'
    title = 'リッチメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichMessageEditView(HeadView):
    template_name = 'head/template/richmessage/edit.html'
    title = 'リッチメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichVideoView(HeadView):
    template_name = 'head/template/richvideo/index.html'
    title = 'リッチビデオメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichVideoEditView(HeadView):
    template_name = 'head/template/richvideo/edit.html'
    title = 'リッチビデオメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CardTypeView(HeadView):
    template_name = 'head/template/cardtype/index.html'
    title = 'カードタイプメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CardTypeEditView(HeadView):
    template_name = 'head/template/cardtype/edit.html'
    title = 'カードタイプメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class GreetingView(HeadView):
    template_name = 'head/template/greeting/index.html'
    title = 'あいさつメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateGreeting.objects.order_by('number').all()
        for template_index, template_item in enumerate(context['template']):
            if template_item.text:
                context['template'][template_index].text = template_item.text.replace( '\r', '<br>' ).replace( '\n', '' ).replace( '<br><br>', '<br><div>&nbsp;</div>' )
            
        return context