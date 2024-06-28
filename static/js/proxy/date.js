$( function(){
    $( document ).on( 'click', '.date-area .content-area .input-select-setting-dropdown .dropdown-menu button', function () {
        $( '.date-area .content-area .date-content-area' ).addClass( 'd-none' );
        $( '.date-area .content-area .date-loader-area' ).removeClass( 'd-none' );

        var id = '';
        if ( check_empty($( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val()) ) {
            id = $( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val();
        } else if ( check_empty($( '[name=course_setting]' ).val()) ) {
            id = $( '[name=course_setting]' ).val();
        } else if ( check_empty($( '[name=date_setting]' ).val()) ) {
            id = $( '[name=date_setting]' ).val();
        }

        var form_data = new FormData();
        form_data.append( 'id', id );
        if ( check_empty($( '.course-area .content-area .content-item-area .content-course-area [name=course]:checked' ).val()) ) {
            form_data.append( 'course_id', $( '.course-area .content-area .content-item-area .content-course-area [name=course]:checked' ).val() );
        } else {
            form_data.append( 'course_id', '' );
        }
        form_data.append( 'setting_id', $( this ).val() );
        form_data.append( 'year', $( '.date-area .content-area .date-year-text' ).next().val() );
        form_data.append( 'month', $( '.date-area .content-area .date-week-text' ).next().val() );
        form_data.append( 'day', $( '.date-area .content-area .date-week-text' ).next().next().val() );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            change_date(response);
        }).fail( function(){
            
        });
    });

    $( '.date-area .content-area .date-arrow-icon' ).on( 'click', function() {
        $( '.date-area .content-area .date-content-area' ).addClass( 'd-none' );
        $( '.date-area .content-area .date-loader-area' ).removeClass( 'd-none' );

        var id = '';
        if ( check_empty($( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val()) ) {
            id = $( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val();
        } else if ( check_empty($( '[name=course_setting]' ).val()) ) {
            id = $( '[name=course_setting]' ).val();
        } else if ( check_empty($( '[name=date_setting]' ).val()) ) {
            id = $( '[name=date_setting]' ).val();
        }

        var form_data = new FormData();
        form_data.append( 'id', id );
        if ( check_empty($( '.course-area .content-area .content-item-area .content-course-area [name=course]:checked' ).val()) ) {
            form_data.append( 'course_id', $( '.course-area .content-area .content-item-area .content-course-area [name=course]:checked' ).val() );
        } else {
            form_data.append( 'course_id', '' );
        }
        form_data.append( 'setting_id', $( '.date-area [name=select_setting]' ).next().val() );
        form_data.append( 'year', $( this ).next().val() );
        form_data.append( 'month', $( this ).next().next().val() );
        form_data.append( 'day', $( this ).next().next().next().val() );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_date_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            change_date(response);
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.date-area .content-area .date-table td.yes', function () {
        $( '.date-area .content-area .date-table td.yes' ).each( function( index, value ) {
            $( this ).removeClass( 'active' );
            $( this ).find( 'span' ).text( '◎' );
            $( this ).css( 'color', '#00B074' );
        });
        $( this ).addClass( 'active' );
        $( this ).find( 'span' ).text( '●' );
        $( this ).css( 'color', '#FF0000' );
        
        $( '.footer-area .footer-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.check-area .check-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.end-area .end-date-text' ).text( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.button-area .reserve-button' ).val( $( this ).find( 'input[type=hidden]' ).val() );
        $( '.date-area .footer-area' ).removeClass( 'd-none' );
    });

    $( '.date-area .footer-area .footer-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );

        if ( $( '[name=question_flg]' ).val() == 'true' ) {
            var id = '';
            if ( check_empty($( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val()) ) {
                id = $( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val();
            } else if ( check_empty($( '[name=course_setting]' ).val()) ) {
                id = $( '[name=course_setting]' ).val();
            } else if ( check_empty($( '[name=date_setting]' ).val()) ) {
                id = $( '[name=date_setting]' ).val();
            }

            var form_data = new FormData();
            form_data.append( 'id', id );
            form_data.append( 'setting_id', $( '.date-area [name=select_setting]' ).next().val() );

            if ( check_empty($( '.course-area [name=course]:checked' ).val()) ) {
                form_data.append( 'course_id', $( '.course-area [name=course]:checked' ).val() );
            } else {
                form_data.append( 'course_id', '' );
            }

            form_data.append( 'year', $( '.button-area .reserve-button' ).val().substring( 0, $( '.button-area .reserve-button' ).val().indexOf('年') ) );
            form_data.append( 'month', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('年')+1, $( '.button-area .reserve-button' ).val().indexOf('月') ) );
            form_data.append( 'day', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('月')+1, $( '.button-area .reserve-button' ).val().indexOf('日') ) );
            form_data.append( 'hour', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(')')+2, $( '.button-area .reserve-button' ).val().indexOf(':') ) );
            form_data.append( 'minute', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(':')+1, $( '.button-area .reserve-button' ).val().indexOf('～') ) );

            form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#get_question_url' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    $( '.question-area .content-area #question_id' ).val( response.question.display_id );
                    $( '.question-area .content-area .content-title' ).text( response.question.title );
                    $( '.question-area .content-area .content-description' ).html( response.question.description.replace(/\r?\n/g, '<br>') );

                    $( '#question_form' ).empty();
                    $.each( response.question.item, function( index, value ) {
                        var html = '<div class="row">';
                        html += '<div class="col-12 mb-3">';
                        html += '<div class="d-flex align-items-start mb-2" style="justify-content: space-between;">';
                        html += '<span class="input-label" style="max-width: 260px; font-size: 16px;">' + value.title + '</span>';
                        if ( value.required_flg ) {
                            html += '<span class="input-required-label ms-2 p-1 ps-3 pe-3 mt-0" style="max-width: 60px;" >必須</span>';
                        }
                        html += '</div>';
                        html += '<input type="hidden" name="type_' + value.number + '" value="' + value.type + '">';
                        if ( value.type == 1 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="">';
                                }
                            }
                        } else if ( value.type == 2 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[\u30A1-\u30FC]*" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[\u30A1-\u30FC]*" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="">';
                                }
                            }
                        } else if ( value.type == 3 ) {
                            html += '<div class="dropdown input-select-dropdown d-inline-block w-100 p-0">';
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" id="select_age_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="' + value.description + '" data-bs-toggle="dropdown" data-parsley-errors-container="#error_age_' + value.number + '"  data-parsley-error-message="選択してください" readonly required>';
                                } else {
                                    html += '<input type="text" id="select_age_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="" data-bs-toggle="dropdown" data-parsley-errors-container="#error_age_' + value.number + '"  data-parsley-error-message="選択してください" readonly required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" id="select_age_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="' + value.description + '" data-bs-toggle="dropdown" data-parsley-errors-container="#error_age_' + value.number + '"  data-parsley-error-message="選択してください" readonly>';
                                } else {
                                    html += '<input type="text" id="select_age_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="" data-bs-toggle="dropdown" data-parsley-errors-container="#error_age_' + value.number + '"  data-parsley-error-message="選択してください" readonly>';
                                }
                            }
                            html += '<input type="hidden">';
                            html += '<div class="dropdown-menu" aria-labelledby="select_age_{{ form_content_item.number }}">';
                            $.each( response.age_list, function( index, value ) {
                                if ( value >= 15 ) {
                                    if ( value == 15) {
                                        html += '<button type="button" value="' + value + '" class="btn dropdown-item fw-bold text-center">' + value + '歳</button>';
                                    } else {
                                        html += '<button type="button" value="' + value + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + value + '歳</button>';
                                    }
                                }
                            });
                            html += '</div>';
                            html += '</div>';
                            html += '<div id="error_age_' + value.number + '"></div>';
                        } else if ( value.type == 4 ) {
                            html += '<div class="dropdown input-select-dropdown d-inline-block w-100 p-0">';
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" id="select_sex_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="' + value.description + '" data-bs-toggle="dropdown" data-parsley-errors-container="#error_sex_' + value.number + '"  data-parsley-error-message="選択してください" readonly required>';
                                } else {
                                    html += '<input type="text" id="select_sex_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="" data-bs-toggle="dropdown" data-parsley-errors-container="#error_sex_' + value.number + '"  data-parsley-error-message="選択してください" readonly required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" id="select_sex_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="' + value.description + '" data-bs-toggle="dropdown" data-parsley-errors-container="#error_sex_' + value.number + '"  data-parsley-error-message="選択してください" readonly>';
                                } else {
                                    html += '<input type="text" id="select_sex_' + value.number + '" name="value_' + value.number + '" class="input-text input-select ps-2 pe-2" placeholder="" data-bs-toggle="dropdown" data-parsley-errors-container="#error_sex_' + value.number + '"  data-parsley-error-message="選択してください" readonly>';
                                }
                            }
                            html += '<input type="hidden">';
                            html += '<div class="dropdown-menu" aria-labelledby="select_sex_' + value.number + '">';
                            html += '<button type="button" value="1" class="btn dropdown-item fw-bold text-center">男性</button>';
                            html += '<button type="button" value="2" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">女性</button>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div id="error_sex_' + value.number + '"></div>';
                        } else if ( value.type == 5 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[0-9-]+$" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[0-9-]+$" placeholder="" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[0-9-]+$" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" pattern="[0-9-]+$" placeholder="">';
                                }
                            }
                        } else if ( value.type == 6 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="email" name="email_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="email" name="email_' + value.number + '" class="input-text ps-2" placeholder="" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="email" name="email_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="email" name="email_' + value.number + '" class="input-text ps-2" placeholder="">';
                                }
                            }
                        } else if ( value.type == 7 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="date_' + value.number + '" class="input-text input-birth-date ps-2 pe-2" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="text" name="date_' + value.number + '" class="input-text input-birth-date ps-2 pe-2" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="date_' + value.number + '" class="input-text input-birth-date ps-2 pe-2" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="text" name="date_' + value.number + '" class="input-text input-birth-date ps-2 pe-2">';
                                }
                            }
                        } else if ( value.type == 8 ) {
                            if ( value.required_flg ) {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '" required>';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="" required>';
                                }
                            } else {
                                if ( check_empty(value.description) ) {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="' + value.description + '">';
                                } else {
                                    html += '<input type="text" name="text_' + value.number + '" class="input-text ps-2" placeholder="">';
                                }
                            }
                        } else if ( value.type == 9 ) {
                            if ( check_empty(value.description) ) {
                                html += '<p class="mb-0">' + value.description + '</p>';
                            }
                            html += '<div class="error-message-image d-none mt-3 mb-1">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<p class="mb-0 d-none">提出可能なファイル形式は JPG,JPEG,PNGのみです</p>';
                            html += '<p class="mb-0 d-none">提出可能なファイルサイズは 10MBまでです</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-zone-wrap mb-3">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<div class="drop-zone image-drop-zone position-relative">';
                            html += '<input type="file" name="profile_file_' + value.number + '" class="image-file" accept=".jpg,.jpeg,.png" style="display: none;">';
                            if ( value.required_flg ) {
                                html += '<input type="text" name="image_' + value.number + '" class="image-upload-file d-none" data-parsley-errors-container="#error_image_' + value.number + '"  data-parsley-error-message="選択してください" required>';
                            } else {
                                html += '<input type="text" name="image_' + value.number + '" class="image-upload-file d-none">';
                            }
                            html += '<div class="dz-message image-drop-area me-4">';
                            html += '<i class="drop-icon text-muted bx bxs-cloud-upload mb-0"></i>';
                            html += '<p class="drop-button mb-2">選択</p>';
                            html += '<p class="drop-description mb-0">ファイル形式 JPG,JPEG,PNG</p>';
                            html += '<p class="drop-description mb-0">ファイルサイズ 10MBまで</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-display-zone d-none">';
                            html += '<img id="image_url_' + value.number + '" class="w-100 p-1">';
                            html += '<button type="button" class="btn image-delete-button mt-2">削除</button>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div id="error_image_' + value.number + '"></div>';
                            html += '</div>';
                        } else if ( value.type == 10 ) {
                            if ( check_empty(value.description) ) {
                                html += '<p class="mb-0">' + value.description + '</p>';
                            }
                            html += '<div class="error-message-image d-none mt-3 mb-1">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<p class="mb-0 d-none">提出可能なファイル形式は JPG,JPEG,PNGのみです</p>';
                            html += '<p class="mb-0 d-none">提出可能なファイルサイズは 10MBまでです</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-zone-wrap mb-3">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<div class="drop-zone image-drop-zone position-relative">';
                            html += '<input type="file" name="profile_file_' + value.number + '" class="image-file" accept=".jpg,.jpeg,.png" style="display: none;">';
                            if ( value.required_flg ) {
                                html += '<input type="text" name="image_' + value.number + '" class="image-upload-file d-none" data-parsley-errors-container="#error_image_' + value.number + '"  data-parsley-error-message="選択してください" required>';
                            } else {
                                html += '<input type="text" name="image_' + value.number + '" class="image-upload-file d-none">';
                            }
                            html += '<div class="dz-message image-drop-area me-4">';
                            html += '<i class="drop-icon text-muted bx bxs-cloud-upload mb-0"></i>';
                            html += '<p class="drop-button mb-2">選択</p>';
                            html += '<p class="drop-description mb-0">ファイル形式 JPG,JPEG,PNG</p>';
                            html += '<p class="drop-description mb-0">ファイルサイズ 10MBまで</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-display-zone d-none">';
                            html += '<img id="image_url_' + value.number + '" class="w-100 p-1">';
                            html += '<button type="button" class="btn image-delete-button mt-2">削除</button>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div id="error_image_' + value.number + '"></div>';
                            html += '</div>';
                        } else if ( value.type == 11 ) {
                            if ( check_empty(value.description) ) {
                                html += '<p class="mb-0">' + value.description + '</p>';
                            }
                            html += '<div class="error-message-video d-none mt-3 mb-1">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<p class="mb-0 d-none">提出可能なファイル形式は MP4,MOV,WMVのみです</p>';
                            html += '<p class="mb-0 d-none">提出可能なファイルサイズは 200MBまでです</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-zone-wrap mb-3">';
                            html += '<div class="row">';
                            html += '<div class="col-12 text-center">';
                            html += '<div class="drop-zone video-drop-zone position-relative">';
                            html += '<input type="file" name="vitae_file_' + value.number + '" class="video-file" accept=".mp4,.mov,.wmv,.hevc" style="display: none;">';
                            if ( value.required_flg ) {
                                html += '<input type="text" name="video_' + value.number + '" class="video-upload-file d-none" data-parsley-errors-container="#error_video_' + value.number + '"  data-parsley-error-message="選択してください" required>';
                            } else {
                                html += '<input type="text" name="video_' + value.number + '" class="video-upload-file d-none">';
                            }
                            html += '<div class="dz-message video-drop-area me-4">';
                            html += '<i class="drop-icon text-muted bx bxs-cloud-upload mb-0"></i>';
                            html += '<p class="drop-button mb-2">選択</p>';
                            html += '<p class="drop-description mb-0">ファイル形式 MP4,MOV,WMV</p>';
                            html += '<p class="drop-description mb-0">ファイルサイズ 200MBまで</p>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div class="drop-display-zone d-none">';
                            html += '<video id="video_url_' + value.number + '" class="w-100 p-1" controls>';
                            html += '<button type="button" class="btn video-delete-button mt-2 d-none">削除</button>';
                            html += '</div>';
                            html += '</div>';
                            html += '</div>';
                            html += '<div id="error_video_' + value.number + '"></div>';
                            html += '</div>';
                        } else if ( value.type == 99 ) {
                            if ( check_empty(value.description) ) {
                                html += '<p class="mb-2">' + value.description + '</p>';
                            }
                            if ( value.choice_type == 1 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    if ( value.required_flg ) {
                                        if ( choice_index == 0 ) {
                                            if ( check_empty(choice_value.text) ) {
                                                html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder="' + choice_value.text + '" required></textarea>';
                                            } else {
                                                html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder="" required></textarea>';
                                            }
                                        } else {
                                            if ( check_empty(choice_value.text) ) {
                                                html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder="' + choice_value.text + '"></textarea>';
                                            } else {
                                                html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder=""></textarea>';
                                            }
                                        }
                                    } else {
                                        if ( check_empty(choice_value.text) ) {
                                            html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder="' + choice_value.text + '"></textarea>';
                                        } else {
                                            html += '<textarea name="text_' + value.number + '_' + choice_value.number + '" class="input-text input-textarea ps-2 mt-2" placeholder=""></textarea>';
                                        }
                                    }
                                });
                            } else if ( value.choice_type == 2 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    html += '<div class="form-check mb-2">';
                                    html += '<div class="input-radio-wrap position-relative mb-1">';
                                    html += '<label for="radio_' + value.number + '_' + choice_value.number + '" class="ps-4 mb-0">' + choice_value.text + '</label>';
                                    if ( value.required_flg ) {
                                        html += '<input id="radio_' + value.number + '_' + choice_value.number + '" type="radio" name="choice_value_' + value.number + '" value="' + choice_value.number + '" class="form-check-input input-radio" data-parsley-errors-container="#error_radio_' + value.number + '" data-parsley-error-message="選択してください" required>';
                                    } else {
                                        html += '<input id="radio_' + value.number + '_' + choice_value.number + '" type="radio" name="choice_value_' + value.number + '" value="' + choice_value.number + '" class="form-check-input input-radio" >';
                                    }
                                    html += '<label for="radio_' + value.number + '_' + choice_value.number + '" class="input-radio-mark"></label>';
                                    html += '</div>';
                                    html += '</div>';
                                });
                                html += '<div id="error_radio_' + value.number + '"></div>';
                            } else if ( value.choice_type == 3 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    html += '<div class="form-check mb-2">';
                                    html += '<div class="input-check-wrap ps-4 mt-1 mb-0"> ';
                                    html += '<label for="check_' + value.number + '_' + choice_value.number + '" class="mb-0">' + choice_value.text + '</label>';
                                    if ( value.required_flg ) {
                                        if ( choice_index == 0 ) {
                                            html += '<input id="check_' + value.number + '_' + choice_value.number + '" type="checkbox" name="choice_value_' + value.number + '[]" value="' + choice_value.number + '" class="form-check-input input-check" data-parsley-errors-container="#error_check_' + value.number + '" data-parsley-error-message="選択してください" data-parsley-mincheck="1" required>';
                                        } else {
                                            html += '<input id="check_' + value.number + '_' + choice_value.number + '" type="checkbox" name="choice_value_' + value.number + '[]" value="' + choice_value.number + '" class="form-check-input input-check">';
                                        }
                                    } else {
                                        html += '<input id="check_' + value.number + '_' + choice_value.number + '" type="checkbox" name="choice_value_' + value.number + '[]" value="' + choice_value.number + '" class="form-check-input input-check">';
                                    }
                                    html += '<label for="check_' + value.number + '_' + choice_value.number + '" class="input-check-mark mb-0"></label>';
                                    html += '</div>';
                                    html += '</div>';
                                });
                                html += '<div id="error_check_' + value.number + '"></div>';
                            } else if ( value.choice_type == 4 ) {
                                html += '<div class="dropdown input-select-dropdown d-inline-block w-100 p-0">';
                                if ( value.required_flg ) {
                                    html += '<input type="text" id="dropdown_' + value.number + '" name="choice_text_' + value.number + '" class="input-text input-select ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-container="#error_dropdown_' + value.number + '"  data-parsley-error-message="選択してください" readonly required>';
                                } else {
                                    html += '<input type="text" id="dropdown_' + value.number + '" name="choice_text_' + value.number + '" class="input-text input-select ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-container="#error_dropdown_' + value.number + '"  data-parsley-error-message="選択してください" readonly>';
                                }
                                html += '<input type="hidden">';
                                html += '<div class="dropdown-menu" aria-labelledby="dropdown_' + value.number + '">';
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    if ( choice_index == 0 ) {
                                        html += '<button type="button" value="' + choice_value.number + '" class="btn dropdown-item fw-bold text-center">' + choice_value.text + '</button>';
                                    } else {
                                        html += '<button type="button" value="' + choice_value.number + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + choice_value.text + '</button>';
                                    }
                                });
                                html += '</div>';
                                html += '</div>';
                                html += '<div id="error_dropdown_' + value.number + '"></div>';
                            } else if ( value.choice_type == 5 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    if ( check_empty(choice_value.text) ) {
                                        html += '<p class="mb-0">' + choice_value.text + '</p>';
                                    }
                                    if ( value.required_flg ) {
                                        if ( choice_index == 0 ) {
                                            html += '<input type="text" name="date_' + value.number + '_' + choice_value.number + '" class="input-text input-date ps-2 mt-2" data-mindate=today required>';
                                        } else {
                                            html += '<input type="text" name="date_' + value.number + '_' + choice_value.number + '" class="input-text input-date ps-2 mt-2" data-mindate=today>';
                                        }
                                    } else {
                                        html += '<input type="text" name="date_' + value.number + '_' + choice_value.number + '" class="input-text input-date ps-2 mt-2" data-mindate=today>';
                                    }
                                });
                            } else if ( value.choice_type == 6 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    if ( check_empty(choice_value.text) ) {
                                        html += '<p class="mb-0">' + choice_value.text + '</p>';
                                    }
                                    if ( value.required_flg ) {
                                        if ( choice_index == 0 ) {
                                            html += '<input type="text" name="time_' + value.number + '_' + choice_value.number + '" class="input-text input-time ps-2 mt-2" data-mindate=today required>';
                                        } else {
                                            html += '<input type="text" name="time_' + value.number + '_' + choice_value.number + '" class="input-text input-time ps-2 mt-2" data-mindate=today>';
                                        }
                                    } else {
                                        html += '<input type="text" name="time_' + value.number + '_' + choice_value.number + '" class="input-text input-time ps-2 mt-2" data-mindate=today>';
                                    }
                                });
                            } else if ( value.choice_type == 7 ) {
                                $.each( value.choice, function( choice_index, choice_value ) {
                                    if ( check_empty(choice_value.text) ) {
                                        html += '<p class="mb-0">' + choice_value.text + '</p>';
                                    }
                                    if ( value.required_flg ) {
                                        if ( choice_index == 0 ) {
                                            html += '<input type="text" name="date_time_' + value.number + '_' + choice_value.number + '" class="input-text input-date-time ps-2 mt-2" data-mindate=today required>';
                                        } else {
                                            html += '<input type="text" name="date_time_' + value.number + '_' + choice_value.number + '" class="input-text input-date-time ps-2 mt-2" data-mindate=today>';
                                        }
                                    } else {
                                        html += '<input type="text" name="date_time_' + value.number + '_' + choice_value.number + '" class="input-text input-date-time ps-2 mt-2" data-mindate=today>';
                                    }
                                });
                            }
                            html += '<input type="hidden" name="choice_type_' + value.number + '" value="' + value.choice_type + '">';
                            html += '<input type="hidden" name="choice_count_' + value.number + '" value="' + value.choice.length + '">';
                        }
                        html += '</div>';
                        html += '</div>';
                        $( '#question_form' ).append(html);
                    });

                    var now = new Date();
                    var today = now.getFullYear() + '/' +  ( now.getMonth() + 1 ) + '/' + now.getDate() + ' 12:00'
                    flatpickr( '.input-date', {
                        "locale": "ja",
                        dateFormat : 'Y/m/d',
                    });
                    flatpickr( '.input-time', {
                        "locale": "ja",
                        enableTime : true,
                        noCalendar : true,
                        minuteIncrement : 15,
                        defaultDate : '12:00'
                    });
                    flatpickr( '.input-date-time', {
                        "locale": "ja",
                        enableTime : true,
                        minuteIncrement : 15,
                        defaultDate : today
                    });
                    flatpickr( '.input-birth-date', {
                        "locale": "ja",
                        dateFormat : 'Y/m/d',
                        defaultDate : '1992/01/01',
                    });

                    setTimeout( function() {
                        $( '.loader-area' ).css( 'opacity', '0' );
                        $( '.loader-area' ).addClass( 'd-none' );
                        $( '.question-area' ).removeClass( 'd-none' );
                    }, 750 );
                } else {
                    setTimeout( function() {
                        $( '.loader-area' ).css( 'opacity', '0' );
                        $( '.loader-area' ).addClass( 'd-none' );
                        $( '.check-area' ).removeClass( 'd-none' );
                    }, 750 );
                }
            }).fail( function(){
            
            });
        } else {
            var id = '';
            if ( check_empty($( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val()) ) {
                id = $( '.place-area .content-area .content-item-area .content-place-area [name=setting]:checked' ).val();
            } else if ( check_empty($( '[name=course_setting]' ).val()) ) {
                id = $( '[name=course_setting]' ).val();
            } else if ( check_empty($( '[name=date_setting]' ).val()) ) {
                id = $( '[name=date_setting]' ).val();
            }

            var form_data = new FormData();
            form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
            form_data.append( 'user_id', liff.getContext().userId );
            form_data.append( 'id', id );
            form_data.append( 'setting_id', $( '.date-area [name=select_setting]' ).next().val() );
            if ( check_empty($( '.course-area [name=course]:checked' ).val()) ) {
                form_data.append( 'course_id', $( '.course-area [name=course]:checked' ).val() );
            } else {
                form_data.append( 'course_id', '' );
            }

            form_data.append( 'year', $( '.button-area .reserve-button' ).val().substring( 0, $( '.button-area .reserve-button' ).val().indexOf('年') ) );
            form_data.append( 'month', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('年')+1, $( '.button-area .reserve-button' ).val().indexOf('月') ) );
            form_data.append( 'day', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf('月')+1, $( '.button-area .reserve-button' ).val().indexOf('日') ) );
            form_data.append( 'hour', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(')')+2, $( '.button-area .reserve-button' ).val().indexOf(':') ) );
            form_data.append( 'minute', $( '.button-area .reserve-button' ).val().substring( $( '.button-area .reserve-button' ).val().indexOf(':')+1, $( '.button-area .reserve-button' ).val().indexOf('～') ) );

            form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#save_temp_url' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                setTimeout( function() {
                    $( '.loader-area' ).css( 'opacity', '0' );
                    $( '.loader-area' ).addClass( 'd-none' );
                    $( '.check-area' ).removeClass( 'd-none' );
                }, 750 );
            }).fail( function(){
            
            });
        }
    });
});

function change_date(response) {
    $( '.date-area .content-area .date-year-text' ).text( response.year );
    $( '.date-area .content-area .date-year-text' ).next().val( response.year );
    $( '.date-area .content-area .date-week-text' ).text( response.start + '～' + response.end );
    $( '.date-area .content-area .date-week-text' ).next().val( response.start.substring(0, response.start.indexOf('月')) );
    $( '.date-area .content-area .date-week-text' ).next().next().val( response.start.substring(response.start.indexOf('月')+1, response.start.indexOf('日')) );

    $( '.date-area .content-area .prev-date-arrow' ).next().val( response.prev_year );
    $( '.date-area .content-area .prev-date-arrow' ).next().next().val( response.prev_month );
    $( '.date-area .content-area .prev-date-arrow' ).next().next().next().val( response.prev_day );
    $( '.date-area .content-area .next-date-arrow' ).next().val( response.next_year );
    $( '.date-area .content-area .next-date-arrow' ).next().next().val( response.next_month );
    $( '.date-area .content-area .next-date-arrow' ).next().next().next().val( response.next_day );

    $( '.date-area .content-area .date-table tbody' ).empty();
    $.each( response.week_day, function( index, value ){
        $( '.date-area .content-area .date-table th .calendar-day-text' ).eq(index).text( value.day );
    });

    $( '.date-area .content-area' ).append( '<input type="hidden" name="date_setting" value="' + response.online_offline.display_id + '">' );
    $( '.date-area [name=select_setting]' ).val( response.setting.name );
    $( '.date-area [name=select_setting]' ).next().val( response.setting.display_id );
    $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).empty();
    $.each( response.setting_list, function( index, value ) {
        if ( index == 0 ) {
            $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).append( '<button type="button" value="' + value.display_id + '" class="btn dropdown-item fw-bold text-center">' + value.name + '</button>' );
        } else {
            $( '.date-area [name=select_setting]' ).parent().find( '.dropdown-menu' ).append( '<button type="button" value="' + value.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + value.name + '</button>' );
        }
    });

    if ( response.week_schedule.length > 0 ) {
        $.each( response.week_schedule, function( schedule_index, schedule_value ){
            $( '.date-area .content-area .date-table tbody' ).append( '<tr></tr>' );

            var html = '<td class="p-1">' + schedule_value.time + '</td>';
            $.each( schedule_value.week, function( week_index, week_value ){
                var date = new Date(week_value.year, week_value.month - 1, week_value.day, Number(schedule_value.time.substr( 0, schedule_value.time.indexOf( ':' ) )), Number(schedule_value.time.substr( schedule_value.time.indexOf( ':' ) + 1 )), 0);
                var start_date = new Date(Number(response.start_date.year), Number(response.start_date.month) - 1, Number(response.start_date.day), Number(response.start_date.hour), Number(response.start_date.minute), 0);
                if ( check_empty( response.end_date ) ) {
                    var end_date = new Date(response.end_date.year, response.end_date.month - 1, response.end_date.day, 0, 0, 0);
                    if ( date < start_date || date >= end_date ) {
                        html += '<td class="no p-1">';
                        html += '<span style="color: #000;">-</span>';
                        if ( week_index == 0 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 1 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 2 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 3 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 4 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 5 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 6 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        }
                        html += '</td>';
                    } else {
                        if ( week_value.reception_flg ) {
                            html += '<td class="no p-1">';
                            html += '<span>✕</span>';
                            if ( week_index == 0 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 1 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 2 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 3 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 4 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 5 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 6 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            }
                            html += '</td>';
                        } else {
                            html += '<td class="yes p-1">';
                            html += '<span>◎</span>';
                            if ( week_index == 0 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 1 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 2 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 3 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 4 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 5 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            } else if ( week_index == 6 ) {
                                html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                            }
                            html += '</td>';
                        }
                    }
                } else {
                    if ( week_value.reception_flg ) {
                        html += '<td class="no p-1">';
                        html += '<span>✕</span>';
                        if ( week_index == 0 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 1 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 2 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 3 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 4 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 5 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 6 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        }
                        html += '</td>';
                    } else {
                        html += '<td class="yes p-1">';
                        html += '<span>◎</span>';
                        if ( week_index == 0 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(月) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 1 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(火) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 2 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(水) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 3 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(木) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 4 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(金) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 5 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(土) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        } else if ( week_index == 6 ) {
                            html += '<input type=hidden value="' + week_value.year + '年' + week_value.month + '月' + week_value.day + '日(日) ' + schedule_value.time + '～' + schedule_value.add_time + '">';
                        }
                        html += '</td>';
                    }
                }
            });
            $( '.date-area .content-area .date-table tbody tr' ).eq(schedule_index).append(html);
        });
    }
    if ( response.question_flg ) {
        $( '.date-area .footer-area .footer-button' ).text( '設問へ' );
    } else {
        $( '.date-area .footer-area .footer-button' ).text( '予約内容確認へ' );
    }
    $( '.date-area' ).removeClass( 'd-none' );

    setTimeout( function() {
        $( '.date-area .content-area .date-loader-area' ).addClass( 'd-none' );
        $( '.date-area .content-area .date-content-area' ).removeClass( 'd-none' );
    }, 750 );
}