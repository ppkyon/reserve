$( function() {
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview( $( this ).find( 'input[type=hidden]' ).val() );
    });

    $( '#save_question_form .color-area button' ).on( 'click', function() {
        var target = $( this );
        $( this ).parents( '.color-area' ).prev().val( $( this ).val() );
        $( this ).parents( '.color-area' ).find( 'button' ).each( function( index, value ) {
            $( this ).empty();
            if ( $( target ).val() == $( this ).val() ) {
                $( this ).append( '<i class="bx bx-check"></i>' );
            } else {
                $( this ).append( '<span>A</span>' );
            }
        });
    });

    $( '#save_question_form .add-display-area button' ).on( 'click', function() {
        $( '#save_question_form .display-area-wrap' ).append( append_setting_area() );
        append_order_button();
    });
    $( document ).on( 'click', '#save_question_form .display-area .action-area .copy-item-button', function () {
        var target = $( this );
        var number = $( this ).parents( '.display-area' ).find( '.pin-area input' ).attr( 'id' ).replace( 'check_pin_', '' );
        var copy_clone = $( this ).parents( '.display-area' ).clone();
        $( copy_clone ).html( $( copy_clone ).html().replaceAll( number, ( Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2 ) ) );
        $( '#save_question_form .display-area-wrap' ).append( copy_clone );
        $( '#save_question_form .display-area' ).each( function( index, value ) {
            if ( index == $( '#save_question_form .display-area' ).length - 1 ) {
                $( this ).find( 'input' ).each( function( index, value ) {
                    $( this ).val( $( target ).parents( '.display-area' ).find( 'input' ).eq( index ).val() );
                    $( this ).prop( 'checked', $( target ).parents( '.display-area' ).find( 'input' ).eq( index ).prop( 'checked' ) );
                });
            }
        });
    });

    $( document ).on( 'click', '#save_question_form .display-area .top-area .dropdown-menu button', function () {
        if ( $( this ).parents( '.content-area' ).find( '.type-area' ).length ) {
            $( this ).parents( '.content-area' ).find( '.type-area' ).next().remove();
            $( this ).parents( '.content-area' ).find( '.type-area' ).remove();
        }
        if ( $( this ).parents( '.content-area' ).find( '.option-area' ).length ) {
            $( this ).parents( '.content-area' ).find( '.option-area' ).remove();
        }
        if ( $( this ).val() == '51' ) {
            if ( !$( this ).parents( '.content-area' ).find( '.type-area' ).length ) {
                $( this ).parents( '.content-area' ).append( append_reserve_type_area() );
            }
        } else if ( $( this ).val() == '52' ) {
            if ( !$( this ).parents( '.content-area' ).find( '.type-area' ).length ) {
                $( this ).parents( '.content-area' ).append( append_reserve_date_area() );
            }
        } else if ( $( this ).val() == '53' || $( this ).val() == '54' ) {
            if ( !$( this ).parents( '.content-area' ).find( '.type-area' ).length ) {
                $( this ).parents( '.content-area' ).append( append_reserve_best_area() );
            }
        } else if ( $( this ).val() == '99' ) {
            if ( !$( this ).parents( '.content-area' ).find( '.type-area' ).length ) {
                $( this ).parents( '.content-area' ).append( append_question_type_area() );
            }
        }
    });

    $( document ).on( 'click', '#save_question_form .display-area .type-area .dropdown-menu button', function () {
        $( this ).parents( '.content-area' ).find( '.item-area' ).remove();
        if ( $( this ).val() == '2' || $( this ).val() == '3' || $( this ).val() == '4' ) {
            $( this ).parents( '.content-area' ).append( append_item_area( true ) );
        } else {
            $( this ).parents( '.content-area' ).append( append_item_area( false ) );
        }
        $( this ).parents( '.display-area' ).find( '.add-list-button' ).val( $( this ).val() );
    });

    $( document ).on( 'click', '#save_question_form .display-area .item-area .add-list-button', function () {
        var target = $( this );
        $( this ).parents( '.item-area' ).find( '.row' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).append( append_list_area(target) );
            }
        });
    });

    var delete_clone = '';
    $( document ).on( 'click', '#save_question_form .display-area .item-area .delete-list-button', function () {
        $( '#delete_list_check_modal .yes-button' ).val( $( this ).parents( '.col-6' ).find( 'span' ).text().replace( '.', '' ) );
        delete_clone = $( this );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_list_check_modal .yes-button' ).on( 'click', function() {
        var target = $( this );
        var delete_flg = false;
        $( delete_clone ).parents( '.item-area' ).find( '.col-6' ).each( function( index, value ) {
            if ( !delete_flg && $( this ).find( 'span' ).text().replace( '.', '' ) == $( target ).val() ) {
                $( this ).remove();
                delete_flg = true;
            }
            if ( delete_flg ) {
                $( this ).find( 'span' ).text( ( Number($( this ).find( 'span' ).text().replace( '.', '' )) - 1 ) + '.' );
            }
        });
        $( '#delete_list_check_modal .no-button' ).trigger( 'click' );
    });

    var delete_item_clone = '';
    $( document ).on( 'click', '#save_question_form .display-area .action-area .delete-item-button', function () {
        delete_item_clone = $( this ).parents( '.display-area' );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_item_check_modal .yes-button' ).on( 'click', function() {
        $( delete_item_clone ).remove();
        $( '#delete_item_check_modal .no-button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '#save_question_form .display-area .action-area .order-up-button', function () {
        var clone = $( this ).parents( '.display-area' ).clone();
        $( this ).parents( '.display-area' ).prev().before( clone );
        $( this ).parents( '.display-area' ).remove();
        append_order_button();
    });
    $( document ).on( 'click', '#save_question_form .display-area .action-area .order-down-button', function () {
        var clone = $( this ).parents( '.display-area' ).clone();
        $( this ).parents( '.display-area' ).next().after( clone );
        $( this ).parents( '.display-area' ).remove();
        append_order_button();
    });

    $( document ).on( 'click', '#save_question_form .display-area .item-area .delete-offline-button', function () {
        var parent = $( this ).parents( '.col-6' ).parent();
        $( parent ).empty();
        $( parent ).append( append_delete_offline() );
    });
    $( document ).on( 'click', '#save_question_form .display-area .item-area .delete-online-button', function () {
        var parent = $( this ).parents( '.col-6' ).parent();
        $( parent ).empty();
        $( parent ).append( append_delete_online() );
    });
    $( document ).on( 'click', '#save_question_form .display-area .item-area .add-offline-button', function () {
        var parent = $( this ).parents( '.col-6' ).parent();
        $( parent ).empty();
        $( parent ).append( append_add_offline() );
    });
    $( document ).on( 'click', '#save_question_form .display-area .item-area .add-online-button', function () {
        var parent = $( this ).parents( '.col-6' ).parent();
        $( parent ).empty();
        $( parent ).append( append_add_online() );
    });
});