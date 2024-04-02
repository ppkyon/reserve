var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#save_data_form' ).length ) {
        $( '#save_data_form' ).parsley();
    }

    save_data.data = function() {
        var form_data = new FormData();
        form_data.append( 'auto_flg', $( '#save_data_form [name=auto_flg]:checked' ).val() );
        return form_data;
    }
    save_success.data = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'data' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.data = function( message='' ) {
        
    };
});