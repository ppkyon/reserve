var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#save_facility_form' ).length ) {
        $( '#save_facility_form' ).parsley();
        $( '#save_facility_form' ).parsley().options.requiredMessage = "入力してください";
    }
    save_data.facility = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '.save-button' ).next().val() );
        form_data.append( 'count', $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).length );

        $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
            var random = $( this ).find( '.count-text' ).next().val();
            form_data.append( 'random_' + ( index + 1 ), random );
            form_data.append( 'name_' + ( index + 1 ), $( this ).find( 'input[name=name_' + random + ']' ).val() );
            form_data.append( 'count_' + ( index + 1 ), $( this ).find( 'input[name=count_' + random + ']' ).val() );
            form_data.append( 'order_' + ( index + 1 ), $( this ).find( 'input[name=order_' + random + ']' ).val() );
        });
        return form_data;
    }
    save_success.facility = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'facility' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.facility = function( message='' ) {
        
    };
});