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
            html += '<p class="line-question-preview-description">' + response.description + '</p>';
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
                    html += '<div>';
                    html += '<input type="radio" readonly> 対面';
                    html += '</div>';
                    html += '<div>';
                    html += '<input type="radio" readonly> オンライン';
                    html += '</div>';
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
                        html += '<p class="list-item">';
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
                        if ( check_empty(value.description) ) {
                            html += '<p>' + value.description + '</p>';
                        }
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