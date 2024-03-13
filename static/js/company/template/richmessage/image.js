$( function() {
    create_drop_zone( 'image_normal', 'image' );
    create_drop_zone( 'image_custom', 'image' );
});

upload.image_normal = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_normal', '.error-message-image-normal' ) ) {
        return;
    }

    var image = new Image();
    var reader = new FileReader();
    reader.onload = function () {
        var result = {};
        image.src = reader.result;
        image.onload = function() {
            result = {
                width: image.naturalWidth,
                height: image.naturalHeight
            };

            if ( result.width != 1040 && result.height != 1040 ) {
                $( '#image_normal_drop_zone [name=image_file]' ).val( '' );
                $( '.error-message-image-normal' ).removeClass( 'd-none' );
                $( '.error-message-image-normal p' ).each( function( index, value ) {
                    if ( index == 2 ) {
                        $( this ).removeClass( 'd-none' );
                    } else {
                        $( this ).addClass( 'd-none' );
                    }
                });
                return;
            }
            $( '.error-message-image-normal' ).addClass( 'd-none' );
            $( '.error-message-image-normal p' ).each( function( index, value ) {
                $( this ).addClass( 'd-none' );
            });

            $( '#save_richmessage_form .template-area img' ).remove();
            $( '#save_richmessage_form .template-area' ).css( 'padding-top', '0' );
            $( '#save_richmessage_form .template-area' ).prepend( '<img src="' + reader.result + '">' );
            $( '#save_richmessage_form .template-area p' ).remove();

            create_preview();

            $( '#save_richmessage_form [name=upload_image]' ).val( reader.result );
            $( '#image_normal_drop_zone [name=image_file]' ).val( '' );
            $( '#image_normal_drop_zone' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
        }
    }
    reader.readAsDataURL( file );
}

upload.image_custom = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_custom', '.error-message-image-custom' ) ) {
        return;
    }

    var image = new Image();
    var reader = new FileReader();
    reader.onload = function () {
        var result = {};
        image.src = reader.result;
        image.onload = function() {
            result = {
                width: image.naturalWidth,
                height: image.naturalHeight
            };

            if ( result.width != 1040 && result.height >= 520 && result.height <= 2080 ) {
                $( '#image_custom_drop_zone [name=image_file]' ).val( '' );
                $( '.error-message-image-custom' ).removeClass( 'd-none' );
                $( '.error-message-image-custom p' ).each( function( index, value ) {
                    if ( index == 2 ) {
                        $( this ).removeClass( 'd-none' );
                    } else {
                        $( this ).addClass( 'd-none' );
                    }
                });
                return;
            }
            $( '.error-message-image-custom' ).addClass( 'd-none' );
            $( '.error-message-image-custom p' ).each( function( index, value ) {
                $( this ).addClass( 'd-none' );
            });

            $( '#save_richmessage_form .template-area img' ).remove();
            $( '#save_richmessage_form .template-area' ).css( 'padding-top', '0' );
            $( '#save_richmessage_form .template-area' ).css( 'height', '100%' );
            $( '#save_richmessage_form .template-area' ).append( '<img src="' + reader.result + '">' );
            $( '#save_richmessage_form .template-area p' ).remove();

            create_preview();

            $( '#save_richmessage_form [name=upload_image]' ).val( reader.result );
            $( '#image_custom_drop_zone [name=image_file]' ).val( '' );
            $( '#image_custom_drop_zone' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
        }
    }
    reader.readAsDataURL( file );
}