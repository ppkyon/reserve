$( function() {
    create_drop_zone( 'richvideo', 'video' );
});

upload.richvideo = function( files ) {
    var file = files[0];
    if ( !error_video( file, 'richvideo', '.error-message-video', 2 ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#save_richvideo_form .template-area p' ).remove();
        $( '#save_richvideo_form .template-area' ).css( 'padding-top', '0' );
        $( '#save_richvideo_form .template-area video' ).remove();
        $( '#save_richvideo_form .template-area' ).append( '<video src="' + reader.result + '" controls></video>' );
        $( '#save_richvideo_form .video-text-area video' ).attr( 'src', reader.result );

        if ( file.size >= 1000000 ) {
            $( '#save_richvideo_form .video-text-area .video-size' ).text( '容量 : ' + Math.ceil( file.size / 1000000 ) + 'MB' );
        } else if ( file.size >= 1000 ) {
            $( '#save_richvideo_form .video-text-area .video-size' ).text( '容量 : ' + Math.ceil( file.size / 1000 ) + 'KB' );
        } else {
            $( '#save_richvideo_form .video-text-area .video-size' ).text( '容量 : ' + file.size + 'B' );
        }

        $( '#save_richvideo_form .video-text-area' ).removeClass( 'd-none' );
        $( '#save_richvideo_form .video-text-area .video-time' ).removeClass( 'd-none' );
        $( '#save_richvideo_form [name=size]' ).val( file.size );
        $( '#save_richvideo_form [name=upload_video]' ).val( reader.result );

        $( '#richvideo_drop_zone [name=video_file]' ).val( '' );
        $( '#richvideo_drop_zone [name=upload_video]' ).parents( '.modal-body' ).next().find( '.cancel-button' ).trigger( 'click' );
    }
    reader.readAsDataURL( file );
}