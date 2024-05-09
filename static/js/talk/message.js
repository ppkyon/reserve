$( function() {
    $( '.talk-slide' ).each( function( index, value ) {
        $( this ).slick({
            infinite: false,
            arrows: false,
            variableWidth: true,
        });
    });

    setInterval( function() {
        $.ajax({
            'url': $( '#update_talk_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( response.update ) {
                $( '.user-item-area' ).each( function( index, element ){
                    if ( $( this ).prev().val() == $( '#send_id' ).val() ) {
                        $( this ).trigger( 'click' );
                    }
                });
                $( '#user_search' ).trigger( 'keyup' );
            }
        }).fail( function(){
            
        });
    }, 5000 );
    scroll_message();
});

function create_message( response, value, last_date ) {
    var html = '';
    var date = new Date( value.send_date );
    var send_date = ( '00' + date.getHours() ).slice(-2) + ':' + ( '00' + date.getMinutes() ).slice(-2);
    if ( value.account_type == 0 ) {
        image = $( '#env_static_url' ).val() + 'img/user-none.png';
        if ( response.line_user.profile != null && response.line_user.profile.image != null && response.line_user.profile.image != '' ) {
            image = $( '#env_media_url' ).val() + response.line_user.profile.image;
        } else if ( response.line_user.display_image ) {
            image = response.line_user.display_image;
        }

        if ( last_date != date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2) ) {
            var display_date = value.display_date;
            if( display_date.indexOf( '年' ) !== -1 ) {
                var date = new Date( display_date.replace('年','/').replace('月','/').replace('日', '') );
                display_date = ( date.getMonth() + 1 ) + '月' + ( date.getDate() ) + '日(' + week[date.getDay()] + ')';
            }
            html += '<div class="date-area text-center"><label class="p-1 ps-3 pe-3 mt-2 mb-0"><span>' + display_date + '</span></label></div>';
        }

        if ( value.message_type == 0 || value.message_type == 3 || value.message_type == 4 ) {
            html += '<div class="content-item d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img id="line_message_user_image" src="' + image + '">';
            html += '<div class="text-area p-2 ms-5 position-relative">';
            html += '<p class="mb-0">' + value.text.replaceAll('\\n','\n').replaceAll('\\r','') + '</p>';
            html += '</div>';
            html += '<p class="ps-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        } else if ( value.message_type == 1 || value.message_type == 5 ) {
            html += '<div class="content-item d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img id="line_message_user_image" src="' + image + '">';
            if ( value.image_width >= value.image_height ) {
                html += '<div class="image-area ms-5 position-relative">';
            } else {
                html += '<div class="image-area half ms-5 position-relative">';
            }
            html += '<img src="' + $( '#env_media_url' ).val() + value.image + '">';
            html += '</div>';
            html += '<p class="ps-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        } else if ( value.message_type == 2 ) {
            html += '<div class="content-item d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img id="line_message_user_image" src="' + image + '">';
            if ( check_empty( value.video ) ) {
                if ( value.video_width >= value.video_height ) {
                    html += '<div class="video-area ms-5 position-relative">';
                } else {
                    html += '<div class="video-area half ms-5 position-relative">';
                }
            }
            html += '<video src="' + $( '#env_media_url' ).val() + value.video + '" controls></video>';
            html += '</div>';
            html += '<p class="ps-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        }
    } else if ( value.account_type == 1 ) {
        if ( value.author_profile && value.author_profile.image ) {
            image = $( '#env_media_url' ).val() + value.author_profile.image;
        } else {
            image = $( '#env_static_url' ).val() + 'img/manager-none.png';
        }
        
        if ( last_date != date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2) ) {
            var display_date = value.display_date;
            if( display_date.indexOf( '年' ) !== -1 ) {
                var date = new Date( display_date.replace('年','/').replace('月','/').replace('日', '') );
                display_date = ( date.getMonth() + 1 ) + '月' + ( date.getDate() ) + '日(' + week[date.getDay()] + ')';
            }
            html += '<div class="date-area text-center"><label class="p-1 ps-3 pe-3 mt-2 mb-0"><span>' + display_date + '</span></label></div>';
        }
        
        if ( value.message_type == 0 || value.message_type == 3 || value.message_type == 4 ) {
            html += '<div class="content-item manager d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img src="' + image + '">';
            html += '<div class="text-area p-2 me-5 position-relative">';
            html += '<p class="mb-0">' + value.text + '</p>';
            html += '</div>';
            html += '<p class="pe-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        } else if ( value.message_type == 1 || value.message_type == 5 ) {
            html += '<div class="content-item manager d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img src="' + image + '">';
            if ( value.image_width >= value.image_height ) {
                html += '<div class="image-area me-5 position-relative">';
            } else {
                html += '<div class="image-area half me-5 position-relative">';
            }
            html += '<img src="' + $( '#env_media_url' ).val() + value.image + '">';
            html += '</div>';
            html += '<p class="pe-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        } else if ( value.message_type == 2 ) {
            html += '<div class="content-item manager d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img src="' + image + '">';
            if ( check_empty( value.video ) ) {
                if ( value.video_width >= value.video_height ) {
                    html += '<div class="video-area me-5 position-relative">';
                } else {
                    html += '<div class="video-area half me-5 position-relative">';
                }
            }
            html += '<video src="' + $( '#env_media_url' ).val() + value.video + '" controls></video>';
            html += '</div>';
            html += '<p class="pe-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        } else if ( value.message_type == 7 ) {
            html += '<div class="content-item manager d-flex align-items-center position-relative mt-3 mb-3">';
            html += '<img id="line_message_user_image" src="' + image + '">';
            html += '<div class="position-relative overflow-hidden w-100 me-5">';
            html += '<ul class="talk-slide p-0">';
            $.each( value.template, function( template_index, template_value ) {
                if ( template_value.type == 1 ) {
                    html += '<li style="margin-right: 0.5rem;">';
                    html += '<div class="card-type-area"  style="width: 180px; height: auto; border: 1px solid rgba(0,0,0,0.1); border-radius: 0.8rem; overflow: hidden;">';
                    html += '<div class="card-type-header-area">';
                    html += '<div class="d-flex position-relative w-100">';
                    if ( template_value.announce.image_flg ) {
                        if ( template_value.announce.image_count == 1 ) {
                            html += '<div class="card-type-image-area d-flex flex-row position-relative w-100">';
                            html += '<div class="one card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_1 + '\' );"></span>';
                            html += '</div>';
                            html += '</div>';
                        } else if ( template_value.announce.image_count == 2 ) {
                            html += '<div class="card-type-image-area d-flex flex-row position-relative w-100">';
                            html += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_1 + '\' );"></span>';
                            html += '</div>';
                            html += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_2 + '\' );"></span>';
                            html += '</div>';
                            html += '</div>';
                        } else if ( template_value.announce.image_count == 3 ) {
                            html += '<div class="card-type-image-area d-flex flex-row position-relative w-100">';
                            html += '<div class="two card-type-image-item position-relative" style="padding-bottom: 7.5rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_1 + '\' );"></span>';
                            html += '</div>';
                            html += '<div class="two flex-column position-relative">';
                            html += '<div class="three card-type-image-item position-relative" style="padding-bottom: 3.75rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_2 + '\' );"></span>';
                            html += '</div>';
                            html += '<div class="three card-type-image-item position-relative" style="padding-bottom: 3.75rem;">';
                            html += '<span style="background-image: url( \'' + $( '#env_media_url' ).val() + template_value.announce.image_3 + '\' );"></span>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                        }
                    }
                    if ( template_value.announce.label_flg ) {
                        if ( template_value.announce.label_color == 0 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #fff; background-color: #666f86;">' + template_value.announce.label + '</label>';
                        } else if ( template_value.announce.label_color == 1 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #666f86; background-color: #fff; border: 1px solid #666f86;">' + template_value.announce.label + '</label>';
                        } else if ( template_value.announce.label_color == 2 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #fff; background-color: #eb4e3d;">' + template_value.announce.label + '</label>';
                        } else if ( template_value.announce.label_color == 3 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #fff; background-color: #ed8537;">' + template_value.announce.label + '</label>';
                        } else if ( template_value.announce.label_color == 4 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #fff; background-color: #00B900;">' + template_value.announce.label + '</label>';
                        } else if ( template_value.announce.label_color == 5 ) {
                            html += '<label class="label ps-1 pe-1" style="color: #fff; background-color: #5b82db;">' + template_value.announce.label + '</label>';
                        }
                    }
                    html += '</div>';
                    html += '</div>';
                    html += '<div class="card-type-body-area p-2">';
                    html += '<p class="title mb-1" style="font-size: 0.85rem;">' + template_value.announce.title + '</p>';
                    if ( template_value.announce.description_flg ) {
                        html += '<p class="description mb-1">' + template_value.announce.description + '</p>';
                    }
                    $.each( template_value.text, function( text_index, text_value ) {
                        if ( text_value.flg ) {
                            if ( text_index == 0 ) {
                                html += '<div class="mt-2 mb-2">';
                                html += '<p class="mb-0" style="font-size: 0.7rem; font-weight: bold;">' + text_value.title + '</p>';
                                html += '<p class="mb-0" style="font-size: 0.5rem;">' + text_value.text + '</p>';
                                html += '</div>';
                            } else {
                                html += '<div class="mt-1 mb-2">';
                                html += '<p class="mb-0" style="font-size: 0.7rem; font-weight: bold;">' + text_value.title + '</p>';
                                html += '<p class="mb-0" style="font-size: 0.5rem;">' + text_value.text + '</p>';
                                html += '</div>';
                            }
                        }
                    });
                    html += '</div>';
                    html += '<div class="card-type-footer-area text-center">';
                    $.each( template_value.action, function( action_index, action_value ) {
                        if ( action_value.flg ) {
                            if ( action_value.button_type == 0 ) {
                                if ( action_value.button_color == 0 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #666f86;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 1 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 2 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #eb4e3d;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 3 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #ed8537;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 4 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #00B900;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 5 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #5b82db;">' + action_value.label + '</button>';
                                }
                            } else if ( action_value.button_type == 1 ) {
                                if ( action_value.button_color == 0 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #666f86; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 1 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #fff; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 2 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #eb4e3d; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 3 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #ed8537; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 4 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #00B900; background-color: #fff;">' + action_value.label + '</button>';
                                } else if ( action_value.button_color == 5 ) {
                                    html += '<button type="button" class="btn p-0 mb-2" style="width: 90%; color: #5b82db; background-color: #fff;">' + action_value.label + '</button>';
                                }
                            }
                        }
                    });
                    html += '</div>';
                    html += '</div>';
                    html += '</li>';
                } else if ( template_value.type == 2 ) {
                    console.log(template_value);
                } else if ( template_value.type == 3 ) {
                    console.log(template_value);
                } else if ( template_value.type == 4 ) {
                    console.log(template_value);
                }
            });
            html += '</ul>';
            html += '</div>';
            html += '<p class="pe-1 mt-auto mb-2"> ' + send_date + '</p>';
            html += '</div>';
        }
    }
    return html;
}

function scroll_message() {
    setTimeout( function() {
        $( '.content-item' ).each( function( index, element ) {
            $( this ).get(0).scrollIntoView(false);
        });
    }, 250 );
}