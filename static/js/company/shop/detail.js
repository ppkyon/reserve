$( function() {
    $( document ).on( 'keyup', '#edit_shop_modal #save_shop_form [name=shop_postcode]', function () {
        AjaxZip3.zip2addr( 'shop_postcode', '', 'shop_prefecture', 'shop_address' );
    });

    $( '#edit_shop_modal .modal-body .add-tag-button-area .add-tag-button' ).on( 'click', function() {
        var target = $( this );
        var form_data = new FormData();
        $.ajax({
            'data': form_data,
            'url': $( '#get_company_tag_all_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#company_tag_modal .genre-table tbody' ).empty();
            if ( response.genre_list.length > 0 ) {
                $.each( response.genre_list, function( index, value ) {
                    $( '#company_tag_modal .genre-table tbody' ).append( append_genre_modal(index, value) );
                });
            }

            $( '#company_tag_modal .tag-table tbody' ).empty();
            if ( response.tag_list.length > 0 ) {
                $.each( response.tag_list, function( index, value ) {
                    $( '#company_tag_modal .tag-table tbody' ).append( append_tag_modal(index, value, $( '#edit_shop_modal .modal-body .add-tag-area input' ) ) );
                });
            }

            $( target ).next().trigger( 'click' );
            up_modal();
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#edit_shop_modal .modal-body .add-tag-area .delete-tag-button', function () {
        $( this ).parent().remove();
    });
    $( document ).on( 'click', '#company_tag_modal .table-area tbody button', function () {
        var html = '<div class="position-relative">';
        html += '<label class="tag-label text-center p-1 me-1">' + $( this ).next().val() + '</label>';
        html += '<input type="hidden" name="tag[]" value="' + $( this ).val() + '">';
        html += '<button type="button" value="" class="btn delete-tag-button p-0">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
        html += '</button>';
        html += '</div>';
        $( '#edit_shop_modal #save_shop_form .tag-area .add-tag-area' ).append( html );
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });

    $( '#delete_shop_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        $( '#delete_shop_check_modal .no-button' ).trigger( 'click' );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_shop_form [name=id]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#delete_shop_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( target ).next().trigger( 'click' );
        }).fail( function(){
            $( target ).next().next().trigger( 'click' );
        });
    });

    $( document ).on( 'click', '.setting-area .content .dropdown .edit-button', function () {
        $( '#line_edit_check_modal .yes-button' ).val( $( this ).val() );
        if ( $( '.setting-area .content .input-area #' + $( this ).val() ).val() == '' ) {
            $( '#line_edit_check_modal .yes-button' ).trigger( 'click' );
        } else {
            $( this ).next().trigger( 'click' );
        }
    });
    $( document ).on( 'click', '#line_edit_check_modal .yes-button', function () {
        var text = $( '.setting-area .content .input-area #' + $( this ).val() );
        $( text ).removeClass( 'readonly' );
        $( text ).prop( 'readonly', false );
        $( text ).focus();
        $( '#line_edit_check_modal .no-button' ).trigger( 'click' );
    });
    $( document ).on( 'blur', '.setting-area .content .input-area input[type=text]', function () {
        var target =  $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_shop_form [name=id]' ).val() );
        form_data.append( 'channel_id', $( '.setting-area .content .input-area #channel_id' ).val() );
        form_data.append( 'channel_secret', $( '.setting-area .content .input-area #channel_secret' ).val() );
        form_data.append( 'channel_access_token', $( '.setting-area .content .input-area #channel_access_token' ).val() );
        form_data.append( 'liff_id', $( '.setting-area .content .input-area #liff_id' ).val() );
        form_data.append( 'analytics_id', $( '.setting-area .content .input-area #analytics_id' ).val() );
        form_data.append( 'qrcode_id', $( '.setting-area .content .input-area #qrcode_id' ).val() );
        form_data.append( 'reserve_id', $( '.setting-area .content .input-area #reserve_id' ).val() );
        form_data.append( 'bot_id', $( '.setting-area .content .input-area #bot_id' ).val() );
        form_data.append( 'follow_url', $( '.setting-area .content .input-area #follow_url' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_shop_line_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( target ).addClass( 'readonly' );
            $( target ).prop( 'readonly', true );
        }).fail( function(){
            $( target ).addClass( 'readonly' );
            $( target ).prop( 'readonly', true );
        });
    });
    $( '.setting-area .content .dropdown .copy-button' ).on( 'click', function() {
        var toast = $( this ).parents( '.content' ).find( '.input-area .toast' );
        $( toast ).addClass( 'show' );

        var text = $( this ).parents( '.content' ).find( '.input-area input[type=text]' ).val();
        var $textarea = $('<textarea></textarea>');
        $textarea.text( text );
        $( this ).append( $textarea );
        $textarea.select();
        document.execCommand( 'copy' );
        $textarea.remove();

        setTimeout( function() {
            $( toast ).removeClass( 'show' );
        }, 2500 );
    });
});