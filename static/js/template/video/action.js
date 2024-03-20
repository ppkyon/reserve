$( function() {
    create_preview();

    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview( $( this ).find( '[name=id]' ).val() );
    });

    $( '#save_video_form .title-area img' ).on( 'click', function() {
        $( '#save_video_form .title-area img' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'd-none' ) ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
            if ( $( this ).attr( 'src' ).indexOf( 'color' ) !== -1 ) {
                if ( $( this ).hasClass( 'd-none' ) ) {
                    $( '#save_video_form [name=favorite]' ).prop( 'checked', false );
                } else {
                    $( '#save_video_form [name=favorite]' ).prop( 'checked', true );
                }
            } else {
                if ( $( this ).hasClass( 'd-none' ) ) {
                    $( '#save_video_form [name=favorite]' ).prop( 'checked', true );
                } else {
                    $( '#save_video_form [name=favorite]' ).prop( 'checked', false );
                }
            }
        });
    });

    $( '#video_display_area .delete-button' ).on( 'click', function() {
        $( '#video_drop_zone [name=video_file]' ).val( '' );
        $( '#video_display_area [name=upload_video]' ).val( '' );
        $( '#video_display_area video' ).attr( 'src', '' );
        
        $( '#video_drop_zone' ).removeClass( 'd-none' );
        $( '#video_display_area' ).addClass( 'd-none' );
        create_preview();
    });
});