$( function(){
    liff.init( {
        liffId: $( '#liff_id' ).val(),
    }).then( () => {
        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#check_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( check_empty(response.user.profile.image) ) {
                $( '.history-area .profile-area img' ).attr( 'src', $( '#env_media_url' ).val() + response.user.profile.image );
            } else if ( check_empty(response.user.display_image) ) {
                $( '.history-area .profile-area img' ).attr( 'src', response.user.display_image );
            } else {
                $( '.history-area .profile-area img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
            }
            if ( check_empty(response.user.profile.name) ) {
                $( '.history-area .profile-area p' ).text( response.user.profile.name );
            } else {
                $( '.history-area .profile-area p' ).text( response.user.display_name );
            }

            $( '.history-area .content-area' ).find( '#history' ).empty();
            $.each( response.history, function( index, value ) {
                if ( check_empty(value.schedule) && check_empty(value.reserve) ) {
                    var html = '';
                    if ( value.end_flg ) {
                        html += '<div class="history-content-area m-3">';
                    } else {
                        html += '<div class="history-content-area active m-3">';
                    }
                    html += '<input type="hidden" name="flow" value="' + value.display_id + '">';
                    html += '<input type="hidden" name="schedule" value="' + value.schedule.display_id + '">';
                    html += '<input type="hidden" name="place" value="' + value.place.display_id + '">';
                    if ( check_empty(value.course) ) {
                        html += '<input type="hidden" name="course" value="' + value.course.display_id + '">';
                    }
                    html += '<input type="hidden" name="setting" value="' + value.setting.display_id + '">';
                    html += '<p class="fw-bold pt-3 ps-3 pe-3 mb-0" style="font-size: 1rem;">' + value.reserve + '</p>';
                    html += '<p class="fw-bold ps-3 pe-3 mb-0" style="font-size: 0.8rem;">会場</p>';
                    html += '<p class="ps-3 pe-3 mb-1" style="font-size: 0.8rem;">' + value.place.title + '</p>';
                    html += '<p class="fw-bold ps-3 pe-3 mb-0" style="font-size: 0.8rem;">コース</p>';
                    html += '<p class="ps-3 pe-3 mb-0 mb-1">' + value.setting.title + '</p>';
                    if ( check_empty(value.setting.outline) ) {
                        html += '<p class="ps-3 pe-3 mb-0">' + value.setting.outline + '</p>';
                    }
                    if ( check_empty(value.setting.note) ) {
                        html += '<p class="ps-3 pe-3 mb-2">' + value.setting.note + '</p>';
                    }
                    if ( value.end_flg ) {
                        html += '<p class="text-center mb-0" style="color: #FFF; background-color: #4D4D4D; border-radius: 0 0 1rem 1rem;">過去の履歴</p>';
                    } else {
                        html += '<p class="text-center mb-0" style="color: #FFF; background-color: #EC6561; border-radius: 0 0 1rem 1rem;">予約を変更する</p>';
                    }
                    html += '</div>';
                    $( '.history-area .content-area' ).find( '#history' ).append(html);
                }
            });

            $( '.history-area .question-content-area' ).empty();
            $.each( response.question, function( index, value ) {
                $.each( value.item, function( item_index, item_value ) {
                    var html = '';
                    if ( item_index != 0 ) {
                        html += '<hr>';
                    }
                    html += '<div class="question-content-item-area position-relative">';
                    html += '<input type="hidden" name="question_id" value="' + value.display_id + '">';
                    if ( item_index == 0 ) {
                        html += '<p class="fw-bold pt-3 ps-3 pe-3 mb-0">' + item_value.title + '</p>';
                    } else {
                        html += '<p class="fw-bold ps-3 pe-3 mb-0">' + item_value.title + '</p>';
                    }
                    if ( item_index == value.item.length - 1 ) {
                        if ( check_empty(item_value.text) ) {
                            html += '<p class="pb-3 ps-3 pe-3 mb-0">' + item_value.text + '</p>';
                        } else if ( check_empty(item_value.email) ) {
                            html += '<p class="pb-3 ps-3 pe-3 mb-0">' + item_value.email + '</p>';
                        } else if ( check_empty(item_value.date) ) {
                            var date = new Date( item_value.date );
                            date = date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2);
                            html += '<p class="pb-3 ps-3 pe-3 mb-0">' + date + '</p>';
                        } else if ( check_empty(item_value.choice) ) {
                            if ( item_value.choice.length > 0 ) {
                                var choice_count = 0
                                html += '<p class="pb-3 ps-3 pe-3 mb-0">';
                                $.each( item_value.choice, function( choice_index, choice_value ) {
                                    if ( choice_value.text == '1' ) {
                                        if ( choice_count != 0 ) {
                                            html += ',';
                                        }
                                        html += choice_value.title;
                                        choice_count = choice_count + 1;
                                    }
                                });
                                html += '</p>';
                            }
                        }
                    } else {
                        if ( check_empty(item_value.text) ) {
                            html += '<p class="ps-3 pe-3 mb-0">' + item_value.text + '</p>';
                        } else if ( check_empty(item_value.email) ) {
                            html += '<p class="ps-3 pe-3 mb-0">' + item_value.email + '</p>';
                        } else if ( check_empty(item_value.date) ) {
                            var date = new Date( item_value.date );
                            date = date.getFullYear() + '/' + ( '00' + ( date.getMonth() + 1 ) ).slice(-2) + '/' + ( '00' + date.getDate() ).slice(-2);
                            html += '<p class="ps-3 pe-3 mb-0">' + date + '</p>';
                        } else if ( check_empty(item_value.choice) ) {
                            if ( item_value.choice.length > 0 ) {
                                var choice_count = 0
                                html += '<p class="pb-3 ps-3 pe-3 mb-0">';
                                $.each( item_value.choice, function( choice_index, choice_value ) {
                                    if ( choice_value.type == 1 ) {
                                        if ( check_empty(choice_value.text) ) {
                                            if ( choice_index != 0 ) {
                                                html += ',';
                                            }
                                            html += choice_value.text;
                                            choice_count = choice_count + 1;
                                        }
                                    } else if ( choice_value.type == 2 || choice_value.type == 3 || choice_value.type == 4 ) {
                                        if ( choice_value.text == '1' ) {
                                            if ( choice_count != 0 ) {
                                                html += ',';
                                            }
                                            html += choice_value.title;
                                            choice_count = choice_count + 1;
                                        }
                                    } else if ( choice_value.type == 5 || choice_value.type == 7 ) {
                                        if ( check_empty(choice_value.date) ) {
                                            if ( choice_index != 0 ) {
                                                html += ',';
                                            }
                                            html += choice_value.date;
                                            choice_count = choice_count + 1;
                                        }
                                    } else if ( choice_value.type == 6 ) {
                                        if ( check_empty(choice_value.time) ) {
                                            if ( choice_index != 0 ) {
                                                html += ',';
                                            }
                                            html += choice_value.time;
                                            choice_count = choice_count + 1;
                                        }
                                    }
                                });
                                html += '</p>';
                            }
                        }
                    }
                    if ( item_index == 0 ) {
                        html += '<img src="' + $( '#env_static_url' ).val() + 'img/history/question-arrow.svg" class="position-absolute" style="top: 65%; right: 8%;" width="15" height="15">';
                    } else if ( item_index == value.item.length - 1 ) {
                        html += '<img src="' + $( '#env_static_url' ).val() + 'img/history/question-arrow.svg" class="position-absolute" style="top: 33%; right: 8%;" width="15" height="15">';
                    } else {
                        html += '<img src="' + $( '#env_static_url' ).val() + 'img/history/question-arrow.svg" class="position-absolute" style="top: 53%; right: 8%;" width="15" height="15">';
                    }
                    html += '</div>';
                    $( '.history-area .question-content-area' ).append(html);
                });
            });

            $( '.history-area' ).removeClass( 'd-none' );
        }).fail( function(){
            
        });
    }).catch( ( err ) => {
        window.open('about:blank','_self').close();
    });
});