$( function(){
    $( document ).on( 'click', '.history-area .tab-area .nav-link', function () {
        $( '.history-area .tab-area .nav-link' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                $( this ).find( 'img' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).addClass( 'd-none' );
                    } else if ( index == 1 ) {
                        $( this ).removeClass( 'd-none' );
                    }
                });
            } else {
                $( this ).find( 'img' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).removeClass( 'd-none' );
                    } else if ( index == 1 ) {
                        $( this ).addClass( 'd-none' );
                    }
                });
            }
        });
    });
});