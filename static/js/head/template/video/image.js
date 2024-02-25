$( function() {
    create_drop_zone( 'video', 'video' );

    $( '#video_display_area video' ).on( 'loadedmetadata', function() {
        var time = Math.floor($( '#video_display_area video' ).get(0).duration );
        let minite = Math.floor( time % 3600 / 60 );
        let second = time % 60;
        $( '#video_display_area .video-text-area .video-time' ).text( '時間 : ' + ( '00' + minite ).slice( -2 ) + ' : ' + ( '00' + second ).slice( -2 ) );
    });
});

upload.video = function( files ) {
    var file = files[0];
    if ( !error_video( file, 'message', '.error-message-video', 3 ) ) {
        return;
    }

    $( '.all-loader-area' ).removeClass( 'd-none' );
    var reader = new FileReader();
    reader.onload = function () {
        $( '#video_drop_zone' ).addClass( 'd-none' );
        $( '#video_display_area' ).removeClass( 'd-none' );
        $( '#video_display_area' ).find( 'video' ).attr( 'src', reader.result );
        $( '#video_display_area' ).find( '[name=upload_video]' ).val( reader.result );

        if ( file.size >= 1000000 ) {
            $( '#video_display_area' ).find( '.video-size' ).text( '容量 : ' + Math.ceil( file.size / 1000000 ) + 'MB' );
        } else if ( file.size >= 1000 ) {
            $( '#video_display_area' ).find( '.video-size' ).text( '容量 : ' + Math.ceil( file.size / 1000 ) + 'KB' );
        } else {
            $( '#video_display_area' ).find( '.video-size' ).text( '容量 : ' + file.size + 'B' );
        }
        $( '#video_display_area' ).find( '[name=size]' ).val( file.size );
        
        $( '#video_drop_zone [name=video_file]' ).val( '' );
    }
    reader.readAsDataURL( file );
}