function append_flow( data ) {
    var type = '';
    if ( data.type == 1 ) {
        type = 'template_greeting';
    } else if ( data.type == 2 ) {
        type = 'template_message';
    } else if ( data.type == 3 ) {
        type = 'template_video';
    } else if ( data.type == 4 ) {
        type = 'template_rich_message';
    } else if ( data.type == 5 ) {
        type = 'template_rich_video';
    } else if ( data.type == 6 ) {
        type = 'template_card_type';
    } else if ( data.type == 7 ) {
        type = 'rich_menu';
    } else if ( data.type == 8 ) {
        type = 'action';
    } else if ( data.type == 9 ) {
        type = 'step';
    } else if ( data.type == 10 ) {
        type = 'wait';
    } else if ( data.type == 11 ) {
        type = 'end';
    } else if ( data.type == 51 ) {
        type = 'manual';
    } else if ( data.type == 52 ) {
        type = 'timer';
    } else if ( data.type == 53 ) {
        type = 'condition';
    } else if ( data.type == 54 ) {
        type = 'schedule';
    } else if ( data.type == 55 ) {
        type = 'result';
    }

    if ( data.type == 1 ) {
        if ( 'id' in data.template ) {
            if ( data.template.message_type == 1 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/greeting/" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '</a>';
                html += '<p class="chart-content-text p-2 mb-0">' + data.template.text + '</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.message_type == 2 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/greeting/" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '</a>';
                html += '<p class="chart-content-text p-2 mb-0">画像メッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.message_type == 3 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/greeting/" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '</a>';
                html += '<p class="chart-content-text p-2 mb-0">動画メッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.message_type == 4 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/greeting/" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #FF0202;">挨拶メッセージ</p>';
                html += '</a>';
                html += '<p class="chart-content-text p-2 mb-0">テンプレートメッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            }
        }
    } else if ( data.type == 2 ) {
        return '<td></td>';
    } else if ( data.type == 3 ) {
        return '<td></td>';
    } else if ( data.type == 4 ) {
        return '<td></td>';
    } else if ( data.type == 5 ) {
        return '<td></td>';
    } else if ( data.type == 6 ) {
        if ( check_empty( data.template ) ) {
            if ( data.template.type == 1 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #A1007E;">' + data.name + '</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/cardtype/edit/?id=' + data.template.display_id + '" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #A1007E">' + data.template.name + '</p>';
                html += '</a>';
                html += '<input type="hidden" name="template" value="' + data.template.display_id + '">';
                html += '<p class="chart-content-title p-2 mb-0">アナウンステンプレートメッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.type == 2 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #A1007E;">' + data.name + '</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/cardtype/edit/?id=' + data.template.display_id + '" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #A1007E">' + data.template.name + '</p>';
                html += '</a>';
                html += '<input type="hidden" name="template" value="' + data.template.display_id + '">';
                html += '<p class="chart-content-title p-2 mb-0">ロケーションテンプレートメッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.type == 3 ) {
                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #A1007E;">' + data.name + '</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/cardtype/edit/?id=' + data.template.display_id + '" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #A1007E">' + data.template.name + '</p>';
                html += '</a>';
                html += '<input type="hidden" name="template" value="' + data.template.display_id + '">';
                html += '<p class="chart-content-title p-2 mb-0">パーソンテンプレートメッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            } else if ( data.template.type == 4 ) {

                var html = '<td>';
                html += '<input type="hidden" name="type" value="' + type + '">';
                html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #A1007E;">' + data.name + '</p>';
                html += '<div class="chart-content position-relative mb-4">';
                html += '<a href="/head/template/cardtype/edit/?id=' + data.template.display_id + '" target="_blank">';
                html += '<p class="chart-sub-title p-1 ps-2 pe-5 mb-0" style="background-color: #A1007E">' + data.template.name + '</p>';
                html += '</a>';
                html += '<input type="hidden" name="template" value="' + data.template.display_id + '">';
                html += '<p class="chart-content-title p-2 mb-0">イメージテンプレートメッセージ</p>';
                html += '<i class="bx bx-chevron-right next-icon"></i>';
                html += '</div>';
                html += '</td>';
                return html;
            }
        }
    } else if ( data.type == 7 ) {
        var number = data.x + '_' + data.y
        var display_id = '';
        var name = '';
        if ( 'rich_menu' in data ) {
            display_id = data.rich_menu.display_id;
            name = data.rich_menu.name;
        }
        var html = '<td>';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #0900FF;">リッチメニュー</p>';
        html += '<div class="chart-content mb-4">';
        html += '<div class="dropdown input-select-dropdown d-inline-block position-relative p-0 m-2 mt-4 mb-3">';
        html += '<input type="hidden" name="rich_menu" value="' + display_id + '">';
        html += '<input type="text" class="input-text input-select input-richmenu ps-2 pe-2" value="' + name + '" placeholder="なし" readonly>';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#rich_menu_modal"></button>';
        html += '<div class="input-check-wrap ps-4 ms-2 mt-2 mb-0">';
        html += '<label for="analytics_' + number + '" class="mb-0">アナリティクス</label>';
        if ( data.analytics ) {
            html += '<input id="analytics_' + number + '" type="checkbox" name="analytics" class="form-check-input input-check" checked disabled>';
        } else {
            html += '<input id="analytics_' + number + '" type="checkbox" name="analytics" class="form-check-input input-check" disabled>';
        }
        html += '<label for="analytics_' + number + '" class="input-check-mark mb-0"></label>';
        html += '</div>';
        if ( check_empty(name) ) {
            html += '<a href="/head/richmenu/edit/?id=' + display_id + '" target=_blank>';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/search.svg" class="search-icon">';
            html += '</a>';
        } else {
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/search.svg" class="search-icon">';
        }
        html += '</div>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 8 ) {
        var html = '<td>';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<p class="chart-title p-1 ps-2 mb-0" style="color: #000; background-color: #FFFF2D;">' + data.name + '</p>';
        html += '<div class="chart-content position-relative mb-4">';
        html += '<div class="d-inline-block position-relative p-0 m-2 mt-3 mb-1">';
        html += '<input type="text" class="input-text input-select input-type ps-2 pe-2" value="' + data.action.action.name + '" readonly>';
        html += '</div>';
        html += '<div>';
        html += '<input type="hidden" name="action" value="' + data.action.action.number + '">';
        if ( check_empty(data.reminder.template_text) ) {
            html += '<input type="hidden" name="reminder_action_template" value="テキストメッセージ">';
            html += '<input type="hidden" name="reminder_action_template_item" value="' + data.reminder.template_text.display_id + '">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="' + data.reminder.template_text.name + '">';
        } else if ( check_empty(data.reminder.template_video) ) {
            html += '<input type="hidden" name="reminder_action_template" value="動画メッセージ">';
            html += '<input type="hidden" name="reminder_action_template_item" value="' + data.reminder.template_video.display_id + '">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="' + data.reminder.template_video.name + '">';
        } else if ( check_empty(data.reminder.template_richmessage) ) {
            html += '<input type="hidden" name="reminder_action_template" value="リッチメッセージ">';
            html += '<input type="hidden" name="reminder_action_template_item" value="' + data.reminder.template_richmessage.display_id + '">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="' + data.reminder.template_richmessage.name + '">';
        } else if ( check_empty(data.reminder.template_richvideo) ) {
            html += '<input type="hidden" name="reminder_action_template" value="リッチビデオメッセージ">';
            html += '<input type="hidden" name="reminder_action_template_item" value="' + data.reminder.template_richvideo.display_id + '">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="' + data.reminder.template_richvideo.name + '">';
        } else if ( check_empty(data.reminder.template_cardtype) ) {
            html += '<input type="hidden" name="reminder_action_template" value="カードタイプメッセージ">';
            html += '<input type="hidden" name="reminder_action_template_item" value="' + data.reminder.template_cardtype.display_id + '">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="' + data.reminder.template_cardtype.name + '">';
        } else {
            html += '<input type="hidden" name="reminder_action_template" value="">';
            html += '<input type="hidden" name="reminder_action_template_item" value="">';
            html += '<input type="hidden" name="reminder_action_template_item_name" value="">';
        }
        html += '<input type="hidden" name="reminder_action_date" value="' + data.reminder.date + '">';
        html += '<input type="hidden" name="reminder_action_time" value="' + data.reminder.time + '">';
        html += '<button type="button" class="btn action-reminder-button link-button p-0 ms-3">' + data.name + 'リマインダー設定</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#action_reminder_modal"></button>';
        if ( check_empty(data.message.template_text) ) {
            html += '<input type="hidden" name="message_action_template" value="テキストメッセージ">';
            html += '<input type="hidden" name="message_action_template_item" value="' + data.message.template_text.display_id + '">';
            html += '<input type="hidden" name="message_action_template_item_name" value="' + data.message.template_text.name + '">';
        } else if ( check_empty(data.message.template_video) ) {
            html += '<input type="hidden" name="message_action_template" value="動画メッセージ">';
            html += '<input type="hidden" name="message_action_template_item" value="' + data.message.template_video.display_id + '">';
            html += '<input type="hidden" name="message_action_template_item_name" value="' + data.message.template_video.name + '">';
        } else if ( check_empty(data.message.template_richmessage) ) {
            html += '<input type="hidden" name="message_action_template" value="リッチメッセージ">';
            html += '<input type="hidden" name="message_action_template_item" value="' + data.message.template_richmessage.display_id + '">';
            html += '<input type="hidden" name="message_action_template_item_name" value="' + data.message.template_richmessage.name + '">';
        } else if ( check_empty(data.message.template_richvideo) ) {
            html += '<input type="hidden" name="message_action_template" value="リッチビデオメッセージ">';
            html += '<input type="hidden" name="message_action_template_item" value="' + data.message.template_richvideo.display_id + '">';
            html += '<input type="hidden" name="message_action_template_item_name" value="' + data.message.template_richvideo.name + '">';
        } else if ( check_empty(data.message.template_cardtype) ) {
            html += '<input type="hidden" name="message_action_template" value="カードタイプメッセージ">';
            html += '<input type="hidden" name="message_action_template_item" value="' + data.message.template_cardtype.display_id + '">';
            html += '<input type="hidden" name="message_action_template_item_name" value="' + data.message.template_cardtype.name + '">';
        } else {
            html += '<input type="hidden" name="message_action_template" value="">';
            html += '<input type="hidden" name="message_action_template_item" value="">';
            html += '<input type="hidden" name="message_action_template_item_name" value="">';
        }
        html += '<input type="hidden" name="message_action_template_timer" value="' + data.message.type + '">';
        html += '<input type="hidden" name="message_action_template_timer_date" value="' + data.message.date + '">';
        html += '<input type="hidden" name="message_action_template_timer_time" value="' + data.message.time + '">';
        html += '<button type="button" class="btn action-message-button link-button p-0 ms-3">' + data.name + '終了後メッセージ設定</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#action_message_modal"></button>';
        html += '</div>';
        html += '<i class="bx bx-chevron-right next-icon"></i>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 9 ) {
        var html = '<td>';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #1484FF;">' + data.name + '</p>';
        html += '<div class="chart-content position-relative mb-4">';
        html += '<div class="d-inline-block position-relative p-0 m-2 mt-4 mb-3">';
        html += '<input type="hidden" name="' + type + '" value="' + data.step.tab.number + '">';
        html += '<input type="text" class="input-text input-select input-type ps-2 pe-2" value="' + data.step.tab.name + '" readonly>';
        html += '</div>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 10 ) {
        var html = '<td>';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #707070;">' + data.name + '</p>';
        html += '<div class="chart-content position-relative mb-4">';
        html += '<div class="d-inline-block position-relative p-0 m-2 mt-4 mb-3">';
        html += '<input type="text" class="input-text input-select input-type ps-2 pe-2" value="' + data.name + '" readonly>';
        html += '</div>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 11 ) {
        var html = '<td>';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<p class="chart-title p-1 ps-2 mb-0" style="background-color: #1484FF;">' + data.name + '</p>';
        html += '<div class="chart-content position-relative mb-4">';
        html += '<div class="d-inline-block position-relative p-0 m-2 mt-4 mb-3">';
        html += '<input type="text" class="input-text input-select input-type ps-2 pe-2" value="' + data.name + '" readonly>';
        html += '</div>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 51 ) {
        var html = '<td style="width: 10rem;">';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<div class="chart-bar first position-relative mb-4" style="background-color: #D06D8C; border: 2.5px solid #D06D8C;"></div>';
        html += '</td>';
        return html;
    } else if ( data.type == 52 ) {
        var html = '<td style="width: 10rem;">';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<div class="chart-bar first position-relative mb-4" style="background-color: #C93A40; border: 2.5px solid #C93A40;">';
        html += '<input type="hidden" name="timer" value="' + data.timer.type + '">';
        if ( check_empty(data.timer.date) && data.timer.date != 0 ) {
            html += '<input type="hidden" name="timer_date" value="' + data.timer.date + '">';
        } else {
            html += '<input type="hidden" name="timer_date">';
        }
        if ( check_empty(data.timer.time) && data.timer.time != 0 ) {
            html += '<input type="hidden" name="timer_time" value="' + data.timer.time + '">';
        } else {
            html += '<input type="hidden" name="timer_time">';
        }
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/timer.svg" class="timer-icon chart-bar-icon">';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#timer_modal"></button>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 53 ) {
        return '<td></td>';
    } else if ( data.type == 54 ) {
        var html = '<td style="width: 10rem;">';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<div class="chart-bar first-break position-relative mb-4" style="background-color: #000000; border: 2.5px solid #000000;">';
        html += '<p class="chart-bar-text text-center p-1 ps-2 pe-2 mb-0" style="border: 3px solid #000000;">' + data.name + '</p>';
        html += '</div>';
        html += '</td>';
        return html;
    } else if ( data.type == 55 ) {
        var html = '<td style="width: 10rem;">';
        html += '<input type="hidden" name="type" value="' + type + '">';
        html += '<div class="chart-bar first-break position-relative mb-4" style="background-color: #007AFF; border: 2.5px solid #007AFF;">';
        html += '<p class="chart-bar-text text-center p-1 ps-2 pe-2 mb-0" style="border: 3px solid #007AFF;">' + data.name + '</p>';
        html += '</div>';
        html += '</td>';
        return html;
    }
    return '<td></td>';
}

function append_table_area(data) {
    var valid_icon = '<td class="position-relative">';
    valid_icon += '<form class="valid-form" action="/company/flow/valid/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    valid_icon += '<input type="hidden" name="id" value="' + data.display_id + '">';
    valid_icon += '</form>';
    valid_icon += '<div class="flg-area">';
    if ( data.valid ) {
        valid_icon += '<input id="valid_' + data.display_id + '" type="checkbox" name="valid_flg" value="1" class="d-none" checked>';
    } else {
        valid_icon += '<input id="valid_' + data.display_id + '" type="checkbox" name="valid_flg" value="1" class="d-none">';
    }
    valid_icon += '<label for="valid_' + data.display_id + '" class="d-block position-relative mb-0" style="width: 35px;"></label>';
    valid_icon += '</div>';
    valid_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#valid_on_modal"></button>';
    valid_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#valid_off_modal"></button>';
    valid_icon += '</td>';

    var button = '<a href="/company/flow/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.description + '</p>';
    html += '</td>';
    html += valid_icon;
    html += '<td>';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}