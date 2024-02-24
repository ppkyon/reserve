
function create_preview() {
    $( '.line-preview .line-preview-content .line-preview-body' ).empty();

    var html = '';
    $( '#save_text_form .message-area' ).each( function( index, value ) {
        var text = display_textarea_replace($( this ).find( '.text-area .false-textarea' ).html());
        if ( check_empty(text) ) {
            html += '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<div class="line-preview-chat-box p-2">';
            html += '<div class="mb-0">' + text + '</div>';
            html += '</div>';
            html += '</div>';
        }
        var image = $( this ).find( '.image-area img' ).attr( 'src' );
        if ( check_empty(image) ) {
            html += '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<img src="' + image + '">';
            html += '</div>';
        }
        var video = $( this ).find( '.video-area video' ).attr( 'src' );
        if ( check_empty(video) ) {
            html += '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<video src="' + video + '" controls>';
            html += '</div>';
        }
    });

    $( '.line-preview .line-preview-content .line-preview-body' ).append(html);
}

function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_text_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        $.each( response.item, function( index, value ) {
            if ( check_empty(value.text) ) {
                var text = display_textarea_replace(value.text);
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<div class="line-preview-chat-box p-2">';
                html += '<div class="mb-0">' + text + '</div>';
                html += '</div>';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
            if ( check_empty(value.image) ) {
                var image = $( '#env_media_url' ).val() + value.image;
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<img src="' + image + '">';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
            if ( check_empty(value.video) ) {
                var video = $( '#env_media_url' ).val() + value.video;
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<video src="' + video + '" controls>';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
        });
    }).fail( function(){

    });
}

function display_textarea_replace(text) {
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/display-name.png" class="ms-1 me-1">', '【応募者の登録名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/line-name.png" class="ms-1 me-1">', '【公式LINE名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/company-name.png" class="ms-1 me-1">', '【企業名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-name.png" class="ms-1 me-1">', '【担当者名】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-phone.png" class="ms-1 me-1">', '【担当者電話番号】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/interview-date.png" class="ms-1 me-1">', '【面接日時】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' );
    text = text.replaceAll( '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' );
    text = text.replaceAll( 'font-size: 12px;', '' )
    text = text.replaceAll( 'font-size: 12.8px;', '' );
    return text;
}