
function create_preview() {
    $( '.line-preview .line-preview-content .line-preview-body' ).empty();
    var image = $( '#save_richmessage_form .message-area .template-area' ).children( 'img' ).attr( 'src' );
    if ( check_empty(image) ) {
        var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
        html += '<img src="' + image + '">';
        html += '</div>';
        $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
    }
}

function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_richmessage_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( check_empty(response.image) ) {
            var image = $( '#env_media_url' ).val() + response.image;
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<img src="' + image + '">';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
    }).fail( function(){

    });
}