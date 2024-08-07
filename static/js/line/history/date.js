$( function(){
    $( '.date-area .content-area .date-arrow-icon' ).on( 'click', function() {
        $( '.date-area .content-area .date-content-area' ).addClass( 'd-none' );
        $( '.date-area .content-area .date-loader-area' ).removeClass( 'd-none' );
        
        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'flow_id', $( '.history-area .history-content-area.select' ).find( 'input[name=flow]' ).val() );
        form_data.append( 'schedule_id', $( '.history-area .history-content-area.select' ).find( 'input[name=schedule]' ).val() );
        form_data.append( 'place_id', $( '.history-area .history-content-area.select' ).find( 'input[name=place]' ).val() );
        if ( check_empty($( '.history-area .history-content-area.select' ).find( 'input[name=course]' ).val()) ) {
            form_data.append( 'course_id', $( '.history-area .history-content-area.select' ).find( 'input[name=course]' ).val() );
        }
        form_data.append( 'setting_id', $( '.history-area .history-content-area.select' ).find( 'input[name=setting]' ).val() );
        form_data.append( 'year', $( this ).next().val() );
        form_data.append( 'month', $( this ).next().next().val() );
        form_data.append( 'day', $( this ).next().next().next().val() );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            
            $( '.date-area .content-area .date-year-text' ).text( response.year );
            $( '.date-area .content-area .date-year-text' ).next().val( response.year );
            $( '.date-area .content-area .date-week-text' ).text( response.start + '～' + response.end );
            $( '.date-area .content-area .date-week-text' ).next().val( response.start.substring(0, response.start.indexOf('月')) );
            $( '.date-area .content-area .date-week-text' ).next().next().val( response.start.substring(response.start.indexOf('月')+1, response.start.indexOf('日')) );

            $( '.date-area .content-area .prev-date-arrow' ).next().val( response.prev_year );
            $( '.date-area .content-area .prev-date-arrow' ).next().next().val( response.prev_month );
            $( '.date-area .content-area .prev-date-arrow' ).next().next().next().val( response.prev_day );
            $( '.date-area .content-area .next-date-arrow' ).next().val( response.next_year );
            $( '.date-area .content-area .next-date-arrow' ).next().next().val( response.next_month );
            $( '.date-area .content-area .next-date-arrow' ).next().next().next().val( response.next_day );

            $( '.date-area .content-area .date-table tbody' ).empty();
            $.each( response.week_day, function( index, value ){
                $( '.date-area .content-area .date-table th .calendar-day-text' ).eq(index).text( value.day );
            });

            $( '.date-area .content-area' ).append( '<input type="hidden" name="date_setting" value="' + response.online_offline.display_id + '">' );
            $( '.date-area [name=select_setting]' ).val( response.setting.name );
            $( '.date-area [name=select_setting]' ).next().val( response.setting.display_id );
            $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).empty();
            $.each( response.setting_list, function( index, value ) {
                if ( index == 0 ) {
                    $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).append( '<button type="button" value="' + value.display_id + '" class="btn dropdown-item fw-bold text-center">' + value.name + '</button>' );
                } else {
                    $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).append( '<button type="button" value="' + value.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + value.name + '</button>' );
                }
            });

            if ( response.week_schedule.length > 0 ) {
                $.each( response.week_schedule, function( schedule_index, schedule_value ){
                    $( '.date-area .content-area .date-table tbody' ).append( '<tr></tr>' );

                    var html = '<td class="p-1">' + schedule_value.time + '</td>';
                    $.each( schedule_value.week, function( week_index, week_value ){
                        var date = new Date(week_value.year, week_value.month - 1, week_value.day, Number(schedule_value.time.substr( 0, schedule_value.time.indexOf( ':' ) )), Number(schedule_value.time.substr( schedule_value.time.indexOf( ':' ) + 1 )), 0);
                        var start_date = new Date(Number(response.start_date.year), Number(response.start_date.month) - 1, Number(response.start_date.day), Number(response.start_date.hour), Number(response.start_date.minute), 0);
                        if ( check_empty( response.end_date ) ) {
                            var end_date = new Date(response.end_date.year, response.end_date.month - 1, response.end_date.day, response.end_date.hour, response.end_date.minute, 0);
                            if ( date < start_date || date >= end_date ) {
                                html += '<td class="no p-1">';
                                html += '<span style="color: #000;">-</span>';
                                if ( week_index == 0 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 1 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 2 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 3 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 4 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 5 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 6 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                }
                                html += '</td>';
                            } else {
                                if ( week_value.reception_flg ) {
                                    html += '<td class="no p-1">';
                                    html += '<span>✕</span>';
                                    if ( week_index == 0 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 1 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 2 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 3 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 4 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 5 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 6 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    }
                                    html += '</td>';
                                } else {
                                    html += '<td class="yes p-1">';
                                    html += '<span>◎</span>';
                                    if ( week_index == 0 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 1 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 2 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 3 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 4 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 5 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    } else if ( week_index == 6 ) {
                                        html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                    }
                                    html += '</td>';
                                }
                            }
                        } else {
                            if ( week_value.reception_flg ) {
                                html += '<td class="no p-1">';
                                html += '<span>✕</span>';
                                if ( week_index == 0 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 1 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 2 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 3 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 4 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 5 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 6 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                }
                                html += '</td>';
                            } else {
                                html += '<td class="yes p-1">';
                                html += '<span>◎</span>';
                                if ( week_index == 0 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 1 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 2 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 3 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 4 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 5 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                } else if ( week_index == 6 ) {
                                    html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                                }
                                html += '</td>';
                            }
                        }
                    });
                    $( '.date-area .content-area .date-table tbody tr' ).eq(schedule_index).append(html);
                });
            }
            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.date-area' ).removeClass( 'd-none' );
                $( '.date-area .content-area .date-loader-area' ).addClass( 'd-none' );
                $( '.date-area .content-area .date-content-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.date-area .content-area .date-table td.yes', function () {
        $( '.date-area .content-area .date-table td.yes' ).each( function( index, value ) {
            $( this ).removeClass( 'active' );
            $( this ).find( 'span' ).text( '◎' );
            $( this ).css( 'color', '#00B074' );
        });
        $( this ).addClass( 'active' );
        $( this ).find( 'span' ).text( '●' );
        $( this ).css( 'color', '#FF0000' );
        
        $( '.footer-area .footer-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.history-check-area .check-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.history-end-area .end-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.button-area .reserve-button' ).val( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.date-area .footer-area' ).removeClass( 'd-none' );
    });

    $( '.date-area .footer-area .footer-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'setting_id', $( '.history-area .history-content-area.select' ).find( 'input[name=setting]' ).val() );
        if ( check_empty($( '.history-area .history-content-area.select' ).find( 'input[name=course]' ).val()) ) {
            form_data.append( 'course_id', $( '.history-area .history-content-area.select' ).find( 'input[name=course]' ).val() );
        } else {
            form_data.append( 'course_id', '' );
        }

        form_data.append( 'year', $( '.button-area .reserve-button' ).val().substring( 0, $( '.button-area .reserve-button' ).val().indexOf('年') ) );
        form_data.append( 'month', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('年')+1, $( '.button-area .reserve-button' ).val().indexOf('月') ) );
        form_data.append( 'day', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('月')+1, $( '.button-area .reserve-button' ).val().indexOf('日') ) );
        form_data.append( 'hour', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(')')+2, $( '.button-area .reserve-button' ).val().indexOf(':') ) );
        form_data.append( 'minute', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(':')+1, $( '.button-area .reserve-button' ).val().indexOf('～') ) );

        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_temp_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.history-check-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
        
        });
    });
});