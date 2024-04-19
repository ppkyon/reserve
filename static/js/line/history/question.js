$( function() {
    $( '.question-area .button-area .check-button' ).on( 'click', function() {
        if ( $( '#question_form' ).parsley().validate() ) {
            $( '.loader-area' ).css( 'opacity', '1' );
            $( '.loader-area' ).removeClass( 'd-none' );
            $( '.question-area' ).addClass( 'd-none' );
    
            for ( var i = 1; i <= $( '#question_form' ).children( 'div.row' ).length; i++ ) {
                var type = Number($( '#question_form' ).find( '[name=type_' + i + ']' ).val());
                var title = $( '#question_form' ).find( '[name=type_' + i + ']' ).prev().find( '.input-label' ).text();
                var html = '<div class="content-item-area p-2">';
                html += '<div class="content-item-title-area d-flex align-items-center mb-1">';
                html += '<p class="content-item-title mb-0">' + title + '</p>';
                html += '</div>';
                if ( type == 1 || type == 2 || type == 5 || type == 8 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">' + $( '#question_form' ).find( '[name=text_' + i + ']' ).val() + '</p>';
                } else if ( type == 3 || type == 4 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">' + $( '#question_form' ).find( '[name=value_' + i + ']' ).val() + '</p>';
                } else if ( type == 6 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">' + $( '#question_form' ).find( '[name=email_' + i + ']' ).val() + '</p>';
                } else if ( type == 7 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">' + $( '#question_form' ).find( '[name=date_' + i + ']' ).val() + '</p>';
                } else if ( type == 9 || type == 10 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">';
                    if ( check_empty($( '#question_form' ).find( '[id=image_url_' + i + ']' ).attr( 'src' )) ) {
                        html += '<img src="' + $( '#question_form' ).find( '[id=image_url_' + i + ']' ).attr( 'src' ) + '" class="w-100 p-1">';
                    }
                    html += '</p>';
                } else if ( type == 11 ) {
                    html += '<p class="content-item-description check-question-text me-5 mb-0">';
                    if ( check_empty($( '#question_form' ).find( '[id=video_url_' + i + ']' ).attr( 'src' )) ) {
                        html += '<video src="' + $( '#question_form' ).find( '[id=video_url_' + i + ']' ).attr( 'src' ) + '" class="w-100 p-1" controls></video>';
                    }
                    html += '</p>';
                } else if ( type == 99 ) {
                    var text = '';
                    var choice_type = Number($( '#question_form' ).find( '[name=choice_type_' + i + ']' ).val());
                    var choice_count = Number($( '#question_form' ).find( '[name=choice_count_' + i + ']' ).val());
                    if ( choice_type == 4 ) {
                        if ( check_empty($( '#question_form' ).find( '[id=dropdown_' + i + ']' ).val()) ) {
                            text += ',' + $( '#question_form' ).find( '[id=dropdown_' + i + ']' ).val();
                        }
                    }
                    for ( var j = 1; j <= choice_count; j++ ) {
                        if ( check_empty(text) ) {
                            if ( choice_type == 1 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=text_' + i + '_' + j + ']' ).val()) ) {
                                    text += ',' + $( '#question_form' ).find( '[name=text_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 2 ) {
                                if ( $( '#question_form' ).find( '[id=radio_' + i + '_' + j + ']' ).prop( 'checked' ) ) {
                                    text += ',' + $( '#question_form' ).find( '[id=radio_' + i + '_' + j + ']' ).prev().text();
                                }
                            } else if ( choice_type == 3 ) {
                                if ( $( '#question_form' ).find( '[id=check_' + i + '_' + j + ']' ).prop( 'checked' ) ) {
                                    text += ',' + $( '#question_form' ).find( '[id=check_' + i + '_' + j + ']' ).prev().text();
                                }
                            } else if ( choice_type == 5 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=date_' + i + '_' + j + ']' ).val()) ) {
                                    text += ',' + $( '#question_form' ).find( '[name=date_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 6 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=time_' + i + '_' + j + ']' ).val()) ) {
                                    text += ',' + $( '#question_form' ).find( '[name=time_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 7 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=date_time_' + i + '_' + j + ']' ).val()) ) {
                                    text += ',' + $( '#question_form' ).find( '[name=date_time_' + i + '_' + j + ']' ).val();
                                }
                            }
                        } else {
                            if ( choice_type == 1 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=text_' + i + '_' + j + ']' ).val()) ) {
                                    text += $( '#question_form' ).find( '[name=text_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 2 ) {
                                if ( $( '#question_form' ).find( '[id=radio_' + i + '_' + j + ']' ).prop( 'checked' ) ) {
                                    text += $( '#question_form' ).find( '[id=radio_' + i + '_' + j + ']' ).prev().text();
                                }
                            } else if ( choice_type == 3 ) {
                                if ( $( '#question_form' ).find( '[id=check_' + i + '_' + j + ']' ).prop( 'checked' ) ) {
                                    text += $( '#question_form' ).find( '[id=check_' + i + '_' + j + ']' ).prev().text();
                                }
                            } else if ( choice_type == 5 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=date_' + i + '_' + j + ']' ).val()) ) {
                                    text += $( '#question_form' ).find( '[name=date_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 6 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=time_' + i + '_' + j + ']' ).val()) ) {
                                    text += $( '#question_form' ).find( '[name=time_' + i + '_' + j + ']' ).val();
                                }
                            } else if ( choice_type == 7 ) {
                                if ( check_empty($( '#question_form' ).find( '[name=date_time_' + i + '_' + j + ']' ).val()) ) {
                                    text += $( '#question_form' ).find( '[name=date_time_' + i + '_' + j + ']' ).val();
                                }
                            }
                        }
                    }
                    html += '<p class="content-item-description check-question-text me-5 mb-0">' + text + '</p>';
                }
                html += '</div>';
                $( '.question-check-area .content-area .content-item-area' ).parent().append(html);
                $( '.question-end-area .content-area .content-item-area' ).parent().append(html);
            }
            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.question-check-area' ).removeClass( 'd-none' );
            }, 750 );
        }
    });
    
    if ( $( '#question_form' ).length ) {
        $( '#question_form' ).parsley();
        $( '#question_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#question_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
        $( '#question_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
    }
});