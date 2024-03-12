$( function() {
    action_preview();
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview( $( this ).find( 'input[type=hidden]' ).val() );
    });

    $( '#save_richmenu_form [name=menu_type]' ).on( 'change', function( index, value ) {
        if ( $( this ).val() == '1' ) {
            $( '#save_richmenu_form [name=menu_text]' ).prop( 'disabled', false );
            $( '#save_richmenu_form [name=menu_text]' ).prop( 'required', true );
        } else {
            $( '#save_richmenu_form [name=menu_text]' ).prop( 'disabled', true );
            $( '#save_richmenu_form [name=menu_text]' ).prop( 'required', false );
        }
    });

    $( '#save_richmenu_form .template-button-area .select-template-button' ).on( 'click', function() {
        $( '#select_template_modal .template-area figure input' ).each( function( index, value ) {
            if ( $( this ).val() == $( '#save_richmenu_form [name=template]' ).val() ) {
                $( this ).parent().find( 'img' ).trigger( 'click' );
            }
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#select_template_modal .template-area img' ).on( 'click', function() {
        var target = $( this ).parent().find( 'input' );
        $( '#select_template_modal .template-area input' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).val() ) {
                if ( Number($( this ).val()) < 7 ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/big-select-' + ( Number($( this ).val()) + 1 ) + '.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/small-select-' + ( Number($( this ).val()) - 6 ) + '.png' );
                }
            } else {
                if ( Number($( this ).val()) < 7 ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/big-' + ( Number($( this ).val()) + 1 ) + '.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/small-' + ( Number($( this ).val()) - 6 ) + '.png' );
                }
            }
        });
        $( '#modal_select_template' ).val( $( target ).val() );
    });
    $( '#select_template_modal .select-button' ).on( 'click', function() {
        if ( check_empty($( '#modal_select_template' ).val()) ) {
            append_template_area( $( '#modal_select_template' ).val() );
            append_action_area( $( '#modal_select_template' ).val() );

            $( "#upload_template_image" ).prop( "disabled", false );
            $( '#save_richmenu_form [name=template]' ).val( $( '#modal_select_template' ).val() );
            $( this ).next().next().trigger( 'click' );
        }
    });
    $( '#select_template_modal .cancel-button' ).on( 'click', function() {
        $( '#select_template_modal .template-area input' ).each( function( index, value ) {
            if ( $( '#save_richmenu_form [name=template]' ).val() == $( this ).val() ) {
                if ( Number($( this ).val()) < 7 ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/big-select-' + ( Number($( this ).val()) + 1 ) + '.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/small-select-' + ( Number($( this ).val()) - 6 ) + '.png' );
                }
            } else {
                if ( Number($( this ).val()) < 7 ) {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/big-' + ( Number($( this ).val()) + 1 ) + '.png' );
                } else {
                    $( this ).next().attr( 'src', $( '#env_static_url' ).val() + 'img/richmenu/small-' + ( Number($( this ).val()) - 6 ) + '.png' );
                }
            }
        });
        $( this ).next().trigger( 'click' );
    });

    $( '#upload_template_image' ).on( 'click', function() {
        if ( $( '#save_richmenu_form [name=template]' ).val() != '' ) {
            if ( Number($( '#save_richmenu_form [name=template]' ).val()) < 7 ) {
                $( this ).next().trigger( 'click' );
            } else {
                $( this ).next().next().trigger( 'click' );
            }
        }
    });
    $( '#image_big_upload_modal .cancel-button, #image_small_upload_modal .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });

    $( document ).on( 'click', '#save_richmenu_form .template-area table td', function () {
        var traget = $( this );
        $( '.action-area' ).each( function() {
            if ( $( this ).find( '[name=number]' ).val() == $( traget ).find( 'input' ).val() ) {
                $( this ).find( 'img' ).css( 'transform', '' );
                $( this ).find( '.content-area-wrap' ).slideDown();
            } else {
                $( this ).find( 'img' ).css( 'transform', 'rotate(-90deg)' );
                $( this ).find( '.content-area-wrap' ).slideUp();
            }
        });
    });
    $( document ).on( 'click', '#save_richmenu_form .action-area .number-area', function () {
        if ( $( this ).next().css( 'display' ) == 'none' ) {
            $( this ).find( 'img' ).css( 'transform', '' );
            $( this ).parent().find( '.content-area-wrap' ).slideToggle();
        } else {
            $( this ).find( 'img' ).css( 'transform', 'rotate(-90deg)' );
            $( this ).parent().find( '.content-area-wrap' ).slideToggle();
        }
    });

    $( document ).on( 'click', '#save_richmenu_form .action-area .dropdown-menu button', function () {
        append_content_area( $( this ), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        if ( $( this ).val() == '2' ) {
            open_template_video_modal($( this ).parents( '.dropdown' ).next(), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '3' ) {
            open_question_modal( $( this ), $( this ).parents( '.action-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '4' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【予約フォーム】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        } else if ( $( this ).val() == '5' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【予約履歴ページ】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        } else if ( $( this ).val() == '6' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【オンラインURL】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        } else if ( $( this ).val() == '7' ) {
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).val( '【会社概要URL】' );
            $( this ).parents( '.content-area' ).next().next().find( 'input[type=text]' ).prop( 'disabled', true );
        }
    });

    $( document ).on( 'click', '#company_template_video_modal .table-area tbody button', function () {
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
    $( document ).on( 'click', '#company_question_modal .table-area tbody button', function () {
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