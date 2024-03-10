$( function() {
    create_preview();
    
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview($( this ).find( '[name=id]' ).val());
    });

    $( '#save_richmessage_form .template-button-area .select-template-button' ).on( 'click', function() {
        $( '.modal .modal-body .template-area figure input' ).each( function( index, value ) {
            if ( $( this ).val() == $( '#save_richmessage_form [name=template]' ).val() ) {
                $( this ).parent().find( 'img' ).trigger( 'click' );
            }
        });
        $( this ).next().trigger( 'click' );
    });
    $( '.modal .modal-body .template-area img' ).on( 'click', function() {
        var target = $( this ).parent().find( 'input' );
        $( '.modal .modal-body .template-area input' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).val() ) {
                if (  $( this ).val() == '0' ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-1.png' );
                    $( this ).next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-2.png' );
                    $( this ).next().next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-3.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-square-select-' + $( this ).val() + '.png' );
                }
            } else {
                if (  $( this ).val() == '0' ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-1.png' );
                    $( this ).next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-2.png' );
                    $( this ).next().next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-3.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-square-' + $( this ).val() + '.png' );
                }
            }
        });
        $( '#modal_select_template' ).val( $( target ).val() );
    });
    $( '#select_template_modal .select-button' ).on( 'click', function() {
        if ( $( '#modal_select_template' ).val() != '' ) {
            append_template_area( $( '#modal_select_template' ).val() );
            append_action_area( $( '#modal_select_template' ).val() );

            $( "#upload_template_image" ).prop( "disabled", false );
            $( '#save_richmessage_form [name=template]' ).val( $( '#modal_select_template' ).val() );
            $( this ).next().next().trigger( 'click' );
        }
    });
    $( '#select_template_modal .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
        $( '.modal .modal-body .template-area input' ).each( function( index, value ) {
            if ( $( '#save_richmessage_form [name=template]' ).val() == $( this ).val() ) {
                if (  $( this ).val() == '0' ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-1.png' );
                    $( this ).next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-2.png' );
                    $( this ).next().next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-select-3.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-square-select-' + $( this ).val() + '.png' );
                }
            } else {
                if (  $( this ).val() == '0' ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-1.png' );
                    $( this ).next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-2.png' );
                    $( this ).next().next().next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-custom-3.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmessage/template-square-' + $( this ).val() + '.png' );
                }
            }
        });
    });

    $( '#upload_template_image' ).on( 'click', function(){
        if ( $( '#save_richmessage_form [name=template]' ).val() != '' ) {
            if ( $( '#save_richmessage_form [name=template]' ).val() == '0' ) {
                $( this ).next().next().trigger( 'click' );
            } else {
                $( this ).next().trigger( 'click' );
            }
        }
    });
    $( '#image_normal_upload_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });
    $( '#image_custom_upload_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });
    
    $( document ).on( 'click', '#save_richmessage_form .action-area .number-area', function () {
        if ( $( this ).next().css( 'display' ) == 'none' ) {
            $( this ).find( 'img' ).css( 'transform', '' );
            $( this ).parent().find( '.content-area-wrap' ).slideToggle();
        } else {
            $( this ).find( 'img' ).css( 'transform', 'rotate(-90deg)' );
            $( this ).parent().find( '.content-area-wrap' ).slideToggle();
        }
    });

    $( document ).on( 'click', '#save_richmessage_form .action-area .dropdown-menu button', function () {
        append_content_area( $( this ), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', false );
        if ( $( this ).val() == '2' ) {
            open_template_video_modal($( this ).parents( '.dropdown' ).next(), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '3' ) {
            open_question_modal( $( this ), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '4' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【予約フォームURL】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        } else if ( $( this ).val() == '5' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【予約履歴ページ】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        } else if ( $( this ).val() == '6' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【会社概要URL】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        }
    });

    $( document ).on( 'click', '#head_template_video_modal .table-area tbody button', function () {
        var target = $( this );
        $( 'form .action-area [name=number]' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).val() ) {
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).val( '【' + $( target ).next().next().val() + '】' );
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).next().val( $( target ).next().val() );
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).prop( 'disabled', true );
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#head_question_modal .table-area tbody button', function () {
        var target = $( this );
        $( 'form .action-area [name=number]' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).val() ) {
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).val( '【' + $( target ).next().next().val() + '】' );
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).next().val( $( target ).next().val() );
                $( this ).parents( '.action-area' ).find( '[name=url_' + $( this ).val() + ']' ).prop( 'disabled', true );
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
});