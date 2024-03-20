from django.shortcuts import redirect

from view import CompanyView, CompanyListView

from sign.models import AuthLogin
from template.models import (
    CompanyTemplateText, CompanyTemplateVideo, CompanyTemplateRichMessage, CompanyTemplateRichVideo, CompanyTemplateGreeting,
    CompanyTemplateCardType, CompanyTemplateCardTypeAnnounce, CompanyTemplateCardTypeLocation, CompanyTemplateCardTypePerson, CompanyTemplateCardTypeImage, CompanyTemplateCardTypeMore,
    CompanyTemplateCardTypeAnnounceText, CompanyTemplateCardTypeAnnounceAction
)

class IndexView(CompanyView):
    def get(self, request, **kwargs):
        return redirect('/company/template/text/')

class TextView(CompanyListView):
    template_name = 'company/template/text/index.html'
    title = 'テキストメッセージ管理'
    model = CompanyTemplateText
    search_target = ['name', 'company_template_text_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class TextEditView(CompanyView):
    template_name = 'company/template/text/edit.html'
    title = 'テキストメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = CompanyTemplateText.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = CompanyTemplateText.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class VideoView(CompanyListView):
    template_name = 'company/template/video/index.html'
    title = '動画メッセージ管理'
    model = CompanyTemplateVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class VideoEditView(CompanyView):
    template_name = 'company/template/video/edit.html'
    title = '動画メッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = CompanyTemplateVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = CompanyTemplateVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichMessageView(CompanyListView):
    template_name = 'company/template/richmessage/index.html'
    title = 'リッチメッセージ管理'
    model = CompanyTemplateRichMessage
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichMessageEditView(CompanyView):
    template_name = 'company/template/richmessage/edit.html'
    title = 'リッチメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = CompanyTemplateRichMessage.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = CompanyTemplateRichMessage.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichVideoView(CompanyListView):
    template_name = 'company/template/richvideo/index.html'
    title = 'リッチビデオメッセージ管理'
    model = CompanyTemplateRichVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichVideoEditView(CompanyView):
    template_name = 'company/template/richvideo/edit.html'
    title = 'リッチビデオメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = CompanyTemplateRichVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = CompanyTemplateRichVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class CardTypeView(CompanyListView):
    template_name = 'company/template/cardtype/index.html'
    title = 'カードタイプメッセージ管理'
    model = CompanyTemplateCardType
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CardTypeEditView(CompanyView):
    template_name = 'company/template/cardtype/edit.html'
    title = 'カードタイプメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = CompanyTemplateCardType.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = CompanyTemplateCardType.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class GreetingView(CompanyView):
    template_name = 'company/template/greeting/index.html'
    title = 'あいさつメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['template'] = CompanyTemplateGreeting.objects.filter(company=auth_login.company).order_by('number').all()
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
