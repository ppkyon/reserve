from django.http import JsonResponse

from flow.models import (
    CompanyFlow, CompanyFlowTab, CompanyFlowItem, CompanyFlowTemplate, CompanyFlowRichMenu,
    CompanyFlowAction, CompanyFlowActionReminder, CompanyFlowActionMessage, CompanyFlowStep,
    CompanyFlowTimer, CompanyFlowSchedule, CompanyFlowResult,
    ShopFlow, ShopFlowTab, ShopFlowItem, ShopFlowTemplate, ShopFlowRichMenu,
    ShopFlowAction, ShopFlowActionReminder, ShopFlowActionMessage, ShopFlowStep,
    ShopFlowTimer, ShopFlowSchedule, ShopFlowResult,
)
from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice
from richmenu.models import ShopRichMenu, ShopRichMenuItem
from sign.models import AuthLogin
from template.models import (
    ShopTemplateText, ShopTemplateTextItem, ShopTemplateVideo, CompanyTemplateGreeting, ShopTemplateGreeting,
    ShopTemplateCardType, ShopTemplateCardTypeAnnounce, ShopTemplateCardTypeAnnounceAction, ShopTemplateCardTypeAnnounceText,
    ShopTemplateCardTypeLocation, ShopTemplateCardTypePerson, ShopTemplateCardTypeImage, ShopTemplateCardTypeMore,
)

from flow.action.list import get_list

from common import create_code
from table.action import action_search

import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    favorite_flg = False
    if request.POST.get('favorite') == '1':
        favorite_flg = True
    
    period_from = None
    if request.POST.get('period_from'):
        period_from = request.POST.get('period_from').replace( '/', '-')
    period_to = None
    if request.POST.get('period_to'):
        period_to = request.POST.get('period_to').replace( '/', '-')
    
    if request.POST.get('id'):
        flow = ShopFlow.objects.filter(display_id=request.POST.get('id')).first()
        flow.name = request.POST.get('name')
        flow.period_from = period_from
        flow.period_to = period_to
        flow.favorite_flg = favorite_flg
        flow.author = request.user.id
        flow.save()
    else:
        company_flow = CompanyFlow.objects.filter(display_id=request.POST.get('flow')).first()
        flow = ShopFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ShopFlow),
            parent = company_flow,
            company = auth_login.shop.company,
            shop = auth_login.shop,
            name = request.POST.get('name'),
            description = company_flow.description,
            period_from = period_from,
            period_to = period_to,
            favorite_flg = favorite_flg,
            author = request.user.id
        )

        for company_flow_tab in CompanyFlowTab.objects.filter(flow=company_flow).all():
            ShopFlowTab.objects.create(
                id = str(uuid.uuid4()),
                flow = flow,
                number = company_flow_tab.number,
                name = company_flow_tab.name,
                value = company_flow_tab.value,
                member = company_flow_tab.member,
            )

        for company_flow_tab in CompanyFlowTab.objects.filter(flow=company_flow).all():
            flow_tab = ShopFlowTab.objects.filter(flow=flow, number=company_flow_tab.number).first()
            for company_flow_item in CompanyFlowItem.objects.filter(flow_tab=company_flow_tab).all():
                flow_item = ShopFlowItem.objects.create(
                    id = str(uuid.uuid4()),
                    flow_tab = flow_tab,
                    x = company_flow_item.x,
                    y = company_flow_item.y,
                    number = company_flow_item.number,
                    type = company_flow_item.type,
                    name = company_flow_item.name,
                    analytics = company_flow_item.analytics,
                )

                if flow_item.type == 1:
                    if not ShopTemplateGreeting.objects.filter(company=auth_login.shop.company, shop=auth_login.shop).exists():
                        for company_template_greeting in CompanyTemplateGreeting.objects.filter(company=auth_login.shop.company).all():
                            ShopTemplateGreeting.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ShopTemplateGreeting),
                                company = auth_login.shop.company,
                                shop = auth_login.shop,
                                number = company_template_greeting.number,
                                message_type = company_template_greeting.message_type,
                                text = company_template_greeting.text,
                                image = company_template_greeting.image,
                                image_width = company_template_greeting.image_width,
                                image_height = company_template_greeting.image_height,
                                video = company_template_greeting.video,
                                video_width = company_template_greeting.video_width,
                                video_height = company_template_greeting.video_height,
                                video_thumbnail = company_template_greeting.video_thumbnail,
                                template_text = company_template_greeting.template_text,
                                template_video = company_template_greeting.template_video,
                                template_richmessage = company_template_greeting.template_richmessage,
                                template_richvideo = company_template_greeting.template_richvideo,
                                template_cardtype = company_template_greeting.template_cardtype,
                                author = company_template_greeting.author,
                            )
                elif flow_item.type == 2:
                    print()
                elif flow_item.type == 3:
                    print()
                elif flow_item.type == 4:
                    print()
                elif flow_item.type == 5:
                    print()
                elif flow_item.type == 6:
                    company_flow_template = CompanyFlowTemplate.objects.filter(flow=company_flow_item).first()
                    if ShopTemplateCardType.objects.filter(parent=company_flow_template.template_cardtype, shop=auth_login.shop).exists():
                        template = ShopTemplateCardType.objects.filter(parent=company_flow_template.template_cardtype, shop=auth_login.shop).first()
                    else:
                        template = ShopTemplateCardType.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, ShopTemplateCardType),
                            parent = company_flow_template.template_cardtype,
                            company = auth_login.shop.company,
                            shop = auth_login.shop,
                            name = company_flow_template.template_cardtype.name,
                            title = company_flow_template.template_cardtype.title,
                            type = company_flow_template.template_cardtype.type,
                            count = company_flow_template.template_cardtype.count,
                        )
                        if company_flow_template.template_cardtype.type == 1:
                            for company_template_card_type_announce in company_flow_template.template_cardtype.company_template_card_type_announce.all():
                                card_type = ShopTemplateCardTypeAnnounce.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = company_template_card_type_announce.number,
                                    title = company_template_card_type_announce.title,
                                    image_count = company_template_card_type_announce.image_count,
                                    image_1 = company_template_card_type_announce.image_1,
                                    image_2 = company_template_card_type_announce.image_2,
                                    image_3 = company_template_card_type_announce.image_3,
                                    image_flg = company_template_card_type_announce.image_flg,
                                    label = company_template_card_type_announce.label,
                                    label_color = company_template_card_type_announce.label_color,
                                    label_flg = company_template_card_type_announce.label_flg,
                                    description = company_template_card_type_announce.description,
                                    description_flg = company_template_card_type_announce.description_flg,
                                )
                                for company_template_card_type_announce_text in company_template_card_type_announce.company_template_card_type_announce_text.all():
                                    ShopTemplateCardTypeAnnounceText.objects.create(
                                        id = str(uuid.uuid4()),
                                        card_type = card_type,
                                        number = company_template_card_type_announce_text.number,
                                        title = company_template_card_type_announce_text.title,
                                        text = company_template_card_type_announce_text.text,
                                        flg = company_template_card_type_announce_text.flg,
                                    )
                                for company_template_card_type_announce_action in company_template_card_type_announce.company_template_card_type_announce_action.all():
                                    video = create_video(company_template_card_type_announce_action.video, auth_login)
                                    question = create_question(company_template_card_type_announce_action.question, auth_login)
                                    ShopTemplateCardTypeAnnounceAction.objects.create(
                                        id = str(uuid.uuid4()),
                                        card_type = card_type,
                                        number = company_template_card_type_announce_action.number,
                                        label = company_template_card_type_announce_action.label,
                                        type = company_template_card_type_announce_action.type,
                                        url = company_template_card_type_announce_action.url,
                                        video = video,
                                        question = question,
                                        text = company_template_card_type_announce_action.text,
                                        button_type = company_template_card_type_announce_action.button_type,
                                        button_color = company_template_card_type_announce_action.button_color,
                                        button_background_color = company_template_card_type_announce_action.button_background_color,
                                        flg = company_template_card_type_announce_action.flg,
                                    )
                        elif company_flow_template.template_cardtype.type == 2:
                            for company_template_card_type_location in company_flow_template.template_cardtype.company_template_card_type_location.all():
                                action_video_1 = create_video(company_template_card_type_location.action_video_1, auth_login)
                                action_question_1 = create_question(company_template_card_type_location.action_question_1, auth_login)
                                action_video_2 = create_video(company_template_card_type_location.action_video_2, auth_login)
                                action_question_2 = create_question(company_template_card_type_location.action_question_2, auth_login)
                                ShopTemplateCardTypeLocation.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = company_template_card_type_location.number,
                                    title = company_template_card_type_location.title,
                                    image_count = company_template_card_type_location.image_count,
                                    image_1 = company_template_card_type_location.image_1,
                                    image_2 = company_template_card_type_location.image_2,
                                    image_3 = company_template_card_type_location.image_3,
                                    label = company_template_card_type_location.label,
                                    label_color = company_template_card_type_location.label_color,
                                    label_flg = company_template_card_type_location.label_flg,
                                    place = company_template_card_type_location.place,
                                    place_flg = company_template_card_type_location.place_flg,
                                    plus = company_template_card_type_location.plus,
                                    plus_type = company_template_card_type_location.plus_type,
                                    plus_flg = company_template_card_type_location.plus_flg,
                                    action_label_1 = company_template_card_type_location.action_label_1,
                                    action_type_1 = company_template_card_type_location.action_type_1,
                                    action_url_1 = company_template_card_type_location.action_url_1,
                                    action_video_1 = action_video_1,
                                    action_question_1 = action_question_1,
                                    action_text_1 = company_template_card_type_location.action_text_1,
                                    action_flg_1 = company_template_card_type_location.action_flg_1,
                                    action_label_2 = company_template_card_type_location.action_label_2,
                                    action_type_2 = company_template_card_type_location.action_type_2,
                                    action_url_2 = company_template_card_type_location.action_url_2,
                                    action_video_2 = action_video_2,
                                    action_question_2 = action_question_2,
                                    action_text_2 = company_template_card_type_location.action_text_2,
                                    action_flg_2 = company_template_card_type_location.action_flg_2,
                                )
                        elif company_flow_template.template_cardtype.type == 3:
                            for company_template_card_type_person in company_flow_template.template_cardtype.company_template_card_type_person.all():
                                action_video_1 = create_video(company_template_card_type_person.action_video_1, auth_login)
                                action_question_1 = create_question(company_template_card_type_person.action_question_1, auth_login)
                                action_video_2 = create_video(company_template_card_type_person.action_video_2, auth_login)
                                action_question_2 = create_question(company_template_card_type_person.action_question_2, auth_login)
                                ShopTemplateCardTypePerson.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = company_template_card_type_person.number,
                                    image = company_template_card_type_person.image,
                                    name = company_template_card_type_person.name,
                                    tag_1 = company_template_card_type_person.tag_1,
                                    tag_color_1 = company_template_card_type_person.tag_color_1,
                                    tag_flg_1 = company_template_card_type_person.tag_flg_1,
                                    tag_2 = company_template_card_type_person.tag_2,
                                    tag_color_2 = company_template_card_type_person.tag_color_2,
                                    tag_flg_2 = company_template_card_type_person.tag_flg_2,
                                    tag_3 = company_template_card_type_person.tag_3,
                                    tag_color_3 = company_template_card_type_person.tag_color_3,
                                    tag_flg_3 = company_template_card_type_person.tag_flg_3,
                                    description = company_template_card_type_person.description,
                                    description_flg = company_template_card_type_person.description_flg,
                                    action_label_1 = company_template_card_type_person.action_label_1,
                                    action_type_1 = company_template_card_type_person.action_type_1,
                                    action_url_1 = company_template_card_type_person.action_url_1,
                                    action_video_1 = action_video_1,
                                    action_question_1 = action_question_1,
                                    action_text_1 = company_template_card_type_person.action_text_1,
                                    action_flg_1 = company_template_card_type_person.action_flg_1,
                                    action_label_2 = company_template_card_type_person.action_label_2,
                                    action_type_2 = company_template_card_type_person.action_type_2,
                                    action_url_2 = company_template_card_type_person.action_url_2,
                                    action_video_2 = action_video_2,
                                    action_question_2 = action_question_2,
                                    action_text_2 = company_template_card_type_person.action_text_2,
                                    action_flg_2 = company_template_card_type_person.action_flg_2,
                                )
                        elif company_flow_template.template_cardtype.type == 4:
                            for company_template_card_type_image in company_flow_template.template_cardtype.company_template_card_type_image.all():
                                action_video = create_video(company_template_card_type_image.action_video, auth_login)
                                action_question = create_question(company_template_card_type_image.action_question, auth_login)
                                ShopTemplateCardTypeImage.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = company_template_card_type_image.number,
                                    image = company_template_card_type_image.image,
                                    label = company_template_card_type_image.label,
                                    label_color = company_template_card_type_image.label_color,
                                    label_flg = company_template_card_type_image.label_flg,
                                    action_label = company_template_card_type_image.action_label,
                                    action_type = company_template_card_type_image.action_type,
                                    action_url = company_template_card_type_image.action_url,
                                    action_video = action_video,
                                    action_question = action_question,
                                    action_text = company_template_card_type_image.action_text,
                                    action_flg = company_template_card_type_image.action_flg,
                                )
                        for company_template_card_type_more in company_flow_template.template_cardtype.company_template_card_type_more.all():
                            action_video = create_video(company_template_card_type_more.action_video, auth_login)
                            action_question = create_question(company_template_card_type_more.action_question, auth_login)
                            ShopTemplateCardTypeMore.objects.create(
                                id = str(uuid.uuid4()),
                                template = template,
                                type = company_template_card_type_more.type,
                                image = company_template_card_type_more.image,
                                action_label = company_template_card_type_more.action_label,
                                action_type = company_template_card_type_more.action_type,
                                action_url = company_template_card_type_more.action_url,
                                action_video = action_video,
                                action_question = action_question,
                                action_text = company_template_card_type_more.action_text,
                            )
                    ShopFlowTemplate.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_cardtype = template,
                    )
                elif flow_item.type == 7:
                    company_flow_rich_menu = CompanyFlowRichMenu.objects.filter(flow=company_flow_item).first()
                    if ShopRichMenu.objects.filter(parent=company_flow_rich_menu.rich_menu, shop=auth_login.shop).exists():
                        rich_menu = ShopRichMenu.objects.filter(parent=company_flow_rich_menu.rich_menu, shop=auth_login.shop).first()
                    else:
                        if company_flow_rich_menu.rich_menu:
                            rich_menu = ShopRichMenu.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ShopRichMenu),
                                parent = company_flow_rich_menu.rich_menu,
                                company = auth_login.shop.company,
                                shop = auth_login.shop,
                                name = company_flow_rich_menu.rich_menu.name,
                                menu_type = company_flow_rich_menu.rich_menu.menu_type,
                                menu_flg = company_flow_rich_menu.rich_menu.menu_flg,
                                menu_text = company_flow_rich_menu.rich_menu.menu_text,
                                type = company_flow_rich_menu.rich_menu.type,
                                image = company_flow_rich_menu.rich_menu.image,
                                image_width = company_flow_rich_menu.rich_menu.image_width,
                                image_height = company_flow_rich_menu.rich_menu.image_height,
                            )
                            for company_rich_menu_item in company_flow_rich_menu.rich_menu.company_rich_menu_item.all():
                                video = create_video(company_rich_menu_item.video, auth_login)
                                question = create_question(company_rich_menu_item.question, auth_login)
                                ShopRichMenuItem.objects.create(
                                    id = str(uuid.uuid4()),
                                    rich_menu = rich_menu,
                                    number = company_rich_menu_item.number,
                                    type = company_rich_menu_item.type,
                                    url = company_rich_menu_item.url,
                                    video = video,
                                    question = question,
                                    label = company_rich_menu_item.label,
                                    text = company_rich_menu_item.text,
                                )
                        else:
                            rich_menu = None
                    ShopFlowRichMenu.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        rich_menu = rich_menu,
                    )
                elif flow_item.type == 8:
                    company_flow_action = CompanyFlowAction.objects.filter(flow=company_flow_item).first()
                    ShopFlowAction.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        action = ShopFlowTab.objects.filter(flow=flow, number=company_flow_action.action.number).first(),
                    )
                    company_flow_action_reminder = CompanyFlowActionReminder.objects.filter(flow=company_flow_item).first()
                    template_text = None
                    if company_flow_action_reminder.template_text:
                        if ShopTemplateText.objects.filter(parent=company_flow_action_reminder.template_text, shop=auth_login.shop).exists():
                            template_text = ShopTemplateText.objects.filter(parent=company_flow_action_reminder.template_text, shop=auth_login.shop).first()
                        else:
                            template_text = ShopTemplateText.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ShopTemplateText),
                                parent = company_flow_action_reminder.template_text,
                                company = auth_login.shop.company,
                                shop = auth_login.shop,
                                name = company_flow_action_reminder.template_text.name,
                            )
                            for company_template_text_item in company_flow_action_reminder.template_text.company_template_text_item.all():
                                ShopTemplateTextItem.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template_text,
                                    number = company_template_text_item.number,
                                    message_type = company_template_text_item.message_type,
                                    text = company_template_text_item.text,
                                    image = company_template_text_item.image,
                                    image_width = company_template_text_item.image_width,
                                    image_height = company_template_text_item.image_height,
                                    video = company_template_text_item.video,
                                    video_width = company_template_text_item.video_width,
                                    video_height = company_template_text_item.video_height,
                                    video_thumbnail = company_template_text_item.video_thumbnail,
                                    template_text = company_template_text_item.template_text,
                                    template_video = company_template_text_item.template_video,
                                    template_richmessage = company_template_text_item.template_richmessage,
                                    template_richvideo = company_template_text_item.template_richvideo,
                                    template_cardtype = company_template_text_item.template_cardtype,
                                )
                    template_video = None
                    template_richmessage = None
                    template_richvideo = None
                    template_cardtype = None
                    ShopFlowActionReminder.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_text = template_text,
                        template_video = template_video,
                        template_richmessage = template_richmessage,
                        template_richvideo = template_richvideo,
                        template_cardtype = template_cardtype,
                        date = company_flow_action_reminder.date,
                        time = company_flow_action_reminder.time,
                    )
                    company_flow_action_message = CompanyFlowActionMessage.objects.filter(flow=company_flow_item).first()
                    template_text = None
                    if company_flow_action_message.template_text:
                        if ShopTemplateText.objects.filter(parent=company_flow_action_message.template_text, shop=auth_login.shop).exists():
                            template_text = ShopTemplateText.objects.filter(parent=company_flow_action_message.template_text, shop=auth_login.shop).first()
                        else:
                            template_text = ShopTemplateText.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ShopTemplateText),
                                parent = company_flow_action_message.template_text,
                                company = auth_login.shop.company,
                                shop = auth_login.shop,
                                name = company_flow_action_message.template_text.name,
                            )
                            for company_template_text_item in company_flow_action_message.template_text.company_template_text_item.all():
                                ShopTemplateTextItem.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template_text,
                                    number = company_template_text_item.number,
                                    message_type = company_template_text_item.message_type,
                                    text = company_template_text_item.text,
                                    image = company_template_text_item.image,
                                    image_width = company_template_text_item.image_width,
                                    image_height = company_template_text_item.image_height,
                                    video = company_template_text_item.video,
                                    video_width = company_template_text_item.video_width,
                                    video_height = company_template_text_item.video_height,
                                    video_thumbnail = company_template_text_item.video_thumbnail,
                                    template_text = company_template_text_item.template_text,
                                    template_video = company_template_text_item.template_video,
                                    template_richmessage = company_template_text_item.template_richmessage,
                                    template_richvideo = company_template_text_item.template_richvideo,
                                    template_cardtype = company_template_text_item.template_cardtype,
                                )
                    template_video = None
                    template_richmessage = None
                    template_richvideo = None
                    template_cardtype = None
                    ShopFlowActionMessage.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_text = template_text,
                        template_video = template_video,
                        template_richmessage = template_richmessage,
                        template_richvideo = template_richvideo,
                        template_cardtype = template_cardtype,
                        type = company_flow_action_message.type,
                        date = company_flow_action_message.date,
                        time = company_flow_action_message.time,
                    )
                elif flow_item.type == 9:
                    company_flow_step = CompanyFlowStep.objects.filter(flow=company_flow_item).first()
                    ShopFlowStep.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        tab = ShopFlowTab.objects.filter(flow=flow, number=company_flow_step.tab.number).first(),
                    )
                elif flow_item.type == 52:
                    company_flow_timer = CompanyFlowTimer.objects.filter(flow=company_flow_item).first()
                    ShopFlowTimer.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        type = company_flow_timer.type,
                        date = company_flow_timer.date,
                        time = company_flow_timer.time,
                    )
                elif flow_item.type == 53:
                    print()
                elif flow_item.type == 54:
                    company_flow_schedule = CompanyFlowSchedule.objects.filter(flow=company_flow_item).first()
                    if company_flow_schedule:
                        ShopFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            flow = flow_item,
                            number = company_flow_schedule.number,
                            name = company_flow_schedule.name,
                        )
                elif flow_item.type == 55:
                    company_flow_result = CompanyFlowResult.objects.filter(flow=company_flow_item).first()
                    if company_flow_result:
                        ShopFlowResult.objects.create(
                            id = str(uuid.uuid4()),
                            flow = flow_item,
                            number = company_flow_result.number,
                            name = company_flow_result.name,
                        )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def favorite(request):
    flow = ShopFlow.objects.filter(display_id=request.POST.get('id')).first()
    if flow.favorite_flg:
        flow.favorite_flg = False
    else:
        flow.favorite_flg = True
    flow.save()
    return JsonResponse( {'check': flow.favorite_flg}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, auth_login.shop, auth_login.shop.company)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )



def create_video(data, auth):
    video = None
    if data:
        if ShopTemplateVideo.objects.filter(parent=data, shop=auth.shop).exists():
            video = ShopTemplateVideo.objects.filter(parent=data, shop=auth.shop).first()
        else:
            video = ShopTemplateVideo.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ShopTemplateVideo),
                parent = data,
                company = auth.shop.company,
                shop = auth.shop,
                name = data.name,
                video = data.video,
                video_width = data.video_width,
                video_height = data.video_height,
                video_time = data.video_time,
                video_size = data.video_size,
                video_thumbnail = data.video_thumbnail,
            )
    return video

def create_question(data, auth):
    question = None
    if data:
        if ShopQuestion.objects.filter(parent=data, shop=auth.shop).exists():
            question = ShopQuestion.objects.filter(parent=data, shop=auth.shop).first()
        else:
            question = ShopQuestion.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ShopQuestion),
                parent = data,
                company = auth.shop.company,
                shop = auth.shop,
                title = data.title,
                name = data.name,
                description = data.description,
                color = data.color,
                count = data.count,
            )
            for company_question_item in data.company_question_item.all():
                question_item = ShopQuestionItem.objects.create(
                    id = str(uuid.uuid4()),
                    question = question,
                    number = company_question_item.number,
                    type = company_question_item.type,
                    title = company_question_item.title,
                    description = company_question_item.description,
                    choice_type = company_question_item.choice_type,
                    choice_count = company_question_item.choice_count,
                    required_flg = company_question_item.required_flg,
                )
                for company_question_item_choice in company_question_item.company_question_item_choice.all():
                    ShopQuestionItemChoice.objects.create(
                        id = str(uuid.uuid4()),
                        question_item = question_item,
                        number = company_question_item_choice.number,
                        text = company_question_item_choice.text,
                    )
    return question