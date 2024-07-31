$( function() {
    $( '#user_search' ).on( 'keyup', function () {
        var form_data = new FormData();
        form_data.append( 'text', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#user_search_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            create_user_list(response);
            setTimeout( function() {
                $( '.user-area .user-item-area' ).removeClass( 'd-none' );
                $( '.user-area .content-loader-area' ).addClass( 'd-none' );
            }, 750 );
        }).fail( function(){
                
        });
    });

    $( document ).on( 'click', '.user-item-area', function () {
        $( '.message-area .content-area' ).addClass( 'd-none' );
        $( '.message-area .content-loader-area' ).removeClass( 'd-none' );

        $( '.user-item-area' ).each( function( index, element ) {
            $( this ).removeClass( 'active' );
        });
        $( this ).addClass( 'active' );

        var form_data = new FormData();
        form_data.append( 'id', $( this ).prev().val() );
        $.ajax({
            'data': form_data,
            'url': $( '#change_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '.send-area' ).each( function( index, element ) {
                $( this ).addClass( 'd-none' );
            });
            $( '#send_' + response.line_user.display_id + '_area' ).removeClass( 'd-none' );
            $( '#send_id' ).val( response.line_user.display_id );

            $( '.user-area-id' ).each( function( index, element ){
                if ( $( this ).val() == response.line_user.display_id ) {
                    $( this ).next().find('.image-area .notice-area').remove();
                }
            });
            if ( response.talk_read.all_read_count >= 100 ) {
                $( '.side-area .menu-area .active .alert-badge' ).text( '+99' );
                $( '.side-area .menu-area .active .alert-badge' ).removeClass( 'd-none' );
            } else if ( response.talk_read.all_read_count > 0 ) {
                $( '.side-area .menu-area .active .alert-badge' ).text( response.talk_read.all_read_count );
                $( '.side-area .menu-area .active .alert-badge' ).removeClass( 'd-none' );
            } else {
                $( '.side-area .menu-area .active .alert-badge' ).text( response.talk_read.all_read_count );
                $( '.side-area .menu-area .active .alert-badge' ).addClass( 'd-none' );
            }

            if ( response.line_user.profile == null || response.line_user.profile.name == null ) {
                $( '#line_message_user_name' ).text( response.line_user.display_name );
            } else {
                $( '#line_message_user_name' ).text( response.line_user.profile.name );
            }
            $( '#line_message_user_name' ).attr( 'href', '/user/detail/?id=' + response.line_user.display_id );
            
            if ( response.line_user.profile != null && response.line_user.profile.image != null && response.line_user.profile.image != '' ) {
                $( '#line_message_user_image' ).attr( 'src', $( '#env_media_url' ).val() + response.line_user.profile.image );
            } else if ( response.line_user.display_image ) {
                $( '#line_message_user_image' ).attr( 'src', response.line_user.display_image );
            } else {
                $( '#line_message_user_image' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
            }
            if ( response.line_user.talk_manager ) {
                $( '#select_manager' ).val( response.line_user.talk_manager.family_name + ' ' + response.line_user.talk_manager.first_name );
                $( '#select_manager' ).removeClass( 'readonly' );
            } else {
                $( '#select_manager' ).val( '担当者なし' );
                $( '#select_manager' ).addClass( 'readonly' );
            }
            if ( response.line_user.talk_status ) {
                $( '#select_status' ).val( response.line_user.talk_status );
                if ( response.line_user.talk_status == '対応なし' ) {
                    $( '#select_status' ).addClass( 'readonly' );
                } else {
                    $( '#select_status' ).removeClass( 'readonly' );
                }
            } else {
                $( '#select_status' ).val( '対応なし' );
                $( '#select_status' ).addClass( 'readonly' );
            }
            if ( response.line_user.talk_pin ) {
                if ( response.line_user.talk_pin.pin_flg ) {
                    $( '#check_pin' ).prop( 'checked', true );
                } else {
                    $( '#check_pin' ).prop( 'checked', false );
                }
            } else {
                $( '#check_pin' ).prop( 'checked', false );
            }

            $( '.message-area .content-area').empty();
            var last_date = '';
            $.each( response.line_user.message, function( index, value ) {
                $( '.message-area .content-area').append( create_message( response, value, last_date ).replace(/\n/g, '<br>') );
                var send_date = new Date( value.send_date );
                last_date = send_date.getFullYear() + '/' + ( '00' + ( send_date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + send_date.getDate() ).slice(-2);
            });
            $( '.talk-slide' ).each( function( index, value ) {
                $( this ).slick({
                    infinite: false,
                    arrows: false,
                    variableWidth: true,
                });
            });
            
            setTimeout( function() {
                $( '.message-area .content-area' ).removeClass( 'd-none' );
                $( '.message-area .content-loader-area' ).addClass( 'd-none' );
                scroll_message();
            }, 750 );
        }).fail( function(){
            
        });
    });
});

function create_user_list(response) {
    $( '.list-area .user-area').empty();
    var html = '<div class="content-loader-area">';
    html += '<div class="loader-area d-flex align-items-center position-absolute text-center">';
    html += '<div class="table-loader spinner-border">';
    html += '<span class="visually-hidden">Loading...</span>';
    html += '</div>';
    html += '<p class="h5 fw-bold ms-3 mb-0">Loading...</p>';
    html += '</div>';
    html += '</div>';
    $( '.list-area .user-area').append(html);

    console.log(response.user_list);
    $.each( response.user_list, function( index, value ){
        user_image = $( '#env_static_url' ).val() + 'img/user-none.png';
        if ( value.line_user_profile != null && value.line_user_profile.image != null && value.line_user_profile.image != '' ) {
            user_image = $( '#env_media_url' ).val() + value.line_user_profile.image;
        } else if ( value.line_user.display_image ) {
            user_image = value.line_user.display_image;
        }
        user_name = value.line_user.display_name;
        if ( value.line_user_profile != null && value.line_user_profile.name != null ) {
            user_name = value.line_user_profile.name;
        }
        message = '';
        if ( value.line_message.message_type == 0 ) {
            console.log(value.line_message.text);
            message = convert_unicode(value.line_message.text).replace('\\n',' ').replace('\\r','');
        } else if ( value.line_message.message_type == 1 ) {
            if ( value.line_message.account_type == 0 ) {
                message = user_name + 'が写真を送信しました';
            } else if ( value.line_message.account_type == 1 ) {
                message = '写真を送信しました';
            }
        } else if ( value.line_message.message_type == 2 ) {
            if ( value.line_message.account_type == 0 ) {
                message = user_name + 'が動画を送信しました';
            } else if ( value.line_message.account_type == 1 ) {
                message = '動画を送信しました';
            }
        } else if ( value.line_message.message_type == 3 || value.line_message.message_type == 4 ) {
            console.log(value.line_message.text);
            if ( value.line_message.account_type == 0 ) {
                message = user_name + 'が' + value.line_message.text;
            } else if ( value.line_message.account_type == 1 ) {
                message = value.line_message.text;
            }
        } else if ( value.line_message.message_type == 5 ) {
            if ( value.line_message.account_type == 0 ) {
                message = user_name + 'が' + value.line_message.text;
            } else if ( value.line_message.account_type == 1 ) {
                message = value.line_message.text;
            }
        } else if ( value.line_message.message_type == 9 ) {
            if ( value.line_message.account_type == 0 ) {
                message = user_name + 'がスタンプを送信しました';
            } else if ( value.line_message.account_type == 1 ) {
                message = 'スタンプを送信しました';
            }
        }
        
        var html = '<input type="hidden" class="user-area-id" value="' + value.line_user.display_id + '">';
        if ( value.line_user.display_id == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
            html += '<div class="user-item-area active d-flex d-none align-items-center justify-content-between position-relative p-2">';
        } else {
            html += '<div class="user-item-area d-flex d-none align-items-center justify-content-between position-relative p-2">';
        }
        html += '<div class="image-area position-relative">';
        html += '<img src="' + user_image + '">';
        html += '</div>';
        html += '<div class="info-area p-1">';
        html += '<div class="name-area d-flex align-items-center">';
        html += '<p class="name mb-0">' + user_name +'</p>';
        html += '<p class="time ms-auto mb-0">' + value.line_message.display_date + '</p>';
        html += '</div>';
        html += '<div class="message-area mb-1">';
        html += '<p class="message mb-0">' + message + '</p>';
        html += '</div>';
        html += '<div class="status-area d-flex align-items-center justify-content-end mt-1"></div>';
        html += '</div>';
        html += '</div>';
        $( '.list-area .user-area').append( html );

        $( '.user-area-id' ).each( function( index, element ){
            if ( $( this ).val() == value.line_user.display_id ) {
                if ( value.talk_pin ) {
                    if ( value.talk_pin.pin_flg ) {
                        $( this ).next().find( '.image-area').append('<div class="pin-area"><img src="' + $( '#env_static_url' ).val() + 'img/icon/pin.svg"></div>');
                    } else {
                        $( this ).next().find( '.image-area').append('<div class="pin-area d-none"><img src="' + $( '#env_static_url' ).val() + 'img/icon/pin.svg"></div>');
                    }
                } else {
                    $( this ).next().find( '.image-area').append('<div class="pin-area d-none"><img src="' + $( '#env_static_url' ).val() + 'img/icon/pin.svg"></div>');
                }
                if ( value.talk_read && value.talk_read.read_count != 0 ) {
                    if ( value.talk_read.read_count >= 100 ) {
                        $( this ).next().find( '.image-area').append('<label class="notice-area">+99</label>');
                    } else {
                        $( this ).next().find( '.image-area').append('<label class="notice-area">' + value.talk_read.read_count + '</label>');
                    }
                }
                if ( value.talk_status ) {
                    if ( value.talk_status.status == 1 ) {
                        $( this ).next().find( '.status-area').append('<span class="danger">要対応</span>');
                    } else if ( value.talk_status.status == 2 ) {
                        $( this ).next().find( '.status-area').append('<span class="complete">対応済み</span>');
                    } else {
                        $( this ).next().find( '.status-area').append('<span class="d-none"></span>');
                    }
                } else {
                    $( this ).next().find( '.status-area').append('<span class="d-none"></span>');
                }
                if ( value.talk_manager ) {
                    $( this ).next().find( '.status-area').append('<span class="manager ms-1">' + value.talk_manager.family_name + ' ' + value.talk_manager.first_name + '</span>');
                } else {
                    $( this ).next().find( '.status-area').append('<span class="d-none"></span>');
                }
            }
        });
    });
    
    if ( response.all_read_count.all_read_count > 0 ) {
        if ( $( '.side-area .menu-area .active .alert-badge' ).length ) {
            $( '.side-area .menu-area .active .alert-badge' ).addClass( 'd-flex' );
            $( '.side-area .menu-area .active .alert-badge' ).removeClass( 'd-none' );
            $( '.side-area .menu-area .active .alert-badge' ).text( response.all_read_count.all_read_count );
        } else {
            $( '.side-area .menu-area li a' ).each( function( index, value ) {
                if ( $( this ).attr( 'href' ) == '/talk/' ) {
                    $( this ).append( '<span class="alert-badge d-flex align-items-center justify-content-center ms-auto">1</span>' );
                }
            });
        }
    } else {
        $( '.side-area .menu-area .active .alert-badge' ).addClass( 'd-none' );
        $( '.side-area .menu-area .active .alert-badge' ).removeClass( 'd-flex' );
        $( '.side-area .menu-area .active .alert-badge' ).text( '' );
    }
}