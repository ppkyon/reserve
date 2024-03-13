var now_textarea_node = null;
var now_textarea_offset = null;
var old_textarea_node = null;
var old_textarea_offset = null;
var old_textarea_number = null;

$( function() {
    create_preview();

    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview( $( this ).find( '[name=id]' ).val() );
    });

    $( document ).on( 'click', '#save_text_form .input-template-dropdown .dropdown-menu button', function () {
        if ( $( this ).val() == '0' ) {
            open_template_text_modal( $( this).next(), $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '1' ) {
            open_template_video_modal( $( this).next(), $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '2' ) {
            open_template_richmessage_modal( $( this).next(), $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '3' ) {
            open_template_richvideo_modal( $( this).next(), $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        } else if ( $( this ).val() == '4' ) {
            open_template_cardtype_modal( $( this).next(), $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        }
    });
    $( document ).on( 'click', '#company_template_text_modal .table-area tbody button', function () {
        var target = $( this );
        var id = $( this ).next().val();
        $( 'form .input-area [name=number]' ).each( function( index, value ) {
            var number = $( this ).val();
            if ( $( target ).val() == number ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                $( message_area ).find( '.text-area' ).addClass( 'd-none' );
                $( message_area ).find( '.image-area' ).addClass( 'd-none' );
                $( message_area ).find( '.video-area' ).addClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).removeClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).empty();

                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '4' );
                $( this ).parents( '.input-area' ).find( '.action-area .menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var form_data = new FormData();
                form_data.append( 'id', id );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_template_text_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<div class="chart-content-area mt-2 ms-2">';
                    html += '<div class="chart-title-area d-flex justify-content-start align-items-center">';
                    html += '<p class="chart-content-title p-1 ps-2 mb-0" style="background-color: #EF0000;">メッセージ</p>';
                    html += '<button type="button" class="btn delete-button ms-auto p-0" value="' + number + '">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                    html += '</button>';
                    html += '</div>';
                    html += '<input type="hidden" name="template_' + number + '" value="' + response.display_id + '">';
                    html += '<input type="hidden" name="template_type_' + number + '" value="0">';
                    html += '<a href="/company/template/text/edit/?id=' + response.display_id + '" target="_blank">';
                    html += '<div class="chart-content position-relative mb-0">';
                    html += '<p class="chart-sub-title p-1 ps-2 mb-0" style="background-color: #FF0202;">' + response.name + '</p>';
                    html += '<div class="d-flex justify-content-start align-items-center">';
                    $.each( response.item, function( index, value ) {
                        if ( index == 0 ) {
                            if ( value.message_type == 0 ) {
                                html += '<img src="' + $( '#env_static_url' ).val() + 'img/image-none.png" class="chart-content-img p-2 ms-2">';
                                html += '<div class="chart-content-text p-1 mb-0">' + display_textarea_replace(value.text) + '</div>';
                            } else if ( value.message_type == 1 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.image + '" class="chart-content-img p-2 ms-2">';
                                html += '<p class="chart-content-text p-1 mb-0">画像メッセージ</p>';
                            } else if ( value.message_type == 2 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.video_thumbnail + '" class="chart-content-img p-2 ms-2">';
                                html += '<p class="chart-content-text p-1 mb-0">動画メッセージ</p>';
                            }
                        }
                    });
                    html += '</div>';
                    html += '</div>';
                    html += '</a>';
                    html += '</div>';
                    $( message_area ).find( '.chart-area' ).append( html );
                    create_preview();
                }).fail( function(){
                    
                });
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#company_template_video_modal .table-area tbody button', function () {
        var target = $( this );
        var id = $( this ).next().val();
        $( 'form .input-area [name=number]' ).each( function( index, value ) {
            var number = $( this ).val();
            if ( $( target ).val() == number ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                $( message_area ).find( '.text-area' ).addClass( 'd-none' );
                $( message_area ).find( '.image-area' ).addClass( 'd-none' );
                $( message_area ).find( '.video-area' ).addClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).removeClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).empty();

                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '4' );
                $( this ).parents( '.input-area' ).find( '.action-area .menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var form_data = new FormData();
                form_data.append( 'id', id );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_template_video_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<div class="chart-content-area mt-2 ms-2">';
                    html += '<div class="chart-title-area d-flex justify-content-start align-items-center">';
                    html += '<p class="chart-content-title p-1 ps-2 mb-0" style="background-color: #FCA000;">動画</p>';
                    html += '<button type="button" class="btn delete-button ms-auto p-0" value="' + number + '">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                    html += '</button>';
                    html += '</div>';
                    html += '<input type="hidden" name="template_' + number + '" value="' + response.display_id + '">';
                    html += '<input type="hidden" name="template_type_' + number + '" value="1">';
                    html += '<a href="/company/template/video/edit/?id=' + response.display_id + '" target="_blank">';
                    html += '<div class="chart-content position-relative mb-0">';
                    html += '<p class="chart-sub-title p-1 ps-2 mb-0" style="background-color: #FCA000;">' + response.name + '</p>';
                    html += '<div class="d-flex justify-content-start align-items-center">';
                    html += '<img src="' + $( '#env_media_url' ).val() + response.video_thumbnail + '" class="chart-content-img p-2 ms-2">';
                    html += '<p class="chart-content-img-text p-2 mb-0">' + response.video_display_time + '</p>';
                    html += '</div>';
                    html += '</div>';
                    html += '</a>';
                    html += '</div>';
                    $( message_area ).find( '.chart-area' ).append( html );
                    create_preview();
                }).fail( function(){
                    
                });
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#company_template_richmessage_modal .table-area tbody button', function () {
        var target = $( this );
        var id = $( this ).next().val();
        $( 'form .input-area [name=number]' ).each( function( index, value ) {
            var number = $( this ).val();
            if ( $( target ).val() == number ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                $( message_area ).find( '.text-area' ).addClass( 'd-none' );
                $( message_area ).find( '.image-area' ).addClass( 'd-none' );
                $( message_area ).find( '.video-area' ).addClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).removeClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).empty();

                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '4' );
                $( this ).parents( '.input-area' ).find( '.action-area .menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var form_data = new FormData();
                form_data.append( 'id', id );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_template_richmessage_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<div class="chart-content-area mt-2 ms-2">';
                    html += '<div class="chart-title-area d-flex justify-content-start align-items-center">';
                    html += '<p class="chart-content-title p-1 ps-2 mb-0" style="background-color: #009E9F;">リッチメッセージ</p>';
                    html += '<button type="button" class="btn delete-button ms-auto p-0" value="' + number + '">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                    html += '</button>';
                    html += '</div>';
                    html += '<input type="hidden" name="template_' + number + '" value="' + response.display_id + '">';
                    html += '<input type="hidden" name="template_type_' + number + '" value="2">';
                    html += '<a href="/company/template/richmessage/edit/?id=' + response.display_id + '" target="_blank">';
                    html += '<div class="chart-content position-relative mb-0">';
                    html += '<p class="chart-sub-title p-1 ps-2 mb-0" style="background-color: #009E9F;">' + response.name + '</p>';
                    html += '<div class="d-flex justify-content-start align-items-center">';
                    html += '<img src="' + $( '#env_media_url' ).val() + response.image + '" class="chart-content-img p-2 ms-2">';
                    html += '<div>';
                    $.each( response.item, function( index, value ) {
                        if ( index < 3 ) {
                            if ( check_empty(value.url) ) {
                                html += '<p class="content-title mb-0" style="color: #000;">' + value.url + '</p>';
                            }
                        }
                    });
                    html += '</div>';
                    html += '</div>';
                    html += '</div>';
                    html += '</a>';
                    html += '</div>';
                    $( message_area ).find( '.chart-area' ).append( html );
                    create_preview();
                }).fail( function(){
                    
                });
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#company_template_richvideo_modal .table-area tbody button', function () {
        var target = $( this );
        var id = $( this ).next().val();
        $( 'form .input-area [name=number]' ).each( function( index, value ) {
            var number = $( this ).val();
            if ( $( target ).val() == number ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                $( message_area ).find( '.text-area' ).addClass( 'd-none' );
                $( message_area ).find( '.image-area' ).addClass( 'd-none' );
                $( message_area ).find( '.video-area' ).addClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).removeClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).empty();

                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '4' );
                $( this ).parents( '.input-area' ).find( '.action-area .menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var form_data = new FormData();
                form_data.append( 'id', id );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_template_richvideo_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<div class="chart-content-area mt-2 ms-2">';
                    html += '<div class="chart-title-area d-flex justify-content-start align-items-center">';
                    html += '<p class="chart-content-title p-1 ps-2 mb-0" style="background-color: #009825;">リッチビデオメッセージ</p>';
                    html += '<button type="button" class="btn delete-button ms-auto p-0" value="' + number + '">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                    html += '</button>';
                    html += '</div>';
                    html += '<input type="hidden" name="template_' + number + '" value="' + response.display_id + '">';
                    html += '<input type="hidden" name="template_type_' + number + '" value="3">';
                    html += '<a href="/company/template/richvideo/edit/?id=' + response.display_id + '" target="_blank">';
                    html += '<div class="chart-content position-relative mb-0">';
                    html += '<p class="chart-sub-title p-1 ps-2 mb-0" style="background-color: #009825;">' + response.name + '</p>';
                    html += '<div class="d-flex justify-content-start align-items-center">';
                    html += '<img src="' + $( '#env_media_url' ).val() + response.video_thumbnail + '" class="chart-content-img p-2 ms-2">';
                    html += '<p class="chart-content-img-text p-2 mb-0">' + response.video_display_time + '</p>';
                    html += '</div>';
                    html += '</div>';
                    html += '</a>';
                    html += '</div>';
                    $( message_area ).find( '.chart-area' ).append( html );
                    create_preview();
                }).fail( function(){
                    
                });
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#company_template_cardtype_modal .table-area tbody button', function () {
        var target = $( this );
        var id = $( this ).next().val();
        $( 'form .input-area [name=number]' ).each( function( index, value ) {
            var number = $( this ).val();
            if ( $( target ).val() == number ) {
                var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
                $( message_area ).find( '.text-area' ).addClass( 'd-none' );
                $( message_area ).find( '.image-area' ).addClass( 'd-none' );
                $( message_area ).find( '.video-area' ).addClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).removeClass( 'd-none' );
                $( message_area ).find( '.chart-area' ).empty();

                $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '4' );
                $( this ).parents( '.input-area' ).find( '.action-area .menu-area button' ).each( function( index, value ) {
                    if ( !$( this ).hasClass( 'd-none' ) ) {
                        $( this ).prop( 'disabled', true );
                    }
                });

                var form_data = new FormData();
                form_data.append( 'id', id );
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_template_cardtype_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<div class="chart-content-area mt-2 ms-2">';
                    html += '<div class="chart-title-area d-flex justify-content-start align-items-center">';
                    html += '<p class="chart-content-title p-1 ps-2 mb-0" style="background-color: #A1007E;">カードタイプメッセージ</p>';
                    html += '<button type="button" class="btn delete-button ms-auto p-0" value="' + number + '">';
                    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                    html += '</button>';
                    html += '</div>';
                    html += '<input type="hidden" name="template_' + number + '" value="' + response.display_id + '">';
                    html += '<input type="hidden" name="template_type_' + number + '" value="4">';
                    html += '<a href="/company/template/cardtype/edit/?id=' + response.display_id + '" target="_blank">';
                    html += '<div class="chart-content position-relative mb-0">';
                    html += '<p class="chart-sub-title p-1 ps-2 mb-0" style="background-color: #A1007E;">' + response.name + '</p>';
                    html += '<div class="d-flex justify-content-start align-items-center">';
                    if ( response.type == 1 ) {
                        $.each( response.item, function( index, value ) {
                            if ( index == 0 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.image_1 + '" class="chart-content-img p-2 ms-2">';
                            }
                        });
                        html += '<p class="chart-content-img-text p-2 mb-0">アナウンス</p>';
                    } else if ( response.type == 2 ) {
                        $.each( response.item, function( index, value ) {
                            if ( index == 0 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.image_1 + '" class="chart-content-img p-2 ms-2">';
                            }
                        });
                        html += '<p class="chart-content-img-text p-2 mb-0">ロケーション</p>';
                    } else if ( response.type == 3 ) {
                        $.each( response.item, function( index, value ) {
                            if ( index == 0 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.image + '" class="chart-content-img p-2 ms-2">';
                            }
                        });
                        html += '<p class="chart-content-img-text p-2 mb-0">パーソン</p>';
                    } else if ( response.type == 4 ) {
                        $.each( response.item, function( index, value ) {
                            if ( index == 0 ) {
                                html += '<img src="' + $( '#env_media_url' ).val() + value.image + '" class="chart-content-img p-2 ms-2">';
                            }
                        });
                        html += '<p class="chart-content-img-text p-2 mb-0">イメージ</p>';
                    }
                    html += '</div>';
                    html += '</div>';
                    html += '</a>';
                    html += '</div>';
                    $( message_area ).find( '.chart-area' ).append( html );
                    create_preview();
                }).fail( function(){
                    
                });
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '.chart-area .delete-button', function () {
        var action_area = $( this ).parents( '.input-area' ).find( '.action-area' );
        var message_area = $( this ).parents( '.input-area' ).find( '.message-area' );
        $( message_area ).find( '.text-area' ).removeClass( 'd-none' );
        $( message_area ).find( '.image-area' ).addClass( 'd-none' );
        $( message_area ).find( '.video-area' ).addClass( 'd-none' );
        $( message_area ).find( '.chart-area' ).addClass( 'd-none' );
        $( message_area ).find( '.chart-area' ).empty();

        $( message_area ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '0' );
        $( action_area ).find( '.menu-area button' ).each( function( index, value ) {
            $( this ).prop( 'disabled', false );
        });
    });

    $( document ).on( 'click', '#save_text_form .action-button-area .name-button', function () {
        var image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/display-name.png" class="ms-1 me-1">';
        input_textarea_image( $( this ), image );
        create_preview();
    });

    $( document ).on( 'click', '#save_text_form .input-action-dropdown .dropdown-menu button', function () {
        var image = '';
        if ( $( this ).val() == 'line' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/line-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'company' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/company-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'name' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-name.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'phone' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/manager-phone.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'date' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/reserve-date.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'address' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/offline-address.png" class="ms-1 me-1">';
        } else if ( $( this ).val() == 'url' ) {
            image = '<img src="' + $( '#env_static_url' ).val() + 'img/textarea/online-url.png" class="ms-1 me-1">';
        }
        input_textarea_image( $( this ), image );
        create_preview();
    });

    $( document ).on( 'click', '#save_text_form .action-button-area .image-button', function () {
        $( '#image_upload_modal .image-drop-zone [name=number]' ).val( $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#save_text_form .image-area .delete-button', function () {
        $( this ).parents( '.input-area' ).find( '.message-area .text-area' ).removeClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .chart-area' ).addClass( 'd-none' );

        $( this ).parents( '.input-area' ).find( '.message-area' ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '1' );
        $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
            $( this ).prop( 'disabled', false );
        });
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).empty();
        create_preview();
    });

    $( document ).on( 'click', '#save_text_form .action-button-area .video-button', function () {
        $( '#video_upload_modal .video-drop-zone [name=number]' ).val( $( this ).parents( '.input-area' ).find( '[name=number]' ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#save_text_form .video-area .delete-button', function () {
        $( this ).parents( '.input-area' ).find( '.message-area .text-area' ).removeClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .image-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).addClass( 'd-none' );
        $( this ).parents( '.input-area' ).find( '.message-area .chart-area' ).addClass( 'd-none' );

        $( this ).parents( '.input-area' ).find( '.message-area' ).find( '[name=message_type_' + $( this ).val() + ']' ).val( '1' );
        $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
            $( this ).prop( 'disabled', false );
        });
        $( this ).parents( '.input-area' ).find( '.message-area .video-area' ).empty();
        create_preview();
    });

    $( document ).on( 'click', '#save_text_form .action-button-area .delete-button', function () {
        $( '#delete_item_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( '#delete_item_check_modal .yes-button' ).on( 'click', function() {
        var target = $( this );
        $( '#save_text_form [name=number]' ).each( function( index, value ) {
            if ( Number($( this ).val()) == Number($( target ).val()) ) {
                $( this ).parents( '.input-area' ).remove();
            } else if ( Number($( this ).val()) > Number($( target ).val()) ) {
                var old_number =  Number( $( this ).val() );
                var new_number =  old_number - 1;
                $( this ).val( new_number );
                $( this ).parents( '.input-area' ).find( '.delete-area button' ).val( new_number );
                $( this ).parents( '.input-area' ).find( '[name=message_type_' + old_number + ']' ).attr( 'name', 'message_type_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=text_' + old_number + ']' ).attr( 'name', 'text_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=upload_image_' + old_number + ']' ).attr( 'name', 'upload_image_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=upload_video_' + old_number + ']' ).attr( 'name', 'upload_video_' + new_number );
                $( this ).parents( '.input-area' ).find( '[name=template_' + old_number + ']' ).attr( 'name', 'template_' + new_number );
            }
        });
        $( '#delete_item_check_modal .no-button' ).trigger( 'click' );
        create_preview();
    });

    $( '.button-area .add-area button' ).on( 'click', function() {
        $( '#save_text_form .input-area-wrap' ).append( append_input_area() );
    });

    $( document ).on( 'mouseup keyup', '#save_text_form .false-textarea', function () {
        var selection = window.getSelection();
        now_textarea_node = selection.focusNode;
        now_textarea_offset = selection.focusOffset;

        if ( check_empty($( this ).html().replaceAll( '<img', '>img' ).replaceAll(/<("[^"]*"|'[^']*'|[^'">])*>/g,'').replaceAll( '>img', '<img' )) ) {
            $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                if ( !$( this ).hasClass( 'name-button' ) && !$( this ).parents( '.dropdown' ).hasClass( 'input-action-dropdown' ) && !$( this ).hasClass( 'd-none' ) ) {
                    $( this ).prop( 'disabled', true );
                }
            });
        } else {
            $( this ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
                $( this ).prop( 'disabled', false );
            });
        }
        create_preview();
    });
    $( document ).on( 'focusout', '#save_text_form .false-textarea', function () {
        old_textarea_number = Number($( this ).parents( '.input-area' ).find( '[name=number]' ).val());
        old_textarea_node = now_textarea_node;
        old_textarea_offset = now_textarea_offset;
        now_textarea_node = null;
        now_textarea_offset = null;
    });
});

function input_textarea_image( target, image ) {
    var textarea = $( target ).parents( '.input-area' ).find( '.false-textarea' );
    if ( now_textarea_node == null && now_textarea_offset == null ) {
        if ( Number($( target ).parents( '.input-area' ).find( '[name=number]' ).val()) == old_textarea_number ) {
            if ( $( old_textarea_node ).text() == " " ) {
                $( textarea ).html( $( textarea ).html().replace( '&nbsp;', image + '<br>' ) );
            } else if ( $( old_textarea_node ).html() == "<br>" ) {
                $( old_textarea_node ).html( image );
            } else {
                var before = $( old_textarea_node ).text().substr( 0, old_textarea_offset );
                var after = $( old_textarea_node ).text().substr( old_textarea_offset );
                $( textarea ).html( $( textarea ).html().replace( $( old_textarea_node ).text(), before + image + after ) );
            }
        } else {
            $( textarea ).html( $( textarea ).html() + image );
        }
    } else {
        var before = $( now_textarea_node ).text().substr( 0, now_textarea_offset );
        var after = $( now_textarea_node ).text().substr( now_textarea_offset );
        $( textarea ).html( $( textarea ).html().replace( $( now_textarea_node ).text(), before + image + after ) );
    }

    $( target ).parents( '.input-area' ).find( '.menu-area button' ).each( function( index, value ) {
        if ( !$( this ).hasClass( 'name-button' ) && !$( this ).parents( '.dropdown' ).hasClass( 'input-action-dropdown' ) && !$( this ).hasClass( 'd-none' ) ) {
            $( this ).prop( 'disabled', true );
        }
    });
    old_textarea_node = null;
    old_textarea_offset = null;
    old_textarea_number = null;
}