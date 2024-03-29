var change_data = new Array();
var change_success = new Array();
var change_error = new Array();
var add_data = new Array();
var add_success = new Array();
var add_error = new Array();
var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();

$( function() {
    flatpickr( '.input-time', {
        "locale": "ja",
        enableTime: true,
        noCalendar: true,
        dateFormat: 'H:i',
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

    $( '#change_email_form' ).parsley();
    $( '#change_email_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#change_email_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    $( '#change_password_form' ).parsley();
    $( '#change_password_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#change_password_form' ).parsley().options.equaltoMessage = "パスワードが一致していません";
    $( '#change_password_form' ).parsley().options.minlengthMessage = "8文字以上で入力してください";

    $( '#add_manager_form' ).parsley();
    $( '#add_manager_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#add_manager_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    $( '#save_manager_form' ).parsley();
    $( '#save_manager_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#save_manager_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
    $( '#save_manager_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    
    $( '#add_offline_form' ).parsley();
    $( '#add_offline_form' ).parsley().options.requiredMessage = "入力してください";
    
    $( '#add_online_form' ).parsley();
    $( '#add_online_form' ).parsley().options.requiredMessage = "入力してください";

    change_data.email = function() {
        var form_data = new FormData();
        form_data.append( 'email', $( '#change_email_form [name=email]' ).val() );
        form_data.append( 'password', $( '#change_email_form [name=password]' ).val() );
        return form_data;
    };
    change_success.email = function(modal) {
        $( '#change_email_form .error-message-area' ).removeClass( 'd-block' );
        $( '#change_email_form .error-message-area' ).addClass( 'd-none' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    change_error.email = function(message='') {
        $( '#change_email_form .error-message' ).text( message );
        $( '#change_email_form .error-message-area' ).removeClass( 'd-none' );
        $( '#change_email_form .error-message-area' ).addClass( 'd-block' );
    };

    change_data.password = function() {
        var form_data = new FormData();
        form_data.append( 'now_password', $( '#change_password_form [name=now_password]' ).val() );
        form_data.append( 'new_password', $( '#change_password_form [name=new_password]' ).val() );
        return form_data;
    };
    change_success.password = function(modal) {
        $( '#change_password_form .error-message-area' ).removeClass( 'd-block' );
        $( '#change_password_form .error-message-area' ).addClass( 'd-none' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    change_error.password = function(message='') {
        $( '#change_password_form .error-message' ).text( message );
        $( '#change_password_form .error-message-area' ).removeClass( 'd-none' );
        $( '#change_password_form .error-message-area' ).addClass( 'd-block' );
    };

    add_data.manager = function() {
        var form_data = new FormData();
        form_data.append( 'family_name', $( '#add_manager_form [name=family_name]' ).val() );
        form_data.append( 'first_name', $( '#add_manager_form [name=first_name]' ).val() );
        form_data.append( 'family_name_kana', $( '#add_manager_form [name=family_name_kana]' ).val() );
        form_data.append( 'first_name_kana', $( '#add_manager_form [name=first_name_kana]' ).val() );
        form_data.append( 'authority', $( '#add_manager_form [name=authority]:checked' ).val() );
        return form_data;
    };
    add_success.manager = function(modal) {
        $( '#add_check_modal .yes-button' ).val( 'manager' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    add_error.manager = function(message='') {
        
    };

    save_data.manager = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_manager_form [name=id]' ).val() );
        form_data.append( 'image_file', $( '#save_manager_form [name=image_file]' )[0].files[0] );
        form_data.append( 'family_name', $( '#save_manager_form [name=family_name]' ).val() );
        form_data.append( 'first_name', $( '#save_manager_form [name=first_name]' ).val() );
        form_data.append( 'family_name_kana', $( '#save_manager_form [name=family_name_kana]' ).val() );
        form_data.append( 'first_name_kana', $( '#save_manager_form [name=first_name_kana]' ).val() );
        form_data.append( 'phone_number', $( '#save_manager_form [name=phone_number]' ).val() );
        form_data.append( 'department', $( '#save_manager_form [name=department]' ).val() );
        form_data.append( 'job', $( '#save_manager_form [name=job]' ).val() );
        form_data.append( 'work', $( '#save_manager_form [name=work]' ).val() );
        if ( check_empty( $( '#save_manager_form [name=age]' ).next().val() ) ) {
            form_data.append( 'age', $( '#save_manager_form [name=age]' ).next().val() );
        } else {
            form_data.append( 'age', '0' );
        }
        if ( check_empty( $( '#save_manager_form [name=sex]' ).next().val() ) ) {
            form_data.append( 'sex', $( '#save_manager_form [name=sex]' ).next().val() );
        } else {
            form_data.append( 'sex', '0' );
        }
        if ( check_empty( $( '#save_manager_form [name=setting]' ).val() ) ) {
            form_data.append( 'setting', $( '#save_manager_form [name=setting]' ).next().val() );
            for ( var i = 1; i <= 8; i++ ) {
                form_data.append( 'time_count_' + i, $( '#save_manager_form [name*=time_from_' + i + ']' ).length );
                for ( var j = 1; j <= $( '#save_manager_form [name*=time_from_' + i + ']' ).length; j++ ) {
                    form_data.append( 'time_from_' + i + '_' + j, $( '#save_manager_form [name=time_from_' + i + '_' + j + ']' ).val() );
                    form_data.append( 'time_to_' + i + '_' + j, $( '#save_manager_form [name=time_to_' + i + '_' + j + ']' ).val() );
                }
                if ( $( '#save_manager_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                    form_data.append( 'time_check_' + i, 1 );
                } else {
                    form_data.append( 'time_check_' + i, 0 );
                }
                if ( $( '#save_manager_form [name=calendar_check_' + i + ']' ).prop( 'checked' ) ) {
                    form_data.append( 'calendar_check_' + i, 1 );
                } else {
                    form_data.append( 'calendar_check_' + i, 0 );
                }
            }
        }
        return form_data;
    };
    save_data.manager = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_manager_' + id + '_form [name=id]' ).val() );
        form_data.append( 'family_name', $( '#save_manager_' + id + '_form [name=family_name]' ).val() );
        form_data.append( 'first_name', $( '#save_manager_' + id + '_form [name=first_name]' ).val() );
        form_data.append( 'family_name_kana', $( '#save_manager_' + id + '_form [name=family_name_kana]' ).val() );
        form_data.append( 'first_name_kana', $( '#save_manager_' + id + '_form [name=first_name_kana]' ).val() );
        form_data.append( 'phone_number', $( '#save_manager_' + id + '_form [name=phone_number]' ).val() );
        form_data.append( 'department', $( '#save_manager_' + id + '_form [name=department]' ).val() );
        form_data.append( 'job', $( '#save_manager_' + id + '_form [name=job]' ).val() );
        form_data.append( 'work', $( '#save_manager_' + id + '_form [name=work]' ).val() );
        if ( check_empty( $( '#save_manager_' + id + '_form [name=age]' ).next().val() ) ) {
            form_data.append( 'age', $( '#save_manager_' + id + '_form [name=age]' ).next().val() );
        } else {
            form_data.append( 'age', '0' );
        }
        if ( check_empty( $( '#save_manager_' + id + '_form [name=sex]' ).next().val() ) ) {
            form_data.append( 'sex', $( '#save_manager_' + id + '_form [name=sex]' ).next().val() );
        } else {
            form_data.append( 'sex', '0' );
        }
        if ( check_empty( $( '#save_manager_' + id + '_form [name=setting]' ).val() ) ) {
            form_data.append( 'setting', $( '#save_manager_' + id + '_form [name=setting]' ).next().val() );
            for ( var i = 1; i <= 8; i++ ) {
                form_data.append( 'time_count_' + i, $( '#save_manager_' + id + '_form [name*=time_from_' + i + ']' ).length );
                for ( var j = 1; j <= $( '#save_manager_' + id + '_form [name*=time_from_' + i + ']' ).length; j++ ) {
                    form_data.append( 'time_from_' + i + '_' + j, $( '#save_manager_' + id + '_form [name=time_from_' + i + '_' + j + ']' ).val() );
                    form_data.append( 'time_to_' + i + '_' + j, $( '#save_manager_' + id + '_form [name=time_to_' + i + '_' + j + ']' ).val() );
                }
                if ( $( '#save_manager_' + id + '_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                    form_data.append( 'time_check_' + i, 1 );
                } else {
                    form_data.append( 'time_check_' + i, 0 );
                }
                if ( $( '#save_manager_' + id + '_form [name=calendar_check_' + i + ']' ).prop( 'checked' ) ) {
                    form_data.append( 'calendar_check_' + i, 1 );
                } else {
                    form_data.append( 'calendar_check_' + i, 0 );
                }
            }
        }
        return form_data;
    };
    save_success.manager = function(modal, value) {
        $( '#save_check_modal .yes-button' ).val(value);
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.manager = function(message='') {
        
    };

    delete_data.manager = function(id) {
        if ( id ) {
            var form_data = new FormData();
            form_data.append( 'id', $( '#delete_manager_' + id + '_form [name=id]' ).val() );
            return form_data;
        } else {
            var form_data = new FormData();
            form_data.append( 'id', $( '#delete_manager_form [name=id]' ).val() );
            return form_data;
        }
    };

    save_data.authority = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_authority_' + id + '_form [name=id]' ).val() );
        form_data.append( 'authority', $( '#save_authority_' + id + '_form [name=authority]:checked' ).val() );
        return form_data;
    };
    save_success.authority = function(modal, value) {
        $( '#save_check_modal .yes-button' ).val(value);
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.authority = function(id, message='') {
        
    };

    add_data.offline = function() {
        var form_data = new FormData();
        form_data.append( 'title', $( '#add_offline_form [name=title]' ).val() );
        form_data.append( 'name', $( '#add_offline_form [name=name]' ).val() );
        form_data.append( 'address', $( '#add_offline_form [name=address]' ).val() );
        form_data.append( 'note', $( '#add_offline_form [name=note]' ).val() );
        for ( var i = 1; i <= 8; i++ ) {
            form_data.append( 'time_count_' + i, $( '#add_offline_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length );
            for ( var j = 1; j <= $( '#add_offline_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length; j++ ) {
                var target = i + '_' + j;
                form_data.append( 'time_from_' + target, $( '#add_offline_form [name=time_from_' + target + ']' ).val() );
                form_data.append( 'time_to_' + target, $( '#add_offline_form [name=time_to_' + target + ']' ).val() );
            }
            if ( $( '#add_offline_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                form_data.append( 'time_check_' + i, 1 );
            } else {
                form_data.append( 'time_check_' + i, 0 );
            }
        }
        return form_data;
    };
    add_success.offline = function(modal) {
        $( '#add_check_modal .modal-description-area' ).addClass( 'd-none' );
        $( '#add_check_modal .yes-button' ).val( 'offline' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    add_error.offline = function(message='') {
        $.each( message, function( index, value ) {
            $( '#add_offline_form [name=time_from_' + value + ']' ).addClass( 'parsley-error' );
            $( '#add_offline_form [name=time_to_' + value + ']' ).addClass( 'parsley-error' );
        });
    };

    add_data.online = function() {
        var form_data = new FormData();
        form_data.append( 'title', $( '#add_online_form [name=title]' ).val() );
        form_data.append( 'name', $( '#add_online_form [name=name]' ).val() );
        form_data.append( 'outline', $( '#add_online_form [name=outline]' ).val() );
        form_data.append( 'note', $( '#add_online_form [name=note]' ).val() );
        for ( var i = 1; i <= 8; i++ ) {
            form_data.append( 'time_count_' + i, $( '#add_online_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length );
            for ( var j = 1; j <= $( '#add_online_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length; j++ ) {
                var target = i + '_' + j;
                form_data.append( 'time_from_' + target, $( '#add_online_form [name=time_from_' + target + ']' ).val() );
                form_data.append( 'time_to_' + target, $( '#add_online_form [name=time_to_' + target + ']' ).val() );
            }
            if ( $( '#add_online_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                form_data.append( 'time_check_' + i, 1 );
            } else {
                form_data.append( 'time_check_' + i, 0 );
            }
        }
        return form_data;
    };
    add_success.online = function(modal) {
        $( '#add_check_modal .modal-description-area' ).addClass( 'd-none' );
        $( '#add_check_modal .yes-button' ).val( 'online' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    add_error.online = function(message='') {
        $.each( message, function( index, value ) {
            $( '#add_online_form [name=time_from_' + value + ']' ).addClass( 'parsley-error' );
            $( '#add_online_form [name=time_to_' + value + ']' ).addClass( 'parsley-error' );
        });
    };

    save_data.offline = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_offline_' + id + '_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_offline_' + id + '_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_offline_' + id + '_form [name=name]' ).val() );
        form_data.append( 'address', $( '#save_offline_' + id + '_form [name=address]' ).val() );
        form_data.append( 'note', $( '#save_offline_' + id + '_form [name=note]' ).val() );
        for ( var i = 1; i <= 8; i++ ) {
            form_data.append( 'time_count_' + i, $( '#save_offline_' + id + '_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length );
            for ( var j = 1; j <= $( '#save_offline_' + id + '_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length; j++ ) {
                var target = i + '_' + j;
                form_data.append( 'time_from_' + target, $( '#save_offline_' + id + '_form [name=time_from_' + target + ']' ).val() );
                form_data.append( 'time_to_' + target, $( '#save_offline_' + id + '_form [name=time_to_' + target + ']' ).val() );
            }
            if ( $( '#save_offline_' + id + '_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                form_data.append( 'time_check_' + i, 1 );
            } else {
                form_data.append( 'time_check_' + i, 0 );
            }
        }
        return form_data;
    };
    save_success.offline = function(modal, value) {
        $( '#save_check_modal .yes-button' ).val( value );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.offline = function(message='', id) {
        $.each( message, function( index, value ) {
            $( '#save_offline_' + id + '_form [name=time_from_' + value + ']' ).addClass( 'parsley-error' );
            $( '#save_offline_' + id + '_form [name=time_to_' + value + ']' ).addClass( 'parsley-error' );
        });
    };

    save_data.online = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_online_' + id + '_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_online_' + id + '_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_online_' + id + '_form [name=name]' ).val() );
        form_data.append( 'outline', $( '#save_online_' + id + '_form [name=outline]' ).val() );
        form_data.append( 'note', $( '#save_online_' + id + '_form [name=note]' ).val() );
        for ( var i = 1; i <= 8; i++ ) {
            form_data.append( 'time_count_' + i, $( '#save_online_' + id + '_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length );
            for ( var j = 1; j <= $( '#save_online_' + id + '_form [name=time_check_' + i + ']' ).parents( '.time-area' ).children( '.d-flex' ).length; j++ ) {
                var target = i + '_' + j;
                form_data.append( 'time_from_' + target, $( '#save_online_' + id + '_form [name=time_from_' + target + ']' ).val() );
                form_data.append( 'time_to_' + target, $( '#save_online_' + id + '_form [name=time_to_' + target + ']' ).val() );
            }
            if ( $( '#save_online_' + id + '_form [name=time_check_' + i + ']' ).prop( 'checked' ) ) {
                form_data.append( 'time_check_' + i, 1 );
            } else {
                form_data.append( 'time_check_' + i, 0 );
            }
        }
        return form_data;
    };
    save_success.online = function(modal, value) {
        $( '#save_check_modal .yes-button' ).val( value );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.online = function(message='', id) {
        $.each( message, function( index, value ) {
            $( '#save_online_' + id + '_form [name=time_from_' + value + ']' ).addClass( 'parsley-error' );
            $( '#save_online_' + id + '_form [name=time_to_' + value + ']' ).addClass( 'parsley-error' );
        });
    };

    delete_data.offline = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_offline_' + id + '_form [name=id]' ).val() );
        return form_data;
    };
    delete_data.online = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_online_' + id + '_form [name=id]' ).val() );
        return form_data;
    };
});