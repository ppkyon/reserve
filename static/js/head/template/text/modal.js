function open_template_text_modal(target, number){
    var form_data = new FormData();
    $.ajax({
        'data': form_data,
        'url': $( '#get_head_template_text_list_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '#head_template_text_modal .table-area tbody' ).empty();
        if ( response.length > 0 ) {
            $.each( response, function( index, value ) {
                $( '#head_template_text_modal .table-area tbody' ).append( append_template_text_modal(value) );
            });
            $( '#head_template_text_modal .table-area tbody button' ).val( number );
            $( '#head_template_text_modal .table-area' ).removeClass( 'd-none' );
            $( '#head_template_text_modal .notice-area' ).addClass( 'd-none' );
        } else {
            $( '#head_template_text_modal .table-area' ).addClass( 'd-none' );
            $( '#head_template_text_modal .notice-area' ).removeClass( 'd-none' );
        }
        $( target ).trigger( 'click' );
        up_modal();
    }).fail( function(){
        
    });
}

function append_template_text_modal(data) {
    if ( data.item.message_type == 4 ) {
        return '';
    }

    var image = $( '#env_static_url' ).val() + 'img/image-none.png';
    var text = '-';
    if ( check_empty(data.item.image) ) {
        image = $( '#env_media_url' ).val() + data.item.image;
        text = '画像メッセージ';
    } else if ( check_empty(data.item.video) ) {
        image = $( '#env_media_url' ).val() + data.item.video_thumbnail;
        text = '動画メッセージ';
    } else if ( check_empty(data.item.text) ) {
        text = display_textarea_replace(data.item.text);
    }

    var target = location.search.slice( location.search.indexOf( '=' ) + 1 );
    var button = '';
    if ( target != data.display_id ) {
        button += '<button type="button" class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
        button += '<input type="hidden" value="' + data.display_id + '">';
    }

    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center position-relative" style="width: 100px;">';
    html += '<div class="d-flex align-items-center">';
    html += '<img class="content-image me-2" src="' + image + '">';
    html += '<div class="content-text text-start">' + text + '</div>';
    html += '</div>';
    html += '<p class="content-date mb-0" style="left: 5rem;">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '</td>';
    html += '<td>';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}

function display_textarea_replace(text) {
    text = text.replaceAll( 'font-size: 12px;', '' )
    text = text.replaceAll( 'font-size: 12.8px;', '' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/display-name.png" class="ms-1 me-1">', '【応募者の登録名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/line-name.png" class="ms-1 me-1">', '【公式LINE名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/company-name.png" class="ms-1 me-1">', '【企業名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-name.png" class="ms-1 me-1">', '【担当者名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-phone.png" class="ms-1 me-1">', '【担当者電話番号】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/reserve-date.png" class="ms-1 me-1">', '【予約日時】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' );
    return text;
}