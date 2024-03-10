var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#action_reminder_form' ).length ) {
        $( '#action_reminder_form' ).parsley();
        $( '#action_reminder_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#action_reminder_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
    }

    save_data.flow = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_flow_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_flow_form [name=name]' ).val() );
        if ( $( '#save_flow_form [name=valid]' ).prop( 'checked' ) ) {
            form_data.append( 'valid', 1 );
        } else {
            form_data.append( 'valid', 0 );
        }
        return form_data;
    };
    save_success.flow = function(modal) {
        $( '#error_period' ).addClass( 'd-none' );
        $( '#save_check_modal .yes-button' ).val('flow');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.flow = function(message='') {
        $( '#error_period' ).removeClass( 'd-none' );
    };
});