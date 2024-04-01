var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#save_basic_form' ).length ) {
        $( '#save_basic_form' ).parsley();
        $( '#save_basic_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.basic = function() {
        var form_data = new FormData();
        form_data.append( 'start', $( '#save_basic_form [name=start]' ).next().val() );
        form_data.append( 'deadline', $( '#save_basic_form [name=deadline]:checked' ).val() );
        form_data.append( 'on_time', $( '#save_basic_form [name=on_time]' ).next().val() );
        form_data.append( 'any_day', $( '#save_basic_form [name=any_day]' ).next().val() );
        form_data.append( 'any_time', $( '#save_basic_form [name=any_time]' ).next().val() );
        form_data.append( 'method', $( '#save_basic_form [name=method]' ).next().val() );
        form_data.append( 'unit', $( '#save_basic_form [name=unit]:checked' ).val() );
        for ( var i = 1; i <= 7; i++ ) {
            if ( $( '#save_basic_form [name=business_check_' + i + ']' ).prop( 'checked' ) ) {
                form_data.append( 'business_check_' + i + '', 1 );
            } else {
                form_data.append( 'business_check_' + i + '', 0 );
            }
        }
        return form_data;
    }
    save_success.basic = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'basic' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.basic = function( message='' ) {
        
    };
});