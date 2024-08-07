var upload = new Array();

$( function() {
    create_drop_zone( 'account', 'image' );
});

upload.account = function( files ) {
    var file = files[0];
    if ( !file.type.match( 'image.*' )) {
        $( '#account_drop_zone [name=image_file]' ).val( '' );
        return;
    }

    var reader = new FileReader();
    reader.onload = function () {
        $( '#profile_image' ).attr( 'src', reader.result );
        $( '#account_drop_zone [name=upload_image]' ).val( reader.result );
    }
    reader.readAsDataURL( file );
}

function create_drop_zone( name, type ) {
    $( '#' + name + '_drop_zone' ).on( 'click', function () {
        $( '#' + name + '_drop_zone [name=' + type + '_file]' )[0].click();
    });
    $( '#' + name + '_drop_zone [name=' + type + '_file]' ).on( 'change', function () {
        upload[name]( this.files );
    });

    $( '#' + name + '_drop_area' ).on( 'dragenter dragover', function ( event ) {
        event.stopPropagation();
        event.preventDefault();
        $( '.' + name + '-drop-zone' ).css( 'border', '2.5px solid #ced4da' );
        $( '.' + name + '-drop-zone' ).css( 'background-color', '#ced4da' );
    });
    $( '#' + name + '_drop_area' ).on( 'dragleave', function ( event ) {
        event.stopPropagation();
        event.preventDefault();
        $( '.' + name + '-drop-zone' ).css( 'border', '2.5px dashed #ced4da' );
        $( '.' + name + '-drop-zone' ).css( 'background-color', '#FFF' );
    });
    $( '#' + name + '_drop_area' ).on( 'drop', function ( event ) {
        event.preventDefault();
        $( '#' + name + '_drop_zone [name=' + type + '_file]' )[0].files = event.originalEvent.dataTransfer.files;
        upload[name]( $( '#' + name + '_drop_zone [name=' + type + '_file]' )[0].files );
        $( '.' + name + '-drop-zone' ).css( 'border', '2.5px dashed #ced4da' );
        $( '.' + name + '-drop-zone' ).css( 'background-color', '#FFF' );
    });
}

function error_image( file, name, error = '.error-message-image', size = 10000000 ) {
    if ( !file.type.match( 'image/jpg' ) && !file.type.match( 'image/jpeg' ) && !file.type.match( 'image/png' )) {
        $( '#' + name + '_drop_zone [name=image_file]' ).val( '' );
        $( error ).removeClass( 'd-none' );
        $( error + ' p' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return false;
    }
    if ( file.size > size ) {
        $( '#' + name + '_drop_zone [name=image_file]' ).val( '' );
        $( error ).removeClass( 'd-none' );
        $( error + ' p' ).each( function( index, value ) {
            if ( index == 1 ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
        });
        return false;
    }
    
    $( error ).addClass( 'd-none' );
    $( error + ' p' ).each( function( index, value ) {
        $( this ).addClass( 'd-none' );
    });
    return true;
}

function error_video( file, name, error = '.error-message-video', type = 1 ) {
    if ( type == 1 || type == 3 ) {
        if ( !file.type.match( 'video/mp4' )) {
            $( '#' + name + '_drop_zone [name=video_file]' ).val( '' );
            $( error ).removeClass( 'd-none' );
            $( error + ' p' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).removeClass( 'd-none' );
                } else {
                    $( this ).addClass( 'd-none' );
                }
            });
            return false;
        }
    } else if ( type == 2 ) {
        if ( !file.type.match( 'video/mp4' ) && !file.type.match( 'video/mov' ) && !file.type.match( 'video/wmv' ) ) {
            $( '#' + name + '_drop_zone [name=video_file]' ).val( '' );
            $( error ).removeClass( 'd-none' );
            $( error + ' p' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).removeClass( 'd-none' );
                } else {
                    $( this ).addClass( 'd-none' );
                }
            });
            return false;
        }
    }
    if ( type == 1 || type == 2 ) {
        if ( file.size > 200000000 ) {
            $( '#' + name + '_drop_zone [name=video_file]' ).val( '' );
            $( error ).removeClass( 'd-none' );
            $( error + ' p' ).each( function( index, value ) {
                if ( index == 1 ) {
                    $( this ).removeClass( 'd-none' );
                } else {
                    $( this ).addClass( 'd-none' );
                }
            });
            return false;
        }
    }
    
    $( error ).addClass( 'd-none' );
    $( error + ' p' ).each( function( index, value ) {
        $( this ).addClass( 'd-none' );
    });
    return true;
}