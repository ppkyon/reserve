$( function() {
    create_preview();
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview($( this ).find( '[name=id]' ).val());
    });

    $( '#save_richvideo_form .title-area img' ).on( 'click', function() {
        $( '#save_richvideo_form .title-area img' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'd-none' ) ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
            if ( $( this ).attr( 'src' ).indexOf( 'color' ) !== -1 ) {
                if ( $( this ).hasClass( 'd-none' ) ) {
                    $( '#save_richvideo_form [name=favorite]' ).prop( 'checked', false );
                } else {
                    $( '#save_richvideo_form [name=favorite]' ).prop( 'checked', true );
                }
            } else {
                if ( $( this ).hasClass( 'd-none' ) ) {
                    $( '#save_richvideo_form [name=favorite]' ).prop( 'checked', true );
                } else {
                    $( '#save_richvideo_form [name=favorite]' ).prop( 'checked', false );
                }
            }
        });
    });

    $( '#save_richvideo_form .template-area' ).on( 'click', function() {
        $( '#upload_template_video' ).trigger( 'click' );
    });
    $( '#upload_template_video' ).on( 'click', function(){
        $( this ).next().trigger( 'click' );
    });
    $( '#richvideo_upload_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });
    $( '#save_richvideo_form .video-text-area video' ).on( 'loadedmetadata', function() {
        var time = Math.floor($( '#save_richvideo_form .template-area video' ).get(0).duration );
        let minite = Math.floor( time % 3600 / 60 );
        let second = time % 60;

        create_preview();
        $( '#save_richvideo_form .video-text-area .video-time' ).text( '時間 : ' + ( '00' + minite ).slice( -2 ) + ' : ' + ( '00' + second ).slice( -2 ) );
    });

    $( '#save_richvideo_form [name=action]' ).on( 'change', function() {
        $( '#save_richvideo_form .display-area' ).each( function( index, value ) {
            if ( index > 0 ) {
                $( value ).remove();
            }
        });
        if ( $( '#save_richvideo_form [name=action]:checked' ).val() == '1' ) {
            append_display_area( null, null );
        }
    });

    $( document ).on( 'focus', '#save_richvideo_form [name=custom]', function () {
        $( '#save_richvideo_form [name=text]:eq(12)' ).prop( 'checked', true );
    });
    $( document ).on( 'click', '#save_richvideo_form [name=text]', function () {
        if ( $( '#save_richvideo_form [name=text]:checked' ).val() == '12' ) {
            $( '#save_richvideo_form [name=custom]' ).attr( 'required', true );
        } else {
            $( '#save_richvideo_form [name=custom]' ).attr( 'required', false );
        }
    });
});