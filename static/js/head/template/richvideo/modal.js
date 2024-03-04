function open_template_richvideo_modal(target, number){
    var form_data = new FormData();
    $.ajax({
        'data': form_data,
        'url': $( '#get_head_template_richvideo_list_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '#head_template_richvideo_modal .table-area tbody' ).empty();
        if ( response.length > 0 ) {
            $.each( response, function( index, value ) {
                $( '#head_template_richvideo_modal .table-area tbody' ).append( append_template_richvideo_modal(value) );
            });
            $( '#head_template_richvideo_modal .table-area tbody button' ).val( number );
            $( '#head_template_richvideo_modal .table-area' ).removeClass( 'd-none' );
            $( '#head_template_richvideo_modal .notice-area' ).addClass( 'd-none' );
        } else {
            $( '#head_template_richvideo_modal .table-area' ).addClass( 'd-none' );
            $( '#head_template_richvideo_modal .notice-area' ).removeClass( 'd-none' );
        }
        $( target ).trigger( 'click' );
    }).fail( function(){
        
    });
}

function append_template_richvideo_modal(data) {
    var size = '';
    if ( data.video_size >= 1000000 ) {
        size = Math.ceil( data.video_size / 1000000 ) + 'MB';
    } else if ( data.video_size >= 1000 ) {
        size = Math.ceil( data.video_size / 1000 ) + 'KB';
    } else {
        size = data.video_size + 'B';
    }
    var button = '<button type="button" class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
    button += '<input type="hidden" value="' + data.display_id + '">';
    button += '<input type="hidden" value="' + data.name + '">';

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
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}