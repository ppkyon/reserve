$( function() {
    $( document ).on( 'click', '.message-area .action-area .dropdown .dropdown-menu button', function () {
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this ).next(), $( this ).val() );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this ).next(), $( this ).val() );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this ).next(), $( this ).val() );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this ).next(), $( this ).val() );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this ).next(), $( this ).val() );
        }
    });
    $( document ).on( 'click', '#template_text_modal .table-area tbody button', function () {
        var id = $( this ).next().val();
        create_text_preview(id);

        $( '.line-preview .line-preview-content .line-preview-header' ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
        $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );

        $( '#template_text_modal .modal-header button' ).trigger( 'click' );
        $( '#template_check_modal .yes-button' ).val(id);
        $( '#template_check_modal .yes-button' ).next().val( 'text' );
        $( '#get_cardtype_preview_url' ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#template_video_modal .table-area tbody button', function () {
        var id = $( this ).next().val();
        create_video_preview(id);

        $( '.line-preview .line-preview-content .line-preview-header' ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
        $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );

        $( '#template_video_modal .modal-header button' ).trigger( 'click' );
        $( '#template_check_modal .yes-button' ).val(id);
        $( '#template_check_modal .yes-button' ).next().val( 'video' );
        $( '#get_cardtype_preview_url' ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richmessage_modal .table-area tbody button', function () {
        var id = $( this ).next().val();
        create_rich_message_preview(id);

        $( '.line-preview .line-preview-content .line-preview-header' ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
        $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );

        $( '#template_richmessage_modal .modal-header button' ).trigger( 'click' );
        $( '#template_check_modal .yes-button' ).val(id);
        $( '#template_check_modal .yes-button' ).next().val( 'richmessage' );
        $( '#get_cardtype_preview_url' ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richvideo_modal .table-area tbody button', function () {
        var id = $( this ).next().val();
        create_rich_video_preview(id);

        $( '.line-preview .line-preview-content .line-preview-header' ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
        $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );

        $( '#template_richvideo_modal .modal-header button' ).trigger( 'click' );
        $( '#template_check_modal .yes-button' ).val(id);
        $( '#template_check_modal .yes-button' ).next().val( 'richvideo' );
        $( '#get_cardtype_preview_url' ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#template_cardtype_modal .table-area tbody button', function () {
        var id = $( this ).next().val();
        create_card_type_preview(id);

        $( '.line-preview .line-preview-content .line-preview-header' ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
        $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );

        $( '#template_cardtype_modal .modal-header button' ).trigger( 'click' );
        $( '#template_check_modal .yes-button' ).val(id);
        $( '#template_check_modal .yes-button' ).next().val( 'cardtype' );
        $( '#get_cardtype_preview_url' ).next().trigger( 'click' );
        up_modal();
    });

    $( '#template_check_modal .yes-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var form_data = new FormData();
        form_data.append( 'user_id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'id', $( this ).val() );
        form_data.append( 'type', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_template_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        });
    });
    $( '#template_check_modal .no-button' ).on( 'click', function() {
        window.location.reload();
    });
    $( '#template_check_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#template_check_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#template_check_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#template_check_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });

    $( '.message-area .action-area .name-button' ).on( 'click', function() {
        var send_message = $( '#send_' + $( '#send_id' ).val() + '_form [name=message]' );
        var position = $( send_message ).get(0).selectionStart;
        var before = $( send_message ).val().substr( 0, position );
        var after = $( send_message ).val().substr( position );
        $( send_message ).focus();
        $( send_message ).val( before + $( '#line_message_user_name' ).text() );
        $( send_message ).val( $( send_message ).val() + after );

        $( send_message ).get(0).focus();
        $( send_message ).get(0).setSelectionRange( position + $( '#line_message_user_name' ).text().length, position + $( '#line_message_user_name' ).text().length );
    });

    $( '.message-area .action-area .image-button' ).on( 'click', function() {
        $( '#upload_image_modal_button' ).trigger( 'click' );
    });
    $( '#upload_image_modal .send-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.button-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        $( this ).parents( '.modal' ).find( '.drop-zone' ).removeClass( 'd-none' );
        $( this ).parents( '.modal' ).find( '.drop-display-zone' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '#login_shop_id' ).val() );
        form_data.append( 'id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'image', $( '#upload_image_modal [name=upload_image]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_image_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        });
    });
    $( '#upload_image_modal .cancel-button' ).on( 'click', function() {
        $( '#upload_image_modal .drop-zone' ).removeClass( 'd-none' );
        $( '#upload_image_modal .drop-display-zone' ).addClass( 'd-none' );
        $( '#upload_image_modal .send-button' ).addClass( 'd-none' );

        $( '#upload_image_modal .drop-display-zone img' ).attr( 'src', '' );
        $( '#upload_image_modal [name=upload_image]' ).val( '' );
        $( '#upload_image_modal [name=image_file]' ).val( '' );

        $( this ).next().trigger( 'click' );
    });

    $( '.message-area .action-area .video-button' ).on( 'click', function() {
        $( '#upload_video_modal_button' ).trigger( 'click' );
    });
    $( '#upload_video_modal .send-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.button-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        $( this ).parents( '.modal' ).find( '.drop-zone' ).removeClass( 'd-none' );
        $( this ).parents( '.modal' ).find( '.drop-display-zone' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '#login_shop_id' ).val() );
        form_data.append( 'id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'video', $( '#upload_video_modal [name=upload_video]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_video_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                window.location.reload();
            }, 750 );
        });
    });
    $( '#upload_video_modal .cancel-button' ).on( 'click', function() {
        $( '#upload_video_modal .drop-zone' ).removeClass( 'd-none' );
        $( '#upload_video_modal .drop-display-zone' ).addClass( 'd-none' );
        $( '#upload_video_modal .send-button' ).addClass( 'd-none' );

        $( '#upload_video_modal .drop-display-zone video' ).attr( 'src', '' );
        $( '#upload_video_modal [name=upload_video]' ).val( '' );
        $( '#upload_video_modal [name=video_file]' ).val( '' );

        $( this ).next().trigger( 'click' );
    });
    $( '#video_file' ).on( 'change', function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'video_file', $( '#video_file' )[0].files[0] );
        $.ajax({
            'data': form_data,
            'url': $( '#video_check_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#video_check_modal .video-area video' ).attr( 'src', $( '#env_media_url' ).val() + response.message['video'] );
            $( '#video_check_modal .yes-button' ).val( response.message['display_id'] );
            $( '#video_check_modal .no-button' ).val( response.message['display_id'] );
            $( '#video_check_modal_button' ).trigger( 'click' );
        }).fail( function(){
            $( '#video_check_modal .video-area video' ).attr( 'src', '' );
            $( '#video_check_modal .yes-button' ).val( '' );
            $( '#video_check_modal .no-button' ).val( '' );
        });
    });
    $( '#video_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#video_send_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            window.location.reload();
        }).fail( function(){
            window.location.reload();
        });
    });
    $( '#video_check_modal .no-button' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#video_delete_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            window.location.reload();
        }).fail( function(){
            window.location.reload();
        });
    });

    $( '#line_message_send_button' ).on( 'click', function() {
        if ( $( '#send_' + $( '#send_id' ).val() + '_form [name=message]' ).val() ) {
            $( this ).prop( 'disabled', true );
            var form_data = new FormData();
            form_data.append( 'id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
            form_data.append( 'message', $( '#send_' + $( '#send_id' ).val() + '_form [name=message]' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#send_' + $( '#send_id' ).val() + '_form' ).attr( 'action' ),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                window.location.reload();
            }).fail( function(){
                window.location.reload();
            });
        }
    });
});

function create_text_preview( id ) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_text_preview_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        $.each( response.item, function( index, value ) {
            if ( value.text != '' && value.text != undefined ) {
                var text = display_textarea_replace(value.text);
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<div class="line-preview-chat-box p-2">';
                html += '<p class="mb-0">' + text + '</p>';
                html += '</div>';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
            if ( value.image != '' && value.image != undefined ) {
                var image = $( '#env_media_url' ).val() + value.image;
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<img src="' + image + '">';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
            if ( value.video != '' && value.video != undefined ) {
                var video = $( '#env_media_url' ).val() + value.video;
                var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
                html += '<video src="' + video + '" controls>';
                html += '</div>';
                $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            }
        });
        
        $( '#template_check_modal .modal-title' ).text( 'メッセージテンプレート【' + response.name + '】を送信してもよろしいですか?' );
    }).fail( function(){

    });
}
function create_video_preview( id ) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_video_preview_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( response.video != '' && response.video != undefined ) {
            var video = $( '#env_media_url' ).val() + response.video;
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<video src="' + video + '" controls>';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
        $( '#template_check_modal .modal-title' ).text( '動画テンプレート【' + response.name + '】を送信してもよろしいですか?' );
    }).fail( function(){

    });
}
function create_rich_message_preview( id ) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_richmessage_preview_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( response.image != '' && response.image != undefined ) {
            var image = $( '#env_media_url' ).val() + response.image;
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<img src="' + image + '">';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
        $( '#template_check_modal .modal-title' ).text( 'リッチメッセージ【' + response.name + '】を送信してもよろしいですか?' );
    }).fail( function(){

    });
}
function create_rich_video_preview( id ) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_richvideo_preview_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( response.video != '' && response.video != undefined ) {
            var video = $( '#env_media_url' ).val() + response.video;
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<video src="' + video + '" controls>';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        }
        $( '#template_check_modal .modal-title' ).text( 'リッチビデオメッセージ【' + response.name + '】を送信してもよろしいですか?' );
    }).fail( function(){

    });
}
function create_card_type_preview( id ) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_cardtype_preview_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        if ( response != null && response != undefined && response != '' ) {
            $( '.line-preview .line-preview-content .line-preview-body' ).empty();
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<div class="position-relative overflow-hidden w-100">';
            html += '<ul class="preview-slide p-0">';
            var data = '';
            $.each( response.item, function( index, value ) {
                var number = value.number;
                if ( number != 10 ) {
                    if ( response.type == 1 ) {
                        html += append_card_type_preview_announce(value);
                    } else if ( response.type == 2 ) {
                        html += append_card_type_preview_location(value);
                    } else if ( response.type == 3 ) {
                        html += append_card_type_preview_person(value);
                    } else if ( response.type == 4 ) {
                        html += append_card_type_preview_image(value);
                    }
                }
            });
            html += '</ul></div></div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
        
            append_card_type_preview_more(response.more);
        }
        $( '#template_check_modal .modal-title' ).text( 'カードタイプメッセージ【' + response.name + '】を送信してもよろしいですか?' );
        slide_preview();
    }).fail( function(){

    });
}
function append_card_type_preview_location(data) {
    var image = '';
    if ( data.image_count == '1' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/part/card-type-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        image += '<div id="display_image_area_1" class="card-type-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="one card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '</div>'
    } else if ( data.image_count == '2' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/part/card-type-half-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/part/card-type-half-b.png';
        if ( data.image_2 != '' ) {
            if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + data.image_2;
            } else {
                image_b = data.image_2;
            }
        }
        image += '<div id="display_image_area_2" class="card-type-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '</div>'
    } else if ( data.image_count == '3' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/part/card-type-half-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/part/card-type-b.png';
        if ( data.image_2 != '' ) {
            if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + data.image_2;
            } else {
                image_b = data.image_2;
            }
        }
        var image_c = $( '#env_static_url' ).val() + 'img/part/card-type-c.png';
        if ( data.image_3 != '' ) {
            if ( data.image_3.indexOf( 'uploads' ) !== -1 ) {
                image_c = $( '#env_media_url' ).val() + data.image_3;
            } else {
                image_c = data.image_3;
            }
        }
        image += '<div id="display_image_area_1" class="card-type-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two flex-column position-relative">';
        image += '<div class="three card-type-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '<div class="three card-type-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="c">';
        image += '<span style="background-image: url( ' + image_c + ' );"></span>';
        image += '</div>';
        image += '</div>';
        image += '</div>'
    }
    var title = '';
    if ( data.title == '' ) {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">' + data.title + '</p>';
    }
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var place = '';
    if ( data.place_flg ) {
        place += '<p id="display_place_' + data.number + '" class="place d-flex align-items-center mb-1">'
        place += '<img src="/static/img/icon/map.png" class="me-1">'
        if ( data.place == '' ) {
            place += '<span>住所を入力</span>'
        } else {
            place += '<span>' + data.place + '</span>'
        }
        place += '</p>';
    }
    var plus = '';
    if ( data.plus_flg ) {
        var icon = '';
        if ( data.plus_type == 1 ) {
            icon = '<img src="/static/img/icon/time.png" class="me-1">';
        } else if ( data.plus_type == 2 ) {
            icon = '<img src="/static/img/icon/coin.png" class="me-1">';
        }
        if ( data.plus == '' ) {
            plus = '<p id="display_plus_' + data.number + '" class="plus d-flex align-items-center mb-0">' + icon + '<span>追加情報を入力</span></p>';
        } else {
            plus = '<p id="display_plus_' + data.number + '" class="plus d-flex align-items-center mb-0">' + icon + '<span>' + data.plus + '</span></p>';
        }
    }
    var action1 = '';
    if ( data.action_flg_1 ) {
        if ( data.action_label_1 == '' ) {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_1 + '</button>';
        }
    }
    var action2 = '';
    if ( data.action_flg_2 ) {
        if ( data.action_label_2 == '' ) {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_2 + '</button>';
        }
    }
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="card-type-area" style="height: auto;">';
    html += '<div class="card-type-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="card-type-body-area p-2">' + title + place + plus + '</div>';
    html += '<div class="card-type-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}
function append_card_type_preview_person(data) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/part/card-type-person-default.png );"></span>';
    if ( data.image != '' ) {
        if ( data.image.indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + data.image + '"></span>';
        }
    }
    var image_area = '<div id="display_image_area_' + data.number + '" class="card-type-image-area d-flex flex-row position-relative w-100 pt-3 ps-4 pe-4"><div class="person card-type-image-item position-relative" style="padding-bottom: 7.5rem;"><input type="hidden" value="account">' + image + '</div></div>';
    var name = '';
    if ( data.name == '' ) {
        name = '<p id="display_name_' + data.number + '" class="name mb-1">名前を入力</p>';
    } else {
        name = '<p id="display_name_' + data.number + '" class="name mb-1">' + data.name + '</p>';
    }
    var tag1 = '';
    if ( data.tag_flg_1 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_1 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_1 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_1 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_1 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_1 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_1 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_1 == '' ) {
            tag1 = '<label id="display_tag_1_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag1 = '<label id="display_tag_1_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_1 + '</label>';
        }
    }
    var tag2 = '';
    if ( data.tag_flg_2 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_2 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_2 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_2 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_2 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_2 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_2 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_2 == '' ) {
            tag2 = '<label id="display_tag_2_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag2 = '<label id="display_tag_2_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_2 + '</label>';
        }
    }
    var tag3 = '';
    if ( data.tag_flg_3 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_3 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_3 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_3 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_3 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_3 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_3 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_3 == '' ) {
            tag3 = '<label id="display_tag_3_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag3 = '<label id="display_tag_3_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_3 + '</label>';
        }
    }
    var description = '';
    if ( data.description_flg ) {
        if ( data.description == '' ) {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">' + data.description + '</p>';
        }
    }
    var action1 = '';
    if ( data.action_flg_1 ) {
        if ( data.action_label_1 == '' ) {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_1 + '</button>';
        }
    }
    var action2 = '';
    if ( data.action_flg_2 ) {
        if ( data.action_label_2 == '' ) {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_2 + '</button>';
        }
    }
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="card-type-area" style="height: auto;">';
    html += '<div class="card-type-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
    html += '</div>';
    html += '<div class="card-type-body-area p-2">' + name + '<p class="text-center mb-0">' + tag1 + tag2 + tag3 + '</p>' + description + '</div>';
    html += '<div class="card-type-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}
function append_card_type_preview_image(data) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/part/card-type-image-default.png );"></span>';
    if ( data.image != '' ) {
        if ( data.image.indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + data.image + '"></span>';
        }
    }
    var image_area = '<div id="display_image_area_' + data.number + '" class="card-type-image-area d-flex flex-row position-relative w-100">';
    image_area += '<div class="one card-type-image-item position-relative" style="padding-bottom: 10rem;"><input type="hidden" value="image">' + image + '</div>';
    image_area += '</div>';
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var action1 = '';
    if ( data.action_flg ) {
        if ( data.action_label == '' ) {
            action1 = '<label id="display_action_1_' + data.number + '" class="action-label ps-1 pe-1">アクションラベルを入力</label>';
        } else {
            action1 = '<label id="display_action_1_' + data.number + '" class="action-label ps-1 pe-1">' + data.action_label + '</label>';
        }
    }
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="card-type-area" style="height: auto;">';
    html += '<div class="card-type-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + label + action1 + '</div>';
    html += '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}
function append_card_type_preview_announce(data) {
    var image = '';
    if ( data.image_flg ) {
        if ( data.image_count == '1' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '</div>';
        } else if ( data.image_count == '2' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png';
            if ( data.image_2 != '' ) {
                if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + data.image_2;
                } else {
                    image_b = data.image_2;
                }
            }
            image += '<div id="display_image_area_2" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>';
            image += '</div>';
        } else if ( data.image_count == '3' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png';
            if ( data.image_2 != '' ) {
                if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + data.image_2;
                } else {
                    image_b = data.image_2;
                }
            }
            var image_c = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png';
            if ( data.image_3 != '' ) {
                if ( data.image_3.indexOf( 'uploads' ) !== -1 ) {
                    image_c = $( '#env_media_url' ).val() + data.image_3;
                } else {
                    image_c = data.image_3;
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two flex-column position-relative">';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="c">';
            image += '<span style="background-image: url( ' + image_c + ' );"></span>';
            image += '</div>';
            image += '</div>';
            image += '</div>';
        }
    } else {
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        if ( data.label_flg ) {
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 2.5rem;">';
        } else {
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 0rem;">';
        }
        image += '<input type="hidden" value="a">';
        image += '<span></span>';
        image += '</div>';
        image += '</div>';
    }
    var title = '';
    if ( data.title == '' ) {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">' + data.title + '</p>';
    }
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var description = '';
    if ( data.description_flg ) {
        if ( data.description == '' ) {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">' + data.description + '</p>';
        }
    }
    var text = '';
    $.each( data.text, function( index, value ) {
        if ( value.flg ) {
            text += '<div class="mt-2">';
            text += '<p id="display_text_title_' + ( index + 1 ) + '_' + data.number + '" class="mb-0" style="font-size: 0.5rem; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">' + value.title + '</p>';
            text += '<p id="display_text_text_' + ( index + 1 ) + '_' + data.number + '" class="mb-0" style="font-size: 0.5rem; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">' + value.text + '</p>';
            text += '</div>';
        }
    });
    var action = '';
    $.each( data.action, function( index, value ) {
        if ( value.flg ) {
            if ( value.button_type == 0 ) {
                var color = '#fff';
                var background = '#fff';
                if ( value.button_color == 0 ) {
                    background = '#666f86';
                } else if ( value.button_color == 1 ) {
                    background = '#fff';
                } else if ( value.button_color == 2 ) {
                    background = '#eb4e3d';
                } else if ( value.button_color == 3 ) {
                    background = '#ed8537';
                } else if ( value.button_color == 4 ) {
                    background = '#00B900';
                } else if ( value.button_color == 5 ) {
                    background = '#5b82db';
                }
                action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + data.number + '" class="btn p-0 mb-2" style="width: 90%; color: ' + color + '; background-color: ' + background + '; border: none;" tabindex="0">' + value.label + '</button>';
            } else if ( value.button_type == 1 ) {
                var color = '#5b82db';
                var background = '#fff';
                if ( value.button_color == 0 ) {
                    color = '#666f86';
                } else if ( value.button_color == 1 ) {
                    color = '#fff';
                } else if ( value.button_color == 2 ) {
                    color = '#eb4e3d';
                } else if ( value.button_color == 3 ) {
                    color = '#ed8537';
                } else if ( value.button_color == 4 ) {
                    color = '#00B900';
                } else if ( value.button_color == 5 ) {
                    color = '#5b82db';
                }
                action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + data.number + '" class="btn p-0 mb-2" style="width: 90%; color: ' + color + '; background-color: ' + background + '; border: none;" tabindex="0">' + value.label + '</button>';
            }
        }
    });
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">' + title + description + text + '</div>';
    html += '<div class="cardtype-footer-area text-center">' + action + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}
function append_card_type_preview_more(data) {
    if ( data != null ) {
        var height = '14rem';
        $( '.line-preview .line-preview-content .line-preview-body .cardtype-area' ).each( function( index, value ) {
            height = $( this ).outerHeight(true);
        });
        if ( data.template == '1' ) {
            var html = '<li style="margin-right: 0.5rem;">';
            html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
            html += '<div class="cardtype-body-area position-relative ps-2 pe-2">';
            html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
            html += '</div>';
            html += '</div>';
            html += '</li>';
            $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
        } else if ( data.template == '2' ) {
            var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png );"></span>';
            if ( data.image != '' ) {
                if ( data.image.indexOf( 'uploads' ) !== -1 ) {
                    image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
                } else {
                    image = '<span style="background-image: url( ' + data.image + '"></span>';
                }
            }
            var image_area = '<div id="display_image_area_' + data.number + '" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image_area += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;"><input type="hidden" value="more">' + image + '</div>';
            image_area += '</div>';

            var html = '<li style="margin-right: 0.5rem;">';
            html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
            html += '<div class="cardtype-header-area">';
            html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
            html += '</div>';
            html += '<div class="cardtype-body-area position-relative ps-2 pe-2" style="height: calc(100% - 120px)">';
            html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
            html += '</div>';
            html += '</div>';
            html += '</li>';
            $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
        }
    }
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