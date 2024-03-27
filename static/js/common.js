$( function() {
    $( '[data-bs-toggle="tooltip"]' ).tooltip();
});

function check_empty( data ) {
    if ( data != null && data != undefined && data != '' ) {
        return true;
    } else {
        return false;
    }
}