$( function() {
    $( document ).on( 'click', '.today-area .action-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_step_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( check_empty(response.profile) && check_empty(response.profile.image) ) {
                $( '#edit_step_modal .user-image' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
                $( '#select_schedule_modal .user-image' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
            } else if ( check_empty(response.display_image) ) {
                $( '#edit_step_modal .user-image' ).attr( 'src', response.display_image );
                $( '#select_schedule_modal .user-image' ).attr( 'src', response.display_image );
            } else {
                $( '#edit_step_modal .user-image' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                $( '#select_schedule_modal .user-image' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
            }
            if ( check_empty(response.profile) && check_empty(response.profile.name) ) {
                if ( check_empty(response.profile) && check_empty(response.profile.age) ) {
                    $( '#edit_step_modal .modal-header .title' ).text( response.profile.name + ' (' + response.profile.age + ')' );
                    $( '#select_schedule_modal .modal-header .title' ).text( response.profile.name + ' (' + response.profile.age + ')' );
                } else {
                    $( '#edit_step_modal .modal-header .title' ).text( response.profile.name );
                    $( '#select_schedule_modal .modal-header .title' ).text( response.profile.name );
                }
            } else {
                if ( check_empty(response.profile) && check_empty(response.profile.age) ) {
                    $( '#edit_step_modal .modal-header .title' ).text( response.display_name + ' (' + response.profile.age + ')' );
                    $( '#select_schedule_modal .modal-header .title' ).text( response.display_name + ' (' + response.profile.age + ')' );
                } else {
                    $( '#edit_step_modal .modal-header .title' ).text( response.display_name );
                    $( '#select_schedule_modal .modal-header .title' ).text( response.display_name );
                }
            }
            if ( check_empty(response.profile) && check_empty(response.profile.atelle_id) ) {
                $( '#edit_step_modal .modal-header .sub' ).text( '#' + response.profile.atelle_id );
                $( '#select_schedule_modal .modal-header .sub' ).text( '#' + response.profile.atelle_id );
            } else {
                $( '#edit_step_modal .modal-header .sub' ).text( '' );
                $( '#select_schedule_modal .modal-header .sub' ).text( '' );
            }
            $( '#save_step_form [name=user_id]' ).val( response.display_id );

            $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu' ).empty();
            $( '#save_step_form table tbody' ).empty();
            $.each( response.flow, function( index ,value ) {
                if ( !value.end_flg ) {
                    var setting_count = 0;
                    $.each( value.schedule, function( schedule_index, schedule_value ) {
                        if ( schedule_value.join == 0 ) {
                            if ( setting_count == 0 ) {
                                if ( check_empty( schedule_value.online ) ) {
                                    $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu' ).append( '<button type="button" value="' + schedule_value.online.display_id + '" class="btn dropdown-item fw-bold text-start p-1 pt-2 pb-2 ps-2">' + schedule_value.online.name + '</button>' );
                                } else if ( check_empty( schedule_value.offline ) ) {
                                    $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu' ).append( '<button type="button" value="' + schedule_value.offline.display_id + '" class="btn dropdown-item fw-bold text-start p-1 pt-2 pb-2 ps-2">' + schedule_value.offline.name + '</button>' );
                                }
                            } else {
                                if ( check_empty( schedule_value.online ) ) {
                                    $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu' ).append( '<button type="button" value="' + schedule_value.online.display_id + '" class="btn dropdown-item fw-bold text-start border-top p-1 pt-2 ps-2">' + schedule_value.online.name + '</button>' );
                                } else if ( check_empty( schedule_value.offline ) ) {
                                    $( '#select_schedule_modal .input-schedule-setting-dropdown .dropdown-menu' ).append( '<button type="button" value="' + schedule_value.offline.display_id + '" class="btn dropdown-item fw-bold text-start border-top p-1 pt-2 ps-2">' + schedule_value.offline.name + '</button>' );
                                }
                            }
                            setting_count++;
                        }
                    });
                }

                var html = '<tr>';
                html += '<td class="position-relative ps-3 pe-1" rowspan="2">';
                if ( index == 0 ) {
                    if ( value.end_flg ) {
                        html += '<label class="process pass mb-0"></label>';
                    } else {
                        html += '<label class="process mb-0"></label>';
                    }
                } else {
                    if ( value.end_flg ) {
                        html += '<label class="process any pass mb-0"></label>';
                    } else {
                        html += '<label class="process any mb-0"></label>';
                    }
                }
                html += '</td>';
                html += '<td class="position-relative" rowspan="2">';
                $.each( value.schedule, function( schedule_index, schedule_value ) {
                    if ( schedule_index == value.schedule.length - 1 ) {
                        if ( check_empty( schedule_value.online ) ) {
                            html += '<label class="online-offline-mark ps-2 pe-2 mb-0">オンライン</label>';
                            if ( check_empty(schedule_value.online_course) ) {
                                html += '<p class="content-course mb-0">' + schedule_value.online_course.title + '</p>';
                            } else {
                                html += '<p class="content-course mb-0">-</p>';
                            }
                            html += '<input type="hidden" value="' + schedule_value.online.display_id + '">';
                            html += '<input type="hidden" value="' + schedule_value.online.name + '">';
                            if ( check_empty(schedule_value.online_course) ) {
                                html += '<input type="hidden" value="' + schedule_value.online_course.display_id + '">';
                            } else {
                                html += '<input type="hidden" value="">';
                            }
                        } else if ( check_empty( schedule_value.offline ) ) {
                            html += '<label class="online-offline-mark ps-2 pe-2 mb-0">対面</label>';
                            if ( check_empty(schedule_value.offline_course) ) {
                                html += '<p class="content-course mb-0">' + schedule_value.offline_course.title + '</p>';
                            } else {
                                html += '<p class="content-course mb-0">-</p>';
                            }
                            html += '<input type="hidden" value="' + schedule_value.offline.display_id + '">';
                            html += '<input type="hidden" value="' + schedule_value.offline.name + '">';
                            if ( check_empty(schedule_value.offline_course) ) {
                                html += '<input type="hidden" value="' + schedule_value.offline_course.display_id + '">';
                            } else {
                                html += '<input type="hidden" value="">';
                            } 
                        }
                    }
                });
                html += '<div class="d-flex justify-content-start align-items-center">';
                html += '<p class="content-title mb-0">' + value.name + '</p>';
                html += '<input type="hidden" value="' + value.display_id + '">';
                html += '<input type="hidden" value="' + value.schedule.length + '">';
                html += '</div>';
                if ( check_empty(value.updated_at) ) {
                    html += '<p class="content-date mb-0">' + value.updated_at + '</p>';
                } else {
                    html += '<p class="content-date mb-0">' + value.created_at + '</p>';
                }
                if ( check_empty(value.alert) ) {
                    html += '<div class="alert-area">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/warning.svg" class="ms-2 alert-image">';
                    html += '<label class="alert-text mb-0 p-1 ps-2 pe-2">' + value.alert.text + '</label>';
                    html += '</div>';
                }
                html += '</td>';
                html += '<td>';
                if ( value.schedule.length > 0 ) {
                    $.each( value.schedule, function( schedule_index, schedule_value ) {
                        if ( schedule_index == value.schedule.length - 1 ) {
                            if ( check_empty(schedule_value.date) && check_empty(schedule_value.time) ) {
                                if ( value.end_flg || schedule_value.join == 2 ) {
                                    html += '<input type="text" name="date_' + value.display_id +'_' + schedule_value.number + '" class="input-text readonly w-100 ps-1" value="' + schedule_value.date + ' ' + schedule_value.time + '" readonly>';
                                } else {
                                    html += '<input type="text" name="date_' + value.display_id +'_' + schedule_value.number + '" class="input-text input-schedule w-100 ps-1" value="' + schedule_value.date + ' ' + schedule_value.time + '" style="cursor: pointer;" readonly>';
                                }
                            } else {
                                if ( value.end_flg || schedule_value.join == 2 ) {
                                    html += '<input type="text" name="date_' + value.display_id +'_' + schedule_value.number + '" class="input-text readonly w-100 ps-1" value="-" readonly>';
                                } else {
                                    html += '<input type="text" name="date_' + value.display_id +'_' + schedule_value.number + '" class="input-text input-schedule readonly w-100 ps-1" value="" style="cursor: pointer;" readonly>';
                                }
                            }
                        }
                    });
                } else {
                    html += '<input type="text" name="date_' + value.display_id + '_1" class="input-text w-100 ps-1" value="-" readonly>';
                }
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#select_schedule_modal"></button>';
                html += '</td>';
                html += '<td>';
                if ( value.schedule.length > 0 ) {
                    $.each( value.schedule, function( schedule_index, schedule_value ) {
                        if ( schedule_index == value.schedule.length - 1 ) {
                            if ( check_empty(schedule_value.date) && check_empty(schedule_value.time) ) {
                                if ( value.end_flg || schedule_value.join == 2 ) {
                                    if ( check_empty(schedule_value.join) ) {
                                        if ( schedule_value.join == 0 ) {
                                            html += '<input type="text" class="input-text text-center readonly w-100" value="未定" readonly>';
                                        } else if ( schedule_value.join == 1 ) {
                                            html += '<input type="text" class="input-text text-center readonly w-100" value="参加" readonly>';
                                        } else if ( schedule_value.join == 2 ) {
                                            html += '<input type="text" class="input-text text-center readonly w-100" value="不参加" readonly>';
                                        }
                                        html += '<input type="hidden" value="' + schedule_value.join + '">';
                                    } else {
                                        html += '<input type="text" class="input-text text-center readonly w-100" value="-" readonly>';
                                        html += '<input type="hidden">';
                                    }
                                } else {
                                    html += '<div class="dropdown input-select-dropdown input-join-dropdown d-inline-block w-100 p-0">';
                                    if ( schedule_value.join == 0 ) {
                                        html += '<input type="text" name="join_' + value.display_id +'_' + schedule_value.number + '" value="未定" class="input-text input-select ps-2 pe-2" data-bs-toggle="dropdown" readonly>';
                                    } else if ( schedule_value.join == 1 ) {
                                        html += '<input type="text" name="join_' + value.display_id +'_' + schedule_value.number + '" value="参加" class="input-text input-select ps-2 pe-2" data-bs-toggle="dropdown" readonly>';
                                    } else if ( schedule_value.join == 2 ) {
                                        html += '<input type="text" name="join_' + value.display_id +'_' + schedule_value.number + '" value="不参加" class="input-text input-select ps-2 pe-2" data-bs-toggle="dropdown" readonly>';
                                    }
                                    html += '<input type="hidden" value="' + schedule_value.join + '">';
                                    html += '<div class="dropdown-menu" style="max-height: 75px;">';
                                    html += '<button type="button" value="1" class="btn dropdown-item fw-bold text-center">参加</button>';
                                    html += '<button type="button" value="2" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">不参加</button>';
                                    html += '</div>';
                                    html += '</div>';
                                }
                            } else {
                                html += '<input type="text" class="input-text text-center readonly w-100" value="-" readonly>';
                                html += '<input type="hidden">';
                            }
                        }
                    });
                } else {
                    html += '<input type="text" class="input-text text-center readonly w-100" value="-" readonly>';
                    html += '<input type="hidden">';
                }
                html += '</td>';
                html += '<td>';
                if ( value.schedule.length > 0 ) {
                    $.each( value.schedule, function( schedule_index, schedule_value ) {
                        if ( schedule_index == value.schedule.length - 1 ) {
                            if ( value.end_flg || schedule_value.join == 2 ) {
                                if ( check_empty(schedule_value.manager) ) {
                                    html += '<input type="text" name="manager_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.manager.profile.family_name + ' ' + schedule_value.manager.profile.first_name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.manager.display_id + '">';
                                } else {
                                    html += '<input type="text" name="manager_' + value.display_id + '_' + schedule_value.number + '" class="input-text text-center readonly w-100" value="-" readonly>';
                                    html += '<input type="hidden">';
                                }
                            } else {
                                html += '<div class="dropdown input-manager-select-dropdown d-inline-block w-100 p-0">';
                                if ( check_empty(schedule_value.manager) ) {
                                    html += '<input type="text" name="manager_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.manager.profile.family_name + ' ' + schedule_value.manager.profile.first_name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.manager.display_id + '">';
                                } else {
                                    html += '<input type="text" name="manager_' + value.display_id + '_' + schedule_value.number + '" class="input-text text-center readonly w-100" value="-" readonly>';
                                    html += '<input type="hidden">';
                                }
                                html += '</div>';
                            }
                        }
                    });
                } else {
                    html += '<input type="text" class="input-text text-center readonly w-100" value="-" readonly>';
                }
                html += '</td>';
                html += '<td>';
                if ( value.schedule.length > 0 ) {
                    $.each( value.schedule, function( schedule_index, schedule_value ) {
                        if ( schedule_index == value.schedule.length - 1 ) {
                            if ( value.end_flg || schedule_value.join == 2 ) {
                                if ( check_empty(schedule_value.online_facility) ) {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.online_facility.name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.online_facility.display_id + '">';
                                } else if ( check_empty(schedule_value.offline_facility) ) {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.offline_facility.name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.offline_facility.display_id + '">';
                                } else {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="-" class="input-text input-select w-100 readonly ps-2 pe-2"  readonly>';
                                    html += '<input type="hidden" value="">';
                                }
                            } else {
                                html += '<div class="dropdown input-select-dropdown d-inline-block w-100 p-0">';
                                if ( check_empty(schedule_value.online_facility) ) {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.online_facility.name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.online_facility.display_id + '">';
                                } else if ( check_empty(schedule_value.offline_facility) ) {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="' + schedule_value.offline_facility.name + '" class="input-text text-center readonly w-100" readonly>';
                                    html += '<input type="hidden" value="' + schedule_value.offline_facility.display_id + '">';
                                } else {
                                    html += '<input type="text" name="facility_' + value.display_id + '_' + schedule_value.number + '" value="-" class="input-text input-select w-100 readonly ps-2 pe-2"  readonly>';
                                    html += '<input type="hidden" value="">';
                                }
                                html += '</div>';
                            }
                        }
                    });
                } else {
                    html += '<input type="text" class="input-text text-center readonly w-100" value="-" readonly>';
                }
                html += '</td>';
                html += '</tr>';
                html += '<tr>';
                html += '<td class="pt-0" colspan="4">';
                if ( value.end_flg ) {
                    html += '<input type="text" name="memo_' + value.display_id + '" class="input-text text-center readonly w-100" value="-" readonly>';
                } else {
                    html += '<input type="text" name="memo_' + value.display_id + '" class="input-text w-100" value="">';
                }
                html += '</td>';
                html += '</tr>';
                $( '#save_step_form table tbody' ).append( html );
            });

            $( target ).next().trigger( 'click' );
        }).fail( function(){

        });
    });

    $( document ).on( 'click', '.new-area .check-button', function () {
        $( '#check_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '.line-area .check-button', function () {
        $( '#check_user_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#check_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#check_schedule_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#check_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#check_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    $( document ).on( 'click', '#check_user_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#check_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#check_user_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#check_user_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'check' );

    $( document ).on( 'click', '.table tbody .dropdown-preview-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#edit_user_modal .modal-body' ).find( 'input[type=hidden]' ).eq(1).val( response.display_id );

            if ( check_empty( response.profile ) && check_empty( response.profile.image ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
                $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
            } else {
                if ( check_empty( response.display_image ) ) {
                    $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', response.display_image );
                    $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', response.display_image );
                } else {
                    $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                    $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                }
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.title' ).text( response.profile.name );
                $( '#edit_user_modal .modal-header' ).find( '.title' ).text( response.profile.name );
            } else {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.title' ).text( response.display_name );
                $( '#edit_user_modal .modal-header' ).find( '.title' ).text( response.display_name );
            }

            if ( response.status == 2 ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( 'ブロック' );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( 'ブロック' );
            } else if ( check_empty( response.active_flow ) && check_empty( response.active_flow.tab ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( response.active_flow.tab.name );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( response.active_flow.tab.name );
            } else {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( '-' );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( '-' );
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                $( '#edit_user_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( response.profile.email );
            } else {
                $( '#edit_user_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( '' );
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.memo ) ) {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( 'textarea' ).val( response.profile.memo );
                $( '#edit_user_modal .modal-body' ).find( 'textarea' ).val( response.profile.memo );
            } else {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( 'textarea' ).val( '' );
                $( '#edit_user_modal .modal-body' ).find( 'textarea' ).val( '' );
            }

            $( '#user_profile_offcanvas .offcanvas-body' ).find( 'input' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).val( response.display_date );
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.atelle_id ) ) {
                        $( this ).val( '#' + response.profile.atelle_id );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 6 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 7 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 8 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                        $( this ).val( response.profile.email );
                    } else {
                        $( this ).val( '-' );
                    }
                }
            });

            $( '#edit_user_modal .modal-body' ).find( 'input[type=text]' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).val( response.display_date );
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.atelle_id ) ) {
                        $( this ).val( '#' + response.profile.atelle_id );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                        $( this ).next().val( response.profile.age );
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 6 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                            $( this ).next().val( response.profile.sex );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                            $( this ).next().val( response.profile.sex );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 7 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '' );
                    }
                }
            });

            $( '#user_profile_offcanvas .offcanvas-body' ).find( '.tag-area' ).empty();
            $( '#edit_user_modal .modal-body' ).find( '.tag-area .add-tag-area' ).empty();
            $.each( response.tag, function( index, value ) {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( '.tag-area' ).append( '<label class="tag-label text-center p-1 me-1 mb-0">' + value.tag.name + '</label>' );
                $( '#edit_user_modal .modal-body' ).find( '.tag-area .add-tag-area' ).append( '<div class="position-relative"><label class="tag-label text-center p-1 me-1">' + value.tag.name + '</label><input type="hidden" name="tag[]" value="' + value.tag.display_id + '"><button type="button" value="" class="btn delete-tag-button p-0"><img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg"></button></div>' );
            });

            $( target ).next().trigger( 'click' );
            down_modal();
        }).fail( function(){
            
        });
    });
    $( '#user_profile_offcanvas .offcanvas-header .edit-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });

    $( '#edit_user_modal .modal-body .add-tag-button-area .add-tag-button' ).on( 'click', function() {
        var target = $( this );
        var form_data = new FormData();
        $.ajax({
            'data': form_data,
            'url': $( '#get_tag_all_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#tag_modal .genre-table tbody' ).empty();
            if ( response.genre_list.length > 0 ) {
                $.each( response.genre_list, function( index, value ) {
                    $( '#tag_modal .genre-table tbody' ).append( append_genre_modal(index, value) );
                });
            }
            $( '#tag_modal .tag-table tbody' ).empty();
            if ( response.tag_list.length > 0 ) {
                $.each( response.tag_list, function( index, value ) {
                    $( '#tag_modal .tag-table tbody' ).append( append_tag_modal(index, value, $( '#edit_user_modal .modal-body .add-tag-area input' ) ) );
                });
            }
            $( target ).next().trigger( 'click' );
            up_modal();
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#edit_user_modal .modal-body .add-tag-area .delete-tag-button', function () {
        $( this ).parent().remove();
    });
    $( document ).on( 'click', '#tag_modal .table-area tbody button', function () {
        var html = '<div class="position-relative">';
        html += '<label class="tag-label text-center p-1 me-1">' + $( this ).next().val() + '</label>';
        html += '<input type="hidden" name="tag[]" value="' + $( this ).val() + '">';
        html += '<button type="button" value="" class="btn delete-tag-button p-0">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
        html += '</button>';
        html += '</div>';
        $( '#edit_user_modal #save_user_form .tag-area .add-tag-area' ).append( html );
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '.table tbody .dropdown-menu .member-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                $( '#member_user_check_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( response.profile.email );
            } else {
                $( '#member_user_check_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( '' );
            }
            $( '#member_user_check_modal .modal-body' ).find( 'input[type=text]' ).each( function( index, value ) {
                if ( index == 0 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                        $( this ).next().val( response.profile.age );
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                            $( this ).next().val( response.profile.sex );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                            $( this ).next().val( response.profile.sex );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '' );
                    }
                }
            });

            $( '#member_user_check_modal .yes-button' ).val( $( target ).val() );
            $( target ).next().trigger( 'click' );
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '#member_user_check_modal .yes-button', function () {
        $( '#member_user_check_modal .no-button' ).trigger( 'click' );
        $( '#member_user_message_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });

    $( document ).on( 'change', '#member_user_message_check_modal [name=type]', function () {
        if ( $( this ).val() == '0' ) {
            $( '#member_user_message_check_modal #member_user_message_area' ).addClass( 'd-none' );
            $( '#member_user_message_check_modal #member_user_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '1' ) {
            $( '#member_user_message_check_modal #member_user_message_area' ).removeClass( 'd-none' );
            $( '#member_user_message_check_modal #member_user_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '2' ) {
            $( '#member_user_message_check_modal #member_user_message_area' ).addClass( 'd-none' );
            $( '#member_user_message_check_modal #member_user_template_area' ).removeClass( 'd-none' );
        }
    });
    $( document ).on( 'click', '#member_user_message_check_modal #member_user_template_area .dropdown-menu button', function () {
        $( '#member_user_message_check_modal' ).removeClass( 'up-modal' );
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this).next(), null );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this).next(), null );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this).next(), null );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this).next(), null );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this).next(), null );
        }
        up_modal();
    });
    $( document ).on( 'click', '#template_text_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_text_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#member_user_message_check_modal [name=template]' ).val( response.name );
            $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        }).fail( function(){
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_text_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_video_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_video_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#member_user_message_check_modal [name=template]' ).val( response.name );
            $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        }).fail( function(){
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_video_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richmessage_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_richmessage_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#member_user_message_check_modal [name=template]' ).val( response.name );
            $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        }).fail( function(){
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_richmessage_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_richvideo_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_richvideo_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#member_user_message_check_modal [name=template]' ).val( response.name );
            $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        }).fail( function(){
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_richvideo_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });
    $( document ).on( 'click', '#template_cardtype_modal .table-area tbody button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).next().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_template_cardtype_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#member_user_message_check_modal [name=template]' ).val( response.name );
            $( '#member_user_message_check_modal [name=template]' ).next().val( $( target ).next().val() );
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        }).fail( function(){
            $( target ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
            $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
            up_modal();
        });
    });
    $( document ).on( 'click', '#template_cardtype_modal .btn-close', function () {
        $( '#member_user_message_check_modal' ).addClass( 'up-modal' );
        up_modal();
    });

    $( document ).on( 'click', '#member_user_message_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        form_data.append( 'name', $( '#member_user_check_modal [name=name]' ).val() );
        form_data.append( 'name_kana', $( '#member_user_check_modal [name=name_kana]' ).val() );
        form_data.append( 'birth', $( '#member_user_check_modal [name=birth]' ).val().replace( '年', '-' ).replace( '月', '-' ).replace( '日', '' ) );
        form_data.append( 'age', $( '#member_user_check_modal [name=age]' ).next().val() );
        form_data.append( 'sex', $( '#member_user_check_modal [name=sex]' ).next().val() );
        form_data.append( 'phone_number', $( '#member_user_check_modal [name=phone_number]' ).val() );
        form_data.append( 'email', $( '#member_user_check_modal [name=email]' ).val() );
        form_data.append( 'message_type', $( '#member_user_message_check_modal [name=type]:checked' ).val() );
        if ( $( '#member_user_message_check_modal [name=type]:checked' ).val() == '1' ) {
            form_data.append( 'message', $( '#member_user_message_check_modal [name=message]' ).val() );
        } else if ( $( '#member_user_message_check_modal [name=type]:checked' ).val() == '2' ) {
            form_data.append( 'message_template_type', $( '#member_user_message_check_modal [name=template_type]' ).next().val() );
            form_data.append( 'message_template', $( '#member_user_message_check_modal [name=template]' ).next().val() );
        }
        $.ajax({
            'data': form_data,
            'url': $( '#save_member_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#member_user_message_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#member_user_message_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'member_user' );

    $( document ).on( 'click', '#edit_step_modal .input-join-dropdown .dropdown-menu button', function () {
        $( '#save_step_form [name=edit_type]' ).val( $( this ).val() );
        $( '#edit_step_modal .input-join-dropdown input[type=text]' ).each( function( index, value ) {
            $( this ).addClass( 'readonly' );
            $( this ).prop( 'disabled', true  );
        });
        $( this ).parents( '.input-join-dropdown' ).find( 'input[type=text]' ).removeClass( 'readonly' );
        $( this ).parents( '.input-join-dropdown' ).find( 'input[type=text]' ).prop( 'disabled', false  );
    });

    $( document ).on( 'click', '#edit_step_modal .edit-button', function () {
        if ( $( '#save_step_form [name=edit_type]' ).val() == '1' ) {
            $( this ).next().trigger( 'click' );
        } else if ( $( '#save_step_form [name=edit_type]' ).val() == '2' ) {
            $( this ).next().next().next().trigger( 'click' );
        } else {
            $( this ).next().trigger( 'click' );
        }
        up_modal();
    });

    $( document ).on( 'change', '#edit_step_yes_message_modal [name=yes_type]', function () {
        if ( $( this ).val() == '0' ) {
            $( '#edit_step_yes_message_modal #step_yes_message_area' ).addClass( 'd-none' );
            $( '#edit_step_yes_message_modal #step_yes_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '1' ) {
            $( '#edit_step_yes_message_modal #step_yes_message_area' ).removeClass( 'd-none' );
            $( '#edit_step_yes_message_modal #step_yes_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '2' ) {
            $( '#edit_step_yes_message_modal #step_yes_message_area' ).addClass( 'd-none' );
            $( '#edit_step_yes_message_modal #step_yes_template_area' ).removeClass( 'd-none' );
        }
    });
    
    $( document ).on( 'change', '#edit_step_yes_message_modal .yes-button', function () {
        $( '#edit_step_yes_message_modal .no-button' ).trigger( 'click' );
        $( this ).next().trigger( 'click' );
        up_modal();
    });

    $( document ).on( 'change', '#edit_step_no_message_modal [name=no_type]', function () {
        if ( $( this ).val() == '0' ) {
            $( '#edit_step_no_message_modal #step_no_message_area' ).addClass( 'd-none' );
            $( '#edit_step_no_message_modal #step_no_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '1' ) {
            $( '#edit_step_no_message_modal #step_no_message_area' ).removeClass( 'd-none' );
            $( '#edit_step_no_message_modal #step_no_template_area' ).addClass( 'd-none' );
        } else if ( $( this ).val() == '2' ) {
            $( '#edit_step_no_message_modal #step_no_message_area' ).addClass( 'd-none' );
            $( '#edit_step_no_message_modal #step_no_template_area' ).removeClass( 'd-none' );
        }
    });
    
    $( document ).on( 'change', '#edit_step_no_message_modal .yes-button', function () {
        $( '#edit_step_no_message_modal .no-button' ).trigger( 'click' );
        $( this ).next().trigger( 'click' );
        up_modal();
    });

    $( document ).on( 'click', '#edit_step_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        
        var form_data = new FormData();
        form_data.append( 'user_id', $( '#save_step_form [name=user_id]' ).val() );
        $( '#save_step_form table tbody tr' ).each( function( index, value ) {
            if ( index % 2 == 0 ) {
                var id = $( this ).find( '.content-title' ).next().val();
                var count = $( this ).find( '.content-title' ).next().next().val();
                for ( var i = 1; i <= count; i++ ) {
                    if ( check_empty($( '#save_step_form [name=date_' + id + '_' + i + ']' ).val()) ) {
                        form_data.append( 'date_' + id + '_' + i, $( '#save_step_form [name=date_' + id + '_' + i + ']' ).val() );
                    }
                    if ( check_empty($( '#save_step_form [name=join_' + id + '_' + i + ']' ).next().val()) ) {
                        form_data.append( 'join_' + id + '_' + i, $( '#save_step_form [name=join_' + id + '_' + i + ']' ).next().val() );
                    }
                    if ( check_empty($( '#save_step_form [name=manager_' + id + '_' + i + ']' ).next().val()) ) {
                        form_data.append( 'manager_' + id + '_' + i, $( '#save_step_form [name=manager_' + id + '_' + i + ']' ).next().val() );
                    }
                    if ( check_empty($( '#save_step_form [name=facility_' + id + '_' + i + ']' ).next().val()) ) {
                        form_data.append( 'facility_' + id + '_' + i, $( '#save_step_form [name=facility_' + id + '_' + i + ']' ).next().val() );
                    }
                }
                form_data.append( 'memo_' + id, $( '#save_step_form [name=memo_' + id + ']' ).val() );
                if ( $( '#save_step_form [name=edit_type]' ).val() == '1' ) {
                    form_data.append( 'message_type', $( '#edit_step_yes_message_modal [name=yes_type]:checked' ).val() );
                    if ( $( '#edit_step_yes_message_modal [name=yes_type]:checked' ).val() == '1' ) {
                        form_data.append( 'message', $( '#edit_step_yes_message_modal [name=yes_message]' ).val() );
                    } else if ( $( '#edit_step_yes_message_modal [name=yes_type]:checked' ).val() == '2' ) {
                        form_data.append( 'message_template_type', $( '#edit_step_yes_message_modal [name=yes_template_type]' ).next().val() );
                        form_data.append( 'message_template', $( '#edit_step_yes_message_modal [name=yes_template]' ).next().val() );
                    }
                } else if ( $( '#save_step_form [name=edit_type]' ).val() == '2' ) {
                    form_data.append( 'message_type', $( '#edit_step_no_message_modal [name=no_type]:checked' ).val() );
                    if ( $( '#edit_step_no_message_modal [name=no_type]:checked' ).val() == '1' ) {
                        form_data.append( 'message', $( '#edit_step_no_message_modal [name=no_message]' ).val() );
                    } else if ( $( '#edit_step_no_message_modal [name=no_type]:checked' ).val() == '2' ) {
                        form_data.append( 'message_template_type', $( '#edit_step_no_message_modal [name=no_template_type]' ).next().val() );
                        form_data.append( 'message_template', $( '#edit_step_no_message_modal [name=no_template]' ).next().val() );
                    }
                }
            }
        });
        $.ajax({
            'data': form_data,
            'url': $( '#save_step_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#edit_step_check_modal .no-button' ).trigger( 'click' );
                $( '#edit_step_success_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#edit_step_check_modal .no-button' ).trigger( 'click' );
                $( '#edit_step_error_button' ).trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'edit_step' );
});