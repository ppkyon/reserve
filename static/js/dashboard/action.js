$( function() {
    $( document ).on( 'click', '.new-area .check-button', function () {
        $( '#check_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( document ).on( 'click', '#check_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#check_schedule_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#check_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#check_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'check' );

    $( document ).on( 'click', '.table tbody .dropdown-preview-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#edit_user_modal .modal-body' ).find( 'input[type=hidden]' ).eq(1).val( response.display_id );

            if ( check_empty( response.profile ) && check_empty( response.profile.image ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
                $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', $( '#env_media_url' ).val() + response.profile.image );
            } else {
                if ( check_empty( response.display_image ) ) {
                    $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', response.display_image );
                    $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', response.display_image );
                } else {
                    $( '#user_profile_offcanvas .offcanvas-header' ).find( 'img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                    $( '#edit_user_modal .modal-header' ).find( 'img' ).attr( 'src', $( '#env_static_url' ).val() + 'img/user-none.png' );
                }
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.title' ).text( response.profile.name );
                $( '#edit_user_modal .modal-header' ).find( '.title' ).text( response.profile.name );
            } else {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.title' ).text( response.display_name );
                $( '#edit_user_modal .modal-header' ).find( '.title' ).text( response.display_name );
            }

            if ( response.status == 2 ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( 'ブロック' );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( 'ブロック' );
            } else if ( check_empty( response.active_flow ) && check_empty( response.active_flow.tab ) ) {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( response.active_flow.tab.name );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( response.active_flow.tab.name );
            } else {
                $( '#user_profile_offcanvas .offcanvas-header' ).find( '.sub' ).text( '-' );
                $( '#edit_user_modal .modal-header' ).find( '.sub' ).text( '-' );
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                $( '#edit_user_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( response.profile.email );
            } else {
                $( '#edit_user_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( '' );
            }

            if ( check_empty( response.profile ) && check_empty( response.profile.memo ) ) {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( 'textarea' ).val( response.profile.memo );
                $( '#edit_user_modal .modal-body' ).find( 'textarea' ).val( response.profile.memo );
            } else {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( 'textarea' ).val( '' );
                $( '#edit_user_modal .modal-body' ).find( 'textarea' ).val( '' );
            }

            $( '#user_profile_offcanvas .offcanvas-body' ).find( 'input' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).val( response.display_date );
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.atelle_id ) ) {
                        $( this ).val( '#' + response.profile.atelle_id );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 6 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                        } else {
                            $( this ).val( '-' );
                        }
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 7 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 8 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                        $( this ).val( response.profile.email );
                    } else {
                        $( this ).val( '-' );
                    }
                }
            });

            $( '#edit_user_modal .modal-body' ).find( 'input[type=text]' ).each( function( index, value ) {
                if ( index == 0 ) {
                    $( this ).val( response.display_date );
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.atelle_id ) ) {
                        $( this ).val( '#' + response.profile.atelle_id );
                    } else {
                        $( this ).val( '-' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                        $( this ).next().val( response.profile.age );
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 6 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                            $( this ).next().val( response.profile.sex );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                            $( this ).next().val( response.profile.sex );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 7 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '' );
                    }
                }
            });

            $( '#user_profile_offcanvas .offcanvas-body' ).find( '.tag-area' ).empty();
            $( '#edit_user_modal .modal-body' ).find( '.tag-area .add-tag-area' ).empty();
            $.each( response.tag, function( index, value ) {
                $( '#user_profile_offcanvas .offcanvas-body' ).find( '.tag-area' ).append( '<label class="tag-label text-center p-1 me-1 mb-0">' + value.tag.name + '</label>' );
                $( '#edit_user_modal .modal-body' ).find( '.tag-area .add-tag-area' ).append( '<div class="position-relative"><label class="tag-label text-center p-1 me-1">' + value.tag.name + '</label><input type="hidden" name="tag[]" value="' + value.tag.display_id + '"><button type="button" value="" class="btn delete-tag-button p-0"><img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg"></button></div>' );
            });

            $( target ).next().trigger( 'click' );
            down_modal();
        }).fail( function(){
            
        });
    });
    $( '#user_profile_offcanvas .offcanvas-header .edit-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
    });

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

    $( document ).on( 'click', '.table tbody .dropdown-menu .member-button', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( check_empty( response.profile ) && check_empty( response.profile.email ) ) {
                $( '#member_user_check_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( response.profile.email );
            } else {
                $( '#member_user_check_modal .modal-body' ).find( 'input[type=email]' ).eq(0).val( '' );
            }
            $( '#member_user_check_modal .modal-body' ).find( 'input[type=text]' ).each( function( index, value ) {
                if ( index == 0 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name ) ) {
                        $( this ).val( response.profile.name );
                    } else {
                        $( this ).val( response.display_name );
                    }
                } else if ( index == 1 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.name_kana ) ) {
                        $( this ).val( response.profile.name_kana );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 2 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.birth ) ) {
                        $( this ).val( response.profile.display_birth );
                    } else {
                        $( this ).val( '' );
                    }
                } else if ( index == 3 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.age ) && response.profile.age != 0 ) {
                        $( this ).val( response.profile.age + '歳' );
                        $( this ).next().val( response.profile.age );
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 4 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.sex ) ) {
                        if ( response.profile.sex == '1' ) {
                            $( this ).val( '男性' );
                            $( this ).next().val( response.profile.sex );
                        } else if ( response.profile.sex == '2' ) {
                            $( this ).val( '女性' );
                            $( this ).next().val( response.profile.sex );
                        } else {
                            $( this ).val( '' );
                            $( this ).next().val( '' );
                        }
                    } else {
                        $( this ).val( '' );
                        $( this ).next().val( '' );
                    }
                } else if ( index == 5 ) {
                    if ( check_empty( response.profile ) && check_empty( response.profile.phone_number ) ) {
                        $( this ).val( response.profile.phone_number );
                    } else {
                        $( this ).val( '' );
                    }
                }
            });

            $( '#member_user_check_modal .yes-button' ).val( $( target ).val() );
            $( target ).next().trigger( 'click' );
        }).fail( function(){
            
        });
    });
    $( document ).on( 'click', '#member_user_check_modal .yes-button', function () {
        $( this ).parents( '.modal' ).find( '.content-area' ).css( 'opacity', 0 );
        $( this ).parents( '.modal' ).find( '.loader-area' ).css( 'opacity', 1 );
        $( this ).prop( 'disabled', true );

        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        form_data.append( 'name', $( '#member_user_check_modal [name=name]' ).val() );
        form_data.append( 'name_kana', $( '#member_user_check_modal [name=name_kana]' ).val() );
        form_data.append( 'birth', $( '#member_user_check_modal [name=birth]' ).val().replace( '年', '-' ).replace( '月', '-' ).replace( '日', '' ) );
        form_data.append( 'age', $( '#member_user_check_modal [name=age]' ).next().val() );
        form_data.append( 'sex', $( '#member_user_check_modal [name=sex]' ).next().val() );
        form_data.append( 'phone_number', $( '#member_user_check_modal [name=phone_number]' ).val() );
        form_data.append( 'email', $( '#member_user_check_modal [name=email]' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_member_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '#member_user_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().trigger( 'click' );
                up_modal();
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '#member_user_check_modal .no-button' ).trigger( 'click' );
                $( target ).next().next().trigger( 'click' );
                up_modal();
            }, 750 );
        });
    });
    action_reload( 'member_user' );
});