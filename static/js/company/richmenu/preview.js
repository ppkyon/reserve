function action_preview() {
    create_preview();
    $( '#save_richmenu_form [name=menu_type]' ).on( 'change', function() {
        create_preview();
    });
    $( '#save_richmenu_form [name=menu_flg]' ).on( 'change', function() {
        create_preview();
    });
    $( '#save_richmenu_form [name=menu_text]' ).on( 'mouseup keyup', function() {
        create_preview();
    });
}
function create_preview() {
    $( '.line-preview .line-preview-content .line-preview-body' ).empty();
    var image = $( '#save_richmenu_form .template-area' ).children( 'img' ).attr( 'src' );
    var text = 'メニュー';
    if ( $( '#save_richmenu_form [name=menu_type]:checked' ).val() == '1' && check_empty($( '#save_richmenu_form [name=menu_text]' ).val()) ) {
        text = $( '#save_richmenu_form [name=menu_text]' ).val();
    }
    if ( check_empty(image) ) {
        var html = '<div class="line-preview-richmenu">';
        html += '<img src="' + image + '" class="w-100">';
        if ( $( '#save_richmenu_form [name=menu_flg]:checked' ).val() == '1' ) {
            html += '<div class="line-preview-menu position-relative text-center p-1">';
            html += '<span class="mb-0">' + text + '</span>';
            html += '<i class="bx bxs-down-arrow"></i>';
            html += '</div>';
        }
        html += '</div>';
        $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
    }
}
function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_richmenu_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( check_empty(response.image) ) {
            var text = 'メニュー';
            if ( response.menu_type == 1 && check_empty(response.menu_text) ) {
                text = response.menu_text;
            }

            var html = '<div class="line-preview-richmenu">';
            html += '<img src="' + $( '#env_media_url' ).val() + response.image + '" class="w-100">';
            if ( response.menu_flg ) {
                html += '<div class="line-preview-menu position-relative text-center p-1">';
                html += '<span class="mb-0">' + text + '</span>';
                html += '<i class="bx bxs-down-arrow"></i>';
                html += '</div>';
            }
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
    }).fail( function(){

    });
}