
$( function() {
    create_drop_zone( 'image_big', 'image' );
    create_drop_zone( 'image_small', 'image' );
});

upload.image_big = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_big', '.error-message-big-image', 1000000 ) ) {
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

            if ( !( result.width == 2500 && result.height == 1686 ) && !( result.width == 1200 && result.height == 810 ) && !( result.width == 800 && result.height == 540 ) ) {
                $( '#image_big_drop_zone [name=image_file]' ).val( '' );
                $( '.error-message-big-image' ).removeClass( 'd-none' );
                $( '.error-message-big-image p' ).each( function( index, value ) {
                    if ( index == 2 ) {
                        $( this ).removeClass( 'd-none' );
                    } else {
                        $( this ).addClass( 'd-none' );
                    }
                });
                return;
            }
            
            $( '#save_richmenu_form .template-area img' ).remove();
            $( '#save_richmenu_form .template-area' ).css( 'padding-top', '0' );
            $( '#save_richmenu_form .template-area' ).css( 'height', '100%' );
            $( '#save_richmenu_form .template-area' ).append( '<img src="' + reader.result + '">' );
            $( '#save_richmenu_form .template-area p' ).remove();

            create_preview();
            $( '#save_richmenu_form [name=upload_image]' ).val( reader.result );
            $( '#image_big_drop_zone [name=image_file]' ).val( '' );
            $( '#image_big_drop_zone' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
        }
    }
    reader.readAsDataURL( file );
}
upload.image_small = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_small', '.error-message-small-image', 1000000 ) ) {
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
            if ( !( result.width == 2500 && result.height == 843 ) && !( result.width == 1200 && result.height == 405 ) && !( result.width == 800 && result.height == 270 ) ) {
                $( '#image_small_drop_zone [name=image_file]' ).val( '' );
                $( '.error-message-small-image' ).removeClass( 'd-none' );
                $( '.error-message-small-image p' ).each( function( index, value ) {
                    if ( index == 2 ) {
                        $( this ).removeClass( 'd-none' );
                    } else {
                        $( this ).addClass( 'd-none' );
                    }
                });
                return;
            }
            
            $( '#save_richmenu_form .template-area img' ).remove();
            $( '#save_richmenu_form .template-area' ).css( 'padding-top', '0' );
            $( '#save_richmenu_form .template-area' ).css( 'height', '100%' );
            $( '#save_richmenu_form .template-area' ).append( '<img src="' + reader.result + '">' );
            $( '#save_richmenu_form .template-area p' ).remove();

            create_preview();
            $( '#save_richmenu_form [name=upload_image]' ).val( reader.result );
            $( '#image_small_drop_zone [name=image_file]' ).val( '' );
            $( '#image_small_drop_zone' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
        }
    }
    reader.readAsDataURL( file );
}