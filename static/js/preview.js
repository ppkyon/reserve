$( function() {
    $( '.line-preview .line-preview-content .line-preview-header' ).on( 'click', function() {
        if ( $( '.line-preview .line-preview-content' ).css( 'height' ) == '33px' ) {
            $( this ).find( 'img' ).css( 'transform', 'rotate(0deg)' );
            $( '.line-preview .line-preview-content' ).css( 'height', '100vh' );
        } else {
            $( this ).find( 'img' ).css( 'transform', 'rotate(-180deg)' );
            $( '.line-preview .line-preview-content' ).css( 'height', '33px' );
        }
    });
});