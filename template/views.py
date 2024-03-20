from django.shortcuts import redirect

from view import ShopView, ShopListView

from sign.models import AuthLogin
from template.models import (
    ShopTemplateText, ShopTemplateVideo, ShopTemplateRichMessage, ShopTemplateRichVideo, ShopTemplateGreeting,
    ShopTemplateCardType, ShopTemplateCardTypeAnnounce, ShopTemplateCardTypeLocation, ShopTemplateCardTypePerson, ShopTemplateCardTypeImage, ShopTemplateCardTypeMore,
    ShopTemplateCardTypeAnnounceText, ShopTemplateCardTypeAnnounceAction
)

class IndexView(ShopView):
    def get(self, request, **kwargs):
        return redirect('/template/text/')

class TextView(ShopListView):
    template_name = 'template/text/index.html'
    title = 'テキストメッセージ管理'
    model = ShopTemplateText
    search_target = ['name', 'shop_template_text_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class TextEditView(ShopView):
    template_name = 'template/text/edit.html'
    title = 'テキストメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = ShopTemplateText.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = ShopTemplateText.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class VideoView(ShopListView):
    template_name = 'template/video/index.html'
    title = '動画メッセージ管理'
    model = ShopTemplateVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class VideoEditView(ShopView):
    template_name = 'template/video/edit.html'
    title = '動画メッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = ShopTemplateVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = ShopTemplateVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichMessageView(ShopListView):
    template_name = 'template/richmessage/index.html'
    title = 'リッチメッセージ管理'
    model = ShopTemplateRichMessage
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichMessageEditView(ShopView):
    template_name = 'template/richmessage/edit.html'
    title = 'リッチメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = ShopTemplateRichMessage.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = ShopTemplateRichMessage.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class RichVideoView(ShopListView):
    template_name = 'template/richvideo/index.html'
    title = 'リッチビデオメッセージ管理'
    model = ShopTemplateRichVideo
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class RichVideoEditView(ShopView):
    template_name = 'template/richvideo/edit.html'
    title = 'リッチビデオメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = ShopTemplateRichVideo.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = ShopTemplateRichVideo.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'
        return context

class CardTypeView(ShopListView):
    template_name = 'template/cardtype/index.html'
    title = 'カードタイプメッセージ管理'
    model = ShopTemplateCardType
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CardTypeEditView(ShopView):
    template_name = 'template/cardtype/edit.html'
    title = 'カードタイプメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['template'] = ShopTemplateCardType.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['template']:
            context['template'] = ShopTemplateCardType.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['template']:
                context['template'].display_id = ''
                context['template'].name = context['template'].name + ' コピー'

        return context

class GreetingView(ShopView):
    template_name = 'template/greeting/index.html'
    title = 'あいさつメッセージ管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['template'] = ShopTemplateGreeting.objects.filter(company=auth_login.shop.company, shop=auth_login.shop).order_by('number').all()
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
