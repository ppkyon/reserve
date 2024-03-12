function action_preview() {
    $( document ).on( 'keyup', '#save_question_form input[name=title]', function() {
        create_preview();
    });
    $( document ).on( 'keyup', '#save_question_form textarea[name=description]', function() {
        create_preview();
    });
    $( document ).on( 'keyup', '#save_question_form .display-area .top-area .input-name', function() {
        create_preview();
    });
    $( document ).on( 'keyup', '#save_question_form .display-area .sub-area .input-description', function() {
        create_preview();
    });
    $( document ).on( 'change', '#save_question_form .display-area .action-area .pin-area input[type=checkbox]', function() {
        create_preview();
    });
}

function create_preview() {
    $( '.line-preview .line-preview-content .line-preview-body' ).empty();

    var html = '<div class="line-question-preview">';
    html += '<div class="line-question-preview-header">';
    html += '<h2>' + $( '#save_question_form input[name=title]' ).val() + '</h2>';
    html += '<p class="domain-url">' + $( '#env_domain_url' ).val() + '</p>';
    html += '<p class="close-button">×</p>';
    html += '</div>';
    html += '<p class="line-question-preview-title">' + $( '#save_question_form input[name=title]' ).val() + '</p>';
    html += '<p class="line-question-preview-description">' + $( '#save_question_form textarea[name=description]' ).val().replaceAll('\n', '<br>') + '</p>';
    html += '<form>';
    $( '#save_question_form .display-area' ).each( function( index, value ) {
        var type = Number($( this ).find( '.top-area .input-select-dropdown input[type=hidden]' ).val());
        html += '<div class="line-question-preview-question">';
        if ( type == 1 || type == 2 || type == 5 || type == 6 || type == 8 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            html += '<div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<input class="question-text backcolor-white" type="text" placeholder="' + $( this ).find( '.sub-area .input-description' ).val() + '" disabled>';
            } else {
                html += '<input class="question-text backcolor-white" type="text" disabled>';
            }
            html += '</div>';
        } else if ( type == 3 || type == 4 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            html += '<div>';
            html += '<select class="backcolor-white" disabled>';
            html += '</select>';
            html += '</div>';
        } else if ( type == 7 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            html += '<div>';
            html += '<input class="question-text backcolor-white" type="text" disabled>';
            html += '</div>';
        } else if ( type == 9 || type == 10 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            html += '<div>';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/preview-image.jpg">';
            html += '</div>';
        } else if ( type == 11 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            html += '<div>';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/preview-movie.jpg">';
            html += '</div>';
        } else if ( type == 51 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            $( this ).find( '.content-area .item-area input' ).each( function( choice_index, choice_value ) {
                html += '<div>';
                html += '<input type="radio" readonly> ' + $( choice_value ).val();
                html += '</div>';
            });
        } else if ( type == 52 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            html += '<div>';
            html += '<input type="radio" readonly> 〇年〇月〇日 〇時〇分';
            html += '</div>';
            html += '<div>';
            html += '<input type="radio" readonly> 〇年〇月〇日 〇時〇分';
            html += '</div>';
        } else if ( type == 53 || type == 54 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }
            $( this ).find( '.content-area .item-area input' ).each( function( choice_index, choice_value ) {
                html += '<p class="list-item">' + $( choice_value ).val() + '</p>';
                html += '<div>';
                html += '<input class="question-text backcolor-white" type="text" disabled>';
                html += '</div>';  
            });
        } else if ( type == 99 ) {
            html += '<div class="d-flex">';
            html += '<span>' + $( this ).find( '.top-area .input-name' ).val() + '</span>';
            if ( $( this ).find( '.action-area .pin-area input[type=checkbox]' ).prop( 'checked' ) ) {
                html += '<span class="line-question-preview-required active ms-auto">必須</span>';
            }
            html += '</div>';
            if ( check_empty($( this ).find( '.sub-area .input-description' ).val()) ) {
                html += '<p>' + $( this ).find( '.sub-area .input-description' ).val() + '</p>';
            }

            var choice_type = Number($( this ).find( '.content-area .type-area .input-select-dropdown input[type=hidden]' ).val());
            if ( choice_type == 1 || choice_type == 5 || choice_type == 6 || choice_type == 7 ) {
                $( this ).find( '.content-area .item-area input' ).each( function( choice_index, choice_value ) {
                    html += '<div>';
                    html += '<input class="question-text backcolor-white" type="text" placeholder="' + $( choice_value ).val() + '" disabled>';
                    html += '</div>';
                });
            } else if ( choice_type == 2 ) {
                $( this ).find( '.content-area .item-area input' ).each( function( choice_index, choice_value ) {
                    html += '<div>';
                    html += '<input type="radio" readonly>';
                    html += '<span> ' + $( choice_value ).val() + '</span>';
                    html += '</div>';
                });
            } else if ( choice_type == 3 ) {
                $( this ).find( '.content-area .item-area input' ).each( function( choice_index, choice_value ) {
                    html += '<div>';
                    html += '<input type="checkbox" readonly>';
                    html += '<span> ' + $( choice_value ).val() + '</span>';
                    html += '</div>';
                });
            } else if ( choice_type == 4 ) {
                html += '<div>';
                html += '<select class="backcolor-white" disabled></select>';
                html += '</div>';
            }
        }
        html += '</div>';
    });
    html += '<p class="line-question-preview-submit">確認する</p>';
    html += '</form>';

    $( '.line-preview .line-preview-content .line-preview-body' ).append(html);

    var color = Number($( '.color-label-area i' ).parent().val());
    $( '.line-question-preview-title' ).addClass( 'color' + color );
}

function create_list_preview(id) {
    var form_data = new FormData();
    form_data.append( 'id', id );
    $.ajax({
        'data': form_data,
        'url': $( '#get_question_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '.line-preview .line-preview-content .line-preview-body' ).empty();
        if ( check_empty(response) ) {
            var html = '<div class="line-question-preview">';
            html += '<div class="line-question-preview-header">';
            html += '<h2>' + response.title + '</h2>';
            html += '<p class="domain-url">' + $( '#env_domain_url' ).val() + '</p>';
            html += '<p class="close-button">×</p>';
            html += '</div>';
            html += '<p class="line-question-preview-title">' + response.title + '</p>';
            html += '<p class="line-question-preview-description">' + response.description.replaceAll('\n', '<br>') + '</p>';
            html += '<form>';
            $( response.item ).each( function( index, value ) {
                html += '<div class="line-question-preview-question">';
                if ( value.type == 1 || value.type == 2 || value.type == 5 || value.type == 6 || value.type == 8 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    html += '<div>';
                    if ( check_empty(value.description) ) {
                        html += '<input class="question-text backcolor-white" type="text" placeholder="' + value.description + '" disabled>';
                    } else {
                        html += '<input class="question-text backcolor-white" type="text" disabled>';
                    }
                    html += '</div>';
                } else if ( value.type == 3 || value.type == 4 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    html += '<div>';
                    html += '<select class="backcolor-white" disabled>';
                    html += '</select>';
                    html += '</div>';
                } else if ( value.type == 7 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    html += '<div>';
                    html += '<input class="question-text backcolor-white" type="text" disabled>';
                    html += '</div>';
                } else if ( value.type == 9 || value.type == 10 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    html += '<div>';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/preview-image.jpg">';
                    html += '</div>';
                } else if ( value.type == 11 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    html += '<div>';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/preview-movie.jpg">';
                    html += '</div>';
                } else if ( value.type == 51 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    $.each( value.choice, function( choice_index, choice_value ) {
                        html += '<div>';
                        html += '<input type="radio" readonly> ' + choice_value.text;
                        html += '</div>';
                    });
                } else if ( value.type == 52 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    html += '<div>';
                    html += '<input type="radio" readonly> 〇年〇月〇日 〇時〇分';
                    html += '</div>';
                    html += '<div>';
                    html += '<input type="radio" readonly> 〇年〇月〇日 〇時〇分';
                    html += '</div>';
                } else if ( value.type == 53 || value.type == 54 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    $.each( value.choice, function( choice_index, choice_value ) {
                        if ( check_empty(choice_value.text) ) {
                            html += '<p class="list-item">' + choice_value.text + '</p>';
                        }
                        html += '<div>';
                        html += '<input class="question-text backcolor-white" type="text" disabled>';
                        html += '</div>';  
                    });           
                } else if ( value.type == 99 ) {
                    html += '<div class="d-flex">';
                    html += '<span>' + value.title + '</span>';
                    if ( value.required_flg ) {
                        html += '<span class="line-question-preview-required active ms-auto">必須</span>';
                    }
                    html += '</div>';
                    if ( check_empty(value.description) ) {
                        html += '<p>' + value.description + '</p>';
                    }
                    if ( value.choice_type == 1 || value.choice_type == 5 || value.choice_type == 6 || value.choice_type == 7 ) {
                        $.each( value.choice, function( choice_index, choice_value ) {
                            html += '<div>';
                            if ( check_empty(choice_value.text) ) {
                                html += '<input class="question-text backcolor-white" type="text" placeholder="' + choice_value.text + '" disabled>';
                            } else {
                                html += '<input class="question-text backcolor-white" type="text" disabled>';
                            }
                            html += '</div>';
                        });
                    } else if ( value.choice_type == 2 ) {
                        $.each( value.choice, function( choice_index, choice_value ) {
                            html += '<div>';
                            html += '<input type="radio" readonly>';
                            html += '<span> ' + choice_value.text + '</span>';
                            html += '</div>';
                        });
                    } else if ( value.choice_type == 3 ) {
                        $.each( value.choice, function( choice_index, choice_value ) {
                            html += '<div>';
                            html += '<input type="checkbox" readonly>';
                            html += '<span> ' + choice_value.text + '</span>';
                            html += '</div>';
                        });
                    } else if ( value.choice_type == 4 ) {
                        html += '<div>';
                        html += '<select class="backcolor-white" disabled></select>';
                        html += '</div>';
                    }
                }
                html += '</div>';
            });
            html += '<p class="line-question-preview-submit">確認する</p>';
            html += '</form>';
            html += '</div>';
            $( '.line-preview .line-preview-content .line-preview-body' ).append(html);
            $( '.line-question-preview-title' ).addClass( "color" + response.color );
        }
    }).fail( function(){

    });
}