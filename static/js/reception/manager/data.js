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
                form_data.append( 'count_' + setting + '_' + manager + '_' + day, ( $( this ).find( '.data-area input[type=hidden]' ).length - 1 ) / 2 );
                for ( var i = 1; i <= ( $( this ).find( '.data-area input[type=hidden]' ).length - 1 ) / 2; i++ ) {
                    form_data.append( 'from_' + setting + '_' + manager + '_' + day + '_' + i, $( '#save_manager_form [name="from_' + setting + '_' + manager + '_' + day + '_' + i + '"]' ).val() );
                    form_data.append( 'to_' + setting + '_' + manager + '_' + day + '_' + i, $( '#save_manager_form [name="to_' + setting + '_' + manager + '_' + day + '_' + i + '"]' ).val() );
                }
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