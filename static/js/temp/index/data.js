var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    flatpickr( '.input-date', {
        "locale": "ja",
        dateFormat : 'Y/m/d',
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
    flatpickr( '.input-birth-date', {
        "locale": "ja",
        dateFormat : 'Y年m月d日',
    });

    $( '#save_user_form' ).parsley();
    $( '#save_user_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#save_user_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    $( '#save_user_form' ).parsley().options.patternMessage = "正しい形式で入力してください";

    save_data.user = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_user_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_user_form [name=name]' ).val() );
        form_data.append( 'name_kana', $( '#save_user_form [name=name_kana]' ).val() );
        form_data.append( 'birth', $( '#save_user_form [name=birth]' ).val().replace( '年', '-' ).replace( '月', '-' ).replace( '日', '' ) );
        form_data.append( 'age', $( '#save_user_form [name=age]' ).next().val() );
        form_data.append( 'sex', $( '#save_user_form [name=sex]' ).next().val() );
        form_data.append( 'phone_number', $( '#save_user_form [name=phone_number]' ).val() );
        form_data.append( 'email', $( '#save_user_form [name=email]' ).val() );
        form_data.append( 'memo', $( '#save_user_form [name=memo]' ).val() );
        var tag = [];
        $( '#save_user_form [name="tag[]"]' ).each( function( index, value ) {
            tag.push( $( this ).val() );
        });
        form_data.append( 'tag[]', tag );
        return form_data;
    };
    save_success.user = function(modal) {
        $( '#save_check_modal .yes-button' ).val('user');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.user = function(message='') {
        
    };
});