$( function() {
    $( document ).on( 'change', '#save_facility_form input[type=text]', function () {
        $( '.facility-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
    });
    $( document ).on( 'click', '#save_facility_form .dropdown .dropdown-menu button', function () {
        $( '.facility-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
    });

    $( document ).on( 'click', '.table-area .facility-table tbody tr', function () {
        if ( $( this ).hasClass( 'active' ) ) {
            var change_flg = false;
            $( '.facility-table tr td' ).each( function( index, value ) {
                if ( $( this ).children( 'input[type=hidden]' ).val() == 'true' ) {
                    change_flg = true;
                }
            });
            if ( change_flg ) {
                $( '#facility_change_modal .yes-button' ).val( $( this ).find( '.title-id' ).val() );
                $( '#facility_change_button' ).trigger( 'click' );
            } else {
                $( this ).parent().find( 'tr' ).each( function( index, value ) {
                    $( this ).css( 'background-color', '#FFF' );
                    $( this ).removeClass( 'active' );
                });
                $( '.facility-list-area' ).each( function( index, value ) {
                    $( this ).addClass( 'd-none' );
                });
                $( this ).css( 'background-color', '' );
                $( this ).addClass( 'active' );
                $( '#' + $( this ).find( '.title-id' ).val() ).removeClass( 'd-none' );
                $( '.save-button' ).next().val( $( this ).find( '.title-id' ).val() );
            }
        }
    });
    $( document ).on( 'click', '#facility_change_modal .yes-button', function () {
        var target = $( this );
        $( '.facility-list-area' ).each( function( index, value ) {
            $( this ).addClass( 'd-none' );
        });
        $( '.facility-table tr' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).find( '.title-id' ).val() ) {
                $( this ).css( 'background-color', '' );
                $( this ).addClass( 'active' );
                $( '#' + $( target ).val() ).removeClass( 'd-none' );
                $( '.save-button' ).next().val( $( target ).val() );
            } else {
                $( this ).css( 'background-color', '#FFF' );
                $( this ).removeClass( 'active' );
            }
        });
        $( '#facility_change_modal .no-button' ).trigger( 'click' );
    });

    var old_value = null;
    $( document ).on( 'click', '#save_facility_form .input-order-dropdown input[type=text]', function () {
        old_value = Number($( this ).val());
    });
    $( document ).on( 'click', '#save_facility_form .input-order-dropdown .dropdown-menu button', function () {
        var target_number = Number($( this ).parents( '.facility-area' ).find( '.count-text' ).text().replace( '.', '' ));
        var new_value = Number($( this ).parents( '.input-order-dropdown' ).find( 'input[type=text]' ).val());
        if ( old_value > new_value ) {
            $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
                var number = Number($( this ).find( '.count-text' ).text().replace( '.', '' ));
                var random = $( this ).find( '.count-text' ).next().val();
                var target_value = Number($( this ).find( 'input[name=order_' + random + ']' ).val());
                if ( new_value <= target_value && old_value > target_value && target_number != number ) {
                    $( this ).find( 'input[name=order_' + random + ']' ).val( Number($( this ).find( 'input[name=order_' + random + ']' ).val()) + 1 );
                }
            });
        } else if ( old_value < new_value ) {
            $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
                var number = Number($( this ).find( '.count-text' ).text().replace( '.', '' ));
                var random = $( this ).find( '.count-text' ).next().val();
                var target_value = Number($( this ).find( 'input[name=order_' + random + ']' ).val());
                if ( new_value >= target_value && old_value < target_value && target_number != number) {
                    $( this ).find( 'input[name=order_' + random + ']' ).val( Number($( this ).find( 'input[name=order_' + random + ']' ).val()) - 1 );
                }
            });
        }
    });

    var delete_item_area = '';
    $( document ).on( 'click', '.delete-item-button', function () {
        delete_item_area = $( this ).parents( 'tr' );
        $( '#delete_item_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_item_check_modal .yes-button' ).on( 'click', function() {
        var delete_count = null;
        var random = $( delete_item_area ).find( '.count-text' ).next().val();
        delete_count = $( delete_item_area ).find( 'input[name=order_' + random + ']' ).val();

        $( delete_item_area ).remove();
        var count = $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).length;
        $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
            $( this ).find( '.count-text' ).text( ( index + 1 ) + '.' );

            var random = $( this ).find( '.count-text' ).next().val();
            if ( delete_count < Number($( this ).find( 'input[name=order_' + random + ']' ).val()) ) {
                $( this ).find( 'input[name=order_' + random + ']' ).val( Number($( this ).find( 'input[name=order_' + random + ']' ).val()) - 1 );
            }

            $( this ).find( 'input[name=order_' + random + ']' ).next().empty();
            for ( var i = 1; i <= count; i++ ) {
                if ( i == 1 ) {
                    $( this ).find( 'input[name=order_' + random + ']' ).next().append( '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center">' + i + '</button>' );
                } else {
                    $( this ).find( 'input[name=order_' + random + ']' ).next().append( '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + i + '</button>' );
                }
            }

        });
        $( '.facility-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
        $( '#delete_item_check_modal .no-button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '.add-facility-button', function () {
        $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).append( append_facility_area() );
        var count = $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).length;
        $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
            var random = $( this ).find( '.count-text' ).next().val();
            $( this ).find( 'input[name=order_' + random + ']' ).next().empty();
            for ( var i = 1; i <= count; i++ ) {
                if ( i == 1 ) {
                    $( this ).find( 'input[name=order_' + random + ']' ).next().append( '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center">' + i + '</button>' );
                } else {
                    $( this ).find( 'input[name=order_' + random + ']' ).next().append( '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + i + '</button>' );
                }
            }
        });
    });

    $( document ).on( 'click', '.save-facility-button', function () {
        $( '.facility-list-area' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'd-none' ) ) {
                $( this ).find( 'input' ).prop( 'required', false );
            } else {
                $( this ).find( '.input-name' ).prop( 'required', true );
                $( this ).find( '.input-count' ).prop( 'required', true );
                $( this ).find( '.input-order' ).prop( 'required', true );
            }
        });
        $( this ).next().trigger( 'click' );
    });
});