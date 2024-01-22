$( function() {
    $( document ).on( 'click', '.input-select-dropdown .dropdown-item', function () {
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).val( $( this ).text() );
        $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).val( $( this ).val() );
    });
});