var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#save_menu_form' ).length ) {
        $( '#save_menu_form' ).parsley();
    }

    save_data.menu = function() {
        manager_list = []
        facility_list = []
        flow_list = []
        $( 'input[type=checkbox]' ).each( function( index, value ) {
            if ( !$( this ).hasClass( 'all-check' ) ) {
                if ( $( this ).attr( 'id' ).indexOf( 'manager' ) >= 0 ) {
                    if ( $( this ).prop( 'checked' ) ) {
                        manager_list.push($( this ).attr( 'id' ).replace('manager_', ''));
                    }
                } else if ( $( this ).attr( 'id' ).indexOf( 'facility' ) >= 0 ) {
                    if ( $( this ).prop( 'checked' ) ) {
                        facility_list.push($( this ).attr( 'id' ).replace('facility_', ''));
                    }
                } else if ( $( this ).attr( 'id' ).indexOf( 'flow' ) >= 0 ) {
                    if ( $( this ).prop( 'checked' ) ) {
                        flow_list.push($( this ).attr( 'id' ).replace('flow_', ''));
                    }
                }
            }
        });
        var form_data = new FormData();
        form_data.append( 'manager_list', manager_list );
        form_data.append( 'facility_list', facility_list );
        form_data.append( 'flow_list', flow_list );
        return form_data;
    }
    save_success.menu = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'menu' );
        $( '#save_check_modal .modal-description' ).text( '変更内容のカレンダーへの反映には10分程時間がかかる場合があります。' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.menu = function( message='' ) {
        
    };
});