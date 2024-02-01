$( function() {
    $( '#add_shop_modal .modal-footer .action-button' ).on( 'click', function( index, value ) {
        if ( $( '#add_shop_form' ).parsley().validate() ) {
            $( this ).parents( '.modal-content' ).find( '.modal-header button' ).trigger( 'click' );
            $( this ).next().trigger( 'click' );
        }
    });
    $( '#add_shop_check_modal .modal-body .yes-button' ).on( 'click', function( index, value ) {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'email', $( '#add_shop_form [name=email]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#add_shop_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#add_shop_check_modal .modal-body .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#add_shop_check_modal .modal-body .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'add_shop' );

    $( '#offcanvas_shop_profile .offcanvas-header .edit-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '.table tbody .preview-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_profile_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( check_empty(response.shop.profile) ) {
                if ( check_empty(response.shop.profile.shop_logo_image) ) {
                    $( '#offcanvas_shop_profile .offcanvas-header img' ).attr( 'src', $( '#env_media_url' ).val() + response.shop.profile.shop_logo_image );
                    $( '#edit_shop_modal .modal-header img' ).attr( 'src', $( '#env_media_url' ).val() + response.shop.profile.shop_logo_image );
                } else {
                    $( '#offcanvas_shop_profile .offcanvas-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                    $( '#edit_shop_modal .modal-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                }
                if ( check_empty(response.shop.profile.shop_name) ) {
                    $( '#offcanvas_shop_profile .offcanvas-header .title' ).text( response.shop.profile.shop_name );
                    $( '#edit_shop_modal .modal-header .title' ).text( response.shop.profile.shop_name );
                } else {
                    $( '#offcanvas_shop_profile .offcanvas-header .title' ).text( '-' );
                    $( '#edit_shop_modal .modal-header .title' ).text( '-' );
                }
                if ( check_empty(response.shop.profile.memo) ) {
                    $( '#offcanvas_shop_profile .offcanvas-body textarea' ).val( response.shop.profile.memo );
                    $( '#edit_shop_modal .modal-body textarea' ).val( response.shop.profile.memo );
                } else {
                    $( '#offcanvas_shop_profile .offcanvas-body textarea' ).val( '' );
                    $( '#edit_shop_modal .modal-body textarea' ).val( '' );
                }

                $( '#offcanvas_shop_profile .offcanvas-body input' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).val( response.shop.display_date );
                    } else if ( index == 1 ) {
                        if ( check_empty(response.shop.display_id) ) {
                            $( this ).val( '#' + response.shop.display_id );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 2 ) {
                        if ( check_empty(response.shop.profile.shop_name) ) {
                            $( this ).val( response.shop.profile.shop_name );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 3 ) {
                        if ( check_empty(response.shop.profile.head_family_name) && check_empty(response.shop.profile.head_first_name) ) {
                            $( this ).val( response.shop.profile.head_family_name + response.shop.profile.head_first_name );
                        } else if ( check_empty(response.shop.profile.head_family_name) ) {
                            $( this ).val( response.shop.profile.head_family_name );
                        } else if ( check_empty(response.shop.profile.head_first_name) ) {
                            $( this ).val( response.shop.profile.head_first_name );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 4 ) {
                        if ( check_empty(response.shop.profile.head_family_name_kana) && check_empty(response.shop.profile.head_first_name_kana) ) {
                            $( this ).val( response.shop.profile.head_family_name_kana + response.shop.profile.head_first_name_kana );
                        } else if ( check_empty(response.shop.profile.head_family_name_kana) ) {
                            $( this ).val( response.shop.profile.head_family_name_kana );
                        } else if ( check_empty(response.shop.profile.head_first_name_kana) ) {
                            $( this ).val( response.shop.profile.head_first_name_kana );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 5 ) {
                        if ( check_empty(response.shop.profile.shop_postcode) ) {
                            $( this ).val( String(response.shop.profile.shop_postcode).substring( 0, 3 ) + '-' + String(response.shop.profile.shop_postcode).substring( 3, 7 ) );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 6 ) {
                        if ( check_empty(response.shop.prefecture) || check_empty(response.shop.prefecture.name) ) {
                            $( this ).val( response.shop.prefecture.name );
                            $( this ).next().val( response.shop.prefecture.value );
                        } else {
                            $( this ).val( '-' );
                            $( this ).next().val( '' );
                        }
                    } else if ( index == 7 ) {
                        if ( check_empty(response.shop.profile.shop_address) ) {
                            $( this ).val( response.shop.profile.shop_address );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 8 ) {
                        if ( check_empty(response.shop.phone_number) ) {
                            $( this ).val( response.shop.phone_number );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 9 ) {
                        if ( check_empty(response.shop.profile.head_email) ) {
                            $( this ).val( response.shop.profile.head_email );
                        } else {
                            $( this ).val( '-' );
                        }
                    }
                });
                $( '#edit_shop_modal .modal-body input[type=text]' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).val( response.shop.display_date );
                    } else if ( index == 1 ) {
                        if ( check_empty(response.shop.display_id) ) {
                            $( this ).val( '#' + response.shop.display_id );
                            $( '#save_shop_form [name=id]' ).val( response.shop.display_id );
                        } else {
                            $( this ).val( '' );
                            $( '#save_shop_form [name=id]' ).val( '' );
                        }
                    } else if ( index == 2 ) {
                        if ( check_empty(response.shop.profile.shop_name) ) {
                            $( this ).val( response.shop.profile.shop_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 3 ) {
                        if ( check_empty(response.shop.profile.head_family_name) ) {
                            $( this ).val( response.shop.profile.head_family_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 4 ) {
                        if ( check_empty(response.shop.profile.head_first_name) ) {
                            $( this ).val( response.shop.profile.head_first_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 5 ) {
                        if ( check_empty(response.shop.profile.head_family_name_kana) ) {
                            $( this ).val( response.shop.profile.head_family_name_kana );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 6 ) {
                        if ( check_empty(response.shop.profile.head_first_name_kana) ) {
                            $( this ).val( response.shop.profile.head_first_name_kana );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 7 ) {
                        if ( check_empty(response.shop.profile.shop_postcode) ) {
                            $( this ).val( String(response.shop.profile.shop_postcode).substring( 0, 3 ) + '-' + String(response.shop.profile.shop_postcode).substring( 3, 7 ) );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 8 ) {
                        if ( check_empty(response.shop.prefecture) || check_empty(response.shop.prefecture.name) ) {
                            $( this ).val( response.shop.prefecture.name );
                            $( this ).next().val( response.shop.prefecture.value );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else if ( index == 9 ) {
                        if ( check_empty(response.shop.profile.shop_address) ) {
                            $( this ).val( response.shop.profile.shop_address );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 10 ) {
                        if ( check_empty(response.shop.phone_number) ) {
                            $( this ).val( response.shop.phone_number );
                        } else {
                            $( this ).val( '' );
                        }
                    }
                });
                if ( check_empty(response.shop.profile.head_email) ) {
                    $( '#edit_shop_modal .modal-body input[type=email]' ).eq(0).val( response.shop.profile.head_email );
                } else {
                    $( '#edit_shop_modal .modal-body input[type=email]' ).eq(0).val( '' );
                }
            } else {
                $( '#offcanvas_shop_profile .offcanvas-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                $( '#offcanvas_shop_profile .offcanvas-header .title' ).text( '-' );

                $( '#offcanvas_shop_profile .offcanvas-body input' ).each( function( index, value ) {
                    $( this ).val( '-' );
                });
                $( '#edit_shop_modal .modal-body input[type=text]' ).each( function( index, value ) {
                    $( this ).val( '' );
                });
                $( '#edit_shop_modal .modal-body input[type=email]' ).eq(0).val( '' );
            }

            $( '#offcanvas_shop_profile .offcanvas-body .tag-area' ).empty();
            $( '#edit_shop_modal #save_shop_form .tag-area .add-tag-area' ).empty();
            $.each( response.shop.tag, function( index, value ) {
                var html = '<div class="position-relative">';
                html += '<label class="tag-label text-center p-1 me-1">' + value.name + '</label>';
                html += '<input type="hidden" name="tag[]" value="' + value.display_id + '">';
                html += '<button type="button" value="" class="btn delete-tag-button p-0">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                html += '</button>';
                html += '</div>';
                $( '#offcanvas_shop_profile .offcanvas-body .tag-area' ).append( '<label class="tag-label text-center p-1 me-1 mb-0">' + value.name + '</label>' );
                $( '#edit_shop_modal #save_shop_form .tag-area .add-tag-area' ).append( html );
            });

            $( target ).next().trigger( 'click' );
            down_modal();
        }).fail( function(){
            
        });
    });

    $( document ).on( 'keyup', '#edit_shop_modal #save_shop_form [name=shop_postcode]', function () {
        AjaxZip3.zip2addr( 'shop_postcode', '', 'shop_prefecture', 'shop_address' );
    });
    
    $( '#edit_shop_modal .modal-body .add-tag-button-area .add-tag-button' ).on( 'click', function() {
        var target = $( this );
        var form_data = new FormData();
        $.ajax({
            'data': form_data,
            'url': $( '#get_company_tag_all_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#company_tag_modal .genre-table tbody' ).empty();
            if ( response.genre_list.length > 0 ) {
                $.each( response.genre_list, function( index, value ) {
                    $( '#company_tag_modal .genre-table tbody' ).append( append_genre_modal(index, value) );
                });
            }

            $( '#company_tag_modal .tag-table tbody' ).empty();
            if ( response.tag_list.length > 0 ) {
                $.each( response.tag_list, function( index, value ) {
                    $( '#company_tag_modal .tag-table tbody' ).append( append_tag_modal(index, value, $( '#edit_shop_modal .modal-body .add-tag-area input' ) ) );
                });
            }

            $( target ).next().trigger( 'click' );
            up_modal();
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#edit_shop_modal .modal-body .add-tag-area .delete-tag-button', function () {
        $( this ).parent().remove();
    });
    $( document ).on( 'click', '#company_tag_modal .table-area tbody button', function () {
        var html = '<div class="position-relative">';
        html += '<label class="tag-label text-center p-1 me-1">' + $( this ).next().val() + '</label>';
        html += '<input type="hidden" name="tag[]" value="' + $( this ).val() + '">';
        html += '<button type="button" value="" class="btn delete-tag-button p-0">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
        html += '</button>';
        html += '</div>';
        $( '#edit_shop_modal #save_shop_form .tag-area .add-tag-area' ).append( html );
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
});