$( function() {
    create_drop_zone( 'image', 'image' );
    create_drop_zone( 'video', 'video' );
});

upload.image = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#save_text_form [name=number]' ).each( function( index, value ) {
            if ( Number($( '#image_drop_zone [name=number]' ).val()) == Number($( this ).val()) ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                var text_area = $( message_area ).find( '.text-area' );
                var image_area = $( message_area ).find( '.image-area' );
                var video_area = $( message_area ).find( '.video-area' );
                var chart_area = $( message_area ).find( '.chart-area' );

                $( text_area ).addClass( 'd-none' );
                $( image_area ).removeClass( 'd-none' );
                $( video_area ).addClass( 'd-none' );
                $( chart_area ).addClass( 'd-none' );
                $( text_area ).find( '.false-textarea' ).empty();
                $( image_area ).empty();
                $( video_area ).empty();
                $( chart_area ).empty();
                $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var html = '<div class="image position-relative">';
                html += '<img src="' + reader.result + '">';
                html += '<input type="hidden" name="upload_image_' + $( this ).val() + '">';
                html += '<button type="button" class="btn delete-button" value="' + $( this ).val() + '">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                html += '</button>';
                html += '</div>';
                $( image_area ).append( html );
                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '2' );
                $( message_area ).find( '.image-area [name=upload_image_' + $( this ).val() + ']' ).val( reader.result );
                $( message_area ).find( '.image-area > .image > img' ).bind( 'load', function() {
                    if ( $( this ).width() < $( this ).height() ) {
                        $( this ).parent().parent().addClass( 'half' );
                    }
                });

                $( '#image_drop_zone [name=image_file]' ).val( '' );
                $( '#image_drop_zone [name=number]' ).val( '' );
                $( '#image_drop_zone [name=number]' ).parents( '.modal-content' ).find( '.cancel-button' ).trigger( 'click' );
            }
        });
    }
    reader.readAsDataURL( file );
}

upload.video = function( files ) {
    var file = files[0];
    if ( !error_video( file, 'video' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#save_text_form [name=number]' ).each( function( index, value ) {
            if ( Number($( '#video_drop_zone [name=number]' ).val()) == Number($( this ).val()) ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                var text_area = $( message_area ).find( '.text-area' );
                var image_area = $( message_area ).find( '.image-area' );
                var video_area = $( message_area ).find( '.video-area' );
                var chart_area = $( message_area ).find( '.chart-area' );

                $( text_area ).addClass( 'd-none' );
                $( image_area ).addClass( 'd-none' );
                $( video_area ).removeClass( 'd-none' );
                $( chart_area ).addClass( 'd-none' );
                $( text_area ).find( '.false-textarea' ).empty();
                $( image_area ).empty();
                $( video_area ).empty();
                $( chart_area ).empty();
                $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var html = '<div class="video position-relative">';
                html += '<button type="button" class="btn delete-button" value="' + $( this ).val() + '">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                html += '</button>';
                html += '<video src="' + reader.result + '" controls>';
                html += '<input type="hidden" name="upload_video_' + $( this ).val() + '">';
                html += '</div>';
                $( video_area ).append( html );
                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '3' );
                $( message_area ).find( '.video-area [name=upload_video_' + $( this ).val() + ']' ).val( reader.result );
                
                $( '#video_drop_zone [name=video_file]' ).val( '' );
                $( '#video_drop_zone [name=number]' ).val( '' );
                $( '#video_drop_zone [name=number]' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
            }
        });
    }
    reader.readAsDataURL( file );
}