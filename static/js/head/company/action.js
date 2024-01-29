$( function() {
    $( '#add_company_modal .modal-footer .action-button' ).on( 'click', function( index, value ) {
        if ( $( '#add_company_form' ).parsley().validate() ) {
            $( this ).parents( '.modal-content' ).find( '.modal-header button' ).trigger( 'click' );
            $( this ).next().trigger( 'click' );
        }
    });
    $( '#add_company_check_modal .modal-body .yes-button' ).on( 'click', function( index, value ) {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );
        
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'email', $( '#add_company_form [name=email]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#add_company_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#add_company_check_modal .modal-body .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#add_company_check_modal .modal-body .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'add_company' );

    $( '#offcanvas_company_profile .offcanvas-header .edit-button' ).on( 'click', function() {
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
            if ( check_empty(response.company.profile) ) {
                if ( check_empty(response.company.profile.company_logo_image) ) {
                    $( '#offcanvas_company_profile .offcanvas-header img' ).attr( 'src', $( '#env_media_url' ).val() + response.company.profile.company_logo_image );
                    $( '#edit_company_modal .modal-header img' ).attr( 'src', $( '#env_media_url' ).val() + response.company.profile.company_logo_image );
                } else {
                    $( '#offcanvas_company_profile .offcanvas-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                    $( '#edit_company_modal .modal-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                }
                if ( check_empty(response.company.profile.company_name) ) {
                    $( '#offcanvas_company_profile .offcanvas-header .title' ).text( response.company.profile.company_name );
                    $( '#edit_company_modal .modal-header .title' ).text( response.company.profile.company_name );
                } else {
                    $( '#offcanvas_company_profile .offcanvas-header .title' ).text( '-' );
                    $( '#edit_company_modal .modal-header .title' ).text( '-' );
                }
                if ( check_empty(response.company.profile.memo) ) {
                    $( '#offcanvas_company_profile .offcanvas-body textarea' ).val( response.company.profile.memo );
                    $( '#edit_company_modal .modal-body textarea' ).val( response.company.profile.memo );
                } else {
                    $( '#offcanvas_company_profile .offcanvas-body textarea' ).val( '' );
                    $( '#edit_company_modal .modal-body textarea' ).val( '' );
                }
                
                $( '#offcanvas_company_profile .offcanvas-body input' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).val( response.company.display_date );
                    } else if ( index == 1 ) {
                        if ( check_empty(response.company.display_id) ) {
                            $( this ).val( '#' + response.company.display_id );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 2 ) {
                        if ( check_empty(response.company.profile.company_name) ) {
                            $( this ).val( response.company.profile.company_name );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 3 ) {
                        if ( check_empty(response.company.profile.head_family_name) && check_empty(response.company.profile.head_first_name) ) {
                            $( this ).val( response.company.profile.head_family_name + response.company.profile.head_first_name );
                        } else if ( check_empty(response.company.profile.head_family_name) ) {
                            $( this ).val( response.company.profile.head_family_name );
                        } else if ( check_empty(response.company.profile.head_first_name) ) {
                            $( this ).val( response.company.profile.head_first_name );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 4 ) {
                        if ( check_empty(response.company.profile.head_family_name_kana) && check_empty(response.company.profile.head_first_name_kana) ) {
                            $( this ).val( response.company.profile.head_family_name_kana + response.company.profile.head_first_name_kana );
                        } else if ( check_empty(response.company.profile.head_family_name_kana) ) {
                            $( this ).val( response.company.profile.head_family_name_kana );
                        } else if ( check_empty(response.company.profile.head_first_name_kana) ) {
                            $( this ).val( response.company.profile.head_first_name_kana );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 5 ) {
                        if ( check_empty(response.company.profile.company_postcode) ) {
                            $( this ).val( String(response.company.profile.company_postcode).substring( 0, 3 ) + '-' + String(response.company.profile.company_postcode).substring( 3, 7 ) );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 6 ) {
                        if ( check_empty(response.company.prefecture) || check_empty(response.company.prefecture.name) ) {
                            $( this ).val( response.company.prefecture.name );
                            $( this ).next().val( response.company.prefecture.value );
                        } else {
                            $( this ).val( '-' );
                            $( this ).next().val( '' );
                        }
                    } else if ( index == 7 ) {
                        if ( check_empty(response.company.profile.company_address) ) {
                            $( this ).val( response.company.profile.company_address );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 8 ) {
                        if ( check_empty(response.company.phone_number) ) {
                            $( this ).val( response.company.phone_number );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else if ( index == 9 ) {
                        if ( check_empty(response.company.profile.head_email) ) {
                            $( this ).val( response.company.profile.head_email );
                        } else {
                            $( this ).val( '-' );
                        }
                    }
                });
                $( '#edit_company_modal .modal-body input[type=text]' ).each( function( index, value ) {
                    if ( index == 0 ) {
                        $( this ).val( response.company.display_date );
                    } else if ( index == 1 ) {
                        if ( check_empty(response.company.display_id) ) {
                            $( this ).val( '#' + response.company.display_id );
                            $( '#save_company_form [name=id]' ).val( response.company.display_id );
                        } else {
                            $( this ).val( '' );
                            $( '#save_company_form [name=id]' ).val( '' );
                        }
                    } else if ( index == 2 ) {
                        if ( check_empty(response.company.profile.company_name) ) {
                            $( this ).val( response.company.profile.company_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 3 ) {
                        if ( check_empty(response.company.profile.head_family_name) ) {
                            $( this ).val( response.company.profile.head_family_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 4 ) {
                        if ( check_empty(response.company.profile.head_first_name) ) {
                            $( this ).val( response.company.profile.head_first_name );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 5 ) {
                        if ( check_empty(response.company.profile.head_family_name_kana) ) {
                            $( this ).val( response.company.profile.head_family_name_kana );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 6 ) {
                        if ( check_empty(response.company.profile.head_first_name_kana) ) {
                            $( this ).val( response.company.profile.head_first_name_kana );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 7 ) {
                        if ( check_empty(response.company.profile.company_postcode) ) {
                            $( this ).val( String(response.company.profile.company_postcode).substring( 0, 3 ) + '-' + String(response.company.profile.company_postcode).substring( 3, 7 ) );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 8 ) {
                        if ( check_empty(response.company.prefecture) || check_empty(response.company.prefecture.name) ) {
                            $( this ).val( response.company.prefecture.name );
                            $( this ).next().val( response.company.prefecture.value );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else if ( index == 9 ) {
                        if ( check_empty(response.company.profile.company_address) ) {
                            $( this ).val( response.company.profile.company_address );
                        } else {
                            $( this ).val( '' );
                        }
                    } else if ( index == 10 ) {
                        if ( check_empty(response.company.phone_number) ) {
                            $( this ).val( response.company.phone_number );
                        } else {
                            $( this ).val( '' );
                        }
                    }
                });
                if ( check_empty(response.company.profile.head_email) ) {
                    $( '#edit_company_modal .modal-body input[type=email]' ).eq(0).val( response.company.profile.head_email );
                } else {
                    $( '#edit_company_modal .modal-body input[type=email]' ).eq(0).val( '' );
                }
            } else {
                $( '#offcanvas_company_profile .offcanvas-header img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                $( '#offcanvas_company_profile .offcanvas-header .title' ).text( '-' );

                $( '#offcanvas_company_profile .offcanvas-body input' ).each( function( index, value ) {
                    $( this ).val( '-' );
                });
                $( '#edit_company_modal .modal-body input[type=text]' ).each( function( index, value ) {
                    $( this ).val( '' );
                });
                $( '#edit_company_modal .modal-body input[type=email]' ).eq(0).val( '' );
            }

            $( '#offcanvas_company_profile .offcanvas-body .tag-area' ).empty();
            $( '#edit_company_modal #save_company_form .tag-area .add-tag-area' ).empty();
            $.each( response.company.tag, function( index, value ) {
                var html = '<div class="position-relative">';
                html += '<label class="tag-label text-center p-1 me-1">' + value.name + '</label>';
                html += '<input type="hidden" name="tag[]" value="' + value.display_id + '">';
                html += '<button type="button" value="" class="btn delete-tag-button p-0">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                html += '</button>';
                html += '</div>';
                $( '#offcanvas_company_profile .offcanvas-body .tag-area' ).append( '<label class="tag-label text-center p-1 me-1 mb-0">' + value.name + '</label>' );
                $( '#edit_company_modal #save_company_form .tag-area .add-tag-area' ).append( html );
            });

            $( target ).next().trigger( 'click' );
            down_modal();
        }).fail( function(){
            
        });
    });

    $( document ).on( 'keyup', '#edit_company_modal #save_company_form [name=company_postcode]', function () {
        AjaxZip3.zip2addr( 'company_postcode', '', 'company_prefecture', 'company_address' );
    });
    $( '#edit_company_modal .modal-body .add-tag-button-area .add-tag-button' ).on( 'click', function() {
        var target = $( this );
        var form_data = new FormData();
        $.ajax({
            'data': form_data,
            'url': $( '#get_head_tag_all_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#head_tag_modal .genre-table tbody' ).empty();
            if ( response.genre_list.length > 0 ) {
                $.each( response.genre_list, function( index, value ) {
                    $( '#head_tag_modal .genre-table tbody' ).append( append_genre_modal(index, value) );
                });
            }

            $( '#head_tag_modal .tag-table tbody' ).empty();
            if ( response.tag_list.length > 0 ) {
                $.each( response.tag_list, function( index, value ) {
                    $( '#head_tag_modal .tag-table tbody' ).append( append_tag_modal(index, value, $( '#edit_company_modal .modal-body .add-tag-area input' ) ) );
                });
            }

            $( target ).next().trigger( 'click' );
            up_modal();
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#edit_company_modal .modal-body .add-tag-area .delete-tag-button', function () {
        $( this ).parent().remove();
    });
    $( document ).on( 'click', '#head_tag_modal .table-area tbody button', function () {
        var html = '<div class="position-relative">';
        html += '<label class="tag-label text-center p-1 me-1">' + $( this ).next().val() + '</label>';
        html += '<input type="hidden" name="tag[]" value="' + $( this ).val() + '">';
        html += '<button type="button" value="" class="btn delete-tag-button p-0">';
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
        html += '</button>';
        html += '</div>';
        $( '#edit_company_modal #save_company_form .tag-area .add-tag-area' ).append( html );
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
});