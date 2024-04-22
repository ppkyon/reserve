var upload = new Array();

$( function() {
    create_drop_zone( 'image_talk', 'image' );
    create_drop_zone( 'video_talk', 'video' );
});

upload.image_talk = function( files ) {
    var file = files[0];
    if ( !error_image( file, 'image_talk', '.error-message-talk-image' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#upload_image_modal .drop-zone' ).addClass( 'd-none' );
        $( '#upload_image_modal .drop-display-zone' ).removeClass( 'd-none' );
        $( '#upload_image_modal .send-button' ).removeClass( 'd-none' );

        $( '#upload_image_modal .drop-display-zone img' ).attr( 'src', reader.result );
        $( '#upload_image_modal [name=upload_image]' ).val( reader.result );
    }
    reader.readAsDataURL( file );
}

upload.video_talk = function( files ) {
    var file = files[0];
    if ( !error_video( file, 'video_talk', '.error-message-talk-video' ) ) {
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#upload_video_modal .drop-zone' ).addClass( 'd-none' );
        $( '#upload_video_modal .drop-display-zone' ).removeClass( 'd-none' );
        $( '#upload_video_modal .send-button' ).removeClass( 'd-none' );

        $( '#upload_video_modal .drop-display-zone video' ).attr( 'src', reader.result );
        $( '#upload_video_modal [name=upload_video]' ).val( reader.result );
    }
    reader.readAsDataURL( file );
}