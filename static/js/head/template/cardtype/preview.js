
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