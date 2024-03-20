function append_display_area() {
    var html = '<div class="display-area d-flex flex-column position-relative p-1 mb-3">';
    html += '<p class="input-label fw-bold mb-2">リンクURL</p>';
    html += '<input type="url" name="url" class="input-text input-select ps-2 pe-2" placeholder="URLを入力" required>';
    html += '</div>';
    html += '<div class="display-area d-flex flex-column position-relative p-1 mb-3">';
    html += '<p class="input-label fw-bold mb-2">アクションボタンテキスト</p>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="detail_text" class="ps-4 mb-0">詳細はこちら</label>';
    html += '<input type="radio" id="detail_text" name="text" value="0" class="input-radio" checked>';
    html += '<label for="detail_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="install_text" class="ps-4 mb-0">インストールする</label>';
    html += '<input type="radio" id="install_text" name="text" value="1" class="input-radio">';
    html += '<label for="install_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="buy_text" class="ps-4 mb-0">購入する</label>';
    html += '<input type="radio" id="buy_text" name="text" value="2" class="input-radio">';
    html += '<label for="buy_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="reserve_text" class="ps-4 mb-0">予約する</label>';
    html += '<input type="radio" id="reserve_text" name="text" value="3" class="input-radio">';
    html += '<label for="reserve_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="app_text" class="ps-4 mb-0">応募する</label>';
    html += '<input type="radio" id="app_text" name="text" value="4" class="input-radio">';
    html += '<label for="app_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="request_text" class="ps-4 mb-0">申し込む</label>';
    html += '<input type="radio" id="request_text" name="text" value="5" class="input-radio">';
    html += '<label for="request_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="join_text" class="ps-4 mb-0">参加する</label>';
    html += '<input type="radio" id="join_text" name="text" value="6" class="input-radio">';
    html += '<label for="join_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="vote_text" class="ps-4 mb-0">投票する</label>';
    html += '<input type="radio" id="vote_text" name="text" value="7" class="input-radio">';
    html += '<label for="vote_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="search_text" class="ps-4 mb-0">お店を探す</label>';
    html += '<input type="radio" id="search_text" name="text" value="8" class="input-radio">';
    html += '<label for="search_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="contact_text" class="ps-4 mb-0">お問い合わせはこちら</label>';
    html += '<input type="radio" id="contact_text" name="text" value="9" class="input-radio">';
    html += '<label for="contact_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="claim_text" class="ps-4 mb-0">資料を請求する</label>';
    html += '<input type="radio" id="claim_text" name="text" value="10" class="input-radio">';
    html += '<label for="claim_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="video_text" class="ps-4 mb-0">ほかの動画をみる</label>';
    html += '<input type="radio" id="video_text" name="text" value="11" class="input-radio">';
    html += '<label for="video_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="custom_text" class="ps-4 mb-0">';
    html += '<input type="text" name="custom" class="input-text input-select ps-2 pe-2" placeholder="テキストを入力" maxlength="20">';
    html += '</label>';
    html += '<input type="radio" id="custom_text" name="text" value="12" class="input-radio">';
    html += '<label for="custom_text" class="input-radio-mark"></label>';
    html += '</div>';
    html += '</div>';
    $( '#save_richvideo_form .display-area-wrap' ).append( html );
}

function append_table_area(data) {
    var size = '';
    if ( data.video_size >= 1000000 ) {
        size = Math.ceil( data.video_size / 1000000 ) + 'MB';
    } else if ( data.video_size >= 1000 ) {
        size = Math.ceil( data.video_size / 1000 ) + 'KB';
    } else {
        size = data.video_size + 'B';
    }
    var button = '<a href="/template/richvideo/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center">';
    html += '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + data.video_thumbnail + '">';
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.video_display_time + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + size + '</p>';
    html += '</td>';
    html += '<td>';
    if ( data.use_flg ) {
        html += '<p class="content-title mb-0">使用中</p>';
    } else {
        html += '<p class="content-title mb-0">-</p>';
    }
    html += '</td>';
    html += '<td>';
    html += '<form id="favorite_form" action="/template/richvideo/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += '</form>';
    if ( data.favorite_flg ) {
        html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    } else {
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    }
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_on_modal"></button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_off_modal"></button>';
    html += '</td>';
    html += '<td>';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}