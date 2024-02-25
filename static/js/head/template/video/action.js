$( function() {
    $( '#video_display_area .delete-button' ).on( 'click', function() {
        $( '#video_drop_zone [name=video_file]' ).val( '' );
        $( '#video_display_area [name=upload_video]' ).val( '' );
        $( '#video_display_area video' ).attr( 'src', '' );
        
        $( '#video_drop_zone' ).removeClass( 'd-none' );
        $( '#video_display_area' ).addClass( 'd-none' );
    });
});