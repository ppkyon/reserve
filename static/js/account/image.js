$( function() {
    create_drop_zone( 'trimming_account_image', 'image' );
    create_drop_zone( 'logo', 'image' );

    $( document ).on( 'click', '.account-image-button', function () {
        $( '.input-area .input-text-area.target' ).removeClass( 'target' );
        $( this ).parents( '.input-text-area' ).addClass( 'target' );
        reset_trimming( $( '.trimming-image-modal .cancel-button' ) );
        $( this ).next().trigger( 'click' )
    });
    $( '#trimming_image_modal .upload-button' ).on( 'click', function() {
        var target_area = $( '.input-area .input-text-area.target' );
        var file_name = $( '#trimming_image_modal [name=upload_image_name]' ).val();

        $( this ).parents( '.modal' ).find( '.trimming-image-area' ).croppie( 'result', 'base64' ).then( function( base64 ) {
            $( target_area ).find( '.upload-image-area input[type=text]' ).each( function( index ,value ) {
                $( this ).val( base64 );
            });
            $( target_area ).find( '.upload-image-area input[type=hidden]' ).each( function( index ,value ) {
                if ( index == 0 ) {
                    $( this ).val( file_name );
                } else if ( index == 1 ) {
                    $( this ).val( base64 );
                }
            });
        });

        $( target_area ).find( '.image-file-name' ).text( file_name );
        $( target_area ).find( '.image-file-name' ).removeClass( 'd-none' );
        $( target_area ).find( '.image-file-name' ).next().removeClass( 'd-none' );
        $( target_area ).removeClass( 'target' );
        reset_trimming( this );

        $( this ).next().trigger( 'click' );
    });
    $( '#trimming_image_modal .cancel-button' ).on( 'click', function() {
        reset_trimming( this );
        $( this ).next().trigger( 'click' );
    });
    $( '#trimming_image_modal .modal-body .drop-delete-button' ).on( 'click', function() {
        reset_trimming( this );
    });

    $( document ).on( 'click', '.logo-image-button', function () {
        $( this ).next().trigger( 'click' )
    });
    $( '.logo-image-modal .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });

    $( '.input-area .input-text-area .image-delete-button' ).on( 'click', function() {
        $( this ).prev().addClass( 'd-none' );
        $( this ).prev().text( '' );
        $( this ).next().find( 'input[type=hidden]' ).val( '' );
        $( this ).addClass( 'd-none' );
    });
});

upload.trimming_account_image = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'trimming_account_image', '.error-message-account-image' ) ) {
        return;
    }
    if ( $( '.trimming-image-modal [name=upload_image_name]' ).length ) {
        $( '.trimming-image-modal [name=upload_image_name]' ).val( file.name );
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#trimming_account_image_drop_zone' ).addClass( 'd-none' );
        $( '#trimming_account_image_zone' ).removeClass( 'd-none' );
        $( '.trimming-image-modal .upload-button' ).addClass( 'd-block' );
        $( '.trimming-image-modal .upload-button' ).removeClass( 'd-none' );

        $( '#trimming_account_image_zone .trimming-image-area' ).croppie( {
            url: reader.result,
            enableExif: true,
            viewport: {
                width: 250,
                height: 250,
                type:'circle'
            },
            boundary: {
                width: 453,
                height: 284
            }
        });
    }
    reader.readAsDataURL( file );
}
upload.logo = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        var area = $( '.input-area .input-text-area' );
        $( area ).find( '.logo-image-file-name' ).removeClass( 'd-none' );
        $( area ).find( '.logo-image-file-name' ).text( file.name );
        $( area ).find( '.logo-image-file-name' ).next().removeClass( 'd-none' );
        $( area ).find( '.upload-logo-image-area input[type=hidden]' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).val( file.name );
            } else if ( index == 1 ) {
                $( this ).val( reader.result );
            }
        });
        $( '.logo-image-modal .cancel-button' ).trigger( 'click' );
    }
    reader.readAsDataURL( file );
}

function reset_trimming( target ) {
    $( target ).parents( '.modal' ).find( '.image-drop-zone [name=image_file]' ).val( '' );
    $( target ).parents( '.modal' ).find( '.image-drop-zone [name=upload_image_name]' ).val( '' );
    $( target ).parents( '.modal' ).find( '.image-drop-zone' ).removeClass( 'd-none' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone' ).addClass( 'd-none' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone .trimming-image-area' ).removeClass( 'croppie-container' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone .trimming-image-area' ).empty();
    $( '.trimming-image-modal .upload-button' ).removeClass( 'd-block' );
    $( '.trimming-image-modal .upload-button' ).addClass( 'd-none' );
}