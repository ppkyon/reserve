$( function() {
    $( '#display_qrcode_modal .copy-button' ).on( 'click', function() {
        var toast = $( this ).next().find( '.toast' );
        $( toast ).addClass( 'show' );

        var text = $( this ).prev().val();
        var $textarea = $('<textarea></textarea>');
        $textarea.text( text );
        $( this ).append( $textarea );
        $textarea.select();
        document.execCommand( 'copy' );
        $textarea.remove();

        setTimeout( function() {
            $( toast ).removeClass( 'show' );
        }, 2500 );
    });

    $( '#change_email_modal .action-button' ).on( 'click', function() {
        if ( $( '#change_email_form' ).parsley().validate() ) {
            var target = $( this );
            $.ajax({
                'data': change_data['email'](),
                'url': $( '#change_email_check_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    change_success['email']($( target ).next());
                } else {
                    change_error['email'](response.message);
                }
            }).fail( function(){
                change_error['email']('メールアドレスの変更に失敗しました');
            });
        }
    });
    $( '#change_email_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        
        $( '#change_email_check_modal .no-button' ).trigger( 'click' );
        $.ajax({
            'data': change_data['email'](),
            'url': $( '#change_email_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#change_email_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#change_email_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'change_email' );

    $( '#change_password_modal .action-button' ).on( 'click', function() {
        if ( $( '#change_password_form' ).parsley().validate() ) {
            var next = $( this ).next();
            $.ajax({
                'data': change_data['password'](),
                'url': $( '#change_password_check_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    change_success['password'](next);
                } else {
                    change_error['password']('パスワードが間違っています')
                }
            }).fail( function(){
                change_error['password']('パスワードの変更に失敗しました')
            });
        }
    });
    $( '#change_password_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        
        $( '#change_password_check_modal .no-button' ).trigger( 'click' );
        $.ajax({
            'data': change_data['password'](),
            'url': $( '#change_password_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#change_password_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#change_password_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'change_password' );

    $( '.detail-manager-modal .reset-button' ).on( 'click', function() {
        if ( $( '#detail_manager_' + $( this ).val() + '_modal [name=password]' ).length ) {
            $( '#reset_password_check_modal .modal-description-area' ).addClass( 'd-none' );
            $( '#reset_password_success_modal .modal-title' ).text( 'パスワードリセットが完了しました' );
        } else {
            $( '#reset_password_check_modal .modal-description-area' ).removeClass( 'd-none' );
            $( '#reset_password_success_modal .modal-title' ).text( 'パスワードリセットメールを送信しました' );
        }
        $( '#reset_password_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( '#reset_password_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        $( '#reset_password_check_modal .no-button' ).trigger( 'click' );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#reset_password_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#reset_password_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#reset_password_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'reset_password' );

    $( '.search-setting-dropdown .dropdown-menu button' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#serach_setting_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            window.location.reload();
        }).fail( function(){
            window.location.reload();
        });
    });

    $( '.manager-setting-dropdown .dropdown-menu button' ).on( 'click', function() {
        var target = $( this );
        var form = $( this ).parents( 'form' );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        form_data.append( 'manager_id', $( this ).parents( '.modal' ).find( '[name=id]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_setting_time_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            var last_week = '';
            $( target ).parents( '.modal' ).find( '.time-area-wrap' ).empty();
            $.each( response.time, function( index, value ){
                if ( last_week == value.week ) {
                    var html = '<div class="content mb-2">';
                    html += '<div class="row">';
                    html += '<div class="col-12">';
                    html += '<div class="d-flex align-items-center justify-content-start">';
                    html += '<div style="width: 20%;"></div>';
                    html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;"></label>';
                    html += '<div class="time-area" style="width: 97.5%;">';
                    html += '<div class="d-flex align-items-center justify-content-start">';
                    html += '<input type="text" name="time_from_' + value.week + '_' + value.number + '" value="' + value.time_from + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
                    html += '<p class="mb-0 me-2" style="width: 2.5%;">～</p>';
                    html += '<input type="text" name="time_to_' + value.week + '_' + value.number + '" value="' + value.time_to + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    $( target ).parents( '.modal' ).find( '.time-area-wrap' ).append( html );
                } else {
                    var html = '<div class="content mb-2">';
                    html += '<div class="row">';
                    html += '<div class="col-12">';
                    html += '<div class="d-flex align-items-center justify-content-start">';
                    html += '<div style="width: 20%;"></div>';
                    if ( value.week == 1 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">月</label>';
                    } else if ( value.week == 2 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">火</label>';
                    } else if ( value.week == 3 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">水</label>';
                    } else if ( value.week == 4 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">木</label>';
                    } else if ( value.week == 5 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">金</label>';
                    } else if ( value.week == 6 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">土</label>';
                    } else if ( value.week == 7 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">日</label>';
                    } else if ( value.week == 8 ) {
                        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;">祝</label>';
                    }
                    html += '<div class="time-area" style="width: 97.5%;">';
                    html += '<div class="d-flex align-items-center justify-content-start">';
                    if ( value.flg || value.holiday_flg ) {
                        html += '<input type="text" name="time_from_' + value.week + '_' + value.number + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
                    } else {
                        html += '<input type="text" name="time_from_' + value.week + '_' + value.number + '" value="' + value.time_from + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled required>';
                    }
                    html += '<p class="mb-0 me-2" style="width: 2.5%;">～</p>';
                    if ( value.flg || value.holiday_flg ) {
                        html += '<input type="text" name="time_to_' + value.week + '_' + value.number + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
                    } else {
                        html += '<input type="text" name="time_to_' + value.week + '_' + value.number + '" value="' + value.time_to + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled required>';
                    }
                    html += '<div class="input-check-wrap ps-4 mb-0" style="width: 12.5%;">';
                    html += '<label for="detail_manager_holiday_check_' + value.week + '" class="mb-0">休日</label>';
                    if ( value.flg || value.holiday_flg ) {
                        html += '<input type="checkbox" id="detail_manager_holiday_check_' + value.week + '" name="time_check_' + value.week + '" value="' + value.week + '" class="time-check input-check" checked>';
                    } else {
                        html += '<input type="checkbox" id="detail_manager_holiday_check_' + value.week + '" name="time_check_' + value.week + '" value="' + value.week + '" class="time-check input-check">';
                    }
                    html += '<label for="detail_manager_holiday_check_' + value.week + '" class="input-check-mark mb-0"></label>';
                    html += '</div>';
                    html += '<div class="d-flex justify-content-start align-items-center ms-1" style="width: 35%;">';
                    html += '<button type="button" value="' + value.week + '" class="btn main-button add-time-button plus p-0 ps-3 me-0">時間を追加する</button>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    $( target ).parents( '.modal' ).find( '.time-area-wrap' ).append( html );
                }
                last_week = value.week;
            });
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
        }).fail( function(){
            
        });
    });

    $( '.manager-list-table .dropdown .dropdown-menu .change-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });

    $( '#add_online_modal .time-check, #add_offline_modal .time-check, .save-online-modal .time-check, .save-offline-modal .time-check' ).on( 'change', function() {
        if ( $( this ).prop( 'checked' ) ) {
            $( this ).parents( '.time-area' ).find( 'input[type=text]' ).val( '' );
            $( this ).parents( '.time-area' ).find( 'input[type=text]' ).prop( 'required', false );
            $( this ).parents( '.time-area' ).find( 'input[type=text]' ).prop( 'disabled', true );
            $( this ).parents( '.time-area' ).find( 'input[type=text]' ).addClass( 'readonly' );
        } else {
            var target = $( this );
            $( this ).parents( '.time-area' ).find( 'input[type=text]' ).each( function( index, value ) {
                if ( $( target ).val() != '8' && ( index == 0 || index == 1 ) ) {
                    $( this ).prop( 'required', true );
                }
                $( this ).prop( 'disabled', false );
                $( this ).removeClass( 'readonly' );
            });
        }
    });
    $( document ).on( 'change', '#save_manager_modal .time-check, .detail-manager-modal .time-check', function () {
        var target = $( this );
        $( this ).parents( '.modal-body' ).find( '.content [name*=time_from_' + $( this ).val() + '_]' ).each( function( index, value ) {
            if ( $( target ).prop( 'checked' ) ) {
                $( this ).val( '' );
                $( this ).prop( 'required', false );
                $( this ).prop( 'disabled', true );
                $( this ).addClass( 'readonly' );
            } else {
                if ( $( target ).val() != '8' && ( index == 0 ) ) {
                    $( this ).prop( 'required', true );
                }
                $( this ).prop( 'disabled', false );
                $( this ).removeClass( 'readonly' );
            }
        });
        $( this ).parents( '.modal-body' ).find( '.content [name*=time_to_' + $( this ).val() + '_]' ).each( function( index, value ) {
            if ( $( target ).prop( 'checked' ) ) {
                $( this ).val( '' );
                $( this ).prop( 'required', false );
                $( this ).prop( 'disabled', true );
                $( this ).addClass( 'readonly' );
            } else {
                if ( $( target ).val() != '8' && ( index == 0 ) ) {
                    $( this ).prop( 'required', true );
                }
                $( this ).prop( 'disabled', false );
                $( this ).removeClass( 'readonly' );
            }
        });
    });

    $( '#add_online_modal .add-time-button, #add_offline_modal .add-time-button, .save-online-modal .add-time-button, .save-offline-modal .add-time-button' ).on( 'click', function() {
        var target = $( this ).val() + '_' + ( $( this ).parents( '.time-area' ).children( '.d-flex' ).length + 1 );

        var html = '<div class="d-flex align-items-center justify-content-start mb-2">';
        html += '<p class="me-2 mb-0" style="width: 2.5%;"></p>';
        if ( $( this ).parents( '.time-area' ).find( '.time-check' ).prop( 'checked' ) ) {
            html += '<input type="text" name="time_from_' + target + '" class="input-text input-time readonly ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
        } else {
            html += '<input type="text" name="time_from_' + target + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
        }
        html += '<p class="mb-0 me-2" style="width: 2.5%;">～</p>';
        if ( $( this ).parents( '.time-area' ).find( '.time-check' ).prop( 'checked' ) ) {
            html += '<input type="text" name="time_to_' + target + '" class="input-text input-time readonly ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
        } else {
            html += '<input type="text" name="time_to_' + target + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
        }
        html += '<div class="d-flex justify-content-start align-items-center ms-1" style="width: 47.5%;"></div>';
        html += '</div>';
        $( this ).parents( '.time-area' ).append( html );
        
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
    });
    $( document ).on( 'click', '#save_manager_modal .add-time-button, .detail-manager-modal .add-time-button', function () {
        var target = $( this );
        var number = $( this ).val() + '_' + ( $( this ).parents( '.modal-body' ).find( '[name*=time_from_' + $( this ).val() + '_]' ).length + 1 );

        var flg = $( this ).parents( '.modal-body' ).find( '[name*=time_check_' + $( this ).val() + ']' ).prop( 'checked' );
        var html = '<div class="content mb-2">';
        html += '<div class="row">';
        html += '<div class="col-12">';
        html += '<div class="d-flex align-items-center justify-content-start">';
        html += '<div style="width: 20%;"></div>';
        html += '<label class="text-end pe-4 mb-0" style="width: 2.5%;"></label>';
        html += '<div class="time-area" style="width: 97.5%;">';
        html += '<div class="d-flex align-items-center justify-content-start">';
        if ( flg ) {
            html += '<input type="text" name="time_from_' + number + '" class="input-text input-time readonly ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
        } else {
            html += '<input type="text" name="time_from_' + number + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
        }
        html += '<p class="mb-0 me-2" style="width: 2.5%;">～</p>';
        if ( flg ) {
            html += '<input type="text" name="time_to_' + number + '" class="input-text input-time readonly ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled disabled>';
        } else {
            html += '<input type="text" name="time_to_' + number + '" class="input-text input-time ps-2 pe-2 me-2" style="width: 22.5%;" data-parsley-errors-messages-disabled>';
        }
        html += '<div class="input-check-wrap ps-4 mb-0" style="width: 50%;"></div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        $( this ).parents( '.modal-body' ).find( '[name*=time_from_' + $( this ).val() + '_]' ).each( function( index, value ) {
            if ( $( target ).parents( '.modal-body' ).find( '[name*=time_from_' + $( target ).val() + '_]' ).length == ( index + 1 )) {
                $( this ).parents( '.content' ).after( html );
            }
        });
        
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
    });
});