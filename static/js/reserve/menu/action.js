$( function() {
    $( document ).on( 'click', '.all-check', function () {
        var target = $( this );
        var target_id = $( this ).attr( 'id' ).substr( $( this ).attr( 'id' ).lastIndexOf( '_' ) + 1 );
        $( 'input[type=checkbox]' ).each( function( index, value ) {
            if ( !$( this ).hasClass( 'all-check' ) ) {
                if ( target_id == $( this ).attr( 'id' ).substr( $( this ).attr( 'id' ).lastIndexOf( '_' ) + 1 ) ) {
                    if ( $( target ).prop( 'checked' ) ) {
                        $( this ).prop( 'checked', true );
                    } else {
                        $( this ).prop( 'checked', false );
                    }
                }
            }
        });
    });
});