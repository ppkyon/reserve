$( function(){
    $( document ).on( 'click', '.course-area .content-area .content-item-area .content-item-title-area', function () {
        $( this ).parent().find( '.content-course-area' ).toggle('fast');
        if ( $( this ).find( 'img' ).css( 'transform' ) == 'none' ) {
            $( this ).find( 'img' ).css( 'transform', 'rotate(180deg)' );
        } else {
            $( this ).find( 'img' ).css( 'transform', '' );
        }
    });
    $( document ).on( 'change', '.course-area .content-area .content-item-area .content-course-area [name=course]', function () {
        $( '.footer-area .footer-course-text' ).text( $( this ).prev().text() );
        $( '.check-area .check-course-text' ).text( $( this ).prev().text() );
        $( '.end-area .end-course-text' ).text( $( this ).prev().text() );
        $( '.course-area .footer-area' ).removeClass( 'd-none' );
    });
    $( '.course-area .footer-area .footer-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.date-area .footer-area' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'course_id', $( '.course-area .content-area .content-item-area .content-course-area [name=course]:checked' ).val() );
        if ( check_empty($( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val())) {
            form_data.append( 'id', $( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val() );
        } else {
            form_data.append( 'id', $( '[name=course_setting]' ).val() );
        }
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
            $( '.date-area .content-area .date-week-text' ).text( response.start + '～' + response.end );

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
                        var date = new Date(week_value.year, week_value.month, week_value.day, Number(schedule_value.time.substr( 0, schedule_value.time.indexOf( ':' ) )), Number(schedule_value.time.substr( schedule_value.time.indexOf( ':' ) + 1 )), 0);
                        var start_date = new Date(Number(response.start_date.year), Number(response.start_date.month), Number(response.start_date.day), Number(response.start_date.hour), Number(response.start_date.minute), 0);
                        if ( check_empty( response.end_date ) ) {
                            var end_date = new Date(response.end_date.year, response.end_date.month, response.end_date.day, 0, 0, 0);
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
            if ( response.question_flg ) {
                $( '.date-area .footer-area .footer-button' ).text( '設問へ' );
            } else {
                $( '.date-area .footer-area .footer-button' ).text( '予約内容確認へ' );
            }
            $( '.date-area' ).removeClass( 'd-none' );

            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.date-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
            
        });
    });
});