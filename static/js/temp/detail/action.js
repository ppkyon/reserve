
$( function() {
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

    $( '.detail-area .step-area tbody' ).on( 'click', function() {
        $( this ).parents( '.step-area' ).next().trigger( 'click' );
    });

    $( '.detail-area .question-area tbody tr' ).on( 'click', function() {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).find( 'input[type=hidden]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_question_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '.question-modal .modal-body .question-answer-area' ).empty();
            $( '#save_question_form [name=id]' ).val( $( target ).find( 'input[type=hidden]' ).val() );
            $( '#save_question_form [name=memo]' ).val( response.memo );
            $.each( response.item, function( index, value ) {
                if ( check_empty( value.data.title ) ) {
                    var html = '<div class="block-area">';
                    html += '<div class="question-area d-flex justify-content-start mb-1">';
                    html += '<i class="bx bx-notepad me-1 ms-3" style="font-size:1.2rem;"></i>';
                    html += '<p class="question-title mb-0">' + value.data.number + '. ' + value.data.title + '</p>';
                    html += '</div>';
                    html += '</div>';
                    $( '.question-modal .modal-body .question-answer-area' ).append( html );
                }
            });
            $.each( response.item, function( index, value ) {
                var html = '<div class="answer-area d-flex justify-content-start mb-2">';
                if ( value.data.type == 1 || value.data.type == 2 || value.data.type == 5 || value.data.type == 8 ) {
                    var answer = '';
                    if ( check_empty(value.text) ) {
                        answer = value.text;
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + answer + '</textarea>';
                } else if ( value.data.type == 3 ) {
                    var answer = '';
                    if ( check_empty(value.value) ) {
                        answer = value.value + '歳';
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + answer + '</textarea>';
                } else if ( value.data.type == 4 ) {
                    if ( value.value == 1 ) {
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>男性</textarea>';
                    } else if ( value.value == 2 ) {
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>女性</textarea>';
                    } else {
                        html += '<textarea class="input-textarea w-100 ms-3" readonly></textarea>';
                    }
                } else if ( value.data.type == 6 ) {
                    var answer = '';
                    if ( check_empty(value.email) ) {
                        answer = value.email;
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + answer + '</textarea>';
                } else if ( value.data.type == 7 ) {
                    date = '';
                    if ( check_empty(value.date) ) {
                        date = new Date( value.date );
                        date = date.getFullYear() + '年' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '月' + ( '00' + date.getDate() ).slice(-2) + '日';
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + date + '</textarea>';
                } else if ( value.data.type == 9 || value.data.type == 10 ) {
                    var answer = '';
                    if ( check_empty(value.image) ) {
                        if ( $( '#env_ngrok' ).val() == 'True' ) {
                            answer = $( '#env_ngrok_url' ).val() + $( '#env_media_url' ).val() + value.image;
                        } else {
                            answer = $( '#env_media_url' ).val() + value.image;
                        }
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + answer + '</textarea>';
                } else if ( value.data.type == 11 ) {
                    var answer = '';
                    if ( check_empty(value.video) ) {
                        if ( $( '#env_ngrok' ).val() == 'True' ) {
                            answer = $( '#env_ngrok_url' ).val() + $( '#env_media_url' ).val() + value.video;
                        } else {
                            answer = $( '#env_media_url' ).val() + value.video;
                        }
                    }
                    html += '<textarea class="input-textarea w-100 ms-3" readonly>' + answer + '</textarea>';
                } else if ( value.data.type == 99 ) {
                    if ( value.data.choice_type == 1 ) {
                        var display_text = '';
                        $.each( value.choice, function( choice_index, choice_value ) {
                            if ( choice_index == 0 ) {
                                if ( check_empty(choice_value.text) ) {
                                    display_text += choice_value.text;
                                }
                            } else {
                                if ( check_empty(choice_value.text) ) {
                                    display_text += ', ' + choice_value.text;
                                }
                            }
                        });
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>' + display_text + '</textarea>';
                    } else if ( value.data.choice_type == 2 || value.data.choice_type == 3 || value.data.choice_type == 4 ) {
                        var display_text = '';
                        var display_flg = false;
                        $.each( value.choice, function( choice_index, choice_value ) {
                            if ( display_flg ) {
                                if ( check_empty(choice_value.text) && choice_value.text == '1' ) {
                                    display_text += ', ' + choice_value.data.text;
                                }
                            } else {
                                if ( check_empty(choice_value.text) && choice_value.text == '1' ) {
                                    display_text += choice_value.data.text;
                                    display_flg = true;
                                }
                            }
                        });
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>' + display_text + '</textarea>';
                    } else if ( value.data.choice_type == 5 ) {
                        var display_date = '';
                        $.each( value.choice, function( choice_index, choice_value ) {
                            if ( check_empty(choice_value.date) ) {
                                var date = new Date( choice_value.date );
                                date = date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2);
                                if ( choice_index == 0 ) {
                                    display_date += date;
                                } else {
                                    display_date += ', ' + date;
                                }
                            }
                        });
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>' + display_date + '</textarea>';
                    } else if ( value.data.choice_type == 6 ) {
                        var display_time = '';
                        $.each( value.choice, function( choice_index, choice_value ) {
                            if ( check_empty(choice_value.time) ) {
                                var time = String(choice_value.time).substring( 0, String(choice_value.time).indexOf(':') ) + String(choice_value.time).substring( String(choice_value.time).indexOf(':'), String(choice_value.time).lastIndexOf(':') );
                                if ( choice_index == 0 ) {
                                    display_time += time;
                                } else {
                                    display_time += ', ' + time;
                                }
                            }
                        });
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>' + display_time + '</textarea>';
                    } else if ( value.data.choice_type == 7 ) {
                        var display_date = '';
                        $.each( value.choice, function( choice_index, choice_value ) {
                            if ( check_empty(choice_value.date) ) {
                                var date = new Date( choice_value.date );
                                date = date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2) + ' ' + ( '00' + date.getHours() ).slice(-2) + ':' + ( '00' + date.getMinutes() ).slice(-2);
                                if ( choice_index == 0 ) {
                                    display_date += date;
                                } else {
                                    display_date += ', ' + date;
                                }
                            }
                        });
                        html += '<textarea class="input-textarea w-100 ms-3" readonly>' + display_date + '</textarea>';
                    }
                }
                html += '<div class="expand-button"></div>';
                html += '</div>';
                $( '.question-modal .modal-body .question-answer-area .block-area' ).eq(index).append(html);
            });
            
            $( target ).addClass( 'active' );
        }).fail( function(){

        });
        $( this ).parents( '.question-area' ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '.question-modal .yes-button', function () {
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#edit_question_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_question_form [name=id]' ).val() );
        form_data.append( 'memo', $( '#save_question_form [name=memo]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_question_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#edit_question_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#edit_question_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'edit_question' );
});