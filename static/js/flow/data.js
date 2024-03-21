var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    flatpickr( '#period_from', {
        "locale": "ja",
        dateFormat : 'Y/m/d H:i',
        enableTime  : true,
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
    flatpickr( '#period_to', {
        "locale": "ja",
        dateFormat : 'Y/m/d H:i',
        enableTime  : true,
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

    if ( $( '#save_flow_form' ).length ) {
        $( '#save_flow_form' ).parsley();
        $( '#save_flow_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.flow = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_flow_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_flow_form [name=name]' ).val() );
        form_data.append( 'period_from', $( '#save_flow_form [name=period_from]' ).val() );
        form_data.append( 'period_to', $( '#save_flow_form [name=period_to]' ).val() );
        form_data.append( 'flow', $( '#save_flow_form [name=flow]' ).val() );
        if ( $( '#save_flow_form [name=favorite]' ).prop( 'checked' ) ) {
            form_data.append( 'favorite', 1 );
        } else {
            form_data.append( 'favorite', 0 );
        }
        return form_data;
    }
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