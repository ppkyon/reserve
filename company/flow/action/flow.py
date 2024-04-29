from django.http import JsonResponse

from flow.models import (
    HeadFlow, HeadFlowTab, HeadFlowItem, HeadFlowTemplate, HeadFlowRichMenu,
    HeadFlowAction, HeadFlowActionReminder, HeadFlowActionMessage, HeadFlowStep,
    HeadFlowTimer, HeadFlowSchedule, HeadFlowResult,
    CompanyFlow, CompanyFlowTab, CompanyFlowItem, CompanyFlowTemplate, CompanyFlowRichMenu,
    CompanyFlowAction, CompanyFlowActionReminder, CompanyFlowActionMessage, CompanyFlowStep,
    CompanyFlowTimer, CompanyFlowSchedule, CompanyFlowResult,
)
from question.models import CompanyQuestion, CompanyQuestionItem, CompanyQuestionItemChoice
from richmenu.models import CompanyRichMenu, CompanyRichMenuItem
from sign.models import AuthLogin
from template.models import (
    CompanyTemplateText, CompanyTemplateTextItem, CompanyTemplateVideo, CompanyTemplateRichMessage, CompanyTemplateRichVideo,
    HeadTemplateGreeting, CompanyTemplateGreeting,
    CompanyTemplateCardType, CompanyTemplateCardTypeAnnounce, CompanyTemplateCardTypeAnnounceAction, CompanyTemplateCardTypeAnnounceText,
    CompanyTemplateCardTypeLocation, CompanyTemplateCardTypePerson, CompanyTemplateCardTypeImage, CompanyTemplateCardTypeMore,
)

from company.flow.action.list import get_list

from common import create_code, get_model_field, display_textarea_replace
from table.action import action_search

import re
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    valid = False
    if request.POST.get('valid') == '1':
        valid = True
    
    if request.POST.get('id'):
        flow = CompanyFlow.objects.filter(display_id=request.POST.get('id')).first()
        flow.name = request.POST.get('name')
        flow.valid = valid
        flow.author = request.user.id
        flow.save()
    else:
        head_flow = HeadFlow.objects.filter(display_id=request.POST.get('flow')).first()
        flow = CompanyFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, CompanyFlow),
            parent = head_flow,
            company = auth_login.company,
            name = request.POST.get('name'),
            description = head_flow.description,
            valid = valid,
            author = request.user.id
        )

        for head_flow_tab in HeadFlowTab.objects.filter(flow=head_flow).all():
            CompanyFlowTab.objects.create(
                id = str(uuid.uuid4()),
                flow = flow,
                number = head_flow_tab.number,
                name = head_flow_tab.name,
                value = head_flow_tab.value,
                member = head_flow_tab.member,
            )

        for head_flow_tab in HeadFlowTab.objects.filter(flow=head_flow).all():
            flow_tab = CompanyFlowTab.objects.filter(flow=flow, number=head_flow_tab.number).first()
            for head_flow_item in HeadFlowItem.objects.filter(flow_tab=head_flow_tab).all():
                flow_item = CompanyFlowItem.objects.create(
                    id = str(uuid.uuid4()),
                    flow_tab = flow_tab,
                    x = head_flow_item.x,
                    y = head_flow_item.y,
                    number = head_flow_item.number,
                    type = head_flow_item.type,
                    name = head_flow_item.name,
                    analytics = head_flow_item.analytics,
                )

                if flow_item.type == 1:
                    if not CompanyTemplateGreeting.objects.filter(company=auth_login.company).exists():
                        for head_template_greeting in HeadTemplateGreeting.objects.all():
                            CompanyTemplateGreeting.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, CompanyTemplateGreeting),
                                company = auth_login.company,
                                number = head_template_greeting.number,
                                message_type = head_template_greeting.message_type,
                                text = head_template_greeting.text,
                                image = head_template_greeting.image,
                                image_width = head_template_greeting.image_width,
                                image_height = head_template_greeting.image_height,
                                video = head_template_greeting.video,
                                video_width = head_template_greeting.video_width,
                                video_height = head_template_greeting.video_height,
                                video_thumbnail = head_template_greeting.video_thumbnail,
                                template_text = head_template_greeting.template_text,
                                template_video = head_template_greeting.template_video,
                                template_richmessage = head_template_greeting.template_richmessage,
                                template_richvideo = head_template_greeting.template_richvideo,
                                template_cardtype = head_template_greeting.template_cardtype,
                                author = head_template_greeting.author,
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
                    head_flow_template = HeadFlowTemplate.objects.filter(flow=head_flow_item).first()
                    if CompanyTemplateCardType.objects.filter(parent=head_flow_template.template_cardtype).exists():
                        template = CompanyTemplateCardType.objects.filter(parent=head_flow_template.template_cardtype).first()
                    else:
                        template = CompanyTemplateCardType.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, CompanyTemplateCardType),
                            parent = head_flow_template.template_cardtype,
                            company = auth_login.company,
                            name = head_flow_template.template_cardtype.name,
                            title = head_flow_template.template_cardtype.title,
                            type = head_flow_template.template_cardtype.type,
                            count = head_flow_template.template_cardtype.count,
                        )
                        if head_flow_template.template_cardtype.type == 1:
                            for head_template_card_type_announce in head_flow_template.template_cardtype.head_template_card_type_announce.all():
                                card_type = CompanyTemplateCardTypeAnnounce.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = head_template_card_type_announce.number,
                                    title = head_template_card_type_announce.title,
                                    image_count = head_template_card_type_announce.image_count,
                                    image_1 = head_template_card_type_announce.image_1,
                                    image_2 = head_template_card_type_announce.image_2,
                                    image_3 = head_template_card_type_announce.image_3,
                                    image_flg = head_template_card_type_announce.image_flg,
                                    label = head_template_card_type_announce.label,
                                    label_color = head_template_card_type_announce.label_color,
                                    label_flg = head_template_card_type_announce.label_flg,
                                    description = head_template_card_type_announce.description,
                                    description_flg = head_template_card_type_announce.description_flg,
                                )
                                for head_template_card_type_announce_text in head_template_card_type_announce.head_template_card_type_announce_text.all():
                                    CompanyTemplateCardTypeAnnounceText.objects.create(
                                        id = str(uuid.uuid4()),
                                        card_type = card_type,
                                        number = head_template_card_type_announce_text.number,
                                        title = head_template_card_type_announce_text.title,
                                        text = head_template_card_type_announce_text.text,
                                        flg = head_template_card_type_announce_text.flg,
                                    )
                                for head_template_card_type_announce_action in head_template_card_type_announce.head_template_card_type_announce_action.all():
                                    video = create_video(head_template_card_type_announce_action.video, auth_login)
                                    question = create_question(head_template_card_type_announce_action.question, auth_login)
                                    CompanyTemplateCardTypeAnnounceAction.objects.create(
                                        id = str(uuid.uuid4()),
                                        card_type = card_type,
                                        number = head_template_card_type_announce_action.number,
                                        label = head_template_card_type_announce_action.label,
                                        type = head_template_card_type_announce_action.type,
                                        url = head_template_card_type_announce_action.url,
                                        video = video,
                                        question = question,
                                        text = head_template_card_type_announce_action.text,
                                        button_type = head_template_card_type_announce_action.button_type,
                                        button_color = head_template_card_type_announce_action.button_color,
                                        button_background_color = head_template_card_type_announce_action.button_background_color,
                                        flg = head_template_card_type_announce_action.flg,
                                    )
                        elif head_flow_template.template_cardtype.type == 2:
                            for head_template_card_type_location in head_flow_template.template_cardtype.head_template_card_type_location.all():
                                action_video_1 = create_video(head_template_card_type_location.action_video_1, auth_login)
                                action_question_1 = create_question(head_template_card_type_location.action_question_1, auth_login)
                                action_video_2 = create_video(head_template_card_type_location.action_video_2, auth_login)
                                action_question_2 = create_question(head_template_card_type_location.action_question_2, auth_login)
                                CompanyTemplateCardTypeLocation.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = head_template_card_type_location.number,
                                    title = head_template_card_type_location.title,
                                    image_count = head_template_card_type_location.image_count,
                                    image_1 = head_template_card_type_location.image_1,
                                    image_2 = head_template_card_type_location.image_2,
                                    image_3 = head_template_card_type_location.image_3,
                                    label = head_template_card_type_location.label,
                                    label_color = head_template_card_type_location.label_color,
                                    label_flg = head_template_card_type_location.label_flg,
                                    place = head_template_card_type_location.place,
                                    place_flg = head_template_card_type_location.place_flg,
                                    plus = head_template_card_type_location.plus,
                                    plus_type = head_template_card_type_location.plus_type,
                                    plus_flg = head_template_card_type_location.plus_flg,
                                    action_label_1 = head_template_card_type_location.action_label_1,
                                    action_type_1 = head_template_card_type_location.action_type_1,
                                    action_url_1 = head_template_card_type_location.action_url_1,
                                    action_video_1 = action_video_1,
                                    action_question_1 = action_question_1,
                                    action_text_1 = head_template_card_type_location.action_text_1,
                                    action_flg_1 = head_template_card_type_location.action_flg_1,
                                    action_label_2 = head_template_card_type_location.action_label_2,
                                    action_type_2 = head_template_card_type_location.action_type_2,
                                    action_url_2 = head_template_card_type_location.action_url_2,
                                    action_video_2 = action_video_2,
                                    action_question_2 = action_question_2,
                                    action_text_2 = head_template_card_type_location.action_text_2,
                                    action_flg_2 = head_template_card_type_location.action_flg_2,
                                )
                        elif head_flow_template.template_cardtype.type == 3:
                            for head_template_card_type_person in head_flow_template.template_cardtype.head_template_card_type_person.all():
                                action_video_1 = create_video(head_template_card_type_person.action_video_1, auth_login)
                                action_question_1 = create_question(head_template_card_type_person.action_question_1, auth_login)
                                action_video_2 = create_video(head_template_card_type_person.action_video_2, auth_login)
                                action_question_2 = create_question(head_template_card_type_person.action_question_2, auth_login)
                                CompanyTemplateCardTypePerson.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = head_template_card_type_person.number,
                                    image = head_template_card_type_person.image,
                                    name = head_template_card_type_person.name,
                                    tag_1 = head_template_card_type_person.tag_1,
                                    tag_color_1 = head_template_card_type_person.tag_color_1,
                                    tag_flg_1 = head_template_card_type_person.tag_flg_1,
                                    tag_2 = head_template_card_type_person.tag_2,
                                    tag_color_2 = head_template_card_type_person.tag_color_2,
                                    tag_flg_2 = head_template_card_type_person.tag_flg_2,
                                    tag_3 = head_template_card_type_person.tag_3,
                                    tag_color_3 = head_template_card_type_person.tag_color_3,
                                    tag_flg_3 = head_template_card_type_person.tag_flg_3,
                                    description = head_template_card_type_person.description,
                                    description_flg = head_template_card_type_person.description_flg,
                                    action_label_1 = head_template_card_type_person.action_label_1,
                                    action_type_1 = head_template_card_type_person.action_type_1,
                                    action_url_1 = head_template_card_type_person.action_url_1,
                                    action_video_1 = action_video_1,
                                    action_question_1 = action_question_1,
                                    action_text_1 = head_template_card_type_person.action_text_1,
                                    action_flg_1 = head_template_card_type_person.action_flg_1,
                                    action_label_2 = head_template_card_type_person.action_label_2,
                                    action_type_2 = head_template_card_type_person.action_type_2,
                                    action_url_2 = head_template_card_type_person.action_url_2,
                                    action_video_2 = action_video_2,
                                    action_question_2 = action_question_2,
                                    action_text_2 = head_template_card_type_person.action_text_2,
                                    action_flg_2 = head_template_card_type_person.action_flg_2,
                                )
                        elif head_flow_template.template_cardtype.type == 4:
                            for head_template_card_type_image in head_flow_template.template_cardtype.head_template_card_type_image.all():
                                action_video = create_video(head_template_card_type_image.action_video, auth_login)
                                action_question = create_question(head_template_card_type_image.action_question, auth_login)
                                CompanyTemplateCardTypeImage.objects.create(
                                    id = str(uuid.uuid4()),
                                    template = template,
                                    number = head_template_card_type_image.number,
                                    image = head_template_card_type_image.image,
                                    label = head_template_card_type_image.label,
                                    label_color = head_template_card_type_image.label_color,
                                    label_flg = head_template_card_type_image.label_flg,
                                    action_label = head_template_card_type_image.action_label,
                                    action_type = head_template_card_type_image.action_type,
                                    action_url = head_template_card_type_image.action_url,
                                    action_video = action_video,
                                    action_question = action_question,
                                    action_text = head_template_card_type_image.action_text,
                                    action_flg = head_template_card_type_image.action_flg,
                                )
                        for head_template_card_type_more in head_flow_template.template_cardtype.head_template_card_type_more.all():
                            action_video = create_video(head_template_card_type_more.action_video, auth_login)
                            action_question = create_question(head_template_card_type_more.action_question, auth_login)
                            CompanyTemplateCardTypeMore.objects.create(
                                id = str(uuid.uuid4()),
                                template = template,
                                type = head_template_card_type_more.type,
                                image = head_template_card_type_more.image,
                                action_label = head_template_card_type_more.action_label,
                                action_type = head_template_card_type_more.action_type,
                                action_url = head_template_card_type_more.action_url,
                                action_video = action_video,
                                action_question = action_question,
                                action_text = head_template_card_type_more.action_text,
                            )
                    CompanyFlowTemplate.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_cardtype = template,
                    )
                elif flow_item.type == 7:
                    head_flow_rich_menu = HeadFlowRichMenu.objects.filter(flow=head_flow_item).first()
                    if CompanyRichMenu.objects.filter(parent=head_flow_rich_menu.rich_menu).exists():
                        rich_menu = CompanyRichMenu.objects.filter(parent=head_flow_rich_menu.rich_menu).first()
                    else:
                        if head_flow_rich_menu.rich_menu:
                            rich_menu = CompanyRichMenu.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, CompanyRichMenu),
                                parent = head_flow_rich_menu.rich_menu,
                                company = auth_login.company,
                                name = head_flow_rich_menu.rich_menu.name,
                                menu_type = head_flow_rich_menu.rich_menu.menu_type,
                                menu_flg = head_flow_rich_menu.rich_menu.menu_flg,
                                menu_text = head_flow_rich_menu.rich_menu.menu_text,
                                type = head_flow_rich_menu.rich_menu.type,
                                image = head_flow_rich_menu.rich_menu.image,
                                image_width = head_flow_rich_menu.rich_menu.image_width,
                                image_height = head_flow_rich_menu.rich_menu.image_height,
                            )
                            for head_rich_menu_item in head_flow_rich_menu.rich_menu.head_rich_menu_item.all():
                                video = create_video(head_rich_menu_item.video, auth_login)
                                question = create_question(head_rich_menu_item.question, auth_login)
                                CompanyRichMenuItem.objects.create(
                                    id = str(uuid.uuid4()),
                                    rich_menu = rich_menu,
                                    number = head_rich_menu_item.number,
                                    type = head_rich_menu_item.type,
                                    url = head_rich_menu_item.url,
                                    video = video,
                                    question = question,
                                    label = head_rich_menu_item.label,
                                    text = head_rich_menu_item.text,
                                )
                        else:
                            rich_menu = None
                    CompanyFlowRichMenu.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        rich_menu = rich_menu,
                    )
                elif flow_item.type == 8:
                    head_flow_action = HeadFlowAction.objects.filter(flow=head_flow_item).first()
                    CompanyFlowAction.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        action = CompanyFlowTab.objects.filter(flow=flow, number=head_flow_action.action.number).first(),
                    )
                    head_flow_action_reminder = HeadFlowActionReminder.objects.filter(flow=head_flow_item).first()
                    template_text = None
                    if head_flow_action_reminder.template_text:
                        if CompanyTemplateText.objects.filter(company=auth_login.company, parent=head_flow_action_reminder.template_text).exists():
                            template_text = CompanyTemplateText.objects.filter(parent=head_flow_action_reminder.template_text).first()
                        else:
                            template_text = CompanyTemplateText.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, CompanyTemplateText),
                                parent = head_flow_action_reminder.template_text,
                                company = auth_login.company,
                                name = head_flow_action_reminder.template_text.name,
                            )
                        for head_template_text_item in head_flow_action_reminder.template_text.head_template_text_item.all():
                            CompanyTemplateTextItem.objects.create(
                                id = str(uuid.uuid4()),
                                template = template_text,
                                number = head_template_text_item.number,
                                message_type = head_template_text_item.message_type,
                                text = head_template_text_item.text,
                                image = head_template_text_item.image,
                                image_width = head_template_text_item.image_width,
                                image_height = head_template_text_item.image_height,
                                video = head_template_text_item.video,
                                video_width = head_template_text_item.video_width,
                                video_height = head_template_text_item.video_height,
                                video_thumbnail = head_template_text_item.video_thumbnail,
                                template_text = head_template_text_item.template_text,
                                template_video = head_template_text_item.template_video,
                                template_richmessage = head_template_text_item.template_richmessage,
                                template_richvideo = head_template_text_item.template_richvideo,
                                template_cardtype = head_template_text_item.template_cardtype,
                            )
                    template_video = None
                    template_richmessage = None
                    template_richvideo = None
                    template_cardtype = None
                    CompanyFlowActionReminder.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_text = template_text,
                        template_video = template_video,
                        template_richmessage = template_richmessage,
                        template_richvideo = template_richvideo,
                        template_cardtype = template_cardtype,
                        date = head_flow_action_reminder.date,
                        time = head_flow_action_reminder.time,
                    )
                    head_flow_action_message = HeadFlowActionMessage.objects.filter(flow=head_flow_item).first()
                    template_text = None
                    if head_flow_action_message.template_text:
                        if CompanyTemplateText.objects.filter(company=auth_login.company, parent=head_flow_action_message.template_text).exists():
                            template_text = CompanyTemplateText.objects.filter(parent=head_flow_action_message.template_text).first()
                        else:
                            template_text = CompanyTemplateText.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, CompanyTemplateText),
                                parent = head_flow_action_message.template_text,
                                company = auth_login.company,
                                name = head_flow_action_message.template_text.name,
                            )
                        for head_template_text_item in head_flow_action_message.template_text.head_template_text_item.all():
                            CompanyTemplateTextItem.objects.create(
                                id = str(uuid.uuid4()),
                                template = template_text,
                                number = head_template_text_item.number,
                                message_type = head_template_text_item.message_type,
                                text = head_template_text_item.text,
                                image = head_template_text_item.image,
                                image_width = head_template_text_item.image_width,
                                image_height = head_template_text_item.image_height,
                                video = head_template_text_item.video,
                                video_width = head_template_text_item.video_width,
                                video_height = head_template_text_item.video_height,
                                video_thumbnail = head_template_text_item.video_thumbnail,
                                template_text = head_template_text_item.template_text,
                                template_video = head_template_text_item.template_video,
                                template_richmessage = head_template_text_item.template_richmessage,
                                template_richvideo = head_template_text_item.template_richvideo,
                                template_cardtype = head_template_text_item.template_cardtype,
                            )
                    template_video = None
                    template_richmessage = None
                    template_richvideo = None
                    template_cardtype = None
                    CompanyFlowActionMessage.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        template_text = template_text,
                        template_video = template_video,
                        template_richmessage = template_richmessage,
                        template_richvideo = template_richvideo,
                        template_cardtype = template_cardtype,
                        type = head_flow_action_message.type,
                        date = head_flow_action_message.date,
                        time = head_flow_action_message.time,
                    )
                elif flow_item.type == 9:
                    head_flow_step = HeadFlowStep.objects.filter(flow=head_flow_item).first()
                    CompanyFlowStep.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        tab = CompanyFlowTab.objects.filter(flow=flow, number=head_flow_step.tab.number).first(),
                    )
                elif flow_item.type == 52:
                    head_flow_timer = HeadFlowTimer.objects.filter(flow=head_flow_item).first()
                    CompanyFlowTimer.objects.create(
                        id = str(uuid.uuid4()),
                        flow = flow_item,
                        type = head_flow_timer.type,
                        date = head_flow_timer.date,
                        time = head_flow_timer.time,
                    )
                elif flow_item.type == 53:
                    print()
                elif flow_item.type == 54:
                    head_flow_schedule = HeadFlowSchedule.objects.filter(flow=head_flow_item).first()
                    if head_flow_schedule:
                        CompanyFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            flow = flow_item,
                            number = head_flow_schedule.number,
                            name = head_flow_schedule.name,
                        )
                elif flow_item.type == 55:
                    head_flow_result = HeadFlowResult.objects.filter(flow=head_flow_item).first()
                    if head_flow_result:
                        CompanyFlowResult.objects.create(
                            id = str(uuid.uuid4()),
                            flow = flow_item,
                            number = head_flow_result.number,
                            name = head_flow_result.name,
                        )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, None, auth_login.company)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def valid(request):
    flow = CompanyFlow.objects.filter(display_id=request.POST.get('id')).first()
    if flow.valid:
        flow.valid = False
    else:
        flow.valid = True
    flow.save()
    return JsonResponse( {'check': flow.valid}, safe=False )

def get(request):
    remove = re.compile(r"<[^>]*?>")
    flow = CompanyFlow.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(CompanyFlow)).first()
    flow['tab'] = list(CompanyFlowTab.objects.filter(flow__id=flow['id']).values(*get_model_field(CompanyFlowTab)).order_by('number').all())
    for tab_index, tab_item in enumerate(flow['tab']):
        flow['tab'][tab_index]['item'] = list(CompanyFlowItem.objects.filter(flow_tab__id=tab_item['id']).values(*get_model_field(CompanyFlowItem)).order_by('x','y').all())
        for flow_index, flow_item in enumerate(flow['tab'][tab_index]['item']):
            if flow_item['type'] == 1:
                flow['tab'][tab_index]['item'][flow_index]['template'] = CompanyTemplateGreeting.objects.filter(number=1).values(*get_model_field(CompanyTemplateGreeting)).first()
                if flow['tab'][tab_index]['item'][flow_index]['template']['text']:
                    flow['tab'][tab_index]['item'][flow_index]['template']['text'] = remove.sub('', display_textarea_replace(flow['tab'][tab_index]['item'][flow_index]['template']['text']))
            elif flow_item['type'] == 2:
                print(flow_item)
            elif flow_item['type'] == 3:
                print(flow_item)
            elif flow_item['type'] == 4:
                print(flow_item)
            elif flow_item['type'] == 5:
                print(flow_item)
            elif flow_item['type'] == 6:
                template = CompanyFlowTemplate.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowTemplate)).first()
                if template['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['template'] = CompanyTemplateCardType.objects.filter(id=template['template_cardtype']).values(*get_model_field(CompanyTemplateCardType)).first()
            elif flow_item['type'] == 7:
                rich_menu = CompanyFlowRichMenu.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowRichMenu)).first()
                if rich_menu['rich_menu']:
                    flow['tab'][tab_index]['item'][flow_index]['rich_menu'] = CompanyRichMenu.objects.filter(id=rich_menu['rich_menu']).values(*get_model_field(CompanyRichMenu)).first()
            elif flow_item['type'] == 8:
                flow['tab'][tab_index]['item'][flow_index]['action'] = CompanyFlowAction.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowAction)).first()
                flow['tab'][tab_index]['item'][flow_index]['action']['action'] = CompanyFlowTab.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['action']['action']).values(*get_model_field(CompanyFlowTab)).first()
                flow['tab'][tab_index]['item'][flow_index]['reminder'] = CompanyFlowActionReminder.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowActionReminder)).first()
                if flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text'] = CompanyTemplateText.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text']).values(*get_model_field(CompanyTemplateText)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video'] = CompanyTemplateVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video']).values(*get_model_field(CompanyTemplateVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage'] = CompanyTemplateRichMessage.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage']).values(*get_model_field(CompanyTemplateRichMessage)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo'] = CompanyTemplateRichVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo']).values(*get_model_field(CompanyTemplateRichVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype'] = CompanyTemplateCardType.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype']).values(*get_model_field(CompanyTemplateCardType)).first()
                flow['tab'][tab_index]['item'][flow_index]['message'] = CompanyFlowActionMessage.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowActionMessage)).first()
                if flow['tab'][tab_index]['item'][flow_index]['message']['template_text']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_text'] = CompanyTemplateText.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_text']).values(*get_model_field(CompanyTemplateText)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_video']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_video'] = CompanyTemplateVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_video']).values(*get_model_field(CompanyTemplateVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage'] = CompanyTemplateRichMessage.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage']).values(*get_model_field(CompanyTemplateRichMessage)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo'] = CompanyTemplateRichVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo']).values(*get_model_field(CompanyTemplateRichVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype'] = CompanyTemplateCardType.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype']).values(*get_model_field(CompanyTemplateCardType)).first()
            elif flow_item['type'] == 9:
                flow['tab'][tab_index]['item'][flow_index]['step'] = CompanyFlowStep.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowStep)).first()
                flow['tab'][tab_index]['item'][flow_index]['step']['tab'] = CompanyFlowTab.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['step']['tab']).values(*get_model_field(CompanyFlowTab)).first()
            elif flow_item['type'] == 52:
                flow['tab'][tab_index]['item'][flow_index]['timer'] = CompanyFlowTimer.objects.filter(flow__id=flow_item['id']).values(*get_model_field(CompanyFlowTimer)).first()
    return JsonResponse( flow, safe=False )



def create_video(data, auth):
    video = None
    if data:
        if CompanyTemplateVideo.objects.filter(parent=data).exists():
            video = CompanyTemplateVideo.objects.filter(parent=data).first()
        else:
            video = CompanyTemplateVideo.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, CompanyTemplateVideo),
                parent = data,
                company = auth.company,
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
        if CompanyQuestion.objects.filter(parent=data).exists():
            question = CompanyQuestion.objects.filter(parent=data).first()
        else:
            question = CompanyQuestion.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, CompanyQuestion),
                parent = data,
                company = auth.company,
                title = data.title,
                name = data.name,
                description = data.description,
                color = data.color,
                count = data.count,
            )
            for head_question_item in data.head_question_item.all():
                question_item = CompanyQuestionItem.objects.create(
                    id = str(uuid.uuid4()),
                    question = question,
                    number = head_question_item.number,
                    type = head_question_item.type,
                    title = head_question_item.title,
                    description = head_question_item.description,
                    choice_type = head_question_item.choice_type,
                    choice_count = head_question_item.choice_count,
                    required_flg = head_question_item.required_flg,
                )
                for head_question_item_choice in head_question_item.head_question_item_choice.all():
                    CompanyQuestionItemChoice.objects.create(
                        id = str(uuid.uuid4()),
                        question_item = question_item,
                        number = head_question_item_choice.number,
                        text = head_question_item_choice.text,
                    )
    return question