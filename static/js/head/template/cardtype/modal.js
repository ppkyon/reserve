function open_template_cardtype_modal(target, number){
    var form_data = new FormData();
    $.ajax({
        'data': form_data,
        'url': $( '#get_head_template_cardtype_list_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '#head_template_cardtype_modal .table-area tbody' ).empty();
        if ( response.length > 0 ) {
            $.each( response, function( index, value ) {
                $( '#head_template_cardtype_modal .table-area tbody' ).append( append_template_cardtype_modal(value) );
            });
            $( '#head_template_cardtype_modal .table-area tbody button' ).val( number );
            $( '#head_template_cardtype_modal .table-area' ).removeClass( 'd-none' );
            $( '#head_template_cardtype_modal .notice-area' ).addClass( 'd-none' );
        } else {
            $( '#head_template_cardtype_modal .table-area' ).addClass( 'd-none' );
            $( '#head_template_cardtype_modal .notice-area' ).removeClass( 'd-none' );
        }
        $( target ).trigger( 'click' );
        up_modal();
    }).fail( function(){
        
    });
}

function append_template_cardtype_modal(data) {
    var type_name = '';
    if ( data.type == 1 ) {
        type_name = 'アナウンス';
    } else if ( data.type == 2 ) {
        type_name = 'ロケーション';
    } else if ( data.type == 3 ) {
        type_name = 'パーソン';
    } else if ( data.type == 4 ) {
        type_name = 'イメージ';
    }

    var button = '<button type="button" class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
    button += '<input type="hidden" value="' + data.display_id + '">';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '';
    if ( data.type == 1 || data.type == 2 ) {
        var image = '';
        $.each( data.item, function( index, value ) {
            if ( index == 0 ) {
                if ( check_empty(value.image_1) ) {
                    image = '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + value.image_1 + '">';
                } else {
                    image = '<img class="content-image me-2" src="' + $( '#env_static_url' ).val() + 'img/image-none.png">';
                }
            }
        });

        html += '<tr>';
        html += '<td class="text-center">';
        html += image;
        html += '</td>';
        html += '<td class="position-relative">';
        html += '<p class="content-title mb-0">' + data.name + '</p>';
        html += '<p class="content-date mb-0">' + created_date + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + type_name + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' +  data.count + '</p>';
        html += '</td>';
        html += '<td>';
        html += button;
        html += '</td>';
        html += '</tr>';
        return html;
    } else if ( data.type == 3 || data.type == 4 ) {
        var image = '';
        $.each( data.item, function( index, value ) {
            if ( index == 0 ) {
                if ( check_empty(value.image) ) {
                    image = '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + value.image + '">';
                } else {
                    image = '<img class="content-image me-2" src="' + $( '#env_static_url' ).val() + 'img/image-none.png">';
                }
            }
        });

        html += '<tr>';
        html += '<td class="text-center">';
        html += image;
        html += '</td>';
        html += '<td class="position-relative">';
        html += '<p class="content-title mb-0">' + data.name + '</p>';
        html += '<p class="content-date mb-0">' + created_date + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + type_name + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.count + '</p>';
        html += '</td>';
        html += '<td>';
        html += button;
        html += '</td>';
        html += '</tr>';
        return html;
    }
}