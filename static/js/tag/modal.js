$( function() {
    $( document ).on( 'click', '#tag_modal .genre-table tbody tr', function () {
        $( this ).parent().find( 'tr' ).each( function( index, value ) {
            $( this ).css( 'background-color', '#FFF' );
            $( this ).removeClass( 'active' );
        });
        $( this ).css( 'background-color', '' );
        $( this ).addClass( 'active' );

        $( '#tag_modal .tag-table tbody' ).css( 'opacity', '0' );
        $( '.table-loader-area' ).css( 'opacity', '1' );
        
        var form_data = new FormData();
        form_data.append( 'id', $( this ).children( 'input' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_tag_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#tag_modal .tag-table tbody' ).empty();
                $.each( response, function( index, value ) {
                    $( '#tag_modal .tag-table tbody' ).append( append_tag_modal( index, value, $( '#edit_shop_modal .modal-body .add-tag-area input' ) ) );
                });
                $( '#tag_modal .tag-table tbody' ).css( 'opacity', '1' );
                $( '.table-loader-area' ).css( 'opacity', '0' );
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#tag_modal .tag-table tbody' ).css( 'opacity', '1' );
                $( '.table-loader-area' ).css( 'opacity', '0' );
            }, 750 );
        });
    });
    $( document ).on( 'click', '#tag_modal .tag-table tbody tr', function () {
        $( this ).parent().find( 'tr' ).each( function( index, value ) {
            $( this ).css( 'background-color', '#FFF' );
            $( this ).removeClass( 'active' );
        });
        $( this ).css( 'background-color', '' );
        $( this ).addClass( 'active' );
    });
});

function append_genre_modal(index, data) {
    var favorite_icon = '';
    if ( data.favorite_flg ) {
        var html = '<td>';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
        html += '</td>';
        favorite_icon += html;
    } else {
        var html = '<td>';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '</td>';
        favorite_icon += html;
    }

    if ( index == 0 ) {
        var html = '<tr class="active" style="height: auto; cursor: pointer;">';
        html += '<input type="hidden" value="' + data.display_id + '">';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<i class="bx bx-folder folder-icon me-1"></i>';
        html += '<p class="content-title mb-0">' + data.name + '(' + data.count + ')</p>';
        html += '</div>';
        html += '</td>';
        html += favorite_icon;
        html += '</tr>';
        return html;
    } else {
        var html = '<tr style="height: auto; background-color: #FFF; cursor: pointer;">';
        html += '<input type="hidden" value="' + data.display_id + '">';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<i class="bx bx-folder folder-icon me-1"></i>';
        html += '<p class="content-title mb-0">' + data.name + '(' + data.count + ')</p>';
        html += '</div>';
        html += '</td>';
        html += favorite_icon;
        html += '</tr>';
        return html;
    }
}
function append_tag_modal(index, data, input) {
    var input_flg = true;
    $( input ).each( function( index, value ) {
        if ( data.display_id == $( this ).val() ) {
            input_flg = false;
        }
    });

    var favorite_icon = '';
    if ( data.favorite_flg ) {
        var html = '<td>';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
        html += '</td>';
        favorite_icon += html;
    } else {
        var html = '<td>';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '</td>';
        favorite_icon += html;
    }
    var select = '';
    if ( input_flg ) {
        var html = '<td>';
        html += '<button type="button" value="' + data.display_id + '"class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
        html += '<input type="hidden" value="' + data.name + '">';
        html += '</td>';
        select = html;
    } else {
        select = '<td></td>';
    }
    if ( index == 0 ) {
        var html = '<tr class="active" style="height: auto; cursor: pointer;">';
        html += '<input type="hidden" value="' + data.display_id + '">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.name + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.display_date + '</p>';
        html += '</td>';
        html += favorite_icon;
        html += select;
        html += '</tr>';
        return html;
    } else {
        var html = '<tr style="height: auto; background-color: #FFF; cursor: pointer;">';
        html += '<input type="hidden" value="' + data.display_id + '">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.name + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.display_date + '</p>';
        html += '</td>';
        html += favorite_icon;
        html += select;
        html += '</tr>';
        return html;
    }
}