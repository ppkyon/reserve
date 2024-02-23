var now_textarea_node = null;
var now_textarea_offset = null;
var old_textarea_node = null;
var old_textarea_offset = null;
var old_textarea_number = null;

$( function() {
    create_preview();

    $( document ).on( 'click', '#save_greeting_form .action-button-area .name-button', function () {
        var image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/display-name.png" class="ms-1 me-1">';
        input_textarea_image( $( this ), image );
        create_preview();
    });

    $( document ).on( 'click', '#save_greeting_form .input-action-dropdown .dropdown-menu button', function () {
        var image = '';
        if ( $( this ).val() == 'line' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/line-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'company' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/company-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'name' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'phone' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-phone.png" class="ms-1 me-1">';
        }
        input_textarea_image( $( this ), image );
        create_preview();
    });

    $( document ).on( 'click', '#save_greeting_form .action-button-area .image-button', function () {
        $( '#image_upload_modal .image-drop-zone [name=number]' ).val( $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#save_greeting_form .image-area .delete-button', function () {
        $( this ).parents( '.input-area' ).find( '.message-area .text-area' ).removeClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .chart-area' ).addClass( 'd-none' );

        $( this ).parents( '.input-area' ).find( '.message-area' ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '1' );
        $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
            $( this ).prop( 'disabled', false );
        });
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).empty();
        create_preview();
    });

    $( document ).on( 'click', '#save_greeting_form .action-button-area .video-button', function () {
        $( '#video_upload_modal .video-drop-zone [name=number]' ).val( $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#save_greeting_form .video-area .delete-button', function () {
        $( this ).parents( '.input-area' ).find( '.message-area .text-area' ).removeClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .chart-area' ).addClass( 'd-none' );

        $( this ).parents( '.input-area' ).find( '.message-area' ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '1' );
        $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
            $( this ).prop( 'disabled', false );
        });
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).empty();
        create_preview();
    });

    $( document ).on( 'click', '#save_greeting_form .action-button-area .delete-button', function () {
        $( '#delete_item_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_item_check_modal .yes-button' ).on( 'click', function() {
        var target = $( this );
        $( '#save_greeting_form [name=number]' ).each( function( index, value ) {
            console.log(Number($( this ).val()));
            console.log(Number($( target ).val()));
            if ( Number($( this ).val()) == Number($( target ).val()) ) {
                $( this ).parents( '.input-area' ).remove();
            } else if ( Number($( this ).val()) > Number($( target ).val()) ) {
                var old_number =  Number( $( this ).val() );
                var new_number =  old_number - 1;
                $( this ).val( new_number );
                $( this ).parents( '.input-area' ).find( '.delete-area button' ).val( new_number );
                $( this ).parents( '.input-area' ).find( '[name=message_type_' + old_number + ']' ).attr( 'name', 'message_type_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=text_' + old_number + ']' ).attr( 'name', 'text_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=upload_image_' + old_number + ']' ).attr( 'name', 'upload_image_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=upload_video_' + old_number + ']' ).attr( 'name', 'upload_video_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=template_' + old_number + ']' ).attr( 'name', 'template_' + new_number );
            }
        });
        $( '#delete_item_check_modal .no-button' ).trigger( 'click' );
        create_preview();
    });

    $( '.button-area .add-area button' ).on( 'click', function() {
        $( '#save_greeting_form .input-area-wrap' ).append( append_input_area() );
    });
    
    $( document ).on( 'mouseup keyup', '#save_greeting_form .false-textarea', function () {
        var selection = window.getSelection();
        now_textarea_node = selection.focusNode;
        now_textarea_offset = selection.focusOffset;

        if ( check_empty($( this ).html().replaceAll( '<img', '>img' ).replaceAll(/<("[^"]*"|'[^']*'|[^'">])*>/g,'').replaceAll( '>img', '<img' )) ) {
            $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                if ( !$( this ).hasClass( 'name-button' ) && !$( this ).parents( '.dropdown' ).hasClass( 'input-action-dropdown' ) && !$( this ).hasClass( 'd-none' ) ) {
                    $( this ).prop( 'disabled', true );
                }
            });
        } else {
            $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                $( this ).prop( 'disabled', false );
            });
        }
        create_preview();
    });
    $( document ).on( 'focusout', '#save_greeting_form .false-textarea', function () {
        old_textarea_number = Number($( this ).parents( '.input-area' ).find( '[name=number]' ).val());
        old_textarea_node = now_textarea_node;
        old_textarea_offset = now_textarea_offset;
        now_textarea_node = null;
        now_textarea_offset = null;
    });
});

function input_textarea_image( target, image ) {
    var textarea = $( target ).parents( '.input-area' ).find( '.false-textarea' );
    if ( now_textarea_node == null && now_textarea_offset == null ) {
        if ( Number($( target ).parents( '.input-area' ).find( '[name=number]' ).val()) == old_textarea_number ) {
            if ( $( old_textarea_node ).text() == " " ) {
                $( textarea ).html( $( textarea ).html().replace( '&nbsp;', image + '<br>' ) );
            } else if ( $( old_textarea_node ).html() == "<br>" ) {
                $( old_textarea_node ).html( image );
            } else {
                var before = $( old_textarea_node ).text().substr( 0, old_textarea_offset );
                var after = $( old_textarea_node ).text().substr( old_textarea_offset );
                $( textarea ).html( $( textarea ).html().replace( $( old_textarea_node ).text(), before + image + after ) );
            }
        } else {
            $( textarea ).html( $( textarea ).html() + image );
        }
    } else {
        var before = $( now_textarea_node ).text().substr( 0, now_textarea_offset );
        var after = $( now_textarea_node ).text().substr( now_textarea_offset );
        $( textarea ).html( $( textarea ).html().replace( $( now_textarea_node ).text(), before + image + after ) );
    }

    $( target ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
        if ( !$( this ).hasClass( 'name-button' ) && !$( this ).parents( '.dropdown' ).hasClass( 'input-action-dropdown' ) && !$( this ).hasClass( 'd-none' ) ) {
            $( this ).prop( 'disabled', true );
        }
    });
    old_textarea_node = null;
    old_textarea_offset = null;
    old_textarea_number = null;
}