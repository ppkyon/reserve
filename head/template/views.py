from django.shortcuts import redirect

from view import HeadView, HeadListView

from template.models import (
    HeadTemplateText, HeadTemplateVideo, HeadTemplateRichMessage, HeadTemplateRichVideo, HeadTemplateGreeting,
    HeadTemplateCardType, HeadTemplateCardTypeAnnounce, HeadTemplateCardTypeLocation, HeadTemplateCardTypePerson, HeadTemplateCardTypeImage, HeadTemplateCardTypeMore,
    HeadTemplateCardTypeAnnounceText, HeadTemplateCardTypeAnnounceAction
)

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
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class VideoView(HeadListView):
    template_name = 'head/template/video/index.html'
    title = '動画メッセージ管理'
    model = HeadTemplateVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class VideoEditView(HeadView):
    template_name = 'head/template/video/edit.html'
    title = '動画メッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = HeadTemplateVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichMessageView(HeadListView):
    template_name = 'head/template/richmessage/index.html'
    title = 'リッチメッセージ管理'
    model = HeadTemplateRichMessage
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichMessageEditView(HeadView):
    template_name = 'head/template/richmessage/edit.html'
    title = 'リッチメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateRichMessage.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = HeadTemplateRichMessage.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichVideoView(HeadListView):
    template_name = 'head/template/richvideo/index.html'
    title = 'リッチビデオメッセージ管理'
    model = HeadTemplateRichVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichVideoEditView(HeadView):
    template_name = 'head/template/richvideo/edit.html'
    title = 'リッチビデオメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateRichVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = HeadTemplateRichVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class CardTypeView(HeadListView):
    template_name = 'head/template/cardtype/index.html'
    title = 'カードタイプメッセージ管理'
    model = HeadTemplateCardType
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CardTypeEditView(HeadView):
    template_name = 'head/template/cardtype/edit.html'
    title = 'カードタイプメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = HeadTemplateCardType.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = HeadTemplateCardType.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
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



def get_template_action_style(action):
    style = 'style=width:90%;'
    if action.button_type == 0:
        style += 'color:#fff;'
        if action.button_color == 0:
            style += 'background-color:#666f86;'
        elif action.button_color == 1:
            style += 'background-color:#fff;'
        elif action.button_color == 2:
            style += 'background-color:#eb4e3d;'
        elif action.button_color == 3:
            style += 'background-color:#ed8537;'
        elif action.button_color == 4:
            style += 'background-color:#00B900;'
        elif action.button_color == 5:
            style += 'background-color:#5b82db;'
        else:
            style += 'background-color:#fff;'
    elif action.button_type == 1:
        if action.button_color == 0:
            style += 'color:#666f86;'
        elif action.button_color == 1:
            style += 'color:#fff;'
        elif action.button_color == 2:
            style += 'color:#eb4e3d;'
        elif action.button_color == 3:
            style += 'color:#ed8537;'
        elif action.button_color == 4:
            style += 'color:#00B900;'
        elif action.button_color == 5:
            style += 'color:#5b82db;'
        else:
            style += 'color:#5b82db;'
        style += 'background-color:#fff;'
    return style