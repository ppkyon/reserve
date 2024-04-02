$( function() {
    $( document ).on( 'click', '.manager-table .no-icon, .manager-table .work-icon, .manager-table .holiday-icon', function () {
        var date = $( '#save_manager_form [name=year]' ).val() + '年' + $( '#save_manager_form [name=month]' ).val() + '月' + $( this ).parent().children( 'input[type=hidden]' ).eq(2).val() + '日';
        if ( $( this ).prev().val() == '1' ) {
            date = date + '(日)';
        } else if ( $( this ).prev().val() == '2' ) {
            date = date + '(月)';
        } else if ( $( this ).prev().val() == '3' ) {
            date = date + '(火)';
        } else if ( $( this ).prev().val() == '4' ) {
            date = date + '(水)';
        } else if ( $( this ).prev().val() == '5' ) {
            date = date + '(木)';
        } else if ( $( this ).prev().val() == '6' ) {
            date = date + '(金)';
        } else if ( $( this ).prev().val() == '7' ) {
            date = date + '(土)';
        }
        var manager_name = ' ' + $( '.manager-name-' + $( this ).parent().children( 'input[type=hidden]' ).eq(1).val() ).eq(0).text();
        var setting_name = '【' + $( '.setting-name-' + $( this ).parent().children( 'input[type=hidden]' ).eq(0).val() ).eq(0).text() + '】';
        $( '#manager_input_modal .modal-title' ).text( date + manager_name + setting_name );

        for ( var i = $( '#manager_input_modal #manager_input_form .d-flex' ).length; i > 3; i-- ) {
            $( '#manager_input_modal #manager_input_form .d-flex' ).eq( i - 3 ).remove();
        }

        $( '#manager_input_modal #input_setting' ).val( $( this ).parent().children( 'input[type=hidden]' ).eq(0).val() );
        $( '#manager_input_modal #input_manager' ).val( $( this ).parent().children( 'input[type=hidden]' ).eq(1).val() );
        $( '#manager_input_modal #input_day' ).val( $( this ).parent().children( 'input[type=hidden]' ).eq(2).val() );

        var target = $( this ).parent().children( 'input[type=hidden]' ).eq(0).val() + '_' + $( this ).parent().children( 'input[type=hidden]' ).eq(1).val() + '_' + $( this ).parent().children( 'input[type=hidden]' ).eq(2).val();
        if ( check_empty( $( this ).parent().find( '.data-area input[type=hidden]' ).length > 0 ) ) {
            if ( $( this ).parent().find( '.data-area [name="flg_' + target + '"]' ).val() == '0' ) {
                $( '#manager_input_modal [name=flg]' ).each( function( index, value ) {
                    if ( $( this ).val() == '0' ) {
                        $( this ).prop( 'checked', true );
                    }
                });
                $( '#manager_input_modal [name=time_from_1]' ).prop( 'disabled', true );
                $( '#manager_input_modal [name=time_from_1]' ).prop( 'required', false );
                $( '#manager_input_modal [name=time_from_1]' ).addClass( 'readonly' );
                $( '#manager_input_modal [name=time_from_1]' ).val( '' );
                $( '#manager_input_modal [name=time_to_1]' ).prop( 'disabled', true );
                $( '#manager_input_modal [name=time_to_1]' ).prop( 'required', false );
                $( '#manager_input_modal [name=time_to_1]' ).addClass( 'readonly' );
                $( '#manager_input_modal [name=time_to_1]' ).val( '' );
            } else if ( $( this ).parent().find( '.data-area [name="flg_' + target + '"]' ).val() == '1' ) {
                $( '#manager_input_modal [name=flg]' ).each( function( index, value ) {
                    if ( $( this ).val() == '1' ) {
                        $( this ).prop( 'checked', true );
                    }
                });
                for ( var i = 1; i <= ( $( this ).parent().find( '.data-area input[type=hidden]' ).length - 1 ) / 2; i++ ) {
                    if ( i >= 2 ) {
                        var html = '<div class="d-flex align-items-center mt-1">';
                        html += '<div style="width: 107.5px;"></div>';
                        html += '<input type="text" name="time_from_' + i + '" class="input-text input-time ps-2 pe-2" style="width: 120px;" data-parsley-errors-messages-disabled readonly>';
                        html += '<p class="ms-1 me-1 mb-0">～</p>';
                        html += '<input type="text" name="time_to_' + i + '" class="input-text input-time ps-2 pe-2" style="width: 120px;" data-parsley-errors-messages-disabled readonly>';
                        html += '</div>';
                        $( '#manager_input_modal .add-time-button' ).parent().before( html );
                    }
                    $( '#manager_input_modal [name=time_from_' + i + ']' ).prop( 'disabled', false );
                    $( '#manager_input_modal [name=time_from_' + i + ']' ).prop( 'required', true );
                    $( '#manager_input_modal [name=time_from_' + i + ']' ).removeClass( 'readonly' );
                    $( '#manager_input_modal [name=time_from_' + i + ']' ).val( $( this ).parent().find( '.data-area [name="from_' + target + '_' + i + '"]' ).val() );
                    $( '#manager_input_modal [name=time_to_' + i + ']' ).prop( 'disabled', false );
                    $( '#manager_input_modal [name=time_to_' + i + ']' ).prop( 'required', true );
                    $( '#manager_input_modal [name=time_to_' + i + ']' ).removeClass( 'readonly' );
                    $( '#manager_input_modal [name=time_to_' + i + ']' ).val( $( this ).parent().find( '.data-area [name="to_' + target + '_' + i + '"]' ).val() );
                }
            }
        } else {
            $( '#manager_input_modal [name=flg]' ).each( function( index, value ) {
                if ( $( this ).val() == '1' ) {
                    $( this ).prop( 'checked', true );
                }
                $( '#manager_input_modal [name=time_from_1]' ).prop( 'disabled', false );
                $( '#manager_input_modal [name=time_from_1]' ).prop( 'required', true );
                $( '#manager_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
                $( '#manager_input_modal [name=time_from_1]' ).val( '' );
                $( '#manager_input_modal [name=time_to_1]' ).prop( 'disabled', false );
                $( '#manager_input_modal [name=time_to_1]' ).prop( 'required', true );
                $( '#manager_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
                $( '#manager_input_modal [name=time_to_1]' ).val( '' );
            });
        }
        $( this ).next().trigger( 'click' );
    });

    $( document ).on( 'change', '#manager_all_input_modal [name=method]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#manager_all_input_form [name=date_1]' ).prop( 'required', false );
            $( '#manager_all_input_form [name=period_from]' ).prop( 'required', false );
            $( '#manager_all_input_form [name=period_to]' ).prop( 'required', false );
            $( '#manager_all_input_form [name=time_from_1]' ).prop( 'required', false );
            $( '#manager_all_input_form [name=time_to_1]' ).prop( 'required', false );
            $( '#manager_all_method_date_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '2' ) {
            if ( $( '#manager_all_input_modal [name=type]:checked' ).val() == '1' ) {
                $( '#manager_all_input_form [name=date_1]' ).prop( 'required', true );
            } else if ( $( '#manager_all_input_modal [name=type]:checked' ).val() == '2' ) {
                $( '#manager_all_input_form [name=period_from]' ).prop( 'required', true );
                $( '#manager_all_input_form [name=period_to]' ).prop( 'required', true );
            }
            if ( $( '#manager_all_input_modal [name=all_flg]:checked' ).val() == '1' ) {
                $( '#manager_all_input_form [name=time_from_1]' ).prop( 'required', true );
                $( '#manager_all_input_form [name=time_to_1]' ).prop( 'required', true );
            }
            $( '#manager_all_method_date_area' ).removeClass( 'd-none' );
        }
    });
    $( document ).on( 'change', '#manager_all_input_modal [name=type]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'required', true );
            $( '#manager_all_input_modal [name=date_1]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_2]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_3]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_4]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_from]' ).val( '' );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_to]' ).val( '' );
            $( '#manager_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        } else if ( $( this ).val() == '2' ) {
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_1]' ).val( '' );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_2]' ).val( '' );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_3]' ).val( '' );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_4]' ).val( '' );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'required', true );
            $( '#manager_all_input_modal [name=period_from]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'required', true );
            $( '#manager_all_input_modal [name=period_to]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        } else if ( $( this ).val() == '3' ) {
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_1]' ).val( '' );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_2]' ).val( '' );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_3]' ).val( '' );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_4]' ).val( '' );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_from]' ).val( '' );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_to]' ).val( '' );
            $( '#manager_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', false );
            });
        } else if ( $( this ).val() == '4' ) {
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_1]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_1]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_1]' ).val( '' );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_2]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_2]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_2]' ).val( '' );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_3]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_3]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_3]' ).val( '' );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=date_4]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=date_4]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=date_4]' ).val( '' );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_from]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_from]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_from]' ).val( '' );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=period_to]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=period_to]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=period_to]' ).val( '' );
            $( '#manager_all_input_modal [name=week]' ).each( function( index, value ) {
                $( this ).prop( 'disabled', true );
                $( this ).prop( 'checked', false );
            });
        }
    });
    $( document ).on( 'change', '#manager_all_input_modal [name=all_flg]', function () {
        if ( $( this ).val() == '0' ) {
            for ( var i = $( '#manager_all_input_modal .manager-all-area .d-flex' ).length; i > 3; i-- ) {
                $( '#manager_all_input_modal .manager-all-area .d-flex' ).eq( i - 3 ).remove();
            }
            $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=time_from_1]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=time_from_1]' ).val( '' );
            $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'disabled', true );
            $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'required', false );
            $( '#manager_all_input_modal [name=time_to_1]' ).addClass( 'readonly' );
            $( '#manager_all_input_modal [name=time_to_1]' ).val( '' );
        } else if ( $( this ).val() == '1' ) {
            $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'required', true );
            $( '#manager_all_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
            $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'disabled', false );
            $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'required', true );
            $( '#manager_all_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
        }
    });

    $( document ).on( 'click', '#manager_all_input_modal .add-time-button', function () {
        if ( $( '#manager_all_input_modal [name=all_flg]:checked' ).val() == '1' ) {
            var number = $( this ).parents( '.manager-all-area' ).find( '.d-flex' ).length - 1;
            
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

    $( document ).on( 'click', '#manager_all_input_modal .yes-button', function () {
        if ( $( '#manager_all_input_form' ).parsley().validate() && check_all_time() ) {
            var setting_list = [];
            $( '#manager_all_input_form [name=setting]:checked' ).each( function( index, value ) {
                setting_list.push( $( this ).val() );
            });
            if ( setting_list.length == 0 ) {
                $( '#manager_all_input_form [name=setting]' ).each( function( index, value ) {
                    setting_list.push( $( this ).val() );
                });
            }

            var manager_list = [];
            $( '#manager_all_input_form [name=manager]:checked' ).each( function( index, value ) {
                manager_list.push( $( this ).val() );
            });
            if ( manager_list.length == 0 ) {
                $( '#manager_all_input_form [name=manager]' ).each( function( index, value ) {
                    manager_list.push( $( this ).val() );
                });
            }

            var date_list = [];
            if ( $( '#manager_all_input_form [name=method]:checked' ).val() == '1' ) {
                for ( var i = 1; i <= 31; i++ ) {
                    date_list.push( i );
                }

                $.each( setting_list, function( setting_index, setting_value ) {
                    $.each( manager_list, function( manager_index, manager_value ) {
                        var form_data = new FormData();
                        form_data.append( 'setting_id', setting_value );
                        form_data.append( 'manager_id', manager_value );
                        $.ajax({
                            'data': form_data,
                            'url': $( '#get_manager_url' ).val(),
                            'type': 'POST',
                            'dataType': 'json',
                            'processData': false,
                            'contentType': false,
                        }).done( function( response ){
                            $.each( date_list, function( date_index, date_value ) {
                                var target_number = setting_value + '_' + manager_value + '_' + date_value;
                                $( '.manager-table tr td' ).each( function( index, value ) {
                                    var target = $( this );
                                    if ( $( this ).find( 'input[type=hidden]' ).eq(0).val() == setting_value && $( this ).find( 'input[type=hidden]' ).eq(1).val() == manager_value && $( this ).find( 'input[type=hidden]' ).eq(2).val() == date_value ) {
                                        var week = $( this ).find( 'input[type=hidden]' ).eq(3).val();
                                        if ( check_empty( week ) ) {
                                            var data_list = [];
                                            var holiday_data_list = [];
                                            $.each( response, function( response_index, response_value ) {
                                                if ( response_value.week == 8 ) {
                                                    holiday_data_list.push(response_value);
                                                } else if ( Number(week) == 1 ) {
                                                    if ( response_value.week == 7 ) {
                                                        data_list.push(response_value);
                                                    }
                                                } else {
                                                    if ( response_value.week == Number(week)-1 ) {
                                                        data_list.push(response_value);
                                                    }
                                                }
                                            });

                                            var holiday_flg = false;
                                            if ( holiday_data_list.length > 0 ) {
                                                $( '.manager-table thead th' ).each( function( index, value ){
                                                    if ( $( this ).text().substr( 0, $( this ).text().indexOf( '(' ) ) == date_value && $( this ).css( 'color' ) == 'rgb(255, 91, 91)' && $( this ).text().indexOf( '(日)' ) === -1 ) {
                                                        holiday_flg = true;
                                                        return false;
                                                    }
                                                });
                                            }

                                            if ( holiday_flg ) {
                                                $.each( holiday_data_list, function( index, value ) {
                                                    if ( ( check_empty(value.flg) && value.flg ) || ( check_empty(value.holiday_flg) && value.holiday_flg ) ) {
                                                        $( target ).find( '.data-area' ).empty();
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target_number + '" value="0">' );
                                                        $( target ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().removeClass( 'work-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().addClass( 'holiday-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().text( '休' );
                                                    } else {
                                                        if ( value.number == 1 ) {
                                                            $( target ).find( '.data-area' ).empty();
                                                            $( target ).find( '.data-area' ).prepend( '<input type="hidden" name="flg_' + target_number + '" value="1">' );
                                                            $( target ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().addClass( 'work-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().removeClass( 'holiday-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().text( '出' );
                                                        }
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="from_' + target_number + '_' + value.number + '" value="' + value.time_from.substr( 0, value.time_from.lastIndexOf(':') ) + '">' );
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="to_' + target_number + '_' + value.number + '" value="' + value.time_to.substr( 0, value.time_to.lastIndexOf(':') ) + '">' );
                                                    }
                                                });
                                            } else {
                                                $.each( data_list, function( index, value ) {
                                                    if ( ( check_empty(value.flg) && value.flg ) || ( check_empty(value.holiday_flg) && value.holiday_flg ) ) {
                                                        $( target ).find( '.data-area' ).empty();
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target_number + '" value="0">' );
                                                        $( target ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().removeClass( 'work-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().addClass( 'holiday-icon' );
                                                        $( target ).find( '.data-area' ).prev().prev().text( '休' );
                                                    } else {
                                                        if ( value.number == 1 ) {
                                                            $( target ).find( '.data-area' ).empty();
                                                            $( target ).find( '.data-area' ).prepend( '<input type="hidden" name="flg_' + target_number + '" value="1">' );
                                                            $( target ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().addClass( 'work-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().removeClass( 'holiday-icon' );
                                                            $( target ).find( '.data-area' ).prev().prev().text( '出' );
                                                        }
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="from_' + target_number + '_' + value.number + '" value="' + value.time_from.substr( 0, value.time_from.lastIndexOf(':') ) + '">' );
                                                        $( target ).find( '.data-area' ).append( '<input type="hidden" name="to_' + target_number + '_' + value.number + '" value="' + value.time_to.substr( 0, value.time_to.lastIndexOf(':') ) + '">' );
                                                    }
                                                });
                                            }
                                        }
                                    }
                                });
                            });
                        }).fail( function(){
                            
                        });
                    });
                });
            } else if ( $( '#manager_all_input_form [name=method]:checked' ).val() == '2' ) {
                if ( $( '#manager_all_input_form [name=type]:checked' ).val() == '1' ) {
                    for ( var i = 1; i <= 4; i++ ) {
                        if ( check_empty( $( '#manager_all_input_form [name=date_' + i + ']' ).val() ) ) {
                            date_list.push( $( '#manager_all_input_form [name=date_' + i + ']' ).val() );
                        }
                    }
                } else if ( $( '#manager_all_input_form [name=type]:checked' ).val() == '2' ) {
                    for ( var i = Number($( '#manager_all_input_form [name=period_from]' ).val()); i <= Number($( '#manager_all_input_form [name=period_to]' ).val()); i++ ) {
                        date_list.push( i );
                    }
                } else if ( $( '#manager_all_input_form [name=type]:checked' ).val() == '3' ) {
                    $( '#manager_all_input_form [name=week]:checked' ).each( function( index, value ) {
                        if ( $( this ).val() == '1' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(日)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(日)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '2' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(月)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(月)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '3' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(火)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(火)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '4' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(水)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(水)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '5' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(木)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(木)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '6' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(金)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(金)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '7' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).text().indexOf( '(土)' ) !== -1 ) {
                                    date_list.push( Number($( this ).text().replace( '(土)', '' )) );
                                }
                            });
                        } else if ( $( this ).val() == '8' ) {
                            $( '.manager-table thead th' ).each( function( index, value ){
                                if ( $( this ).css( 'color' ) == 'rgb(255, 91, 91)' && $( this ).text().indexOf( '(日)' ) === -1 ) {
                                    date_list.push( Number($( this ).text().substr( 0, $( this ).text().indexOf( '(' ) )) );
                                }
                            });
                        }
                    });
                } else if ( $( '#manager_all_input_form [name=type]:checked' ).val() == '4' ) {
                    for ( var i = 1; i <= 31; i++ ) {
                        date_list.push( i );
                    }
                }

                $.each( setting_list, function( setting_index, setting_value ) {
                    $.each( manager_list, function( manager_index, manager_value ) {
                        $.each( date_list, function( date_index, date_value ) {
                            var target = setting_value + '_' + manager_value + '_' + date_value;
                            $( '.manager-table tr td' ).each( function( index, value ) {
                                if ( $( this ).find( 'input[type=hidden]' ).eq(0).val() == setting_value && $( this ).find( 'input[type=hidden]' ).eq(1).val() == manager_value && $( this ).find( 'input[type=hidden]' ).eq(2).val() == date_value ) {
                                    $( this ).find( '.data-area' ).empty();
                                    if ( $( '#manager_all_input_form [name=all_flg]:checked' ).val() == '0' ) {
                                        $( this ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target + '" value="0">' );
                                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'work-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().addClass( 'holiday-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().text( '休' );
                                    } else if ( $( '#manager_all_input_form [name=all_flg]:checked' ).val() == '1' ) {
                                        $( this ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target + '" value="1">' );
                                        for ( var i = 1; i <= $( '#manager_all_input_modal .manager-all-area .d-flex' ).length - 2; i++ ) {
                                            if ( check_empty($( '#manager_all_input_modal [name=time_from_' + i + ']' ).val()) && check_empty($( '#manager_all_input_modal [name=time_to_' + i + ']' ).val()) ) {
                                                $( this ).find( '.data-area' ).append( '<input type="hidden" name="from_' + target + '_' + i + '" value="' + $( '#manager_all_input_modal [name=time_from_' + i + ']' ).val() + '">' );
                                                $( this ).find( '.data-area' ).append( '<input type="hidden" name="to_' + target + '_' + i + '" value="' + $( '#manager_all_input_modal [name=time_to_' + i + ']' ).val() + '">' );
                                            }
                                        }
                                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().addClass( 'work-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'holiday-icon' );
                                        $( this ).find( '.data-area' ).prev().prev().text( '出' );
                                    }
                                }
                            });
                        });
                    });
                });
            }

            $( '#manager_all_input_modal .no-button' ).trigger( 'click' );
        }
    });

    $( document ).on( 'click', '#manager_all_input_modal .no-button', function () {
        $( '#manager_all_input_modal [name=setting]' ).each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#manager_all_input_modal [name=manager]' ).each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#manager_all_input_modal [name=method]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#manager_all_input_modal [name=type]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#manager_all_input_modal [name=date_1]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=date_1]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=date_1]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=date_1]' ).val( '' );
        $( '#manager_all_input_modal [name=date_2]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=date_2]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=date_2]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=date_2]' ).val( '' );
        $( '#manager_all_input_modal [name=date_3]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=date_3]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=date_3]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=date_3]' ).val( '' );
        $( '#manager_all_input_modal [name=date_4]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=date_4]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=date_4]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=date_4]' ).val( '' );
        $( '#manager_all_input_modal [name=period_from]' ).prop( 'disabled', true );
        $( '#manager_all_input_modal [name=period_from]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=period_from]' ).addClass( 'readonly' );
        $( '#manager_all_input_modal [name=period_from]' ).val( '' );
        $( '#manager_all_input_modal [name=period_to]' ).prop( 'disabled', true );
        $( '#manager_all_input_modal [name=period_to]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=period_to]' ).addClass( 'readonly' );
        $( '#manager_all_input_modal [name=period_to]' ).val( '' );
        $( '#manager_all_input_modal [name=week]' ).each( function( index, value ) {
            $( this ).prop( 'disabled', true );
            $( this ).prop( 'checked', false );
        });

        for ( var i = $( '#manager_all_input_modal .manager-all-area .d-flex' ).length; i > 3; i-- ) {
            $( '#manager_all_input_modal .manager-all-area .d-flex' ).eq( i - 3 ).remove();
        }
        $( '#manager_all_input_modal [name=all_flg]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=time_from_1]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=time_from_1]' ).val( '' );
        $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'disabled', false );
        $( '#manager_all_input_modal [name=time_to_1]' ).prop( 'required', false );
        $( '#manager_all_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
        $( '#manager_all_input_modal [name=time_to_1]' ).val( '' );

        $( '#manager_all_input_modal #manager_all_method_date_area' ).addClass( 'd-none' );
    });

    $( document ).on( 'click', '#manager_all_reset_modal .yes-button', function () {
        var setting_list = [];
        $( '#manager_all_input_form [name=setting]' ).each( function( index, value ) {
            setting_list.push( $( this ).val() );
        });
        var manager_list = [];
        $( '#manager_all_input_form [name=manager]' ).each( function( index, value ) {
            manager_list.push( $( this ).val() );
        });
        var date_list = [];
        for ( var i = 1; i <= 31; i++ ) {
            date_list.push( i );
        }
        $.each( setting_list, function( setting_index, setting_value ) {
            $.each( manager_list, function( manager_index, manager_value ) {
                $.each( date_list, function( date_index, date_value ) {
                    var target = setting_value + '_' + manager_value + '_' + date_value;
                    $( '#save_manager_form [name=flg_' + target + ']' ).parent().prev().prev().removeClass( 'work-icon' );
                    $( '#save_manager_form [name=flg_' + target + ']' ).parent().prev().prev().removeClass( 'holiday-icon' );
                    $( '#save_manager_form [name=flg_' + target + ']' ).parent().prev().prev().addClass( 'no-icon' );
                    $( '#save_manager_form [name=flg_' + target + ']' ).parent().prev().prev().text( '' );
                    $( '#save_manager_form [name=flg_' + target + ']' ).parent().empty();
                });
            });
        });
        $( '#manager_all_reset_modal .no-button' ).trigger( 'click' );
    });

    $( document ).on( 'change', '#manager_input_modal [name=flg]', function () {
        if ( $( this ).val() == '0' ) {
            for ( var i = $( '#manager_input_modal #manager_input_form .d-flex' ).length; i > 3; i-- ) {
                $( '#manager_input_modal #manager_input_form .d-flex' ).eq( i - 3 ).remove();
            }
            $( '#manager_input_modal [name=time_from_1]' ).prop( 'disabled', true );
            $( '#manager_input_modal [name=time_from_1]' ).prop( 'required', false );
            $( '#manager_input_modal [name=time_from_1]' ).addClass( 'readonly' );
            $( '#manager_input_modal [name=time_from_1]' ).val( '' );
            $( '#manager_input_modal [name=time_to_1]' ).prop( 'disabled', true );
            $( '#manager_input_modal [name=time_to_1]' ).prop( 'required', false );
            $( '#manager_input_modal [name=time_to_1]' ).addClass( 'readonly' );
            $( '#manager_input_modal [name=time_to_1]' ).val( '' );
        } else if ( $( this ).val() == '1' ) {
            $( '#manager_input_modal [name=time_from_1]' ).prop( 'disabled', false );
            $( '#manager_input_modal [name=time_from_1]' ).prop( 'required', true );
            $( '#manager_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
            $( '#manager_input_modal [name=time_to_1]' ).prop( 'disabled', false );
            $( '#manager_input_modal [name=time_to_1]' ).prop( 'required', true );
            $( '#manager_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
        }
    });

    $( document ).on( 'click', '#manager_input_modal .add-time-button', function () {
        if ( $( '#manager_input_modal [name=flg]:checked' ).val() == '1' ) {
            var number = $( this ).parents( '#manager_input_form' ).find( '.d-flex' ).length - 1;
            
            var html = '<div class="d-flex align-items-center mt-1">';
            html += '<div style="width: 107.5px;"></div>';
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

    $( document ).on( 'click', '#manager_input_modal .yes-button', function () {
        if ( $( '#manager_input_form' ).parsley().validate() && check_time() ) {
            var target = $( '#manager_input_modal #input_setting' ).val() + '_' + $( '#manager_input_modal #input_manager' ).val() + '_' + $( '#manager_input_modal #input_day' ).val();
            $( '.manager-table tr td' ).each( function( index, value ) {
                if ( $( this ).find( 'input[type=hidden]' ).eq(0).val() == $( '#manager_input_modal #input_setting' ).val() && $( this ).find( 'input[type=hidden]' ).eq(1).val() == $( '#manager_input_modal #input_manager' ).val() && $( this ).find( 'input[type=hidden]' ).eq(2).val() == $( '#manager_input_modal #input_day' ).val() ) {
                    $( this ).find( '.data-area' ).empty();
                    if ( $( '#manager_input_form [name=flg]:checked' ).val() == '0' ) {
                        $( this ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target + '" value="0">' );
                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'work-icon' );
                        $( this ).find( '.data-area' ).prev().prev().addClass( 'holiday-icon' );
                        $( this ).find( '.data-area' ).prev().prev().text( '休' );
                    } else if ( $( '#manager_input_form [name=flg]:checked' ).val() == '1' ) {
                        $( this ).find( '.data-area' ).append( '<input type="hidden" name="flg_' + target + '" value="1">' );
                        for ( var i = 1; i <= $( '#manager_input_modal #manager_input_form .d-flex' ).length - 2; i++ ) {
                            if ( check_empty($( '#manager_input_modal [name=time_from_' + i + ']' ).val()) && check_empty($( '#manager_input_modal [name=time_to_' + i + ']' ).val()) ) {
                                $( this ).find( '.data-area' ).append( '<input type="hidden" name="from_' + target + '_' + i + '" value="' + $( '#manager_input_modal [name=time_from_' + i + ']' ).val() + '">' );
                                $( this ).find( '.data-area' ).append( '<input type="hidden" name="to_' + target + '_' + i + '" value="' + $( '#manager_input_modal [name=time_to_' + i + ']' ).val() + '">' );
                            }
                        }
                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'no-icon' );
                        $( this ).find( '.data-area' ).prev().prev().addClass( 'work-icon' );
                        $( this ).find( '.data-area' ).prev().prev().removeClass( 'holiday-icon' );
                        $( this ).find( '.data-area' ).prev().prev().text( '出' );
                    }
                }
            });

            $( '#manager_input_modal .no-button' ).trigger( 'click' );
        }
    });

    $( document ).on( 'click', '#manager_input_modal .no-button', function () {
        for ( var i = $( '#manager_input_modal #manager_input_form .d-flex' ).length; i > 3; i-- ) {
            $( '#manager_input_modal #manager_input_form .d-flex' ).eq( i - 3 ).remove();
        }
        $( '#manager_input_modal [name=flg]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        $( '#manager_input_modal [name=time_from_1]' ).prop( 'disabled', false );
        $( '#manager_input_modal [name=time_from_1]' ).prop( 'required', true );
        $( '#manager_input_modal [name=time_from_1]' ).removeClass( 'readonly' );
        $( '#manager_input_modal [name=time_from_1]' ).val( '' );
        $( '#manager_input_modal [name=time_to_1]' ).prop( 'disabled', false );
        $( '#manager_input_modal [name=time_to_1]' ).prop( 'required', true );
        $( '#manager_input_modal [name=time_to_1]' ).removeClass( 'readonly' );
        $( '#manager_input_modal [name=time_to_1]' ).val( '' );
        $( '#manager_input_modal #input_setting' ).val( '' );
        $( '#manager_input_modal #input_manager' ).val( '' );
        $( '#manager_input_modal #input_day' ).val( '' );
    });
});

function check_all_time() {
    var flg = true;
    if ( $( '#manager_all_input_modal [name=method]:checked' ).val() == '2' && $( '#manager_all_input_modal [name=all_flg]:checked' ).val() == '1' ) {
        var last_time = null;
        for ( var i = 1; i <= $( '#manager_all_input_modal .manager-all-area .d-flex' ).length - 2; i++ ) {
            if ( $( '#manager_all_input_modal [name=time_from_' + i + ']' ).val() >= $( '#manager_all_input_modal [name=time_to_' + i + ']' ).val() ) {
                $( '#manager_all_input_modal [name=time_from_' + i + ']' ).addClass( 'parsley-error' );
                $( '#manager_all_input_modal [name=time_to_' + i + ']' ).addClass( 'parsley-error' );
                flg = false;
            }
            if ( check_empty(last_time) && last_time >= $( '#manager_all_input_modal [name=time_from_' + i + ']' ).val() ) {
                $( '#manager_all_input_modal [name=time_from_' + i + ']' ).addClass( 'parsley-error' );
                $( '#manager_all_input_modal [name=time_to_' + i + ']' ).addClass( 'parsley-error' );
                flg = false;
            }
            last_time = $( '#manager_all_input_modal [name=time_to_' + i + ']' ).val();
        }
    }
    return flg;
}
function check_time() {
    var flg = true;
    if ( $( '#manager_input_modal [name=flg]:checked' ).val() == '1' ) {
        var last_time = null;
        for ( var i = 1; i <= $( '#manager_input_modal #manager_input_form .d-flex' ).length - 2; i++ ) {
            if ( $( '#manager_input_modal [name=time_from_' + i + ']' ).val() >= $( '#manager_input_modal [name=time_to_' + i + ']' ).val() ) {
                $( '#manager_input_modal [name=time_from_' + i + ']' ).addClass( 'parsley-error' );
                $( '#manager_input_modal [name=time_to_' + i + ']' ).addClass( 'parsley-error' );
                flg = false;
            }
            if ( check_empty(last_time) && last_time >= $( '#manager_input_modal [name=time_from_' + i + ']' ).val() ) {
                $( '#manager_input_modal [name=time_from_' + i + ']' ).addClass( 'parsley-error' );
                $( '#manager_input_modal [name=time_to_' + i + ']' ).addClass( 'parsley-error' );
                flg = false;
            }
            last_time = $( '#manager_input_modal [name=time_to_' + i + ']' ).val();
        }
    }
    return flg;
}