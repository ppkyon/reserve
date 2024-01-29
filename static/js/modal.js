$( function() {
    $( '.add-button' ).on( 'click', function() {
        if ( $( '#add_' + $( this ).val() + '_form' ).parsley().validate() ) {
            var target = $( this );
            $.ajax({
                'data': get_form_data( $( this ), add_data ),
                'url': $( '#add_' + $( target ).val() + '_check_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    get_success_data( target, $( target ).next(), add_success );
                } else {
                    if ( check_empty( response.error_list ) ) {
                        get_error_data( target, response.error_list, add_error );
                    } else {
                        get_error_data( target, 'すでに登録済みのデータです', add_error );
                    }
                }
            }).fail( function(){
                get_error_data( target, '追加できませんでした', add_error );
            });
        }
    });
    $( '#add_check_modal .yes-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        $.ajax({
            'data': get_form_data( $( this ), add_data ),
            'url': $( '#add_' + $( this ).val() + '_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#add_check_modal .no-button' ).trigger( 'click' );
                $( '#add_success_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#add_check_modal .no-button' ).trigger( 'click' );
                $( '#add_error_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'add' );

    $( document ).on( 'click', '.save-button', function () {
        if ( $( '#save_' + $( this ).val() + '_form' ).parsley().validate() ) {
            var next = $( this ).next();
            var target = $( this );
            var url = $( '#save_check_form' ).val();
            if ( check_empty( $( '#save_' + $( target ).val() + '_check_form' ).val() ) ) {
                url = $( '#save_' + $( target ).val() + '_check_form' ).val();
            }
            $.ajax({
                'data': get_form_data( $( this ), save_data ),
                'url': url,
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    get_success_data( target, next, save_success );
                } else {
                    if ( check_empty( response.error_list ) ) {
                        get_error_data( target, response.error_list, save_error );
                    } else {
                        get_error_data( target, '', save_error );
                    }
                }
            }).fail( function(XMLHttpRequest, textStatus, errorThrown) {
                get_error_data( target, '', save_error );
                console.log("XMLHttpRequest : " + XMLHttpRequest.status);
                console.log("textStatus     : " + textStatus);
                console.log("errorThrown    : " + errorThrown.message);
            });
        }
    });
    $( '#save_check_modal .yes-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        $.ajax({
            'data': get_form_data( $( this ), save_data ),
            'url': $( '#save_' + $( this ).val() + '_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#save_check_modal .no-button' ).trigger( 'click' );
                $( '#save_success_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#save_check_modal .no-button' ).trigger( 'click' );
                $( '#save_error_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'save' );

    $( document ).on( 'click', '.delete-button', function () {
        $( '#delete_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_check_modal .yes-button' ).on( 'click', function() {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        $.ajax({
            'data': get_form_data( $( this ), delete_data ),
            'url': $( '#delete_' + $( this ).val() + '_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#delete_check_modal .no-button' ).trigger( 'click' );
                $( '#delete_success_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#delete_check_modal .no-button' ).trigger( 'click' );
                $( '#delete_error_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'delete' );

    $( '#favorite_on_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#favorite_on_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#favorite_off_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#favorite_off_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
});

function get_form_data( target, data ) {
    var val = $( target ).val();
    var form_data = new FormData();
    if( $( target ).val().indexOf( '_' ) !== -1 ) {
        val = $( target ).val().split('_');
        form_data = data[val[0]](val[1]);
    } else {
        form_data = data[val]();
    }
    return form_data;
}

function get_success_data( target, modal, data ) {
    var val = $( target ).val();
    var form_data = new FormData();
    if( $( target ).val().indexOf( '_' ) !== -1 ) {
        val = $( target ).val().split('_');
        form_data = data[val[0]](modal, $( target ).val());
    } else {
        form_data = data[val](modal, '');
    }
    return form_data;
}

function get_error_data( target, message, data ) {
    var val = $( target ).val();
    var form_data = new FormData();
    if( $( target ).val().indexOf( '_' ) !== -1 ) {
        val = $( target ).val().split('_');
        form_data = data[val[0]](message, val[1]);
    } else {
        form_data = data[val](message, '');
    }
    return form_data;
}

function action_reload( action ) {
    $( '#' + action + '_success_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#' + action + '_success_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#' + action + '_error_modal' ).on( 'hidden.bs.modal', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
    $( '#' + action + '_error_modal .close-button' ).on( 'click', function () {
        if ( $( '#reload_url' ).length ) {
            window.location.href = $( '#reload_url' ).val();
        } else {
            window.location.reload();
        }
    });
}

function up_modal() {
    $( '.modal-backdrop' ).each( function( index, value ){
        if ( index == $( '.modal-backdrop' ).length - 1 ) {
            $( this ).css( 'z-index', '1060' );
        }
    });
}
function down_modal() {
    $( '.offcanvas' ).css( 'z-index', '1045' );
}