$( function(){
    $( '#edit_step_modal .input-schedule' ).on( 'click', function() {
        $( '#select_schedule_modal .date-area' ).addClass( 'd-none' );
        $( '#select_schedule_modal .date-loader-area' ).removeClass( 'd-none' );
        
        $( this ).next().trigger( 'click' );
        up_modal();

        $( '#select_schedule_modal [name=schedule_setting]' ).val( $( this ).parents( 'tr' ).find( '.content-course' ).next().next().val() );
        $( '#select_schedule_modal [name=schedule_setting]' ).next().val( $( this ).parents( 'tr' ).find( '.content-course' ).next().val() );
        $( '#select_schedule_modal [name=schedule_course]' ).val( $( this ).parents( 'tr' ).find( '.content-course' ).next().next().next().val() );

        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        form_data.append( 'setting_id', $( '#select_schedule_modal [name=schedule_setting]' ).next().val() );
        form_data.append( 'course_id', $( '#select_schedule_modal [name=schedule_course]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            create_date(response);
            $( '#select_schedule_modal .date-loader-area' ).addClass( 'd-none' );
            $( '#select_schedule_modal .date-area' ).removeClass( 'd-none' );
        }).fail( function(){
            
        });

    });
    $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu button' ).on( 'click', function() {
        $( '#select_schedule_modal .date-area' ).addClass( 'd-none' );
        $( '#select_schedule_modal .date-loader-area' ).removeClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        form_data.append( 'setting_id', $( this ).val() );
        form_data.append( 'course_id', $( '#select_schedule_modal [name=schedule_course]' ).val() );
        form_data.append( 'year', $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(0).val() );
        form_data.append( 'month', $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(1).val() );
        form_data.append( 'day', $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(2).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            create_date(response);
            setTimeout( function() {
                $( '#select_schedule_modal .date-loader-area' ).addClass( 'd-none' );
                $( '#select_schedule_modal .date-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
            
        });
    });
    $( '#select_schedule_modal .date-area .prev-text' ).on( 'click', function() {
        $( '#select_schedule_modal .date-area' ).addClass( 'd-none' );
        $( '#select_schedule_modal .date-loader-area' ).removeClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        form_data.append( 'setting_id', $( '#select_schedule_modal [name=schedule_setting]' ).next().val() );
        form_data.append( 'course_id', $( '#select_schedule_modal [name=schedule_course]' ).val() );
        form_data.append( 'year', $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(0).val() );
        form_data.append( 'month', $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(1).val() );
        form_data.append( 'day', $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(2).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            create_date(response);
            setTimeout( function() {
                $( '#select_schedule_modal .date-loader-area' ).addClass( 'd-none' );
                $( '#select_schedule_modal .date-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
            
        });
    });
    $( '#select_schedule_modal .date-area .next-text' ).on( 'click', function() {
        $( '#select_schedule_modal .date-area' ).addClass( 'd-none' );
        $( '#select_schedule_modal .date-loader-area' ).removeClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        form_data.append( 'setting_id', $( '#select_schedule_modal [name=schedule_setting]' ).next().val() );
        form_data.append( 'course_id', $( '#select_schedule_modal [name=schedule_course]' ).val() );
        form_data.append( 'year', $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(0).val() );
        form_data.append( 'month', $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(1).val() );
        form_data.append( 'day', $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(2).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            create_date(response);
            setTimeout( function() {
                $( '#select_schedule_modal .date-loader-area' ).addClass( 'd-none' );
                $( '#select_schedule_modal .date-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#select_schedule_modal .date-area table td.yes', function () {
        $( '#select_schedule_modal .date-area table td.yes' ).each( function( index, value ) {
            $( this ).removeClass( 'active' );
            $( this ).find( 'span' ).text( '◎' );
            $( this ).css( 'color', '#00B074' );
        });
        $( this ).addClass( 'active' );
        $( this ).find( 'span' ).text( '●' );
        $( this ).css( 'color', '#FF0000' );
    });
    $( document ).on( 'click', '#select_schedule_modal .yes-button', function () {
        $( this ).prop( 'disabled', true )
        $( '#select_schedule_modal .date-area' ).css( 'opacity', 0 );
        $( '#select_schedule_modal .loader-area' ).removeClass( 'd-none' );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        form_data.append( 'setting_id', $( '#select_schedule_modal [name=schedule_setting]' ).next().val() );
        form_data.append( 'course_id', $( '#select_schedule_modal [name=schedule_course]' ).val() );

        var year = null;
        var month = null;
        var day = null;
        var hour = null;
        var minute = null;
        $( '#select_schedule_modal .date-area table td.active' ).find( 'input[type=hidden]' ).each( function( index, value ) {
            if ( index == 0 ) {
                year = $( this ).val();
            } else if ( index == 1 ) {
                month = $( this ).val();
            } else if ( index == 2 ) {
                day = $( this ).val();
            } else if ( index == 3 ) {
                hour = $( this ).val().substring( 0, $( this ).val().indexOf(':') );
                minute = $( this ).val().substring( $( this ).val().indexOf(':')+1, $( this ).val().length );
            }
        });
        form_data.append( 'year', year );
        form_data.append( 'month', month );
        form_data.append( 'day', day );
        form_data.append( 'hour', hour );
        form_data.append( 'minute', minute );
        $.ajax({
            'data': form_data,
            'url': $( '#send_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( response.error ) {
                $( '#select_schedule_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
                $( target ).prop( 'disabled', false )
                $( '#select_schedule_modal .loader-area' ).addClass( 'd-none' );
                $( '#select_schedule_modal .date-area' ).css( 'opacity', 1 );
            } else {
                $( '#save_step_form .table-area .content-course' ).each( function( index, value ) {
                    if ( $( this ).next().val() == $( '#select_schedule_modal [name=schedule_setting]' ).next().val() ) {
                        $( this ).parents( 'tr' ).find( 'td' ).eq(2).find( 'input[type=text]' ).val(year + '/' + ('00' + month).slice(-2) + '/' + ('00' + day).slice(-2) + ' ' + hour + ':' + minute);
                        $( this ).parents( 'tr' ).find( 'td' ).eq(4).find( 'input[type=text]' ).val(response.manager.profile.family_name + ' ' + response.manager.profile.first_name);
                        $( this ).parents( 'tr' ).find( 'td' ).eq(4).find( 'input[type=text]' ).next().val(response.manager.display_id);
                        $( this ).parents( 'tr' ).find( 'td' ).eq(5).find( 'input[type=text]' ).val(response.facility.name);
                        $( this ).parents( 'tr' ).find( 'td' ).eq(5).find( 'input[type=text]' ).next().val(response.facility.display_id);
                    }
                });
                $( '#select_schedule_modal .no-button' ).trigger( 'click' );
                $( target ).prop( 'disabled', false )
                $( '#select_schedule_modal .loader-area' ).addClass( 'd-none' );
                $( '#select_schedule_modal .date-area' ).css( 'opacity', 1 );
            }
        }).fail( function(){
            
        });
    });
});

function create_date(response) {
    $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(0).val( response.year );
    $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(1).val( response.month );
    $( '#select_schedule_modal .date-area .date-text' ).find( 'input[type=hidden]' ).eq(2).val( response.day );
    $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(0).val( response.prev_year );
    $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(1).val( response.prev_month );
    $( '#select_schedule_modal .date-area .prev-text' ).find( 'input[type=hidden]' ).eq(2).val( response.prev_day );
    $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(0).val( response.next_year );
    $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(1).val( response.next_month );
    $( '#select_schedule_modal .date-area .next-text' ).find( 'input[type=hidden]' ).eq(2).val( response.next_day );

    var last_month = null;
    var month_flg = false;
    var month_count_1 = 0;
    var month_count_2 = 0;
    $.each( response.week_day, function( index, value ){
        if ( check_empty(last_month) && last_month != value.month ) {
            month_flg = true;
        }
        $( '#select_schedule_modal .date-area .day-text' ).eq(index).find( 'p' ).eq(0).text( value.day );
        if ( month_flg ) {
            month_count_2++;
        } else {
            month_count_1++;
        }
        last_month = value.month;
    });
    $( '#select_schedule_modal .date-area .add-date-text' ).remove();
    if ( month_count_1 > month_count_2 ) {
        if ( month_count_2 != 0 ) {
            $( '#select_schedule_modal .date-area .date-text' ).after( '<th class="add-date-text text-center" colspan="' + month_count_2 + '"></th>' );
            $( '#select_schedule_modal .date-area .date-text span' ).text( response.prev_year + '年' + response.prev_month + '月' );
        } else {
            $( '#select_schedule_modal .date-area .date-text span' ).text( response.year + '年' + response.month + '月' );
        }
        $( '#select_schedule_modal .date-area .date-text' ).attr( 'colspan', month_count_1 );
    } else if ( month_count_1 < month_count_2 ) {
        if ( month_count_1 != 0 ) {
            $( '#select_schedule_modal .date-area .date-text' ).before( '<th class="add-date-text text-center" colspan="' + month_count_1 + '"></th>' );
            $( '#select_schedule_modal .date-area .date-text span' ).text( response.next_year + '年' + response.next_month + '月' );
        } else {
            $( '#select_schedule_modal .date-area .date-text span' ).text( response.year + '年' + response.month + '月' );
        }
        $( '#select_schedule_modal .date-area .date-text' ).attr( 'colspan', month_count_2 );
    } else {
        $( '#select_schedule_modal .date-area .date-text' ).before( '<th class="add-date-text text-center" colspan="' + month_count_1 + '"></th>' );
        $( '#select_schedule_modal .date-area .date-text' ).attr( 'colspan', month_count_2 );
        $( '#select_schedule_modal .date-area .add-date-text' ).text( response.prev_year + '年' + response.prev_month + '月' );
        $( '#select_schedule_modal .date-area .date-text span' ).text( response.next_year + '年' + response.next_month + '月' );
    }

    $( '#select_schedule_modal .date-area table tbody' ).empty();
    if ( response.week_schedule.length > 0 ) {
        $.each( response.week_schedule, function( schedule_index, schedule_value ){
            $( '#select_schedule_modal .date-area table tbody' ).append( '<tr></tr>' );

            var html = '<td class="p-1">' + schedule_value.time + '</td>';
            $.each( schedule_value.week, function( week_index, week_value ){
                var date = new Date(week_value.year, week_value.month - 1, week_value.day, Number(schedule_value.time.substr( 0, schedule_value.time.indexOf( ':' ) )), Number(schedule_value.time.substr( schedule_value.time.indexOf( ':' ) + 1 )), 0);
                var start_date = new Date(Number(response.start_date.year), Number(response.start_date.month) - 1, Number(response.start_date.day), Number(response.start_date.hour), Number(response.start_date.minute), 0);
                if ( check_empty( response.end_date ) ) {
                    var end_date = new Date(response.end_date.year, response.end_date.month - 1, response.end_date.day, response.end_date.hour, response.end_date.minute, 0);
                    if ( date < start_date || date >= end_date ) {
                        html += '<td class="no p-1">';
                        html += '<span style="color: #000;">-</span>';
                        html += '<input type="hidden" value="' + week_value.year + '">';
                        html += '<input type="hidden" value="' + week_value.month + '">';
                        html += '<input type="hidden" value="' + week_value.day + '">';
                        html += '<input type="hidden" value="' + schedule_value.time + '">';
                        html += '<input type="hidden" value="' + schedule_value.add_time + '">';
                        html += '</td>';
                    } else {
                        if ( week_value.reception_flg ) {
                            html += '<td class="no p-1">';
                            html += '<span>✕</span>';
                            html += '<input type="hidden" value="' + week_value.year + '">';
                            html += '<input type="hidden" value="' + week_value.month + '">';
                            html += '<input type="hidden" value="' + week_value.day + '">';
                            html += '<input type="hidden" value="' + schedule_value.time + '">';
                            html += '<input type="hidden" value="' + schedule_value.add_time + '">';
                            html += '</td>';
                        } else {
                            html += '<td class="yes p-1">';
                            html += '<span>◎</span>';
                            html += '<input type="hidden" value="' + week_value.year + '">';
                            html += '<input type="hidden" value="' + week_value.month + '">';
                            html += '<input type="hidden" value="' + week_value.day + '">';
                            html += '<input type="hidden" value="' + schedule_value.time + '">';
                            html += '<input type="hidden" value="' + schedule_value.add_time + '">';
                            html += '</td>';
                        }
                    }
                } else {
                    if ( week_value.reception_flg ) {
                        html += '<td class="no p-1">';
                        html += '<span>✕</span>';
                        html += '<input type="hidden" value="' + week_value.year + '">';
                        html += '<input type="hidden" value="' + week_value.month + '">';
                        html += '<input type="hidden" value="' + week_value.day + '">';
                        html += '<input type="hidden" value="' + schedule_value.time + '">';
                        html += '<input type="hidden" value="' + schedule_value.add_time + '">';
                        html += '</td>';
                    } else {
                        html += '<td class="yes p-1">';
                        html += '<span>◎</span>';
                        html += '<input type="hidden" value="' + week_value.year + '">';
                        html += '<input type="hidden" value="' + week_value.month + '">';
                        html += '<input type="hidden" value="' + week_value.day + '">';
                        html += '<input type="hidden" value="' + schedule_value.time + '">';
                        html += '<input type="hidden" value="' + schedule_value.add_time + '">';
                        html += '</td>';
                    }
                }
            });
            html += '<td class="p-1">' + schedule_value.time + '</td>';
            $( '#select_schedule_modal .date-area table tbody tr' ).eq(schedule_index).append(html);
        });
    }
}