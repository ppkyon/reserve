$( function(){
    var form_data = new FormData();
    form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
    $.ajax({
        'data': form_data,
        'url': $( '#check_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        setTimeout( function() {
            $( '[name=place_flg]' ).val( response.place_flg );
            $( '[name=course_flg]' ).val( response.course_flg );
            $( '[name=question_flg]' ).val( response.question_flg );
            create_menu( response, 'place' );
            create_menu( response, 'course' );
            create_menu( response, 'date' );
            create_menu( response, 'question' );
            create_menu( response, 'check' );
            create_menu( response, 'end' );

            if ( response.error_flg ) {
                $( '.date-area' ).addClass( 'd-none' );
                $( '.error-area' ).removeClass( 'd-none' );
            } else if ( response.place_flg ) {
                create_place(response);
            } else if ( response.course_flg ) {
                create_course(response);
            } else {
                create_date(response);
            }
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
        }, 750 );
    }).fail( function(){
        
    });
});

function create_menu(response, target) {
    $( '.date-area' ).removeClass( 'd-none' );
    var menu_count = 3;
    if ( response.question_flg ) {
        menu_count = menu_count + 1;
    } else {
        $( '.' + target + '-area .menu-area .menu-bar' ).eq(3).remove();
        $( '.' + target + '-area .menu-area .menu-icon' ).eq(3).remove();
        $( '.' + target + '-area .menu-area .menu-text' ).eq(3).remove();
    }
    if ( response.course_flg ) {
        $( '.date-area' ).addClass( 'd-none' );
        $( '.course-area' ).removeClass( 'd-none' );
        menu_count = menu_count + 1;
    } else {
        $( '.' + target + '-area .menu-area .menu-bar' ).eq(1).remove();
        $( '.' + target + '-area .menu-area .menu-icon' ).eq(1).remove();
        $( '.' + target + '-area .menu-area .menu-text' ).eq(1).remove();
    }
    if ( response.place_flg ) {
        $( '.date-area' ).addClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.place-area' ).removeClass( 'd-none' );
        menu_count = menu_count + 1;
    } else {
        $( '.' + target + '-area .menu-area .menu-bar' ).eq(0).remove();
        $( '.' + target + '-area .menu-area .menu-icon' ).eq(0).remove();
        $( '.' + target + '-area .menu-area .menu-text' ).eq(0).remove();
    }
    if ( menu_count == 3 ) {
        $( '.' + target + '-area .menu-area .menu-bar' ).each( function() {
            $( this ).css( 'width', '17.5vw' );
        });
        $( '.' + target + '-area .menu-area .menu-icon' ).each( function() {
            $( this ).css( 'width', '11vw' );
            $( this ).css( 'height', '11vw' );
        });
        $( '.' + target + '-area .menu-area .menu-text' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).css( 'width', '44%' );
            } else if ( index == 1 ) {
                $( this ).css( 'width', '12%' );
            } else if ( index == 2 ) {
                $( this ).css( 'width', '44%' );
            }
        });
    } else if ( menu_count == 4 ) {
        $( '.' + target + '-area .menu-area .menu-bar' ).each( function() {
            $( this ).css( 'width', '12.5vw' );
        });
        $( '.' + target + '-area .menu-area .menu-icon' ).each( function() {
            $( this ).css( 'width', '11vw' );
            $( this ).css( 'height', '11vw' );
        });
        $( '.' + target + '-area .menu-area .menu-text' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).css( 'width', '37%' );
            } else if ( index == 1 ) {
                $( this ).css( 'margin-right', '3.5%' );
                $( this ).css( 'width', '18%' );
            } else if ( index == 2 ) {
                $( this ).css( 'margin-left', '3.5%' );
                $( this ).css( 'width', '18%' );
            } else if ( index == 3 ) {
                $( this ).css( 'width', '37%' );
            }
        });
    } else if ( menu_count == 5 ) {
        $( '.' + target + '-area .menu-area .menu-bar' ).each( function() {
            $( this ).css( 'width', '7.5vw' );
        });
        $( '.' + target + '-area .menu-area .menu-icon' ).each( function() {
            $( this ).css( 'width', '11vw' );
            $( this ).css( 'height', '11vw' );
        });
        $( '.' + target + '-area .menu-area .menu-text' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).css( 'width', '26%' );
            } else if ( index == 1 ) {
                $( this ).css( 'margin-right', '4%' );
                $( this ).css( 'width', '17%' );
            } else if ( index == 2 ) {
                $( this ).css( 'width', '14%' );
            } else if ( index == 3 ) {
                $( this ).css( 'margin-left', '4%' );
                $( this ).css( 'width', '17%' );
            } else if ( index == 4 ) {
                $( this ).css( 'width', '26%' );
            }
        });
    } else if ( menu_count == 6 ) {
        $( '.' + target + '-area .menu-area .menu-bar' ).each( function() {
            $( this ).css( 'width', '7.5vw' );
        });
        $( '.' + target + '-area .menu-area .menu-icon' ).each( function() {
            $( this ).css( 'width', '11vw' );
            $( this ).css( 'height', '11vw' );
        });
        $( '.' + target + '-area .menu-area .menu-text' ).each( function( index, value ) {
            $( this ).css( 'width', '18.8%' );
        });
    }
}

function create_place(response) {
    $( '.place-area .content-area .content-item-area-wrap' ).empty();
    if ( !response.course_flg ) {
        $( '.check-area .content-area .check-course-text' ).parent().remove();
        $( '.end-area .end-course-text' ).parent().remove();
    }
    if ( response.offline_list.length > 0 ) {
        var html = '<div class="content-item-area p-2 pb-3">';
        html += '<div class="content-item-title-area d-flex align-items-center mb-1">';
        html += '<p class="content-item-title mb-0">' + response.offline_place.name + '</p>';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/reserve/arrow.svg" class="arrow-icon ms-auto me-2" style="transform: rotate(180deg);">';
        html += '</div>';
        html += '<p class="content-item-description me-5 mb-1">' + response.offline_place.outline + '</p>';
        html += '<div class="content-place-area">';
        html += '<div class="row">';
        html += '<div class="col-12 p-0">';
        html += '<div class="content-place-item-area">';
        $.each( response.offline_list, function( index, value ) {
            html += '<div class="input-radio-wrap position-relative ms-2 mt-2 mb-1">';
            html += '<label for="setting_' + value.display_id + '" class="input-radio-text offline-setting-title ps-4 mb-0">' + value.name + '</label>';
            html += '<input type="radio" id="setting_' + value.display_id + '" name="setting" value="' + value.display_id + '" class="input-radio">';
            html += '<label for="setting_' + value.display_id + '" class="input-radio-mark mb-0"></label>';
            html += '</div>';
            html += '<p class="input-radio-description ms-4 mb-0">' + value.address + '<br>' + value.note + '</p>';
        });
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        $( '.place-area .content-area .content-item-area-wrap' ).append(html);
    }
    if ( response.online_list.length > 0 ) {
        var html = '<div class="content-item-area p-2 pb-3">';
        html += '<div class="content-item-title-area d-flex align-items-center mb-1">';
        html += '<p class="content-item-title mb-0">' + response.online_place.name + '</p>';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/reserve/arrow.svg" class="arrow-icon ms-auto me-2" style="transform: rotate(180deg);">';
        html += '</div>';
        html += '<p class="content-item-description me-5 mb-1">' + response.online_place.outline + '</p>';
        html += '<div class="content-place-area">';
        html += '<div class="row">';
        html += '<div class="col-12 p-0">';
        html += '<div class="content-place-item-area">';
        $.each( response.online_list, function( index, value ) {
            html += '<div class="input-radio-wrap position-relative ms-2 mt-2 mb-1">';
            html += '<label for="setting_' + value.display_id + '" class="input-radio-text ps-4 mb-0">' + value.name + '</label>';
            html += '<input type="radio" id="setting_' + value.display_id + '" name="setting" value="' + value.display_id + '" class="input-radio">';
            html += '<label for="setting_' + value.display_id + '" class="input-radio-mark mb-0"></label>';
            html += '</div>';
            html += '<p class="input-radio-description ms-4 mb-0">' + value.outline + '<br>' + value.note + '</p>';
        });
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        $( '.place-area .content-area .content-item-area-wrap' ).append(html);
    }
    if ( response.course_flg ) {
        $( '.place-area .footer-area .footer-button' ).text( 'コース選択へ' );
    } else {
        $( '.place-area .footer-area .footer-button' ).text( '日時選択へ' );
    }
}

function create_course(response) {
    $( '.course-area .content-area' ).empty();
    $( '.course-area .footer-area .back-button' ).parent().remove();

    $( '.footer-area .footer-course-text' ).each( function() {
        $( this ).parent().remove();
    });
    $( '.footer-area .footer-place-text' ).each( function() {
        $( this ).addClass( 'footer-course-text' );
    });
    $( '.check-area .content-area .check-place-text' ).parent().remove();
    $( '.end-area .end-place-text' ).parent().remove();
    $( '.course-area .content-area' ).append( '<input type="hidden" name="course_setting" value="' + response.online_offline.display_id + '">' );
    $.each( response.course_list, function( index, value ) {
        var html = '<div class="row mb-3">';
        html += '<div class="col-12 p-0">';
        html += '<div class="content-item-area p-2">';
        html += '<div class="content-course-area">';
        html += '<div class="content-course-item-area">';
        html += '<div class="input-radio-wrap position-relative ms-2 mt-2 mb-1">';
        html += '<div class="content-item-title-area content-item-title d-flex align-items-center mb-1">';
        html += '<label for="course_' + value.display_id + '" class="input-radio-text offline-course-title ps-4 mb-0">' + value.title + '</label>';
        html += '<input type="radio" id="course_' + value.display_id + '" name="course" value="' + value.display_id + '" class="input-radio">';
        html += '<label for="course_' + value.display_id + '" class="input-radio-mark mb-0"></label>';
        html += '</div>';
        html += '</div>';
        html += '<div class="row">';
        html += '<div class="col-12 p-0">';
        html += '<div class="position-relative ms-5 mt-1 mb-1">';
        html += '<p class="offline-course-title mb-0">' + value.outline + '</p>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        $( '.course-area .content-area' ).append( html );
    });
}

function create_date(response) {
    $( '.date-area .footer-area .back-button' ).parent().remove();
    
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
    $( '.footer-area .footer-course-text' ).each( function() {
        $( this ).parent().remove();
    });
    $( '.footer-area .footer-date-text' ).each( function() {
        $( this ).parent().remove();
    });
    $( '.footer-area .footer-place-text' ).each( function() {
        $( this ).addClass( 'footer-date-text' );
    });
    $( '.check-area .content-area .check-place-text' ).parent().remove();
    $( '.check-area .content-area .check-course-text' ).parent().remove();
    $( '.end-area .end-place-text' ).parent().remove();
    $( '.end-area .end-course-text' ).parent().remove();

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
}