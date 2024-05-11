var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    flatpickr( '.input-time', {
        "locale": "ja",
        enableTime: true,
        noCalendar: true,
        dateFormat : 'H:i',
        minuteIncrement: 15,
        onReady: function(dateObj, dateStr, instance) {
            const clearButton = document.createElement("div");
            clearButton.innerHTML = "クリア";
            clearButton.classList.add("clear-button");
            clearButton.style.cursor = "pointer";
            clearButton.addEventListener("click", function() {
                instance.clear();
            });
            instance.calendarContainer.appendChild(clearButton);
        }
    });
    
    if ( $( '#save_manager_form' ).length ) {
        $( '#save_manager_form' ).parsley();
    }

    save_data.manager = function() {
        var form_data = new FormData();
        form_data.append( 'year', $( '#save_manager_form [name=year]' ).val() );
        form_data.append( 'month', $( '#save_manager_form [name=month]' ).val() );
        $( '.manager-table tbody tr td' ).each( function( index, value ) {
            var setting = $( this ).children( 'input[type=hidden]' ).eq(0).val();
            var manager = $( this ).children( 'input[type=hidden]' ).eq(1).val();
            var day = $( this ).children( 'input[type=hidden]' ).eq(2).val();
            if ( $( this ).find( '.data-area input[type=hidden]' ).length > 0 ) {
                form_data.append( 'flg_' + setting + '_' + manager + '_' + day, $( '#save_manager_form [name="flg_' + setting + '_' + manager + '_' + day + '"]' ).val() );

                var data_count = 0;
                $( this ).find( '.data-area input[type=hidden]' ).each( function( index, value ) {
                    if ( $( this ).attr( 'name' ).indexOf( 'from' ) !== -1 ) {
                        data_count++;
                        form_data.append( 'from_' + setting + '_' + manager + '_' + day + '_' + data_count, $( '#save_manager_form [name="from_' + setting + '_' + manager + '_' + day + '_' + data_count + '"]' ).val() );
                        form_data.append( 'to_' + setting + '_' + manager + '_' + day + '_' + data_count, $( '#save_manager_form [name="to_' + setting + '_' + manager + '_' + day + '_' + data_count + '"]' ).val() );

                        var tmp = $( this );
                        $( '#manager_input_form .input-check-wrap' ).each( function( index, value ) {
                            var name = $( this ).find( 'input[type=checkbox]' ).attr( 'name' );
                            if ( name.substring( name.lastIndexOf('_')+1 ) == '1' ) {
                                name = name.substring( 0, name.lastIndexOf('_') );
                                if ( $( '#save_manager_form [name="' + name + '_' + setting + '_' + manager + '_' + day + '_' + data_count + '"]' ).val() == 'false' ) {
                                    form_data.append( name + '_' + setting + '_' + manager + '_' + day + '_' + data_count, false );
                                } else {
                                    form_data.append( name + '_' + setting + '_' + manager + '_' + day + '_' + data_count, true );
                                }
                            }
                        });
                    }
                });
                form_data.append( 'count_' + setting + '_' + manager + '_' + day, data_count );
            }
        });
        return form_data;
    }
    save_success.manager = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'manager' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.manager = function( message='' ) {
        
    };
});