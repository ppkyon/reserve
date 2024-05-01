$( function() {
    $( document ).on( 'click', '#member_user_message_check_modal #member_user_template_area .dropdown-menu button', function () {
        $( '#member_user_message_check_modal' ).removeClass( 'up-modal' );
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this).next(), 'member' );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this).next(), 'member' );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this).next(), 'member' );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this).next(), 'member' );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this).next(), 'member' );
        }
        up_modal();
    });
    $( document ).on( 'click', '#edit_step_yes_message_modal #step_yes_template_area .dropdown-menu button', function () {
        $( '#edit_step_yes_message_modal' ).removeClass( 'up-modal' );
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this).next(), 'yes' );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this).next(), 'yes' );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this).next(), 'yes' );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this).next(), 'yes' );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this).next(), 'yes' );
        }
        up_modal();
    });
    $( document ).on( 'click', '#edit_step_no_message_modal #step_no_template_area .dropdown-menu button', function () {
        $( '#edit_step_no_message_modal' ).removeClass( 'up-modal' );
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this).next(), 'no' );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this).next(), 'no' );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this).next(), 'no' );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this).next(), 'no' );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this).next(), 'no' );
        }
        up_modal();
    });

    $( document ).on( 'click', '#template_text_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_text_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal [name=template]' ).val( response.name );
                $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal [name=yes_template]' ).val( response.name );
                $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal [name=no_template]' ).val( response.name );
                $( '#edit_step_no_message_modal [name=no_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_text_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_video_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_video_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal [name=template]' ).val( response.name );
                $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal [name=yes_template]' ).val( response.name );
                $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal [name=no_template]' ).val( response.name );
                $( '#edit_step_no_message_modal [name=no_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_video_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richmessage_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_richmessage_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal [name=template]' ).val( response.name );
                $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal [name=yes_template]' ).val( response.name );
                $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal [name=no_template]' ).val( response.name );
                $( '#edit_step_no_message_modal [name=no_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_richmessage_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richvideo_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_richvideo_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal [name=template]' ).val( response.name );
                $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal [name=yes_template]' ).val( response.name );
                $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal [name=no_template]' ).val( response.name );
                $( '#edit_step_no_message_modal [name=no_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_richvideo_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_cardtype_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_cardtype_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal [name=template]' ).val( response.name );
                $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal [name=yes_template]' ).val( response.name );
                $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal [name=no_template]' ).val( response.name );
                $( '#edit_step_no_message_modal [name=no_template]' ).next().val( $( target ).next().val() );
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            if ( $( target ).val() == 'member' ) {
                $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'yes' ) {
                $( '#edit_step_yes_message_modal' ).addClass( 'up-modal' );
            } else if ( $( target ).val() == 'no' ) {
                $( '#edit_step_no_message_modal' ).addClass( 'up-modal' );
            }
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_cardtype_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
});