from django.conf import settings
from django.shortcuts import redirect

from flow.models import (
    HeadFlow, HeadFlowTab, HeadFlowItem,
    HeadFlowTemplate, HeadFlowRichMenu, HeadFlowAction, HeadFlowActionReminder, HeadFlowActionMessage, HeadFlowStep,
    HeadFlowTimer,
)
from richmenu.models import HeadRichMenu, HeadRichMenuItem
from template.models import (
    HeadTemplateText, HeadTemplateTextItem, HeadTemplateGreeting,
    HeadTemplateCardType, HeadTemplateCardTypeAnnounce, HeadTemplateCardTypeAnnounceText, HeadTemplateCardTypeAnnounceAction,
)

from common import create_code

import uuid

def add(request):
    if not HeadFlow.objects.filter(name='初期フロー').exists():
        flow = HeadFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadFlow),
            name = '初期フロー',
            description = 'エントリー → 無料体験 → 1回目 → 2回目 → 3回目 → 4回目 → 5回目',
        )

        entry_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 1,
            name = 'エントリー',
            value = 'entry',
        )

        free_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 2,
            name = '無料体験',
            value = 'free',
        )

        first_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 3,
            name = '1回目',
            value = 'first',
        )

        second_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 4,
            name = '2回目',
            value = 'second',
        )

        third_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 5,
            name = '3回目',
            value = 'third',
        )

        fourth_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 6,
            name = '4回目',
            value = 'fourth',
        )

        fifth_flow_tab = HeadFlowTab.objects.create(
            id = str(uuid.uuid4()),
            flow = flow,
            number = 7,
            name = '5回目',
            value = 'fifth',
        )

        if not HeadTemplateGreeting.objects.exists():
            HeadTemplateGreeting.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, HeadTemplateGreeting),
                number = 1,
                message_type = 1,
                text = '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1">にご登録ありがとうございます。<br><br>※「予約をする」をタップあと、認証を求める画面が表示されますが「許可する」をタップしてください。<br><br>ご予約はこちらから可能になります♪',
            )

        create_entry(
            entry_flow_tab,
            free_flow_tab,
        )

        free_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '無料体験',
            menu_type = 0,
            menu_flg = False,
            type = 1,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = free_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = free_rich_menu,
            number = 'b',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = free_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = free_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        free_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【無料体験】予約確定',
            title = '【無料体験】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = free_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '無料体験',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        free_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【無料体験】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = free_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        free_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【無料体験】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = free_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_free(
            free_flow_tab,
            free_rich_menu,
            free_schedule_message_template,
            free_action_reminder_template,
            free_action_message_template,
        )

        first_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '1回目',
            menu_type = 0,
            menu_flg = False,
            type = 2,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = first_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = first_rich_menu,
            number = 'b',
            type = 5,
            url = '【予約履歴ページ】',
            label = '【予約履歴ページ】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = first_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = first_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        first_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【1回目】予約確定',
            title = '【1回目】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = first_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '1回目',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        first_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【1回目】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = first_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        first_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【1回目】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = first_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_first(
            first_flow_tab,
            first_rich_menu,
            first_schedule_message_template,
            first_action_reminder_template,
            first_action_message_template,
        )

        second_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '2回目',
            menu_type = 0,
            menu_flg = False,
            type = 2,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = second_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = second_rich_menu,
            number = 'b',
            type = 5,
            url = '【予約履歴ページ】',
            label = '【予約履歴ページ】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = second_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = second_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        second_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【2回目】予約確定',
            title = '【2回目】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = second_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '2回目',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        second_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【2回目】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = second_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        second_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【2回目】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = second_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_second(
            second_flow_tab,
            second_rich_menu,
            second_schedule_message_template,
            second_action_reminder_template,
            second_action_message_template,
        )

        third_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '3回目',
            menu_type = 0,
            menu_flg = False,
            type = 2,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = third_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = third_rich_menu,
            number = 'b',
            type = 5,
            url = '【予約履歴ページ】',
            label = '【予約履歴ページ】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = third_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = third_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        third_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【3回目】予約確定',
            title = '【3回目】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = third_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '3回目',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        third_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【3回目】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = third_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        third_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【3回目】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = third_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_third(
            third_flow_tab,
            third_rich_menu,
            third_schedule_message_template,
            third_action_reminder_template,
            third_action_message_template,
        )

        fourth_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '4回目',
            menu_type = 0,
            menu_flg = False,
            type = 2,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fourth_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fourth_rich_menu,
            number = 'b',
            type = 5,
            url = '【予約履歴ページ】',
            label = '【予約履歴ページ】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fourth_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fourth_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        fourth_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【4回目】予約確定',
            title = '【4回目】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = fourth_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '4回目',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        fourth_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【4回目】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = fourth_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        fourth_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【4回目】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = fourth_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_fourth(
            fourth_flow_tab,
            fourth_rich_menu,
            fourth_schedule_message_template,
            fourth_action_reminder_template,
            fourth_action_message_template,
        )

        fifth_rich_menu = HeadRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadRichMenu),
            name = '5回目',
            menu_type = 0,
            menu_flg = False,
            type = 2,
            image = None,
            author = None,
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fifth_rich_menu,
            number = 'a',
            type = 4,
            url = '【予約フォーム】',
            label = '【予約フォーム】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fifth_rich_menu,
            number = 'b',
            type = 5,
            url = '【予約履歴ページ】',
            label = '【予約履歴ページ】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fifth_rich_menu,
            number = 'c',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【よくある質問】',
        )
        HeadRichMenuItem.objects.create(
            id = str(uuid.uuid4()),
            rich_menu = fifth_rich_menu,
            number = 'd',
            type = 1,
            url = 'https://www.amazon.co.jp/',
            label = '【Webページ】',
        )

        fifth_schedule_message_template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = '【5回目】予約確定',
            title = '【5回目】予約確定',
            type = 1,
            count = 1,
        )
        card_type = HeadTemplateCardTypeAnnounce.objects.create(
            id = str(uuid.uuid4()),
            template = fifth_schedule_message_template,
            number = 1,
            title = '予約が確定しました!',
            image_count = 0,
            image_1 = None,
            image_2 = None,
            image_3 = None,
            image_flg = False,
            label = None,
            label_color = 0,
            label_flg = False,
            description = 'ご予約ありがとうございます。当日お会いできることを楽しみにしております♪',
            description_flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            title = '日程',
            text = '【予約日時】',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceText.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 2,
            title = 'メニュー',
            text = '5回目',
            flg = True,
        )
        HeadTemplateCardTypeAnnounceAction.objects.create(
            id = str(uuid.uuid4()),
            card_type = card_type,
            number = 1,
            label = '日程を再調整する',
            type = 4,
            url = '【予約フォームURL】',
            video = None,
            question = None,
            text = None,
            button_type = 1,
            button_color = 3,
            button_background_color = 0,
            flg = True,
        )

        fifth_action_reminder_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【5回目】前日リマインダー',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = fifth_action_reminder_template,
            number = 1,
            message_type = 0,
            text = '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">さん、こんにちは😃<br>明日の確認でご連絡いたしました。<br>予定通りご参加可能な場合は、以下「確認しました」をタップしてください🔽<br><br>🔶詳細<br>日時：<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1"><br>持ち物：運動しやすい服装<br><br>【緊急連絡先】<br>当日にトラブル等が発生した場合や、急にご都合が悪くなった際は、こちらにご連絡お願いします。<br>担当者：<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1"><br>連絡先：<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1"><br><br>それでは、ご参加お待ちしております～😊🌷',
        )

        fifth_action_message_template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = '【5回目】お礼メッセージ',
        )
        HeadTemplateTextItem.objects.create(
            id = str(uuid.uuid4()),
            template = fifth_action_message_template,
            number = 1,
            message_type = 0,
            text = 'ご参加いただきまして、有難うございました😊',
        )

        create_fifth(
            fifth_flow_tab,
            fifth_rich_menu,
            fifth_schedule_message_template,
            fifth_action_reminder_template,
            fifth_action_message_template,
        )

    return redirect('/head/flow/')

def create_entry(
        flow_tab,
        next_tab,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = None,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 1,
        name = 'あいさつメッセージ',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 0,
        type = 52,
    )
    HeadFlowTimer.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        type = 0,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 9,
        name = 'ステップ',
    )
    HeadFlowStep.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        tab = next_tab,
    )

    return None

def create_free(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '無料体験',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None

def create_first(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '1回目',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None

def create_second(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '2回目',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None

def create_third(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '3回目',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None

def create_fourth(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '4回目',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None

def create_fifth(
        flow_tab,
        rich_menu,
        schedule_message_template,
        action_reminder_template,
        action_message_template,
    ):

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 1,
        number = 0,
        type = 7,
        name = 'リッチメニュー',
        analytics = True,
    )
    HeadFlowRichMenu.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        rich_menu = rich_menu,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 1,
        y = 2,
        number = 0,
        type = 10,
        name = 'アクション待ち',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 2,
        y = 2,
        number = 1,
        type = 54,
        name = '確定',
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 3,
        y = 2,
        number = 0,
        type = 6,
        name = 'カードタイプメッセージ',
    )
    HeadFlowTemplate.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_cardtype = schedule_message_template,
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 4,
        y = 2,
        number = 0,
        type = 51,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 5,
        y = 2,
        number = 0,
        type = 8,
        name = '5回目',
    )
    HeadFlowAction.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        action = flow_tab,
    )
    HeadFlowActionReminder.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_reminder_template,
        date = 1,
        time = 12,
    )
    HeadFlowActionMessage.objects.create(
        id = str(uuid.uuid4()),
        flow = flow,
        template_text = action_message_template,
        type = 0,
        date = 0,
        time = None,
    )

    flow = HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 6,
        y = 2,
        number = 0,
        type = 55,
        name = '完了',
    )

    HeadFlowItem.objects.create(
        id = str(uuid.uuid4()),
        flow_tab = flow_tab,
        x = 7,
        y = 2,
        number = 0,
        type = 11,
        name = '完了',
    )

    return None