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

    
    if ( $( '#save_place_form' ).length ) {
        $( '#save_place_form' ).parsley();
    }

    save_data.place = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_place_form [name=setting]' ).next().val() );
        form_data.append( 'year', $( '#save_place_form [name=year]' ).val() );
        form_data.append( 'month', $( '#save_place_form [name=month]' ).val() );

        var day_count = 0;
        $( '.calendar-table tbody td' ).each( function( index, value ) {
            if ( $( this ).find( '.setting-not-check' ).length ) {
                var day = $( this ).find( '.setting-not-check' ).val();
                var input_count = 0;
                if ( $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked' ) ) {
                    form_data.append( 'setting_not_' + day, 1 );
                    form_data.append( 'setting_input_count_' + day, 1 );
                } else {
                    form_data.append( 'setting_not_' + day, 0 );
                    for ( var i = 1; i <= $( this ).find( '.d-flex' ).length - 2; i++ ) {
                        form_data.append( 'setting_from_' + day + '_' + i, $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).val() );
                        form_data.append( 'setting_to_' + day + '_' + i, $( '#save_place_form [name=setting_to_' + day + '_' + i + ']' ).val() );
                        input_count++;
                    }
                    form_data.append( 'setting_count_' + day, $( '#save_place_form [name=setting_count_' + day + ']' ).val() );
                    form_data.append( 'setting_input_count_' + day, input_count );
                }
                day_count++;
            }
        });
        form_data.append( 'day', day_count );
        return form_data;
    }
    save_success.place = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'place' );
        $( '#save_check_modal .modal-description' ).text( '変更内容のカレンダーへの反映には10分程時間がかかる場合があります。' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.place = function( message='' ) {
        $.each( message, function( index, value ) {
            $( '#save_place_form [name=setting_from_' + value + ']' ).addClass( 'parsley-error' );
            $( '#save_place_form [name=setting_to_' + value + ']' ).addClass( 'parsley-error' );
        });
    };
});