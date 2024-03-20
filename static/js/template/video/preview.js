
function create_preview() {
    $( '.line-preview .line-preview-content .line-preview-body' ).empty();
    var video = $( '#save_video_form .video-display-area video' ).attr( 'src' );
    if ( check_empty(video) ) {
        var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
        html += '<video src="' + video + '" controls>';
        html += '</div>';
        $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
    }
}

function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_video_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( check_empty(response.video) ) {
            var video = $( '#env_media_url' ).val() + response.video;
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<video src="' + video + '" controls>';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
    }).fail( function(){

    });
}