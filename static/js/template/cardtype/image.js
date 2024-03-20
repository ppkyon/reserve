$( function() {
    create_drop_zone( 'image_trimming', 'image' );
    create_drop_zone( 'image_trimming_half', 'image' );
    create_drop_zone( 'image_trimming_person', 'image' );
    create_drop_zone( 'image_trimming_one', 'image' );
});

upload.image_trimming = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_trimming', '.error-message-trimming-image' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#image_trimming_drop_zone' ).addClass( 'd-none' );
        $( '#image_trimming_zone' ).removeClass( 'd-none' );
        $( '#trimming_image_modal .upload-button' ).addClass( 'd-block' );
        $( '#trimming_image_modal .upload-button' ).removeClass( 'd-none' );
    
        $( '#image_trimming_zone .image-trimming-area' ).croppie( {
            url: reader.result,
            enableExif: true,
            viewport: {
                width: 356,
                height: 231,
                type:'square'
            },
            boundary: {
                width: 453,
                height: 284
            }
        })
    }
    reader.readAsDataURL( file );
}
upload.image_trimming_half = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_trimming_half', '.error-message-trimming-image-half' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#image_trimming_half_drop_zone' ).addClass( 'd-none' );
        $( '#image_trimming_half_zone' ).removeClass( 'd-none' );
        $( '#trimming_half_image_modal .upload-button' ).addClass( 'd-block' );
        $( '#trimming_half_image_modal .upload-button' ).removeClass( 'd-none' );
    
        $( '#image_trimming_half_zone .image-trimming-area' ).croppie( {
            url: reader.result,
            enableExif: true,
            viewport: {
                width: 154,
                height: 200,
                type:'square'
            },
            boundary: {
                width: 453,
                height: 284
            }
        })
    }
    reader.readAsDataURL( file );
}
upload.image_trimming_person = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_trimming_person', '.error-message-image-person' ) ) {
        return;
    }
    if ( $( '.trimming-image-modal [name=upload_image_name]' ).length ) {
        $( '.trimming-image-modal [name=upload_image_name]' ).val( file.name );
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#image_trimming_person_drop_zone' ).addClass( 'd-none' );
        $( '#image_trimming_person_zone' ).removeClass( 'd-none' );
        $( '#trimming_person_image_modal .upload-button' ).addClass( 'd-block' );
        $( '#trimming_person_image_modal .upload-button' ).removeClass( 'd-none' );
        
        $( '#image_trimming_person_zone .image-trimming-area' ).croppie( {
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
        })
    }
    reader.readAsDataURL( file );
}
upload.image_trimming_one = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_trimming_one', '.error-message-trimming-image-one' ) ) {
        return;
    }

    var image = new Image();
    var reader = new FileReader();
    reader.onload = function () {
        $( '#image_trimming_one_drop_zone' ).addClass( 'd-none' );
        $( '#image_trimming_one_zone' ).removeClass( 'd-none' );
        $( '#trimming_one_image_modal .upload-button' ).addClass( 'd-block' );
        $( '#trimming_one_image_modal .upload-button' ).removeClass( 'd-none' );
        
        $( '#image_trimming_one_zone .image-trimming-area' ).croppie( {
            url: reader.result,
            enableExif: true,
            viewport: {
                width: 388,
                height: 350,
                type:'square'
            },
            boundary: {
                width: 408,
                height: 370
            }
        });
    }
    reader.readAsDataURL( file );
}