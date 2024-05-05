$( function() {
    $( document ).on( 'click', '.table-area .setting-table > tbody > tr', function () {
        if ( $( this ).hasClass( 'active' ) ) {
            var change_flg = false;
            $( '.setting-table tr td' ).each( function( index, value ) {
                if ( $( this ).children( 'input[type=hidden]' ).val() == 'true' ) {
                    change_flg = true;
                }
            });
            if ( change_flg ) {
                $( '#setting_change_modal .yes-button' ).val( $( this ).find( '.title-id' ).val() );
                $( '#setting_change_button' ).trigger( 'click' );
            } else {
                $( this ).parent().find( 'tr' ).each( function( index, value ) {
                    $( this ).css( 'background-color', '#FFF' );
                    $( this ).removeClass( 'active' );
                });
                $( '.setting-list-area' ).each( function( index, value ) {
                    $( this ).addClass( 'd-none' );
                });
                $( this ).css( 'background-color', '' );
                $( this ).addClass( 'active' );
                $( '#' + $( this ).find( '.title-id' ).val() ).removeClass( 'd-none' );
                $( '.save-button' ).next().val( $( this ).find( '.title-id' ).val() );
            }
        }
    });
    $( document ).on( 'click', '#setting_change_modal .yes-button', function () {
        var target = $( this );
        $( '.setting-list-area' ).each( function( index, value ) {
            $( this ).addClass( 'd-none' );
        });
        $( '.setting-table tr' ).each( function( index, value ) {
            if ( $( target ).val() == $( this ).find( '.title-id' ).val() ) {
                $( this ).css( 'background-color', '' );
                $( this ).addClass( 'active' );
                $( '#' + $( target ).val() ).removeClass( 'd-none' );
                $( '.save-button' ).next().val( $( target ).val() );
            } else {
                $( this ).css( 'background-color', '#FFF' );
                $( this ).removeClass( 'active' );
            }
        });
        $( '#setting_change_modal .no-button' ).trigger( 'click' );
    });

    $( document ).on( 'change', '#save_setting_form input[type=text], #save_setting_form input[type=checkbox]', function () {
        $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
    });
    $( document ).on( 'click', '#save_setting_form .dropdown .dropdown-menu button', function () {
        $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
    });

    $( document ).on( 'change', '#save_setting_form .input-name', function () {
        var target = $( this );
        $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
            if ( !$( this ).hasClass( 'd-none' ) ) {
                var advance_list = [];
                $( this ).find( '.input-name' ).each( function( index, value ) {
                    advance_list.push({
                        'name': $( this ).val(),
                        'value': $( this ).attr( 'name').replace( 'name_', '' ),
                    });
                    if ( $( target ).attr( 'name' ).replace( 'name_', '' ) == $( this ).parents( '.setting-area' ).find( '.input-advance' ).next().val() ) {
                        $( this ).parents( '.setting-area' ).find( '.input-advance' ).val( $( target ).val() );
                    }
                });
                var target_area = $( this );
                $( this ).find( '.input-advance' ).next().next().empty();
                $.each( advance_list, function( index, value ) {
                    if ( index == 0 ) {
                        $( target_area ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold ps-2">' + value.name + '</button>' );
                    } else {
                        $( target_area ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold border-top p-1 ps-2 pt-2">' + value.name + '</button>' );
                    }
                });
            }
        });
    });

    var delete_item_area = '';
    $( document ).on( 'click', '.delete-item-button', function () {
        delete_item_area = $( this ).parents( 'tr' );
        $( '#delete_item_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_item_check_modal .yes-button' ).on( 'click', function() {
        var delete_value = $( delete_item_area ).find( '.count-text' ).next().val();
        $( delete_item_area ).remove();
        $( '#' + $( '.save-button' ).next().val() ).find( '.reserve-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
            $( this ).find( '.count-text' ).text( ( index + 1 ) + '.' );
        });
        $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
        $( '#delete_item_check_modal .no-button' ).trigger( 'click' );

        $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
            if ( !$( this ).hasClass( 'd-none' ) ) {
                var advance_list = [];
                $( this ).find( '.input-name' ).each( function( index, value ) {
                    advance_list.push({
                        'name': $( this ).val(),
                        'value': $( this ).attr( 'name').replace( 'name_', '' ),
                    });
                    if ( delete_value == $( this ).parents( '.setting-area' ).find( '.input-advance' ).next().val() ) {
                        $( this ).parents( '.setting-area' ).find( '.input-advance' ).val( '' );
                        $( this ).parents( '.setting-area' ).find( '.input-advance' ).next().val( '' );
                    }
                });
                var target_area = $( this );
                $( this ).find( '.input-advance' ).next().next().empty();
                $.each( advance_list, function( index, value ) {
                    if ( index == 0 ) {
                        $( target_area ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold ps-2">' + value.name + '</button>' );
                    } else {
                        $( target_area ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold border-top p-1 ps-2 pt-2">' + value.name + '</button>' );
                    }
                });
            }
        });
    });

    $( document ).on( 'click', '.input-question', function () {
        open_question_modal( $( this ), $( this ).attr( 'name' ).replace( 'question_', '' ) );
    });
    $( document ).on( 'click', '#question_modal .table-area tbody button', function () {
        $( '[name=question_' + $( this ).val() + ']' ).val( '【' + $( this ).next().next().val() + '】' );
        $( '[name=question_' + $( this ).val() + ']' ).next().val( $( this ).next().val() );
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '.add-meeting-modal-button', function () {
        $( '#save_meeting_modal .modal-title' ).text( 'ミーティングを追加' );

        $( '#save_meeting_form [name=name]' ).val( '' );
        $( '#save_meeting_form [name=url]' ).val( '' );
        $( '#save_meeting_form [name=platform_text]' ).val( '' );
        $( '#save_meeting_form [name=create_date]' ).val( '' );

        $( '#save_meeting_form [name=platform]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            }
        });
        $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', true );
        $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', false );
        $( '#save_meeting_modal .create-date-content' ).removeClass( 'd-none' );
        $( '#save_meeting_modal [name=create_date]' ).prop( 'required', true );

        $( '#save_meeting_modal .add-meeting-button' ).val( $( this ).val() );
        $( '#save_meeting_modal .add-meeting-button' ).removeClass( 'd-none' );
        $( '#save_meeting_modal .save-meeting-button' ).addClass( 'd-none' );
        $( this ).next().trigger( 'click' );
    });
    $( '#save_meeting_modal [name=platform]' ).on( 'change', function() {
        if ( $( this ).val() == '1' ) {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', true );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', false );
            $( '#save_meeting_modal .create-date-content' ).removeClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', true );
        } else if ( $( this ).val() == '9' ) {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', false );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', true );
            $( '#save_meeting_modal .create-date-content' ).addClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', false );
        } else {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', true );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', false );
            $( '#save_meeting_modal .create-date-content' ).addClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', false );
        }
    });
    $( document ).on( 'click', '.detail-meeting-button', function () {
        $( '#save_meeting_modal .modal-title' ).text( 'ミーティング詳細' );

        var table = $( this ).parents( 'tr.position-relative' );
        $( '#save_meeting_form [name=name]' ).val( $( table ).find( '.input-meeting-name' ).val() );
        $( '#save_meeting_form [name=url]' ).val( $( table ).find( '.input-meeting-url' ).val() );
        $( '#save_meeting_form [name=platform_text]' ).val( $( table ).find( '.input-meeting-platform-text' ).val() );
        $( '#save_meeting_form [name=create_date]' ).val( $( table ).find( '.input-meeting-start' ).val() );

        $( '#save_meeting_form [name=platform]' ).each( function( index, value ) {
            if ( $( this ).val() == $( table ).find( '.input-meeting-platform' ).val() ) {
                $( this ).prop( 'checked', true );
            }
        });
        if ( $( table ).find( '.input-meeting-platform' ).val() == '1' ) {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', true );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', false );
            $( '#save_meeting_modal .create-date-content' ).removeClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', true );
        } else if ( $( table ).find( '.input-meeting-platform' ).val() == '9' ) {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', false );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', true );
            $( '#save_meeting_modal .create-date-content' ).addClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', false );
        } else {
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'disabled', true );
            $( '#save_meeting_modal [name=platform_text]' ).prop( 'required', false );
            $( '#save_meeting_modal .create-date-content' ).addClass( 'd-none' );
            $( '#save_meeting_modal [name=create_date]' ).prop( 'required', false );
        }
        
        $( '#save_meeting_modal .save-meeting-button' ).val( $( this ).val() );
        $( '#save_meeting_modal .save-meeting-button' ).removeClass( 'd-none' );
        $( '#save_meeting_modal .add-meeting-button' ).addClass( 'd-none' );
        $( this ).next().trigger( 'click' );
    });
    $( '#save_meeting_modal .add-meeting-button' ).on( 'click', function() {
        if ( $( '#save_meeting_form' ).parsley().validate() ) {
            var target = $( this );
            $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
                if ( !$( this ).hasClass( 'd-none' ) ) {
                    $( this ).find( 'table tbody tr' ).each( function( index, value ) {
                        if ( $( target ).val() == $( this ).find( '.count-text' ).next().val() ) {
                            $( this ).find( '.meeting-table-area table tbody' ).append( append_meeting_area(this) );
                        }
                    });
                }
            });
            $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
            $( '#save_meeting_modal .btn-close' ).trigger( 'click' );
        }
    });
    $( '#save_meeting_modal .save-meeting-button' ).on( 'click', function() {
        if ( $( '#save_meeting_form' ).parsley().validate() ) {
            var id = $( this ).val();
            id = id.split('_');
            var number = id[1];
            id = id[0];

            $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
                if ( !$( this ).hasClass( 'd-none' ) ) {
                    $( this ).find( '.reserve-setting-table > tbody > tr' ).each( function( index, value ) {
                        if ( id == $( this ).find( '.count-text' ).next().val() ) {
                            $( this ).find( '.reserve-setting-meeting-table tbody tr' ).each( function( index, value ) {
                                if ( Number(number) == (index+1) ) {
                                    var now_date = new Date();
                                    var limit_date = new Date( $( '#save_meeting_form [name=create_date]' ).val() );
                                    limit_date.setDate( limit_date.getDate() + 90 );
        
                                    $( this ).find( '.input-meeting-name' ).val( $( '#save_meeting_form [name=name]' ).val() );
                                    $( this ).find( '.input-meeting-url' ).val( $( '#save_meeting_form [name=url]' ).val() );
                                    $( this ).find( '.input-meeting-platform-text' ).val( $( '#save_meeting_form [name=platform_text]' ).val() );
                                    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
                                        $( this ).find( '.input-meeting-start' ).val( $( '#save_meeting_form [name=create_date]' ).val() );
                                        $( this ).find( '.input-meeting-limit' ).val( limit_date.getFullYear() + '/' + ( limit_date.getMonth() + 1 ) + '/' + limit_date.getDate() );
                                    } else {
                                        $( this ).find( '.input-meeting-start' ).val( '' );
                                        $( this ).find( '.input-meeting-limit' ).val( '' );
                                    }
                                    
                                    $( this ).find( 'td' ).eq(3).empty();
                                    var html = '';
                                    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
                                        if ( now_date > limit_date ) {
                                            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/warning.svg" class="me-2 alert-image">';
                                            html += '<label class="alert-text mb-0 p-1 ps-2 pe-2" style="top: -40%; left: 43.3%; z-index: 1000;">期限切れです。ミーティングURLを<br>削除してください。</label>';
                                            html += '<span style="color: #FF0000;">期限切れ</span>';
                                            html += '<input type="hidden" value="1" class="input-meeting-status">';
                                        } else {
                                            html += '<span>使用可能</span>';
                                            html += '<input type="hidden" value="0" class="input-meeting-status">';
                                        }
                                    } else {
                                        html += '<span>使用可能</span>';
                                        html += '<input type="hidden" value="0" class="input-meeting-status">';
                                    }
                                    $( this ).find( 'td' ).eq(3).append( html );
                                    
                                    $( this ).find( 'td' ).eq(4).empty();
                                    html = '';
                                    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
                                        html += '<span>LINEミーティング</span>';
                                        html += '<input type="hidden" value="1" class="input-meeting-platform">';
                                        html += '<input type="hidden" value="" class="input-meeting-platform-text">';
                                    } else if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '2' ) {
                                        html += '<span>Zoom</span>';
                                        html += '<input type="hidden" value="2" class="input-meeting-platform">';
                                        html += '<input type="hidden" value="" class="input-meeting-platform-text">';
                                    } else if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '9' ) {
                                        html += '<span>' + $( '#save_meeting_form [name=platform_text]' ).val() + '</span>';
                                        html += '<input type="hidden" value="9" class="input-meeting-platform">';
                                        html += '<input type="hidden" value="' + $( '#save_meeting_form [name=platform_text]' ).val() + '" class="input-meeting-platform-text">';
                                    }
                                    $( this ).find( 'td' ).eq(4).append( html );
                                }
                            });
                        }
                    });
                }
            });
            $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
            $( '#save_meeting_modal .btn-close' ).trigger( 'click' );
        }
    });
    $( document ).on( 'click', '.delete-meeting-button', function () {
        $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
        $( this ).parents( 'tr' ).each( function() {
            $( this ).remove();
            return false;
        });
    });

    $( document ).on( 'click', '.add-setting-button', function () {
        $( '.setting-table tr.active td' ).children( 'input[type=hidden]' ).val( 'true' );
        $( '#' + $( '.save-button' ).next().val() ).find( '.reserve-setting-table' ).children( 'tbody' ).append( append_setting_area($( this ).val()) );
    });

    $( document ).on( 'click', '.save-setting-button', function () {
        $( '.setting-list-area' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'd-none' ) ) {
                $( this ).find( 'input' ).prop( 'required', false );
            } else {
                $( this ).find( '.input-title' ).prop( 'required', true );
                $( this ).find( '.input-name' ).prop( 'required', true );
                $( this ).find( '.input-time' ).prop( 'required', true );
                $( this ).find( '.input-people' ).prop( 'required', true );
                $( this ).find( '.input-facility' ).prop( 'required', true );
            }
        });
        $( this ).next().trigger( 'click' );
    });
});

function create_advance_area() {
    $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
        if ( !$( this ).hasClass( 'd-none' ) ) {
            var target = $( this );
            var advance_list = [];
            $( this ).find( '.input-name' ).each( function( index, value ) {
                advance_list.push({
                    'name': $( this ).val(),
                    'value': $( this ).attr( 'name').replace( 'name_', '' ),
                });
                if ( $( this ).attr( 'name' ).replace( 'name_', '' ) == $( target ).find( '.input-advance' ).eq(index).next().val() ) {
                    $( target ).find( '.input-advance' ).eq(index).val( $( this ).val() );
                }
            });
            $( this ).find( '.input-advance' ).next().next().empty();
            $.each( advance_list, function( index, value ) {
                if ( index == 0 ) {
                    $( target ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold ps-2">' + value.name + '</button>' );
                } else {
                    $( target ).find( '.input-advance' ).next().next().append( '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold border-top p-1 ps-2 pt-2">' + value.name + '</button>' );
                }
            });
        }
    });
}