function action_preview() {
    create_preview();
    slide_preview();
    $( document ).on( 'change', '#save_cardtype_form .display-area input[type=checkbox]', function () {
        create_preview();
        slide_preview();
    });
    $( document ).on( 'mouseup keyup', '#save_cardtype_form .display-area input[type=text]', function () {
        create_preview();
        slide_preview();
    });
    $( document ).on( 'mouseup keyup', '#save_cardtype_form .display-area input[type=number]', function () {
        create_preview();
        slide_preview();
    });
    $( document ).on( 'mouseup keyup', '#save_cardtype_form .display-area textarea', function () {
        create_preview();
        slide_preview();
    });
    $( document ).on( 'click', '#save_cardtype_form .display-area .color-area button', function () {
        create_preview();
        slide_preview();
    });
    $( document ).on( 'click', '#save_cardtype_form .display-area .dropdown .dropdown-menu button', function () {
        create_preview();
        slide_preview();
    });
}

function create_preview() {
    if ( $( '#save_cardtype_form [name=type]' ).val() != null
        && $( '#save_cardtype_form [name=type]' ).val() != undefined
        && $( '#save_cardtype_form [name=type]' ).val() != '' ) {
        
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();

        var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
        html += '<div class="position-relative overflow-hidden w-100">';
        html += '<ul class="preview-slide p-0">';
        $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
            var number = $( this ).find( 'a' ).attr( 'href' ).replace( '#tab', '' );
            if ( number != '10' ) {
                if ( $( '#save_cardtype_form [name=type]' ).val() == '1' ) {
                    html += append_announce_preview(number);
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '2' ) {
                    html += append_location_preview(number);
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '3' ) {
                    html += append_person_preview(number);
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '4' ) {
                    html += append_image_preview(number);
                }
            }
        });
        html += '</ul>';
        html += '</div>';
        html += '</div>';
        $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
    
        append_more_preview('10');
    }
}

function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_cardtype_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( check_empty(response) ) {
            var html = '<div class="line-preview-chat d-flex justify-content-start align-items-start p-2">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/manager-none.png" class="manager-image me-1">';
            html += '<div class="position-relative overflow-hidden w-100">';
            html += '<ul class="preview-slide p-0">';
            $.each( response.item, function( index, value ) {
                if ( value.number != 10 ) {
                    if ( response.type == 1 ) {
                        html += append_list_announce_preview(value);
                    } else if ( response.type == 2 ) {
                        html += append_list_location_preview(value);
                    } else if ( response.type == 3 ) {
                        html += append_list_person_preview(value);
                    } else if ( response.type == 4 ) {
                        html += append_list_image_preview(value);
                    }
                } else {
                    
                }
            });
            html += '</ul>';
            html += '</div>';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append( html );
            append_list_more_preview(response.more);
            slide_preview();
        }
    }).fail( function(){

    });
}

function append_announce_preview(number) {
    var image = '';
    if ( $( '#save_cardtype_form [name=image_check_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '1' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png';
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                } else {
                    image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '</div>'
        } else if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '2' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                } else {
                    image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png';
            if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
                } else {
                    image_b = $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
                }
            }
            image += '<div id="display_image_area_2" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>'
            image += '</div>'
        } else if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '3' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                } else {
                    image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png';
            if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
                } else {
                    image_b = $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
                }
            }
            var image_c = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png';
            if ( $( '#save_cardtype_form [name=image_c_' + number + ']' ).val() != '' ) {
                if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                    image_c = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_c_' + number + ']' ).val();
                } else {
                    image_c = $( '#save_cardtype_form [name=image_c_' + number + ']' ).val();
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two flex-column position-relative">';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="c">';
            image += '<span style="background-image: url( ' + image_c + ' );"></span>';
            image += '</div>';
            image += '</div>';
            image += '</div>'
        }
    } else {
        if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 2.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span></span>';
            image += '</div>';
            image += '</div>'
        } else {
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 0;">';
            image += '<input type="hidden" value="a">';
            image += '<span></span>';
            image += '</div>';
            image += '</div>'
        }
    }
    var title = '';
    if ( $( '#save_cardtype_form [name=title_' + number + ']' ).val() == '' ) {
        title = '<p id="display_title_' + number + '" class="title mb-1" style="font-size: 0.85rem;">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + number + '" class="title mb-1" style="font-size: 0.85rem;">' + $( '#save_cardtype_form [name=title_' + number + ']' ).val() + '</p>';
    }
    var label = '';
    if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() == '' ) {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>' + $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() + '</label>';
        }
    }
    var description = '';
    if ( $( '#save_cardtype_form [name=description_check_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=description_' + number + ']' ).val() == '' ) {
            description = '<p id="display_description_' + number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + number + '" class="description mb-1">' + $( '#save_cardtype_form [name=description_' + number + ']' ).val().replace(/\r?\n/g, '<br>') + '</p>';
        }
    }
    var text = '';
    $( '#save_cardtype_form .message-area .tab-pane' ).eq(Number(number)-1).find( '.content-text-area' ).each( function( index, value ) {
        if ( $( '#save_cardtype_form [name=text_check_' + ( index + 1 ) + '_' + number + ']' ).prop( 'checked' ) ) {
            if ( index == 0 ) {
                text += '<div class="d-flex align-items-center mt-2 mb-2">';
            } else {
                text += '<div class="d-flex align-items-center mt-1 mb-2">';
            }
            if ( $( '#save_cardtype_form [name=text_title_' + ( index + 1 ) + '_' + number + ']' ).val() == '' ) {
                text += '<p id="display_text_title_' + ( index + 1 ) + '_' + number + '" class="mb-0" style="font-size: 0.7rem; font-weight: bold;">タイトル</p>';
            } else {
                text += '<p id="display_text_title_' + ( index + 1 ) + '_' + number + '" class="mb-0" style="font-size: 0.7rem; font-weight: bold;">' + $( '#save_cardtype_form [name=text_title_' + ( index + 1 ) + '_' + number + ']' ).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') + '</p>';
            }
            if ( $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).val() == '' ) {
                text += '<p id="display_text_text_' + ( index + 1 ) + '_' + number + '" class="ms-auto mb-0" style="font-size: 0.5rem;">テキスト</p>';
            } else {
                if ( $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).prop( 'readonly' ) ) {
                    text += '<p id="display_text_text_' + ( index + 1 ) + '_' + number + '" class="ms-auto mb-0" style="font-size: 0.5rem;">【' + $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).val().substring( 1, $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).val().indexOf( 'が' ) ) + '】</p>';
                } else {
                    text += '<p id="display_text_text_' + ( index + 1 ) + '_' + number + '" class="ms-auto mb-0" style="font-size: 0.5rem;">' + $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') + '</p>';
                }
            }
            text += '</div>';
        }
    });
    var action = '';
    $( '#save_cardtype_form .message-area .tab-pane' ).eq(Number(number)-1).find( '.content-action-area' ).each( function( index, value ) {
        if ( $( '#save_cardtype_form [name=action_check_' + ( index + 1 ) + '_' + number + ']' ).prop( 'checked' ) ) {
            if ( $( '#save_cardtype_form [name=action_button_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 'action' ) {
                var color = 'color: #fff;';
                var background_color = 'background-color: #fff;';
                if ( check_empty( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                    if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 0 ) {
                        background_color = 'background-color: #666f86;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 1 ) {
                        background_color = 'background-color: #fff;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 2 ) {
                        background_color = 'background-color: #eb4e3d;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 3 ) {
                        background_color = 'background-color: #ed8537;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 4 ) {
                        background_color = 'background-color: #00B900;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 5 ) {
                        background_color = 'background-color: #5b82db;';
                    }
                }
                if ( $( '#save_cardtype_form [name=action_label_' + ( index + 1 ) + '_' + number + ']' ).val() == '' ) {
                    action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + number + '" class="btn p-0 mb-2" style="width: 90%;' + color + background_color + '">アクションラベルを入力</button>';
                } else {
                    action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + number + '" class="btn p-0 mb-2" style="width: 90%;' + color + background_color + '">' + $( '#save_cardtype_form [name=action_label_' + ( index + 1 ) + '_' + number + ']' ).val() + '</button>';
                }
            } else if ( $( '#save_cardtype_form [name=action_button_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 'text' ) {
                var color = 'color: #5b82db;';
                var background_color = 'background-color: #fff;';
                if ( check_empty( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                    if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 0 ) {
                        color = 'color: #666f86;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 1 ) {
                        color = 'color: #fff;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 2 ) {
                        color = 'color: #eb4e3d;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 3 ) {
                        color = 'color: #ed8537;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 4 ) {
                        color = 'color: #00B900;';
                    } else if ( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() == 5 ) {
                        color = 'color: #5b82db;';
                    }
                }
                if ( $( '#save_cardtype_form [name=action_label_' + ( index + 1 ) + '_' + number + ']' ).val() == '' ) {
                    action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + number + '" class="btn p-0 mb-2" style="width: 90%;' + color + background_color + '">アクションラベルを入力</button>';
                } else {
                    action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + number + '" class="btn p-0 mb-2" style="width: 90%;' + color + background_color + '">' + $( '#save_cardtype_form [name=action_label_' + ( index + 1 ) + '_' + number + ']' ).val() + '</button>';
                }
            }
        }
    });

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">' + title + description + text + '</div>';
    html += '<div class="cardtype-footer-area text-center">' + action + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_location_preview(number) {
    var image = '';
    if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '1' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png';
        if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            } else {
                image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            }
        }
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '</div>';
    } else if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '2' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
        if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            } else {
                image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png';
        if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
            } else {
                image_b = $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
            }
        }
        image += '<div id="display_image_area_2" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '</div>';
    } else if ( $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() == '3' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
        if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_a_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            } else {
                image_a = $( '#save_cardtype_form [name=image_a_' + number + ']' ).val();
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png';
        if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_b_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
            } else {
                image_b = $( '#save_cardtype_form [name=image_b_' + number + ']' ).val();
            }
        }
        var image_c = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png';
        if ( $( '#save_cardtype_form [name=image_c_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_c_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image_c = $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_c_' + number + ']' ).val();
            } else {
                image_c = $( '#save_cardtype_form [name=image_c_' + number + ']' ).val();
            }
        }
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two flex-column position-relative">';
        image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="c">';
        image += '<span style="background-image: url( ' + image_c + ' );"></span>';
        image += '</div>';
        image += '</div>';
        image += '</div>';
    }
    var title = '';
    if ( $( '#save_cardtype_form [name=title_' + number + ']' ).val() == '' ) {
        title = '<p id="display_title_' + number + '" class="title mb-1">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + number + '" class="title mb-1">' + $( '#save_cardtype_form [name=title_' + number + ']' ).val() + '</p>';
    }
    var label = '';
    if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() == '' ) {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>' + $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() + '</label>';
        }
    }
    var place = '';
    if ( $( '#save_cardtype_form [name=place_check_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=place_' + number + ']' ).val() == '' ) {
            place += '<p id="display_place_' + number + '" class="place d-flex align-items-center mb-1">';
            place += '<img src="/static/img/icon/map.png" class="me-1">';
            place += '<span>住所を入力</span>';
            place += '</p>';
        } else {
            place += '<p id="display_place_' + number + '" class="place d-flex align-items-center mb-1">';
            place += '<img src="/static/img/icon/map.png" class="me-1">';
            place += '<span>' + $( '#save_cardtype_form [name=place_' + number + ']' ).val() + '</span>';
            place += '</p>';
        }
    }
    var plus = '';
    if ( $( '#save_cardtype_form [name=plus_check_' + number + ']' ).prop( 'checked' ) ) {
        var icon = '';
        if ( $( '#save_cardtype_form [name=select_plus_' + number + ']' ).val() == '時間' ) {
            icon = '<img src="/static/img/icon/time.png" class="me-1">';
        } else if ( $( '#save_cardtype_form [name=select_plus_' + number + ']' ).val() == '価格' ) {
            icon = '<img src="/static/img/icon/coin.png" class="me-1">';
        }
        if ( $( '#save_cardtype_form [name=plus_' + number + ']' ).val() == '' ) {
            plus += '<p id="display_plus_' + number + '" class="plus d-flex align-items-center mb-0">';
            plus += icon;
            plus += '<span>追加情報を入力</span>';
            plus += '</p>';
        } else {
            plus += '<p id="display_plus_' + number + '" class="plus d-flex align-items-center mb-0">';
            plus += icon;
            plus += '<span>' + $( '#save_cardtype_form [name=plus_' + number + ']' ).val() + '</span>';
            plus += '</p>';
        }
    }
    var action1 = '';
    if ( $( '#save_cardtype_form [name=action_check_1_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() == '' ) {
            action1 = '<button type="button" id="display_action_1_' + number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + number + '" class="btn p-0 mb-2">' + $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() + '</button>';
        }
    }
    var action2 = '';
    if ( $( '#save_cardtype_form [name=action_check_2_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=action_2_' + number + ']' ).val() == '' ) {
            action2 = '<button type="button" id="display_action_2_' + number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + number + '" class="btn p-0 mb-2">' + $( '#save_cardtype_form [name=action_2_' + number + ']' ).val() + '</button>';
        }
    }

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">' + title + place + plus + '</div>';
    html += '<div class="cardtype-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_person_preview(number) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/person-default.png );"></span>';
    if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val() != '' ) {
        if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
        }
    }
    var image_area = '<div id="display_image_area_' + number + '" class="cardtype-image-area d-flex flex-row position-relative w-100 pt-3 ps-4 pe-4">';
    image_area += '<div class="person cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
    image_area += '<input type="hidden" value="account">';
    image_area += image;
    image_area += '</div>';
    image_area += '</div>';
    var name = '';
    if ( $( '#save_cardtype_form [name=name_' + number + ']' ).val() == '' ) {
        name = '<p id="display_name_' + number + '" class="name mb-1">名前を入力</p>';
    } else {
        name = '<p id="display_name_' + number + '" class="name mb-1">' + $( '#save_cardtype_form [name=name_' + number + ']' ).val() + '</p>';
    }
    var tag1 = '';
    if ( $( '#save_cardtype_form [name=tag_check_1_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=tag_check_1_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=tag_check_1_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=tag_check_1_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=tag_input_1_' + number + ']' ).val() == '' ) {
            tag1 = '<label id="display_tag_1_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag1 = '<label id="display_tag_1_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + $( '#save_cardtype_form [name=tag_input_1_' + number + ']' ).val() + '</label>';
        }
    }
    var tag2 = '';
    if ( $( '#save_cardtype_form [name=tag_check_2_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=tag_check_2_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=tag_check_2_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=tag_check_2_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=tag_input_2_' + number + ']' ).val() == '' ) {
            tag2 = '<label id="display_tag_2_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag2 = '<label id="display_tag_2_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + $( '#save_cardtype_form [name=tag_input_2_' + number + ']' ).val() + '</label>';
        }
    }
    var tag3 = '';
    if ( $( '#save_cardtype_form [name=tag_check_3_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=tag_check_3_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=tag_check_3_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=tag_check_3_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=tag_input_3_' + number + ']' ).val() == '' ) {
            tag3 = '<label id="display_tag_3_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag3 = '<label id="display_tag_3_' + number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + $( '#save_cardtype_form [name=tag_input_3_' + number + ']' ).val() + '</label>';
        }
    }
    var description = '';
    if ( $( '#save_cardtype_form [name=description_check_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=description_' + number + ']' ).val() == '' ) {
            description = '<p id="display_description_' + number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + number + '" class="description mb-1">' + $( '#save_cardtype_form [name=description_' + number + ']' ).val() + '</p>';
        }
    }
    var action1 = '';
    if ( $( '#save_cardtype_form [name=action_check_1_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() == '' ) {
            action1 = '<button type="button" id="display_action_1_' + number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + number + '" class="btn p-0 mb-2">' + $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() + '</button>';
        }
    }
    var action2 = '';
    if ( $( '#save_cardtype_form [name=action_check_2_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=action_2_' + number + ']' ).val() == '' ) {
            action2 = '<button type="button" id="display_action_2_' + number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + number + '" class="btn p-0 mb-2">' + $( '#save_cardtype_form [name=action_2_' + number + ']' ).val() + '</button>';
        }
    }
    
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">';
    html += name;
    html += '<p class="text-center mb-0">' + tag1 + tag2 + tag3 + '</p>';
    html += description;
    html += '</div>';
    html += '<div class="cardtype-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_image_preview(number) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png );"></span>';
    if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val() != '' ) {
        if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
        }
    }

    var image_area = '<div id="display_image_area_' + number + '" class="cardtype-image-area d-flex flex-row position-relative w-100">';
    image_area += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 10rem;">';
    image_area += '<input type="hidden" value="image">';
    image_area += image;
    image_area += '</div>';
    image_area += '</div>';
    var label = '';
    if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
        var color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'color' );
        var background_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'background-color' );
        var boder_color = $( '#save_cardtype_form [name=label_check_' + number + ']' ).parent().next().find( '.color-area button i' ).parent().css( 'border' );

        if ( background_color === 'rgb(255, 255, 255)' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() == '' ) {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + number + '" class="label ps-1 pe-1" ' + style + '>' + $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() + '</label>';
        }
    }
    var action1 = '';
    if ( $( '#save_cardtype_form [name=action_check_1_' + number + ']' ).prop( 'checked' ) ) {
        if ( $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() == '' ) {
            action1 = '<label id="display_action_1_' + number + '" class="action-label ps-1 pe-1">アクションラベルを入力</label>';
        } else {
            action1 = '<label id="display_action_1_' + number + '" class="action-label ps-1 pe-1">' + $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() + '</label>';
        }
    }

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + label + action1 + '</div>';
    html += '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_more_preview(number) {
    var height = '14rem';
    $( '.line-preview .line-preview-content .line-preview-body .cardtype-area' ).each( function( index, value ) {
        height = $( this ).outerHeight(true);
    });
    if ( $( '#save_cardtype_form [name=template_' + number + ']' ).val() == '1' ) {
        var html = '<li style="margin-right: 0.5rem;">';
        html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
        html += '<div class="cardtype-body-area position-relative ps-2 pe-2">';
        html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
        html += '</div>';
        html += '</div>';
        html += '</li>';
        $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
    } else if ( $( '#save_cardtype_form [name=template_' + number + ']' ).val() == '2' ) {
        var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png );"></span>';
        if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val() != '' ) {
            if ( $( '#save_cardtype_form [name=image_' + number + ']' ).val().indexOf( 'uploads' ) !== -1 ) {
                image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
            } else {
                image = '<span style="background-image: url( ' + $( '#save_cardtype_form [name=image_' + number + ']' ).val() + '"></span>';
            }
        }

        var image_area = '<div id="display_image_area_' + number + '" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image_area += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image_area += '<input type="hidden" value="more">';
        image_area += image;
        image_area += '</div>';
        image_area += '</div>';
        
        var html = '<li style="margin-right: 0.5rem;">';
        html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
        html += '<div class="cardtype-header-area">';
        html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
        html += '</div>';
        html += '<div class="cardtype-body-area position-relative ps-2 pe-2" style="height: calc(100% - 120px)">';
        html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
        html += '</div>';
        html += '</div>';
        html += '</li>';
        $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
    }
}

function append_list_announce_preview(data) {
    var image = '';
    if ( data.image_flg ) {
        if ( data.image_count == '1' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '</div>';
        } else if ( data.image_count == '2' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png';
            if ( data.image_2 != '' ) {
                if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + data.image_2;
                } else {
                    image_b = data.image_2;
                }
            }
            image += '<div id="display_image_area_2" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>';
            image += '</div>';
        } else if ( data.image_count == '3' ) {
            var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
            if ( data.image_1 != '' ) {
                if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                    image_a = $( '#env_media_url' ).val() + data.image_1;
                } else {
                    image_a = data.image_1;
                }
            }
            var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png';
            if ( data.image_2 != '' ) {
                if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                    image_b = $( '#env_media_url' ).val() + data.image_2;
                } else {
                    image_b = data.image_2;
                }
            }
            var image_c = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png';
            if ( data.image_3 != '' ) {
                if ( data.image_3.indexOf( 'uploads' ) !== -1 ) {
                    image_c = $( '#env_media_url' ).val() + data.image_3;
                } else {
                    image_c = data.image_3;
                }
            }
            image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image += '<input type="hidden" value="a">';
            image += '<span style="background-image: url( ' + image_a + ' );"></span>';
            image += '</div>';
            image += '<div class="two flex-column position-relative">';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="b">';
            image += '<span style="background-image: url( ' + image_b + ' );"></span>';
            image += '</div>';
            image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            image += '<input type="hidden" value="c">';
            image += '<span style="background-image: url( ' + image_c + ' );"></span>';
            image += '</div>';
            image += '</div>';
            image += '</div>';
        }
    } else {
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        if ( data.label_flg ) {
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 2.5rem;">';
        } else {
            image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 0rem;">';
        }
        image += '<input type="hidden" value="a">';
        image += '<span></span>';
        image += '</div>';
        image += '</div>';
    }
    var title = '';
    if ( data.title == '' ) {
        title = '<p id="display_title_' + data.number + '" class="title mb-1" style="font-size: 0.85rem;">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + data.number + '" class="title mb-1" style="font-size: 0.85rem;">' + data.title + '</p>';
    }
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var description = '';
    if ( data.description_flg ) {
        if ( data.description == '' ) {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">' + data.description.replace(/\r?\n/g, '<br>') + '</p>';
        }
    }
    var text = '';
    $.each( data.text, function( index, value ) {
        if ( value.flg ) {
            text += '<div class="d-flex align-items-center mt-2 mb-2">';
            text += '<p id="display_text_title_' + ( index + 1 ) + '_' + data.number + '" class="mb-0" style="font-size: 0.7rem; font-weight: bold;">' + value.title + '</p>';
            text += '<p id="display_text_text_' + ( index + 1 ) + '_' + data.number + '" class="ms-auto mb-0" style="font-size: 0.5rem;">' + value.text + '</p>';
            text += '</div>';
        }
    });
    var action = '';
    $.each( data.action, function( index, value ) {
        if ( value.flg ) {
            if ( value.button_type == 0 ) {
                var color = '#fff';
                var background = '#fff';
                if ( value.button_color == 0 ) {
                    background = '#666f86';
                } else if ( value.button_color == 1 ) {
                    background = '#fff';
                } else if ( value.button_color == 2 ) {
                    background = '#eb4e3d';
                } else if ( value.button_color == 3 ) {
                    background = '#ed8537';
                } else if ( value.button_color == 4 ) {
                    background = '#00B900';
                } else if ( value.button_color == 5 ) {
                    background = '#5b82db';
                }
                action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + data.number + '" class="btn p-0 mb-2" style="width: 90%; color: ' + color + '; background-color: ' + background + '; border: none;" tabindex="0">' + value.label + '</button>';
            } else if ( value.button_type == 1 ) {
                var color = '#5b82db';
                var background = '#fff';
                if ( value.button_color == 0 ) {
                    color = '#666f86';
                } else if ( value.button_color == 1 ) {
                    color = '#fff';
                } else if ( value.button_color == 2 ) {
                    color = '#eb4e3d';
                } else if ( value.button_color == 3 ) {
                    color = '#ed8537';
                } else if ( value.button_color == 4 ) {
                    color = '#00B900';
                } else if ( value.button_color == 5 ) {
                    color = '#5b82db';
                }
                action += '<button type="button" id="display_action_label_' + ( index + 1 ) + '_' + data.number + '" class="btn p-0 mb-2" style="width: 90%; color: ' + color + '; background-color: ' + background + '; border: none;" tabindex="0">' + value.label + '</button>';
            }
        }
    });

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">' + title + description + text + '</div>';
    html += '<div class="cardtype-footer-area text-center">' + action + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_list_location_preview(data) {
    var image = '';
    if ( data.image_count == '1' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '</div>'
    } else if ( data.image_count == '2' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png';
        if ( data.image_2 != '' ) {
            if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + data.image_2;
            } else {
                image_b = data.image_2;
            }
        }
        image += '<div id="display_image_area_2" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '</div>'
    } else if ( data.image_count == '3' ) {
        var image_a = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png';
        if ( data.image_1 != '' ) {
            if ( data.image_1.indexOf( 'uploads' ) !== -1 ) {
                image_a = $( '#env_media_url' ).val() + data.image_1;
            } else {
                image_a = data.image_1;
            }
        }
        var image_b = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png';
        if ( data.image_2 != '' ) {
            if ( data.image_2.indexOf( 'uploads' ) !== -1 ) {
                image_b = $( '#env_media_url' ).val() + data.image_2;
            } else {
                image_b = data.image_2;
            }
        }
        var image_c = $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png';
        if ( data.image_3 != '' ) {
            if ( data.image_3.indexOf( 'uploads' ) !== -1 ) {
                image_c = $( '#env_media_url' ).val() + data.image_3;
            } else {
                image_c = data.image_3;
            }
        }
        image += '<div id="display_image_area_1" class="cardtype-image-area d-flex flex-row position-relative w-100">';
        image += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
        image += '<input type="hidden" value="a">';
        image += '<span style="background-image: url( ' + image_a + ' );"></span>';
        image += '</div>';
        image += '<div class="two flex-column position-relative">';
        image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="b">';
        image += '<span style="background-image: url( ' + image_b + ' );"></span>';
        image += '</div>';
        image += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
        image += '<input type="hidden" value="c">';
        image += '<span style="background-image: url( ' + image_c + ' );"></span>';
        image += '</div>';
        image += '</div>';
        image += '</div>';
    }
    var title = '';
    if ( data.title == '' ) {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">タイトルを入力</p>';
    } else {
        title = '<p id="display_title_' + data.number + '" class="title mb-1">' + data.title + '</p>';
    }
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var place = '';
    if ( data.place_flg ) {
        if ( data.place == '' ) {
            place += '<p id="display_place_' + data.number + '" class="place d-flex align-items-center mb-1">';
            place += '<img src="/static/img/icon/map.png" class="me-1">';
            place += '<span>住所を入力</span>';
            place += '</p>';
        } else {
            place += '<p id="display_place_' + data.number + '" class="place d-flex align-items-center mb-1">';
            place += '<img src="/static/img/icon/map.png" class="me-1">';
            place += '<span>' + data.place + '</span>';
            place += '</p>';
        }
    }
    var plus = '';
    if ( data.plus_flg ) {
        var icon = '';
        if ( data.plus_type == 1 ) {
            icon = '<img src="/static/img/icon/time.png" class="me-1">';
        } else if ( data.plus_type == 2 ) {
            icon = '<img src="/static/img/icon/coin.png" class="me-1">';
        }
        if ( data.plus == '' ) {
            plus += '<p id="display_plus_' + data.number + '" class="plus d-flex align-items-center mb-0">';
            plus += icon;
            plus += '<span>追加情報を入力</span>';
            plus += '</p>';
        } else {
            plus += '<p id="display_plus_' + data.number + '" class="plus d-flex align-items-center mb-0">';
            plus += icon;
            plus += '<span>' + data.plus + '</span>';
            plus += '</p>';
        }
    }
    var action1 = '';
    if ( data.action_flg_1 ) {
        if ( data.action_label_1 == '' ) {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_1 + '</button>';
        }
    }
    var action2 = '';
    if ( data.action_flg_2 ) {
        if ( data.action_label_2 == '' ) {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_2 + '</button>';
        }
    }
    
    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image + label + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">' + title + place + plus + '</div>';
    html += '<div class="cardtype-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_list_person_preview(data) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/person-default.png );"></span>';
    if ( data.image != '' ) {
        if ( data.image.indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + data.image + '"></span>';
        }
    }

    var image_area = '<div id="display_image_area_' + data.number + '" class="cardtype-image-area d-flex flex-row position-relative w-100 pt-3 ps-4 pe-4">';
    image_area += '<div class="person cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
    image_area += '<input type="hidden" value="account">';
    image_area += image;
    image_area += '</div>';
    image_area += '</div>';
    
    var name = '';
    if ( data.name == '' ) {
        name = '<p id="display_name_' + data.number + '" class="name mb-1">名前を入力</p>';
    } else {
        name = '<p id="display_name_' + data.number + '" class="name mb-1">' + data.name + '</p>';
    }
    var tag1 = '';
    if ( data.tag_flg_1 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_1 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_1 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_1 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_1 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_1 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_1 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_1 == '' ) {
            tag1 = '<label id="display_tag_1_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag1 = '<label id="display_tag_1_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_1 + '</label>';
        }
    }
    var tag2 = '';
    if ( data.tag_flg_2 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_2 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_2 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_2 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_2 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_2 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_2 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_2 == '' ) {
            tag2 = '<label id="display_tag_2_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag2 = '<label id="display_tag_2_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_2 + '</label>';
        }
    }
    var tag3 = '';
    if ( data.tag_flg_3 ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.tag_color_3 == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.tag_color_3 == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.tag_color_3 == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.tag_color_3 == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.tag_color_3 == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.tag_color_3 == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.tag_3 == '' ) {
            tag3 = '<label id="display_tag_3_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>ラベルを入力</label>';
        } else {
            tag3 = '<label id="display_tag_3_' + data.number + '" class="tag ps-1 pe-1 mb-0" ' + style + '>' + data.tag_3 + '</label>';
        }
    }
    var description = '';
    if ( data.description_flg ) {
        if ( data.description == '' ) {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">説明文を入力</p>';
        } else {
            description = '<p id="display_description_' + data.number + '" class="description mb-1">' + data.description + '</p>';
        }
    }
    var action1 = '';
    if ( data.action_flg_1 ) {
        if ( data.action_label_1 == '' ) {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action1 = '<button type="button" id="display_action_1_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_1 + '</button>';
        }
    }
    var action2 = '';
    if ( data.action_flg_2 ) {
        if ( data.action_label_2 == '' ) {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        } else {
            action2 = '<button type="button" id="display_action_2_' + data.number + '" class="btn p-0 mb-2">' + data.action_label_2 + '</button>';
        }
    }

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
    html += '</div>';
    html += '<div class="cardtype-body-area p-2">';
    html += name;
    html += '<p class="text-center mb-0">' + tag1 + tag2 + tag3 + '</p>';
    html += description;
    html += '</div>';
    html += '<div class="cardtype-footer-area">' + action1 + action2 + '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_list_image_preview(data) {
    var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png );"></span>';
    if ( data.image != '' ) {
        if ( data.image.indexOf( 'uploads' ) !== -1 ) {
            image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
        } else {
            image = '<span style="background-image: url( ' + data.image + '"></span>';
        }
    }

    var image_area = '<div id="display_image_area_' + data.number + '" class="cardtype-image-area d-flex flex-row position-relative w-100">'
    image_area += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 10rem;">';
    image_area += '<input type="hidden" value="image">';
    image_area += image;
    image_area += '</div>';
    image_area += '</div>';
    
    var label = '';
    if ( data.label_flg ) {
        var color = '';
        var background_color = '';
        var boder_color = '';
        if ( data.label_color == '0' ) {
            color = '#fff';
            background_color = '#666f86';
        } else if ( data.label_color == '1' ) {
            color = '#666f86';
            background_color = '#fff';
            boder_color = '#666f86';
        } else if ( data.label_color == '2' ) {
            color = '#fff';
            background_color = '#eb4e3d';
        } else if ( data.label_color == '3' ) {
            color = '#fff';
            background_color = '#ed8537';
        } else if ( data.label_color == '4' ) {
            color = '#fff';
            background_color = '#00B900';
        } else if ( data.label_color == '5' ) {
            color = '#fff';
            background_color = '#5b82db';
        }

        if ( background_color === '#fff' ) {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + '; border: 1px solid ' + boder_color + ';"';
        } else {
            var style = 'style="color: ' + color + '; background-color: ' + background_color + ';"';
        }

        if ( data.label == '' ) {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>ラベルを入力</label>';
        } else {
            label = '<label id="display_label_' + data.number + '" class="label ps-1 pe-1" ' + style + '>' + data.label + '</label>';
        }
    }
    var action1 = '';
    if ( data.action_flg ) {
        if ( data.action_label == '' ) {
            action1 = '<label id="display_action_1_' + data.number + '" class="action-label ps-1 pe-1">アクションラベルを入力</label>';
        } else {
            action1 = '<label id="display_action_1_' + data.number + '" class="action-label ps-1 pe-1">' + data.action_label + '</label>';
        }
    }

    var html = '<li style="margin-right: 0.5rem;">';
    html += '<div class="cardtype-area" style="height: auto;">';
    html += '<div class="cardtype-header-area">';
    html += '<div class="d-flex position-relative w-100">' + image_area + label + action1 + '</div>';
    html += '</div>';
    html += '</div>';
    html += '</li>';
    return html;
}

function append_list_more_preview(data) {
    if ( check_empty(data) ) {
        var height = '14rem';
        $( '.line-preview .line-preview-content .line-preview-body .cardtype-area' ).each( function( index, value ) {
            height = $( this ).outerHeight(true);
        });
        if ( data.type == '1' ) {
            var html = '<li style="margin-right: 0.5rem;">';
            html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
            html += '<div class="cardtype-body-area position-relative ps-2 pe-2">';
            html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
            html += '</div>';
            html += '</div>';
            html += '</li>';
            $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
        } else if ( data.type == '2' ) {
            var image = '<span style="background-image: url( ' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png );"></span>';
            if ( data.image != '' ) {
                if ( data.image.indexOf( 'uploads' ) !== -1 ) {
                    image = '<span style="background-image: url( ' + $( '#env_media_url' ).val() + data.image + '"></span>';
                } else {
                    image = '<span style="background-image: url( ' + data.image + '"></span>';
                }
            }

            var image_area = '<div id="display_image_area_' + data.number + '" class="cardtype-image-area d-flex flex-row position-relative w-100">';
            image_area += '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            image_area += '<input type="hidden" value="more">';
            image_area += image;
            image_area += '</div>';
            image_area += '</div>';
            
            var html = '<li style="margin-right: 0.5rem;">';
            html += '<div class="cardtype-area" style="height: ' + height + 'px;">';
            html += '<div class="cardtype-header-area">';
            html += '<div class="d-flex position-relative w-100">' + image_area + '</div>';
            html += '</div>';
            html += '<div class="cardtype-body-area position-relative ps-2 pe-2" style="height: calc(100% - 120px)">';
            html += '<p id="display_action_label_10" class="more mb-1">もっと見る</p>';
            html += '</div>';
            html += '</div>';
            html += '</li>';
            $( '.line-preview .line-preview-content .line-preview-body ul' ).append( html );
        }
    }
}