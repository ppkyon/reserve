function open_rich_menu_modal( target ) {
    var form_data = new FormData();
    $.ajax({
        'data': form_data,
        'url': $( '#get_company_rich_menu_list_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '#company_rich_menu_modal .table-area tbody' ).empty();
        if ( response.length > 0 ) {
            $.each( response, function( index, value ) {
                $( '#company_rich_menu_modal .table-area tbody' ).append( append_rich_menu_modal( value ) );
            });
            $( '#company_rich_menu_modal .table-area' ).removeClass( 'd-none' );
            $( '#company_rich_menu_modal .notice-area' ).addClass( 'd-none' );
        } else {
            $( '#company_rich_menu_modal .table-area' ).addClass( 'd-none' );
            $( '#company_rich_menu_modal .notice-area' ).removeClass( 'd-none' );
        }
        $( target ).next().trigger( 'click' );
    }).fail( function(){
        
    });
}

function append_rich_menu_modal(data){
    var action = '';
    $.each( data.item, function( index, value ) {
        if ( value.type == 1 || value.type == 2 || value.type == 3 || value.type == 4 || value.type == 5 || value.type == 6 || value.type == 7 ) {
            action += '<p class="content-title mb-0">' + value.url + '</p>';
        } else if ( value.type == 8 ) {
            action += '<p class="content-title mb-0">' + value.text + '</p>';
        }
    });

    var image = '';
    if ( check_empty(data.image) ) {
        image = '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + data.image + '">';
    } else {
        image = '<img class="content-image me-2" src="' + $( '#env_static_url' ).val() + 'img/image-none.png">';
    }
    var button = '<button type="button" class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
    button += '<input type="hidden" value="' + data.display_id + '">';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center">';
    html += image;
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += action;
    html += '</td>';
    html += '<td>';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}