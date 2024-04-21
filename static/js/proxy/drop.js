$( function() {
    $( document ).on( 'click', '.image-drop-zone', function () {
        $( this ).find( '.image-file' )[0].click();
    });
    $( document ).on( 'change', '.image-drop-zone .image-file', function () {
        upload_image( $( this ), this.files );
    });
    $( document ).on( 'click', '.drop-zone-wrap .image-delete-button', function () {
        $( this ).parents( '.drop-zone-wrap' ).find( '.drop-zone' ).removeClass( 'd-none' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone' ).addClass( 'd-none' );
    
        $( this ).prev().attr( 'src', '' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.image-file' ).val( '' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.image-upload-file' ).val( '' );
    });
    
    $( document ).on( 'click', '.video-drop-zone', function () {
        $( this ).find( '.video-file' )[0].click();
    });
    $( document ).on( 'change', '.video-drop-zone .video-file', function () {
        upload_video( $( this ), this.files );
    });
    $( document ).on( 'click', '.drop-zone-wrap .video-delete-button', function () {
        $( this ).parents( '.drop-zone-wrap' ).find( '.drop-zone' ).removeClass( 'd-none' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone' ).addClass( 'd-none' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.drop-zone-text-area' ).remove();
    
        $( this ).prev().attr( 'src', '' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.video-file' ).val( '' );
        $( this ).parents( '.drop-zone-wrap' ).find( '.video-upload-file' ).val( '' );
        $( this ).addClass( 'd-none' );
    });
});

function upload_image( target, files ) {
    var file = files[0];
    if ( !file.type.match( 'image/jpg' ) && !file.type.match( 'image/jpeg' ) && !file.type.match( 'image/png' ) && !file.type.match( 'application/pdf' )) {
        $( target ).val( '' );
        $( target ).parents( '.drop-zone-wrap' ).prev().removeClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return;
    }
    if ( file.size > 10000000 ) {
        $( target ).val( '' );
        $( target ).parents( '.drop-zone-wrap' ).prev().removeClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
            if ( index == 1 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return;
    }
    
    $( target ).parents( '.drop-zone-wrap' ).prev().addClass( 'd-none' );
    $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
        $( this ).addClass( 'd-none' );
    });
    
    var reader = new FileReader();
    reader.onload = function () {
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-zone' ).addClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone' ).removeClass( 'd-none' );
        
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone img' ).attr( 'src', reader.result );
        $( target ).parent().find( '.image-upload-file' ).val( reader.result );
    }
    reader.readAsDataURL( file );
}

function upload_video( target, files ) {
    var file = files[0];
    if ( !file.type.match( 'video/mp4' ) && !file.type.match( 'video/mov' ) && !file.type.match( 'video/wmv' ) && !file.type.match( 'video/quicktime' ) ) {
        $( target ).val( '' );
        $( target ).parents( '.drop-zone-wrap' ).prev().removeClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return;
    }
    if ( file.size > 200000000 ) {
        $( target ).val( '' );
        $( target ).parents( '.drop-zone-wrap' ).prev().removeClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
            if ( index == 1 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return;
    }
    
    $( target ).parents( '.drop-zone-wrap' ).prev().addClass( 'd-none' );
    $( target ).parents( '.drop-zone-wrap' ).prev().find( 'p' ).each( function( index, value ) {
        $( this ).addClass( 'd-none' );
    });

    var reader = new FileReader();
    reader.onload = function () {
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-zone' ).addClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).find( '.video-delete-button' ).removeClass( 'd-none' );
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone' ).removeClass( 'd-none' );
        
        if ( file.type.match( 'video/quicktime' ) ) {
            $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone video' ).addClass( 'd-none' );
            var html = '<div class="drop-zone-text-area" style="border: 2px dashed rgba(0,0,0,0.3);">';
            html += '<div class="mx-auto mb-2">';
            html += '<i class="mdi mdi-check-circle-outline text-success display-4" style="font-size: 83.5px;"></i>';
            html += '</div>';
            html += '<p class="mb-1" style="font-size: 16px; font-weight: bold;">動画のアップロードを完了しました。</p>';
            html += '<p style="color: red; font-size: 16px; font-weight: bold; text-decoration: underline;">※動画の提出はまだ完了していません。</p>';
            html += '</div>';
            $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone' ).append( html );
        }
        $( target ).parents( '.drop-zone-wrap' ).find( '.drop-display-zone video' ).attr( 'src', reader.result.replace( 'quicktime', 'mp4' ) + '#t=0.001' );
        $( target ).parent().find( '.video-upload-file' ).val( reader.result );
    }
    reader.readAsDataURL( file );
}