function append_input_area() {
    var html = '<div class="input-area">';
    html += '<input type="hidden" name="number" value="' + ( $( '#save_text_form [name=number]' ).length + 1 ) + '">';
    html += '<div class="message-area">';
    html += '<div class="row mb-1">';
    html += '<div class="col-12">';
    html += '<input type="hidden" name="message_type_' + ( $( '#save_text_form [name=number]' ).length + 1 ) + '" value="1">';
    html += '<div class="text-area">';
    html += '<div name="text_' + ( $( '#save_text_form [name=number]' ).length + 1 ) + '" class="false-textarea pt-2 pb-2 ps-5 pe-3" contenteditable="true">';
    html += '</div>';
    html += '<img class="emoji-mark" src="' + $( '#env_static_url' ).val() + 'img/icon/emoji.png">';
    html += '</div>';
    html += '<div class="image-area d-none pt-2 pb-2 ps-3 pe-3"></div>';
    html += '<div class="video-area d-none pt-2 pb-2 ps-3 pe-3"></div>';
    html += '<div class="chart-area d-none pt-2 pb-2 ps-3 pe-3"></div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="action-button-area">';
    html += '<div class="row mb-4">';
    html += '<div class="col-12">';
    html += '<div class="action-area d-flex justify-content-between align-items-center">';
    html += '<div class="menu-area d-flex justify-content-between align-items-center">';
    html += '<div class="dropdown input-template-dropdown d-inline-block p-0">';
    html += '<button class="btn position-relative" data-bs-toggle="dropdown">';
    html += '<span>テンプレートを使用する</span>';
    html += '</button>';
    html += '<div class="dropdown-menu">';
    html += '<button type="button" value="0" class="btn dropdown-item fw-bold text-center p-1">テキスト</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_text_modal"></button>';
    html += '<button type="button" value="1" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">動画</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
    html += '<button type="button" value="2" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">リッチメッセージ</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_richmessage_modal"></button>';
    html += '<button type="button" value="3" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">リッチビデオ</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_richvideo_modal"></button>';
    html += '<button type="button" value="4" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">カードタイプ</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_cardtype_modal"></button>';
    html += '</div>';
    html += '</div>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#template_modal"></button>';
    html += '<button type="button" class="btn name-button position-relative">';
    html += '<span>応募者の登録名</span>';
    html += '</button>';
    html += '<div class="dropdown input-action-dropdown inline-block p-0" style="width: 120px;">';
    html += '<button class="btn text-center position-relative w-100" data-bs-toggle="dropdown">';
    html += '<p class="mb-0">アクション</p>';
    html += '</button>';
    html += '<div class="dropdown-menu">';
    html += '<button type="button" value="line" class="btn  dropdown-item fw-bold text-center p-1">公式LINE名</button>';
    html += '<button type="button" value="company" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">企業名</button>';
    html += '<button type="button" value="name" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">担当者名</button>';
    html += '<button type="button" value="phone" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">担当者電話番号</button>';
    html += '</div>';
    html += '</div>';
    html += '<button type="button" class="btn video-button">';
    html += '<i class="bx bx-play-circle mt-1"></i>';
    html += '</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#video_upload_modal"></button>';
    html += '<button type="button" class="btn image-button">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/image.svg">';
    html += '</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#image_upload_modal"></button>';
    html += '</div>';
    html += '<div class="delete-area ms-auto">';
    html += '<button type="button" class="btn delete-button" value="' + ( $( '#save_text_form [name=number]' ).length + 1 ) + '">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_item_check_modal"></button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}



function append_table_area(data) {
    var image = $( '#env_static_url' ).val() + 'img/image-none.png';
    var text = '-';
    $.each( data.item, function( index, value ) {
        if ( index == 0 ) {
            if ( check_empty(value.image) ) {
                image = $( '#env_media_url' ).val() + value.image;
                text = '画像メッセージ';
            } else if ( check_empty(value.video) ) {
                image = $( '#env_media_url' ).val() + value.video_thumbnail;
                text = '動画メッセージ';
            } else if ( check_empty(value.text) ) {
                text = value.text;
            }
        }
    });

    var button = '<a href="/head/template/text/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center position-relative" style="width: 100px;">';
    html += '<div class="d-flex align-items-center">';
    html += '<img class="content-image me-2" src="' + image + '">';
    html += '<p class="content-text text-start">' + text + '</p>';
    html += '</div>';
    html += '<p class="content-date mb-0" style="left: 5rem;">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}