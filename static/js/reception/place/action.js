$( function() {
    $( document ).on( 'click', '#save_place_form .place-setting-dropdown button', function () {
        window.location.href = '/reception/place/?year=' + $( '#save_place_form [name=year]' ).val() + '&month=' + $( '#save_place_form [name=month]' ).val() + '&id=' + $( this ).val();
    });

    $( document ).on( 'change', '.setting-not-check', function () {
        var day = $( this ).val();
        var count = $( this ).parents( 'td' ).find( '.d-flex' ).length - 2;
        if ( $( this ).prop( 'checked' ) ) {
            for ( var i = 1; i <= count; i++ ) {
                var target = day + '_' + i;
                $( 'input[name=setting_from_' + target + ']' ).prop( 'disabled', true );
                $( 'input[name=setting_from_' + target + ']' ).prop( 'required', false );
                $( 'input[name=setting_from_' + target + ']' ).addClass( 'readonly' );
                $( 'input[name=setting_from_' + target + ']' ).val( '' );
                $( 'input[name=setting_to_' + target + ']' ).prop( 'disabled', true );
                $( 'input[name=setting_to_' + target + ']' ).prop( 'required', false );
                $( 'input[name=setting_to_' + target + ']' ).addClass( 'readonly' );
                $( 'input[name=setting_to_' + target + ']' ).val( '' );
                $( 'input[name=setting_count_' + day + ']' ).prop( 'disabled', true );
                $( 'input[name=setting_count_' + day + ']' ).prop( 'required', false );
                $( 'input[name=setting_count_' + day + ']' ).addClass( 'readonly' );
                $( 'input[name=setting_count_' + day + ']' ).val( '' );
            }
        } else {
            for ( var i = 1; i <= count; i++ ) {
                var target = day + '_' + i;
                $( 'input[name=setting_from_' + target + ']' ).prop( 'disabled', false );
                $( 'input[name=setting_from_' + target + ']' ).prop( 'required', false );
                $( 'input[name=setting_from_' + target + ']' ).removeClass( 'readonly' );
                $( 'input[name=setting_to_' + target + ']' ).prop( 'disabled', false );
                $( 'input[name=setting_to_' + target + ']' ).prop( 'required', false );
                $( 'input[name=setting_to_' + target + ']' ).removeClass( 'readonly' );
                $( 'input[name=setting_count_' + day + ']' ).prop( 'disabled', false );
                $( 'input[name=setting_count_' + day + ']' ).prop( 'required', false );
                $( 'input[name=setting_count_' + day + ']' ).removeClass( 'readonly' );
            }
        }
    });

    $( document ).on( 'click', '#save_place_form .calendar-table .add-time-button', function () {
        var number = $( this ).parents( 'td' ).find( '.d-flex' ).length - 1;
        var target = $( this ).val() + '_' + number;
        
        var flg = $( this ).parents( 'td' ).find( '.setting-not-check' ).prop( 'checked' );
        var html = '<div class="d-flex align-items-center mb-1">';
        if ( flg ) {
            html += '<input type="text" name="setting_from_' + target + '" class="input-text input-time readonly ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly disabled>';
        } else {
            html += '<input type="text" name="setting_from_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
        }
        html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
        if ( flg ) {
            html += '<input type="text" name="setting_to_' + target + '" class="input-text input-time readonly ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly disabled>';
        } else {
            html += '<input type="text" name="setting_to_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
        }
        html += '</div>';
        $( this ).parents( '.d-flex' ).before( html );

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
    });

    $( document ).on( 'change', '#place_all_input_modal [name=method]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#place_all_input_form [name=date_1]' ).prop( 'required', false );
            $( '#place_all_input_form [name=period_from]' ).prop( 'required', false );
            $( '#place_all_input_form [name=period_to]' ).prop( 'required', false );
            $( '#place_all_input_form [name=time_from]' ).prop( 'required', false );
            $( '#place_all_input_form [name=time_to]' ).prop( 'required', false );
            $( '#place_all_method_date_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '2' ) {
            if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '1' ) {
                $( '#place_all_input_form [name=date_1]' ).prop( 'required', true );
            } else if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '2' ) {
                $( '#place_all_input_form [name=period_from]' ).prop( 'required', true );
                $( '#place_all_input_form [name=period_to]' ).prop( 'required', true );
            }
            if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '1' ) {
                $( '#place_all_input_form [name=time_from]' ).prop( 'required', true );
                $( '#place_all_input_form [name=time_to]' ).prop( 'required', true );
            }
            $( '#place_all_method_date_area' ).removeClass( 'd-none' );
        }
    });
    $( document ).on( 'change', '#place_all_input_modal [name=type]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#place_all_input_modal [name=date_1]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=date_1]' ).prop( 'required', true );
            $( '#place_all_input_modal [name=date_1]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_2]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_3]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_4]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_from]' ).val( '' );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_to]' ).val( '' );
            $( '#place_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        } else if ( $( this ).val() == '2' ) {
            $( '#place_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_1]' ).val( '' );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_2]' ).val( '' );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_3]' ).val( '' );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_4]' ).val( '' );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'required', true );
            $( '#place_all_input_modal [name=period_from]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'required', true );
            $( '#place_all_input_modal [name=period_to]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        } else if ( $( this ).val() == '3' ) {
            $( '#place_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_1]' ).val( '' );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_2]' ).val( '' );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_3]' ).val( '' );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_4]' ).val( '' );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_from]' ).val( '' );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_to]' ).val( '' );
            $( '#place_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', false );
            });
        } else if ( $( this ).val() == '4' ) {
            $( '#place_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_1]' ).val( '' );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_2]' ).val( '' );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_3]' ).val( '' );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=date_4]' ).val( '' );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_from]' ).val( '' );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=period_to]' ).val( '' );
            $( '#place_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        }
    });
    $( document ).on( 'change', '#place_all_input_modal [name=all_flg]', function () {
        for ( var i = $( '#place_all_input_modal .place-all-area .d-flex' ).length; i > 3; i-- ) {
            $( '#place_all_input_modal .place-all-area .d-flex' ).eq( i - 3 ).remove();
        }
        if ( $( this ).val() == '0' ) {
            $( '#place_all_input_modal [name=time_from_1]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=time_from_1]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=time_from_1]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=time_from_1]' ).val( '' );
            $( '#place_all_input_modal [name=time_to_1]' ).prop( 'disabled', true );
            $( '#place_all_input_modal [name=time_to_1]' ).prop( 'required', false );
            $( '#place_all_input_modal [name=time_to_1]' ).addClass( 'readonly' );
            $( '#place_all_input_modal [name=time_to_1]' ).val( '' );
        } else if ( $( this ).val() == '1' ) {
            $( '#place_all_input_modal [name=time_from_1]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=time_from_1]' ).prop( 'required', true );
            $( '#place_all_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
            $( '#place_all_input_modal [name=time_to_1]' ).prop( 'disabled', false );
            $( '#place_all_input_modal [name=time_to_1]' ).prop( 'required', true );
            $( '#place_all_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
        }
    });

    $( document ).on( 'click', '#place_all_input_modal .add-time-button', function () {
        if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '1' ) {
            var number = $( this ).parents( '.place-all-area' ).find( '.d-flex' ).length - 1;
            
            var html = '<div class="d-flex align-items-center mt-1">';
            html += '<div style="width: 84px;"></div>';
            html += '<input type="text" name="time_from_' + number + '" class="input-text input-time ps-2 pe-2" style="width: 120px;" data-parsley-errors-messages-disabled readonly>';
            html += '<p class="ms-1 me-1 mb-0">～</p>';
            html += '<input type="text" name="time_to_' + number + '" class="input-text input-time ps-2 pe-2" style="width: 120px;" data-parsley-errors-messages-disabled readonly>';
            html += '</div>';
            $( this ).parent().before( html );
    
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
        }
    });

    $( document ).on( 'click', '#place_all_input_modal .yes-button', function () {
        if ( $( '#place_all_input_form' ).parsley().validate() ) {
            if ( $( '#place_all_input_modal [name=method]:checked' ).val() == '1' ) {
                var form_data = new FormData();
                form_data.append( 'id', $( '#save_place_form [name=setting]' ).next().val() );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_place_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var holiday_flg = false;
                    $.each( response.time, function( time_index, time_value ) {
                        if ( time_value.week == 8 ) {
                            holiday_flg = true;
                            return false;
                        }
                    });
                    $( '.calendar-table tbody tr' ).each( function( week_index, week_value ) {
                        $( this ).find( 'td' ).each( function( day_index, day_value ) {
                            var day = $( this ).find( '.day-text' ).text();
                            if ( check_empty( day ) ) {
                                for ( var i = $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.d-flex' ).length - 2; i >= 2; i-- ) {
                                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).parents( '.d-flex' ).remove();
                                }
                                if ( day_index == 0 ) {
                                    $.each( response.time, function( time_index, time_value ) {
                                        if ( time_value.week == 7 ) {
                                            if ( time_value.number >= 2 ) {
                                                var html = '<div class="d-flex align-items-center mb-1">';
                                                html += '<input type="text" name="setting_from_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                                html += '<input type="text" name="setting_to_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                html += '</div>';
                                                $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                            }
                                            if ( time_value.flg ) {
                                                $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', true );
                                                $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'disabled', true );
                                                $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'required', false );
                                                $( '#save_place_form [name=setting_from_' + day + '_1]' ).addClass( 'readonly' );
                                                $( '#save_place_form [name=setting_from_' + day + '_1]' ).val( '' );
                                                $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'disabled', true );
                                                $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'required', false );
                                                $( '#save_place_form [name=setting_to_' + day + '_1]' ).addClass( 'readonly' );
                                                $( '#save_place_form [name=setting_to_' + day + '_1]' ).val( '' );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', true );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).addClass( 'readonly' );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                                            } else {
                                                $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                                                $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).val( time_value.time_from.substr( 0, time_value.time_from.lastIndexOf(':') ) );
                                                $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).val( time_value.time_to.substr( 0, time_value.time_to.lastIndexOf(':') ) );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', true );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                                                $( '#save_place_form [name=setting_count_' + day + ']' ).val( 0 );
                                            }
                                        }
                                    });
                                } else {
                                    if ( $( this ).find( '.day-text' ).hasClass( 'holiday-text' ) && holiday_flg ) {
                                        $.each( response.time, function( time_index, time_value ) {
                                            if ( time_value.week == 8 ) {
                                                if ( time_value.number >= 2 ) {
                                                    var html = '<div class="d-flex align-items-center mb-1">';
                                                    html += '<input type="text" name="setting_from_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                    html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                                    html += '<input type="text" name="setting_to_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                    html += '</div>';
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                                }
                                                if ( time_value.flg ) {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                                                } else {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).val( time_value.time_from.substr( 0, time_value.time_from.lastIndexOf(':') ) );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).val( time_value.time_to.substr( 0, time_value.time_to.lastIndexOf(':') ) );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( 0 );
                                                }
                                            }
                                        });
                                    } else {
                                        $.each( response.time, function( time_index, time_value ) {
                                            if ( time_value.week == day_index ) {
                                                if ( time_value.number >= 2 ) {
                                                    var html = '<div class="d-flex align-items-center mb-1">';
                                                    html += '<input type="text" name="setting_from_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                    html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                                    html += '<input type="text" name="setting_to_' + day + '_' + time_value.number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                    html += '</div>';
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                                }
                                                if ( time_value.flg ) {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                                                } else {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_from_' + day + '_' + time_value.number + ']' ).val( time_value.time_from.substr( 0, time_value.time_from.lastIndexOf(':') ) );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_' + time_value.number + ']' ).val( time_value.time_to.substr( 0, time_value.time_to.lastIndexOf(':') ) );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( 0 );
                                                }
                                            }
                                        });
                                    }
                                }
                            }
                        });
                    });
                }).fail( function(){
                    
                });
            } else if ( $( '#place_all_input_modal [name=method]:checked' ).val() == '2' ) {
                if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '1' ) {
                    var date_list = [];
                    for ( var i = 1; i <= 4; i++ ) {
                        if ( check_empty( $( '#place_all_input_modal [name=date_' + i + ']' ).val() ) ) {
                            date_list.push( $( '#place_all_input_modal [name=date_' + i + ']' ).val() );
                        }
                    }
                    $.each( date_list, function( index, value ) {
                        for ( var i = $( '#save_place_form [name=setting_not_' + value + ']' ).parents( 'td' ).find( '.d-flex' ).length - 2; i >= 2; i-- ) {
                            $( '#save_place_form [name=setting_from_' + value + '_' + i + ']' ).parents( '.d-flex' ).remove();
                        }
                        if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '0' ) {
                            $( '#save_place_form [name=setting_not_' + value + ']' ).prop( 'checked', true );
                            $( '#save_place_form [name=setting_from_' + value + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_from_' + value + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_from_' + value + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_from_' + value + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_to_' + value + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_to_' + value + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_to_' + value + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_to_' + value + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).val( '' );
                        } else {
                            $( '#save_place_form [name=setting_not_' + value + ']' ).prop( 'checked', false );
                            for ( var i = 1; i <= $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length - 2; i++ ) {
                                var target = value + '_' + i;
                                if ( i >= 2 ) {
                                    var html = '<div class="d-flex align-items-center mb-1">';
                                    html += '<input type="text" name="setting_from_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                    html += '<input type="text" name="setting_to_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '</div>';
                                    $( '#save_place_form [name=setting_not_' + value + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                }
                                $( '#save_place_form [name=setting_from_' + target + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).val( $( '#place_all_input_modal [name=time_from_' + i + ']' ).val() );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).val( $( '#place_all_input_modal [name=time_to_' + i + ']' ).val() );
                            }
                            $( '#save_place_form [name=setting_count_' + value + ']' ).prop( 'disabled', false );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).prop( 'required', true );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).removeClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + value + ']' ).val( $( '#place_all_input_modal [name=count]' ).val() );
                        }
                    });
                } else if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '2' ) {
                    for ( var i = Number($( '#place_all_input_modal [name=period_from]' ).val()); i <= Number($( '#place_all_input_modal [name=period_to]' ).val()); i++ ) {
                        for ( var j = $( '#save_place_form [name=setting_not_' + i + ']' ).parents( 'td' ).find( '.d-flex' ).length - 2; j >= 2; j-- ) {
                            $( '#save_place_form [name=setting_from_' + i + '_' + j + ']' ).parents( '.d-flex' ).remove();
                        }
                        if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '0' ) {
                            $( '#save_place_form [name=setting_not_' + i + ']' ).prop( 'checked', true );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).val( '' );
                        } else {
                            $( '#save_place_form [name=setting_not_' + i + ']' ).prop( 'checked', false );
                            for ( var j = 1; j <= $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length - 2; j++ ) {
                                var target = i + '_' + j;
                                if ( j >= 2 ) {
                                    var html = '<div class="d-flex align-items-center mb-1">';
                                    html += '<input type="text" name="setting_from_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                    html += '<input type="text" name="setting_to_' + target + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '</div>';
                                    $( '#save_place_form [name=setting_not_' + i + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                }
                                $( '#save_place_form [name=setting_from_' + target + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_from_' + target + ']' ).val( $( '#place_all_input_modal [name=time_from_' + j + ']' ).val() );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_to_' + target + ']' ).val( $( '#place_all_input_modal [name=time_to_' + j + ']' ).val() );
                            }
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'disabled', false );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'required', true );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).removeClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).val( $( '#place_all_input_modal [name=count]' ).val() );
                        }
                    }
                } else if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '3' ) {
                    $( '#place_all_input_modal [name=week]:checked' ).each( function( index, value ) {
                        var target = $( this );
                        if ( $( this ).val() == '8' ) {
                            $( '.calendar-table tbody tr' ).each( function( week_index, week_value ) {
                                $( this ).find( 'td' ).each( function( day_index, day_value ) {
                                    if ( day_index != 0 ) {
                                        if ( $( this ).find( '.setting-not-check' ).length && $( this ).find( '.holiday-text' ).length ) {
                                            var day = $( this ).find( '.day-text' ).text();
                                            for ( var i = $( this ).find( '.d-flex' ).length - 2; i >= 2; i-- ) {
                                                $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).parents( '.d-flex' ).remove();
                                            }
                                            if ( check_empty( day ) ) {
                                                if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '0' ) {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_from_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_to_' + day + '_1]' ).val( '' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).addClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                                                } else {
                                                    $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                                                    for ( var i = 1; i <= $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length - 2; i++ ) {
                                                        var number = day + '_' + i;
                                                        if ( i >= 2 ) {
                                                            var html = '<div class="d-flex align-items-center mb-1">';
                                                            html += '<input type="text" name="setting_from_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                            html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                                            html += '<input type="text" name="setting_to_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                            html += '</div>';
                                                            $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                                        }
                                                        $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'disabled', false );
                                                        $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'required', true );
                                                        $( '#save_place_form [name=setting_from_' + number + ']' ).removeClass( 'readonly' );
                                                        $( '#save_place_form [name=setting_from_' + number + ']' ).val( $( '#place_all_input_modal [name=time_from_' + i + ']' ).val() );
                                                        $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'disabled', false );
                                                        $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'required', true );
                                                        $( '#save_place_form [name=setting_to_' + number + ']' ).removeClass( 'readonly' );
                                                        $( '#save_place_form [name=setting_to_' + number + ']' ).val( $( '#place_all_input_modal [name=time_to_' + i + ']' ).val() );
                                                    }
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', true );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                                                    $( '#save_place_form [name=setting_count_' + day + ']' ).val( $( '#place_all_input_modal [name=count]' ).val() );
                                                }
                                            }
                                        }
                                    }
                                });
                            });
                        } else {
                            $( '.calendar-table tbody tr' ).each( function( index, value ) {
                                var day = $( this ).find( 'td' ).eq( Number($( target ).val()) - 1 ).find( '.day-text' ).text();
                                for ( var i = $( this ).find( 'td' ).find( '.d-flex' ).length - 2; i >= 2; i-- ) {
                                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).parents( '.d-flex' ).remove();
                                }
                                if ( check_empty( day ) ) {
                                    if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '0' ) {
                                        $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', true );
                                        $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'disabled', true );
                                        $( '#save_place_form [name=setting_from_' + day + '_1]' ).prop( 'required', false );
                                        $( '#save_place_form [name=setting_from_' + day + '_1]' ).addClass( 'readonly' );
                                        $( '#save_place_form [name=setting_from_' + day + '_1]' ).val( '' );
                                        $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'disabled', true );
                                        $( '#save_place_form [name=setting_to_' + day + '_1]' ).prop( 'required', false );
                                        $( '#save_place_form [name=setting_to_' + day + '_1]' ).addClass( 'readonly' );
                                        $( '#save_place_form [name=setting_to_' + day + '_1]' ).val( '' );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', true );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).addClass( 'readonly' );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                                    } else {
                                        $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                                        for ( var i = 1; i <= $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length - 2; i++ ) {
                                            var number = day + '_' + i;
                                            if ( i >= 2 ) {
                                                var html = '<div class="d-flex align-items-center mb-1">';
                                                html += '<input type="text" name="setting_from_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                                html += '<input type="text" name="setting_to_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                                html += '</div>';
                                                $( '#save_place_form [name=setting_not_' + day + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                            }
                                            $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'disabled', false );
                                            $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'required', true );
                                            $( '#save_place_form [name=setting_from_' + number + ']' ).removeClass( 'readonly' );
                                            $( '#save_place_form [name=setting_from_' + number + ']' ).val( $( '#place_all_input_modal [name=time_from_' + i + ']' ).val() );
                                            $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'disabled', false );
                                            $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'required', true );
                                            $( '#save_place_form [name=setting_to_' + number + ']' ).removeClass( 'readonly' );
                                            $( '#save_place_form [name=setting_to_' + number + ']' ).val( $( '#place_all_input_modal [name=time_to_' + i + ']' ).val() );
                                        }
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', true );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                                        $( '#save_place_form [name=setting_count_' + day + ']' ).val( $( '#place_all_input_modal [name=count]' ).val() );
                                    }
                                }
                            });
                        }
                    });
                } else if ( $( '#place_all_input_modal [name=type]:checked' ).val() == '4' ) {
                    for ( var i = 1; i <= 31; i++ ) {
                        for ( var j = $( '#save_place_form [name=setting_not_' + i + ']' ).parents( 'td' ).find( '.d-flex' ).length - 2; j >= 2; j-- ) {
                            $( '#save_place_form [name=setting_from_' + i + '_' + j + ']' ).parents( '.d-flex' ).remove();
                        }
                        if ( $( '#place_all_input_modal [name=all_flg]:checked' ).val() == '0' ) {
                            $( '#save_place_form [name=setting_not_' + i + ']' ).prop( 'checked', true );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_from_' + i + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_to_' + i + '_1]' ).val( '' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'disabled', true );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'required', false );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).addClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).val( '' );
                        } else {
                            $( '#save_place_form [name=setting_not_' + i + ']' ).prop( 'checked', false );
                            for ( var j = 1; j <= $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length - 2; j++ ) {
                                var number = i + '_' + j;
                                if ( j >= 2 ) {
                                    var html = '<div class="d-flex align-items-center mb-1">';
                                    html += '<input type="text" name="setting_from_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '<p class="text-center mb-0" style="width: 10%;">～</p>';
                                    html += '<input type="text" name="setting_to_' + number + '" class="input-text input-time ps-1 pe-1" style="width: 45%;" data-parsley-errors-messages-disabled readonly>';
                                    html += '</div>';
                                    $( '#save_place_form [name=setting_not_' + i + ']' ).parents( 'td' ).find( '.add-time-button' ).parents( '.d-flex' ).before( html );
                                }
                                $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_from_' + number + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_from_' + number + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_from_' + number + ']' ).val( $( '#place_all_input_modal [name=time_from_' + j + ']' ).val() );
                                $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'disabled', false );
                                $( '#save_place_form [name=setting_to_' + number + ']' ).prop( 'required', true );
                                $( '#save_place_form [name=setting_to_' + number + ']' ).removeClass( 'readonly' );
                                $( '#save_place_form [name=setting_to_' + number + ']' ).val( $( '#place_all_input_modal [name=time_to_' + j + ']' ).val() );
                            }
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'disabled', false );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).prop( 'required', true );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).removeClass( 'readonly' );
                            $( '#save_place_form [name=setting_count_' + i + ']' ).val( $( '#place_all_input_modal [name=count]' ).val() );
                        }
                    }
                }
            }

            $( '#place_all_input_modal .no-button' ).trigger( 'click' );
        }
    });
    $( document ).on( 'click', '#place_all_input_modal .no-button', function () {
        $( '#place_all_input_modal [name=type]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#place_all_input_modal [name=date_1]' ).prop( 'disabled', false );
        $( '#place_all_input_modal [name=date_1]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=date_1]' ).removeClass( 'readonly' );
        $( '#place_all_input_modal [name=date_1]' ).val( '' );
        $( '#place_all_input_modal [name=date_2]' ).prop( 'disabled', false );
        $( '#place_all_input_modal [name=date_2]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=date_2]' ).removeClass( 'readonly' );
        $( '#place_all_input_modal [name=date_2]' ).val( '' );
        $( '#place_all_input_modal [name=date_3]' ).prop( 'disabled', false );
        $( '#place_all_input_modal [name=date_3]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=date_3]' ).removeClass( 'readonly' );
        $( '#place_all_input_modal [name=date_3]' ).val( '' );
        $( '#place_all_input_modal [name=date_4]' ).prop( 'disabled', false );
        $( '#place_all_input_modal [name=date_4]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=date_4]' ).removeClass( 'readonly' );
        $( '#place_all_input_modal [name=date_4]' ).val( '' );
        $( '#place_all_input_modal [name=period_from]' ).prop( 'disabled', true );
        $( '#place_all_input_modal [name=period_from]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=period_from]' ).addClass( 'readonly' );
        $( '#place_all_input_modal [name=period_from]' ).val( '' );
        $( '#place_all_input_modal [name=period_to]' ).prop( 'disabled', true );
        $( '#place_all_input_modal [name=period_to]' ).prop( 'required', false );
        $( '#place_all_input_modal [name=period_to]' ).addClass( 'readonly' );
        $( '#place_all_input_modal [name=period_to]' ).val( '' );
        $( '#place_all_input_modal [name=week]' ).each( function( index, value ) {
            $( this ).prop( 'disabled', true );
            $( this ).prop( 'checked', false );
        });
        $( '#place_all_input_modal [name=all_flg]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        for ( var i = $( '#place_all_input_modal [name=all_flg]' ).parents( '.place-all-area' ).find( '.d-flex' ).length; i > 3; i-- ) {
            $( '#place_all_input_modal [name=time_from_' + ( i - 2 ) + ']' ).parent().remove();
        }
        $( '#place_all_input_modal [name=time_from_1]' ).val( '' );
        $( '#place_all_input_modal [name=time_to_1]' ).val( '' );
        $( '#place_all_input_modal [name=count]' ).val( '' );
        $( '#place_all_input_modal [name=method]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#place_all_input_modal #place_all_method_date_area' ).addClass( 'd-none' );
    });

    $( document ).on( 'click', '#place_all_reset_modal .yes-button', function () {
        $( '.calendar-table tbody td' ).each( function( index, value ) {
            if ( $( this ).find( '.setting-not-check' ).length ) {
                var day = $( this ).find( '.setting-not-check' ).val();
                $( '#save_place_form [name=setting_not_' + day + ']' ).prop( 'checked', false );
                for ( var i = 1; i <= $( this ).find( '.d-flex' ).length - 2; i++ ) {
                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).prop( 'disabled', false );
                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).prop( 'required', false );
                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).removeClass( 'readonly' );
                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).val( '' );
                    $( '#save_place_form [name=setting_to_' + day + '_' + i + ']' ).prop( 'disabled', false );
                    $( '#save_place_form [name=setting_to_' + day + '_' + i + ']' ).prop( 'required', false );
                    $( '#save_place_form [name=setting_to_' + day + '_' + i + ']' ).removeClass( 'readonly' );
                    $( '#save_place_form [name=setting_to_' + day + '_' + i + ']' ).val( '' );
                }
                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'disabled', false );
                $( '#save_place_form [name=setting_count_' + day + ']' ).prop( 'required', false );
                $( '#save_place_form [name=setting_count_' + day + ']' ).removeClass( 'readonly' );
                $( '#save_place_form [name=setting_count_' + day + ']' ).val( '' );
                for ( var i = $( this ).find( '.d-flex' ).length - 2; i >= 2; i-- ) {
                    $( '#save_place_form [name=setting_from_' + day + '_' + i + ']' ).parents( '.d-flex' ).remove();
                }
            }
        });
        $( '#place_all_reset_modal .no-button' ).trigger( 'click' );
    });
});