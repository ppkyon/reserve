$( function() {
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        create_list_preview($( this ).find( '[name=id]' ).val());
    });

    $( document ).on( 'click', '#save_cardtype_form .cardtype-button-area .arrow-button', function () {
        var type = $( this ).val();
        $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
            if ( $( this ).find( 'a' ).hasClass( 'active' ) ) {
                if ( type == 'prev' ) {
                    if ( $( this ).prev().find( 'a' ).attr( 'href' ) != undefined ) {
                        $( '.nav-tabs a[href="' + $( this ).prev().find( 'a' ).attr( 'href' ) + '"]' ).tab( 'show' );
                        return false;
                    }
                } else if ( type == 'next' ) {
                    if ( $( this ).next().find( 'a' ).attr( 'href' ) != undefined ) {
                        $( '.nav-tabs a[href="' + $( this ).next().find( 'a' ).attr( 'href' ) + '"]' ).tab( 'show' );
                        return false;
                    }
                }
            }
        });
    });

    $( document ).on( 'change', '#save_cardtype_form .display-area .display-check', function () {
        var target = $( this );
        if ( $( this ).prop( 'checked' ) ) {
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', '' ) ).removeClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'label_' ) ).removeClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'title_' ) ).parent().removeClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'text_' ) ).parent().removeClass( 'd-none' );
            $( this ).parents( '.content-area' ).find( '.content-input-area input' ).prop( 'disabled', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area input' ).each( function() {
                if ( $( target ).attr( 'id' ).indexOf( 'color' ) == -1 ) {
                    $( this ).prop( 'required', true );
                }
            });
            $( this ).parents( '.content-area' ).find( '.content-input-area textarea' ).prop( 'disabled', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area textarea' ).prop( 'required', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area .color-area button' ).prop( 'disabled', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area .color-area button' ).prop( 'required', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area .dropdown button' ).prop( 'disabled', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area .dropdown input' ).css( 'background-color', '#fff' );
            if ( $( this ).attr( 'id' ).indexOf( 'action' ) !== -1 ) {
                if ( !$( this ).parents( '.content-area' ).hasClass( 'content-action-area' ) ) {
                    $( this ).parents( '.content-area' ).next().find( 'input' ).prop( 'disabled', false );
                    $( this ).parents( '.content-area' ).next().find( 'input' ).prop( 'required', true );
                    $( this ).parents( '.content-area' ).next().find( 'input' ).css( 'background-color', '#fff' );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).prop( 'disabled', false );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).prop( 'required', true );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).css( 'background-color', '#fff' );
                }
            } else if ( $( this ).attr( 'id' ).indexOf( 'plus' ) !== -1 ) {
                $( this ).parents( '.content-area' ).find( 'input [type=text]' ).prop( 'disabled', false );
                $( this ).parents( '.content-area' ).find( 'input [type=text]' ).prop( 'required', true );
                $( this ).parents( '.content-area' ).find( 'input' ).css( 'background-color', '#fff' );
            } else if ( $( this ).attr( 'id' ).indexOf( 'label' ) !== -1 ) {
                if ( $( '#' + $( this ).attr( 'id' ).replace( 'label_', 'image_' ) ).length > 0 ) {
                    if ( $( '#' + $( this ).attr( 'id' ).replace( 'label_', 'image_' ) ).prop( 'checked' ) ) {
                        $( '#' + $( this ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                            if ( $( this ).hasClass( 'three' ) ) {
                                $( this ).css( 'padding-bottom', '3.75rem' );
                            } else {
                                $( this ).css( 'padding-bottom', '7.5rem' );
                            }
                        });
                    } else {
                        $( '#' + $( this ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                            if ( $( '#' + $( target ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).next().hasClass( 'd-none' ) ) {
                                $( this ).css( 'padding-bottom', '0' );
                            } else {
                                if ( $( '#' + $( target ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).length == 3 ) {
                                    $( this ).css( 'padding-bottom', '1rem' );
                                } else {
                                    $( this ).css( 'padding-bottom', '2rem' );
                                }
                            }
                        });
                    }
                }
            } else if ( $( this ).attr( 'id' ).indexOf( 'image' ) !== -1 ) {
                $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'area_' ) ).find( 'span' ).each( function( index, value ) {
                    $( this ).removeClass( 'd-none' );
                });
                $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                    if ( $( this ).hasClass( 'three' ) ) {
                        $( this ).css( 'padding-bottom', '3.75rem' );
                    } else {
                        $( this ).css( 'padding-bottom', '7.5rem' );
                    }
                });
                $( this ).parents( '.content-area' ).find( '.upload-image-area' ).each( function( index, value ) {
                    $( this ).css( 'background-color', 'background-color: rgb(255, 255, 255);' );
                    $( this ).find( 'a' ).prop( 'disabled', false );
                });
            }
        } else {
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', '' ) ).addClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'label_' ) ).addClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'title_' ) ).parent().addClass( 'd-none' );
            $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'text_' ) ).parent().addClass( 'd-none' );
            $( this ).parents( '.content-area' ).find( '.content-input-area input' ).prop( 'disabled', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area input' ).each( function() {
                if ( $( target ).attr( 'id' ).indexOf( 'color' ) == -1 ) {
                    $( this ).prop( 'required', false );
                }
            });
            $( this ).parents( '.content-area' ).find( '.content-input-area textarea' ).prop( 'disabled', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area textarea' ).prop( 'required', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area .color-area button' ).prop( 'disabled', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area .color-area button' ).prop( 'required', false );
            $( this ).parents( '.content-area' ).find( '.content-input-area .dropdown button' ).prop( 'disabled', true );
            $( this ).parents( '.content-area' ).find( '.content-input-area .dropdown input' ).css( 'background-color', 'rgba(239, 239, 239, 0.3)' );
            if ( $( this ).attr( 'id' ).indexOf( 'action' ) !== -1 ) {
                if ( !$( this ).parents( '.content-area' ).hasClass( 'content-action-area' ) ) {
                    $( this ).parents( '.content-area' ).next().find( 'input' ).prop( 'disabled', true );
                    $( this ).parents( '.content-area' ).next().find( 'input' ).prop( 'required', false );
                    $( this ).parents( '.content-area' ).next().find( 'input' ).css( 'background-color', 'rgba(239, 239, 239, 0.3)' );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).prop( 'disabled', true );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).prop( 'required', false );
                    $( this ).parents( '.content-area' ).next().find( 'textarea' ).css( 'background-color', 'rgba(239, 239, 239, 0.3)' );
                }
            } else if ( $( this ).attr( 'id' ).indexOf( 'plus' ) !== -1 ) {
                $( this ).parents( '.content-area' ).find( 'input [type=text]' ).prop( 'disabled', true );
                $( this ).parents( '.content-area' ).find( 'input [type=text]' ).prop( 'required', false );
                $( this ).parents( '.content-area' ).find( 'input' ).css( 'background-color', 'rgba(239, 239, 239, 0.3)' );
            } else if ( $( this ).attr( 'id' ).indexOf( 'label' ) !== -1 ) {
                if ( $( '#' + $( this ).attr( 'id' ).replace( 'label_', 'image_' ) ).length > 0 ) {
                    if ( $( '#' + $( this ).attr( 'id' ).replace( 'label_', 'image_' ) ).prop( 'checked' ) ) {
                        $( '#' + $( this ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                            if ( $( this ).hasClass( 'three' ) ) {
                                $( this ).css( 'padding-bottom', '3.75rem' );
                            } else {
                                $( this ).css( 'padding-bottom', '7.5rem' );
                            }
                        });
                    } else {
                        $( '#' + $( this ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                            if ( $( '#' + $( target ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).next().hasClass( 'd-none' ) ) {
                                $( this ).css( 'padding-bottom', '0' );
                            } else {
                                if ( $( '#' + $( target ).attr( 'id' ).replace( 'label_check_', 'image_area_' ) ).find( '.cardtype-image-item' ).length == 3 ) {
                                    $( this ).css( 'padding-bottom', '1rem' );
                                } else {
                                    $( this ).css( 'padding-bottom', '2rem' );
                                }
                            }
                        });
                    }
                }
            } else if ( $( this ).attr( 'id' ).indexOf( 'image' ) !== -1 ) {
                $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'area_' ) ).find( 'span' ).each( function( index, value ) {
                    $( this ).addClass( 'd-none' );
                });
                $( '#' + $( this ).attr( 'id' ).replace( 'check_', 'area_' ) ).find( '.cardtype-image-item' ).each( function( index, value ) {
                    if ( $( '#' + $( target ).attr( 'id' ).replace( 'check_', 'area_' ) ).next().hasClass( 'd-none' ) ) {
                        $( this ).css( 'padding-bottom', '0' );
                    } else {
                        if ( $( '#' + $( target ).attr( 'id' ).replace( 'check_', 'area_' ) ).find( '.cardtype-image-item' ).length == 3 ) {
                            $( this ).css( 'padding-bottom', '1rem' );
                        } else {
                            $( this ).css( 'padding-bottom', '2rem' );
                        }
                    }
                });
                $( this ).parents( '.content-area' ).find( '.upload-image-area' ).each( function( index, value ) {
                    $( this ).css( 'background-color', 'background-color: rgba(239, 239, 239, 0.3);' );
                    $( this ).find( 'a' ).prop( 'disabled', true );
                });
            }
        }
    });

    $( document ).on( 'keyup', '#save_cardtype_form .display-area .display-input', function () {
        if ( $( this ).attr( 'name' ).indexOf( 'price' ) !== -1 ) {
            if ( $( this ).val() == '' ) {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).text( '￥' + $( this ).attr( 'placeholder' ) );
            } else {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).text( '￥' + $( this ).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') );
            }
        } else if ( $( this ).attr( 'name' ).indexOf( 'place' ) !== -1 ) {
            $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).empty();
            $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<img src="' + $( '#env_static_url' ).val() + 'img/icon/map.png" class="me-1">' );
            $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<span>' + $( this ).val() + '</span>' );
        } else if ( $( this ).attr( 'name' ).indexOf( 'plus' ) !== -1 ) {
            $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).empty();
            if ( $( this ).parent().prev().find( 'input' ).val() == '時間' ) {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<img src="' + $( '#env_static_url' ).val() + 'img/icon/time.png" class="me-1">' );
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<span>' + $( this ).val() + '</span>' );
            } else if ( $( this ).parent().prev().find( 'input' ).val() == '価格' ) {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<img src="' + $( '#env_static_url' ).val() + 'img/icon/coin.png" class="me-1">' );
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).append( '<span>' + $( this ).val().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') + '</span>' );
            }
        } else if ( $( this ).attr( 'name' ).indexOf( 'text_title' ) !== -1 ) {
            if ( $( this ).val() == '' ) {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).text( $( this ).attr( 'placeholder' ) );
            } else {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).html( $( this ).val() );
            }
        } else {
            if ( $( this ).val() == '' ) {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).text( $( this ).attr( 'placeholder' ) );
            } else {
                $( '#display_' + $( this ).attr( 'name' ).replace( 'input_', '' ) ).html( $( this ).val().replace(/\r?\n/g, '<br>') );
            }
        }
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .color-area button', function () {
        var target = $( this );
        $( this ).parents( '.color-area' ).prev().val( $( this ).val() );
        $( '#display_' + $( this ).parents( '.color-area' ).attr( 'id' ).replace( 'color_', '' ).replace( '_area', '' ) ).css( 'color', $( this ).css( 'color' ) );
        $( '#display_' + $( this ).parents( '.color-area' ).attr( 'id' ).replace( 'color_', '' ).replace( '_area', '' ) ).css( 'background-color', $( this ).css( 'background-color' ) );
        if ( $( this ).css( 'color' ) == 'rgb(255, 255, 255)' ) {
            $( '#display_' + $( this ).parents( '.color-area' ).attr( 'id' ).replace( 'color_', '' ).replace( '_area', '' ) ).css( 'border', 'none' );
        } else {
            $( '#display_' + $( this ).parents( '.color-area' ).attr( 'id' ).replace( 'color_', '' ).replace( '_area', '' ) ).css( 'border', $( this ).css( 'border' ) );
        }
        $( this ).parents( '.color-area' ).find( 'button' ).each( function( index, value ){
            $( this ).empty();
            if ( $( target ).val() == $( this ).val() ) {
                $( this ).append( '<i class="bx bx-check"></i>' );
            } else {
                $( this ).append( '<span>A</span>' );
            }
        });
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .display-image-count button', function () {
        var number = $( this ).parents( '.row' ).prev().prev().val();
        var target = $( this );
        $( this ).parents( '.content-input-area' ).find( '.upload-area .upload-image-area' ).each( function( index, value ) {
            if ( index < Number( $( target ).val() ) ) {
                $( this ).removeClass( 'd-none' );
            } else {
                $( this ).addClass( 'd-none' );
            }
            $( this ).find( 'a' ).remove();
            $( this ).find( 'img' ).remove();
            $( this ).find( 'button' ).remove();
            $( this ).append( '<a><span>' + $( this ).find( 'input' ).val().toUpperCase() + '</span></a>' );
        });

        $( '#save_cardtype_form [name=image_a_' + number + ']' ).val( '' );
        $( '#save_cardtype_form [name=image_b_' + number + ']' ).val( '' );
        $( '#save_cardtype_form [name=image_c_' + number + ']' ).val( '' );
        $( '#display_image_area_' + number ).empty();
        if ( $( this ).val() == '1' ) {
            var html = '<div class="one cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            html += '<input type="hidden" value="a">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png\' );"></span>';
            html += '</div>';
            $( '#display_image_area_' + number ).append( html );
            $( '#save_cardtype_form [name=image_a_' + number + ']' ).prop( 'required', true );
            $( '#save_cardtype_form [name=image_b_' + number + ']' ).prop( 'required', false );
            $( '#save_cardtype_form [name=image_c_' + number + ']' ).prop( 'required', false );
        } else if ( $( this ).val() == '2' ) {
            var html = '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            html += '<input type="hidden" value="a">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png\' );"></span>';
            html += '</div>';
            html += '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            html += '<input type="hidden" value="b">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png\' );"></span>';
            html += '</div>';
            $( '#display_image_area_' + number ).append( html );
            $( '#save_cardtype_form [name=image_a_' + number + ']' ).prop( 'required', true );
            $( '#save_cardtype_form [name=image_b_' + number + ']' ).prop( 'required', true );
            $( '#save_cardtype_form [name=image_c_' + number + ']' ).prop( 'required', false );
        } else if ( $( this ).val() == '3' ) {
            var html = '<div class="two cardtype-image-item position-relative" style="padding-bottom: 7.5rem;">';
            html += '<input type="hidden" value="a">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png\' );"></span>';
            html += '</div>';
            html += '<div class="two flex-column position-relative">';
            html += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            html += '<input type="hidden" value="b">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png\' );"></span>';
            html += '</div>';
            html += '<div class="three cardtype-image-item position-relative" style="padding-bottom: 3.75rem;">';
            html += '<input type="hidden" value="c">';
            html += '<span style="background-image: url( \'' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png\' );"></span>';
            html += '</div>';
            html += '</div>';
            $( '#display_image_area_' + number ).append( html );
            $( '#save_cardtype_form [name=image_a_' + number + ']' ).prop( 'required', true );
            $( '#save_cardtype_form [name=image_b_' + number + ']' ).prop( 'required', true );
            $( '#save_cardtype_form [name=image_c_' + number + ']' ).prop( 'required', true );
        }
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .display-plus button', function () {
        var number = $( this ).parents( '.row' ).prev().prev().val();
        $( '#display_plus_' + number ).find( 'img' ).remove();
        if ( $( this ).val() == '1' ) {
            $( '#display_plus_' + number ).prepend( '<img src="' + $( '#env_static_url' ).val() + 'img/icon/time.png" class="me-1">' );
        } else if ( $( this ).val() == '2' ) {
            $( '#display_plus_' + number ).prepend( '<img src="' + $( '#env_static_url' ).val() + 'img/icon/coin.png" class="me-1">' );
        }
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .select-button-dropdown .dropdown-menu button', function () {
        if ( $( this ).val() == 'action' ) {
            var num = $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).attr( 'id' ).replace( 'display_action_button_type_', '' );
            $( '#display_action_label_' + num ).css( 'color', '#fff' );
            if ( $( '#display_action_text_color_' + num ).parent().children( 'label' ).length > 0 ) {
                $( '#display_action_label_' + num ).css( 'background-color', $( '#display_action_text_color_' + num ).parent().children( 'label' ).css( 'background-color' ) );
            } else {
                $( '#display_action_label_' + num ).css( 'background-color', '#fff' );
            }
        } else if ( $( this ).val() == 'text' ) {
            var num = $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).attr( 'id' ).replace( 'display_action_button_type_', '' );
            if ( $( '#display_action_text_color_' + num ).parent().children( 'label' ).length > 0 ) {
                $( '#display_action_label_' + num ).css( 'color', $( '#display_action_text_color_' + num ).parent().children( 'label' ).css( 'background-color' ) );
            } else {
                $( '#display_action_label_' + num ).css( 'color', '#5b82db' );
            }
            $( '#display_action_label_' + num ).css( 'background-color', '#fff' );
        }
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .display-color-select button', function () {
        var number = $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).attr( 'id' ).replace( 'display_action_text_color_', '');
        if ( $( '#display_action_button_type_' + number ).next().val() == 'action' ) {
            $( '#display_action_label_' + number ).css( 'color', '#fff' );
            $( '#display_action_label_' + number ).css( 'background-color', $( this ).find( 'label' ).css( 'background-color' ) );
        } else if ( $( '#display_action_button_type_' + number ).next().val() == 'text' ) {
            $( '#display_action_label_' + number ).css( 'color', $( this ).find( 'label' ).css( 'background-color' ) );
            $( '#display_action_label_' + number ).css( 'background-color', '#fff' );
        }
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .select-text-dropdown .dropdown-menu button', function () {
        var target = $( this ).parents( '.dropdown' ).prev().prev();
        var num = $( target ).attr( 'name' ).replace( 'text_text_', '' );
        if ( $( this ).val() == 'free' ) {
            $( target ).prev().prev().find( 'input' ).val( '' );
            $( target ).val( '' );
            $( target ).attr( 'readonly', false );
            $( target ).attr( 'disabled', false );
            $( target ).attr( 'riqured', true );
            $( '#display_text_title_' + num ).text( 'タイトル' );
            $( '#display_text_text_' + num ).text( 'テキスト' );
        } else {
            $( target ).prev().prev().find( 'input' ).val( $( this ).text() );
            $( target ).val( '※' + $( this ).text() + 'が自動で入力されます' );
            $( target ).attr( 'readonly', true );
            $( target ).attr( 'disabled', true );
            $( target ).attr( 'riqured', false );
            $( '#display_text_title_' + num ).text( $( this ).text() );
            $( '#display_text_text_' + num ).text( '【' + $( this ).text() + '】' );
        }
        $( this ).parents( '.dropdown' ).prev().val( $( this ).val() );
    });
    
    $( document ).on( 'click', '#save_cardtype_form .display-area .display-action-type button', function () {
        var number = $( this ).parent().prev().prev().attr( 'id' ).replace( 'display_action_type_', '');
        var width = $( this ).parents( '.dropdown' ).css( 'width' );
        $( this ).parents( '.content-input-area' ).children().each( function( index, value ) {
            if ( ( $( this ).attr( 'type' ) == 'text' || $( this ).attr( 'type' ) == 'url' ) && $( this ).attr( 'name' ).indexOf( 'action_url' ) !== -1 ) {
                $( this ).remove();
            }
        });
        $( this ).parents( '.content-input-area' ).children( 'textarea' ).remove();
        $( this ).parents( '.content-input-area' ).children( 'div.error-message' ).remove();
        $( this ).parents( '.content-input-area' ).children( 'i' ).remove();
        if ( check_empty($( this ).val()) ) {
            var width = $( this ).parents( '.dropdown' ).css( 'width' );
            if ( $( this ).val() == '4' ) {
                var html = '<input type="text" name="action_url_' + number + '" value="【予約フォーム】" class="input-text input-select ps-2 pe-2 mb-1" style="width: ' + width + ';" placeholder="URLを入力" data-parsley-errors-container="#error_action_url_' + number + '" readonly disabled>';
                html += '<input type="hidden">';
                html += '<div id="error_action_url_' + number + '" class="error-message"></div>';
                $( this ).parents( '.content-input-area' ).append( html );
            } else if ( $( this ).val() == '5' ) {
                var html = '<input type="text" name="action_url_' + number + '" value="【予約履歴ページ】" class="input-text input-select ps-2 pe-2 mb-1" style="width: ' + width + ';" placeholder="URLを入力" data-parsley-errors-container="#error_action_url_' + number + '" readonly disabled>';
                html += '<input type="hidden">';
                html += '<div id="error_action_url_' + number + '" class="error-message"></div>';
                $( this ).parents( '.content-input-area' ).append( html );
            } else if ( $( this ).val() == '6' ) {
                var html = '<input type="text" name="action_url_' + number + '" value="【オンラインURL】" class="input-text input-select ps-2 pe-2 mb-1" style="width: ' + width + ';" placeholder="URLを入力" data-parsley-errors-container="#error_action_url_' + number + '" readonly disabled>';
                html += '<input type="hidden">';
                html += '<div id="error_action_url_' + number + '" class="error-message"></div>';
                $( this ).parents( '.content-input-area' ).append( html );
            } else if ( $( this ).val() == '7' ) {
                var target = $( this );
                var form_data = new FormData();
                $.ajax({
                    'data': form_data,
                    'url': $( '#get_company_profile_url' ).val(),
                    'type': 'POST',
                    'dataType': 'json',
                    'processData': false,
                    'contentType': false,
                }).done( function( response ){
                    var html = '<input type="text" name="action_url_' + number + '" value="' + response.company.profile.company_url + '" class="input-text input-select ps-2 pe-2 mb-1" style="width: ' + width + ';" placeholder="URLを入力" data-parsley-errors-container="#error_action_url_' + number + '" readonly disabled>';
                    html += '<input type="hidden">';
                    html += '<div id="error_action_url_' + number + '" class="error-message"></div>';
                    $( target ).parents( '.content-input-area' ).append( html );
                }).fail( function(){

                });
            } else if ( $( this ).val() == '8' ) {
                var html = '<textarea name="action_text_' + number + '" class="display-text-input d-block input-textarea ms-0" style="width: ' + width + ';" placeholder="入力されたテキストが送信されます。" maxlength="30" data-parsley-errors-container="#error_action_text_' + number + '" required></textarea>';
                html += '<div id="error_action_text_' + number + '" class="error-message"></div>';
                $( this ).parents( '.content-input-area' ).append( html );
            } else {
                var html = '<input type="text" name="action_url_' + number + '" class="input-text input-select ps-2 pe-2 mb-1" style="width: ' + width + ';" placeholder="URLを入力" data-parsley-errors-container="#error_action_url_' + number + '" required>';
                html += '<input type="hidden">';
                html += '<div id="error_action_url_' + number + '" class="error-message"></div>';
                $( this ).parents( '.content-input-area' ).append( html );
            }
        }
        if ( $( this ).val() == '2' ) {
            open_template_video_modal( $( this ).parents( '.dropdown' ).next(), number );
        } else if ( $( this ).val() == '3' ) {
            open_question_modal( $( this ), number );
        }
    });
    $( document ).on( 'click', '#company_template_video_modal .table-area tbody button', function () {
        var target = $( this );
        $( 'form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).val( '【' + $( target ).next().next().val() + '】' );
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).next().val( $( target ).next().val() );
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).prop( 'disabled', true );
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    $( document ).on( 'click', '#company_question_modal .table-area tbody button', function () {
        var target = $( this );
        $( 'form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).val( '【' + $( target ).next().next().val() + '】' );
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).next().val( $( target ).next().val() );
                $( this ).find( '[name=action_url_' + $( target ).val() + ']' ).prop( 'disabled', true );
            }
        });
        $( this ).parents( '.modal-body' ).prev().find( 'button' ).trigger( 'click' );
    });
    
    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .add-text-button', function () {
        var tab = 0;
        $( '#save_cardtype_form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                tab = $( this ).attr( 'id' ).replace( 'tab', '' );
            }
        });
        var num = $( '#save_cardtype_form .tab-pane.active .display-area .content-text-area' ).length + 1;
        $( this ).parents( '.content-area' ).before( append_text_area( tab, num ) );
        var html = '';
        if ( num == 1 ) {
            html += '<div class="d-flex align-items-center mt-2">';
        } else {
            html += '<div class="d-flex align-items-center mt-1">';
        }
        html += '<p id="display_text_title_' + num + '_' + tab + '" class="price mb-0" style="font-size: 0.5rem;">タイトル</p>';
        html += '<p id="display_text_text_' + num + '_' + tab + '" class="price ms-auto mb-0" style="font-size: 0.5rem;">テキスト</p>';
        html += '</div>';
        $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-body-area' ).append( html );
    });
    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .delete-text-button', function () {
        $( '#delete_text_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#delete_text_check_modal .yes-button', function () {
        var tab = 0;
        $( '#save_cardtype_form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                tab = $( this ).attr( 'id' ).replace( 'tab', '' );
            }
        });
        var num = Number($( this ).val());
        $( '#save_cardtype_form .tab-pane.active .display-area .content-text-area' ).each( function( index, value ) {
            if ( index == num - 1 ) {
                $( this ).remove();
                $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-body-area div' ).eq(index).remove();
            } else if ( index > num - 1 ) {
                $( this ).find( '[name=text_check_' + ( index + 1 ) + '_' + tab + ']' ).prev().text( 'テキスト' + index );
                $( this ).find( '[name=text_check_' + ( index + 1 ) + '_' + tab + ']' ).prev().attr( 'for', 'display_text_check_' + index + '_' + tab );
                $( this ).find( '[name=text_check_' + ( index + 1 ) + '_' + tab + ']' ).next().attr( 'for', 'display_text_check_' + index + '_' + tab );
                $( this ).find( '[name=text_check_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'id', 'display_text_check_' + index + '_' + tab );
                $( this ).find( '[name=text_check_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'text_check_' + index + '_' + tab );
                $( this ).find( '[name=text_title_' + ( index + 1 ) + '_' + tab + ']' ).next().val( index );
                $( this ).find( '[name=text_title_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'text_title_' + index + '_' + tab );
                $( this ).find( '[name=text_text_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'text_text_' + index + '_' + tab );
                $( this ).find( '#select_text_' + ( index + 1 ) + '_' + tab ).next().attr( 'aria-labelledby', 'select_text_' + index + '_' + tab );
                $( this ).find( '#select_text_' + ( index + 1 ) + '_' + tab ).attr( 'id', 'select_text_' + index + '_' + tab );
                $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-body-area div' ).eq(index-1).find( 'p' ).eq(0).attr( 'id', 'display_text_title_' + index + '_' + tab );
                $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-body-area div' ).eq(index-1).find( 'p' ).eq(1).attr( 'id', 'display_text_text_' + index + '_' + tab );
            }
        });
        $( '#delete_text_check_modal .no-button' ).trigger( 'click' );
    });
    
    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .add-action-button', function () {
        var tab = 0;
        $( '#save_cardtype_form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                tab = $( this ).attr( 'id' ).replace( 'tab', '' );
            }
        });
        var num = $( '#save_cardtype_form .tab-pane.active .display-area .content-action-area' ).length + 1;
        $( this ).parents( '.content-area' ).before( append_action_area( tab, num ) );
        var html = '<button type="button" id="display_action_label_' + num + '_' + tab + '" class="btn p-0 mb-2">アクションラベルを入力</button>';
        $( '#save_cardtype_form .message-area .tab-pane.active .cardtype-area .cardtype-footer-area' ).append( html );
    });
    $( document ).on( 'click', '#save_cardtype_form .display-area .content-area .delete-action-button', function () {
        $( '#delete_action_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '#delete_action_check_modal .yes-button', function () {
        var tab = 0;
        $( '#save_cardtype_form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                tab = $( this ).attr( 'id' ).replace( 'tab', '' );
            }
        });
        var num = Number($( this ).val());
        $( '#save_cardtype_form .tab-pane.active .display-area .content-action-area' ).each( function( index, value ) {
            if ( index == num - 1 ) {
                $( this ).remove();
                $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-footer-area button' ).eq(index).remove();
            } else if ( index > num - 1 ) {
                $( this ).find( '[name=action_check_' + ( index + 1 ) + '_' + tab + ']' ).prev().text( 'アクション' + index );
                $( this ).find( '[name=action_check_' + ( index + 1 ) + '_' + tab + ']' ).prev().attr( 'for', 'display_action_check_' + index + '_' + tab );
                $( this ).find( '[name=action_check_' + ( index + 1 ) + '_' + tab + ']' ).next().attr( 'for', 'display_action_check_' + index + '_' + tab );
                $( this ).find( '[name=action_check_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'id', 'display_action_check_' + index + '_' + tab );
                $( this ).find( '[name=action_check_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_check_' + index + '_' + tab );
                $( this ).find( '[name=action_button_type_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'id', 'display_action_button_type_' + index + '_' + tab );
                $( this ).find( '[name=action_button_type_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_button_type_' + index + '_' + tab );
                $( this ).find( '[name=action_text_color_' + ( index + 1 ) + '_' + tab + ']' ).parents( '.dropdown' ).next().val( index );
                $( this ).find( '[name=action_text_color_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'id', 'display_action_text_color_' + index + '_' + tab );
                $( this ).find( '[name=action_text_color_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_text_color_' + index + '_' + tab );
                $( this ).find( '[name=action_label_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_label_' + index + '_' + tab );
                $( this ).find( '[name=action_type_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'id', 'display_action_type_' + index + '_' + tab );
                $( this ).find( '[name=action_type_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_type_' + index + '_' + tab );
                $( this ).find( '[name=action_text_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_text_' + index + '_' + tab );
                $( this ).find( '[name=action_url_' + ( index + 1 ) + '_' + tab + ']' ).attr( 'name', 'action_url_' + index + '_' + tab );
                $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-footer-area button' ).eq(index-1).attr( 'id', 'display_action_' + index + '_' + tab );
            }
        });
        $( '#delete_action_check_modal .no-button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '#save_cardtype_form .display-area .upload-area .upload-image-area button', function () {
        $( this ).parents( '.upload-image-area' ).find( 'a' ).remove();
        $( this ).parents( '.upload-image-area' ).find( 'img' ).remove();

        var number = $( this ).parents( '.row' ).prev().prev().val();
        var type = $( this ).parents( '.upload-image-area' ).find( 'input' ).val();
        if ( type == 'account' || type == 'image' || type == 'more' ) {
            $( this ).parents( '.upload-image-area' ).append( '<a><span>写真をアップロード</span></a>' );
        } else {
            if ( $( this ).parents( '.content-input-area' ).prev().find( 'input[type=checkbox]' ).length ) {
                if ( $( this ).parents( '.content-input-area' ).prev().find( 'input[type=checkbox]' ).prop( 'checked' ) ) {
                    $( this ).parents( '.upload-image-area' ).append( '<a><span>' + type.toUpperCase() + '</span></a>' );
                    $( this ).parents( '.upload-image-area' ).prev().prop( 'disabled', false );
                } else {
                    $( this ).parents( '.upload-image-area' ).append( '<a disabled><span>' + type.toUpperCase() + '</span></a>' );
                    $( this ).parents( '.upload-image-area' ).prev().prop( 'disabled', true );
                }
            } else {
                $( this ).parents( '.upload-image-area' ).append( '<a><span>' + type.toUpperCase() + '</span></a>' );
                $( this ).parents( '.upload-image-area' ).prev().prop( 'disabled', false );
            }
        }

        $( '#display_image_area_' + number + ' .cardtype-image-item' ).each( function( index, value ) {
            if ( $( this ).find( 'input' ).val() == type ) {
                if ( type == 'a' ) {
                    if ( Number($( this ).find( '[name=image_count_' + number + ']' ).val()) == 1 ) {
                        $( this ).find( '.cardtype-image-area .cardtype-image-item span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-a.png)' );
                    } else {
                        $( this ).find( 'span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-a.png)' );
                    }
                    $( '#save_cardtype_form [name=image_' + type + '_' + number + ']' ).val( '' );
                } else if ( type == 'b' ) {
                    if ( Number($( this ).find( '[name=image_count_' + number + ']' ).val()) == 2 ) {
                        $( this ).find( 'span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-b.png)' );
                    } else {
                        $( this ).find( 'span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-half-b.png)' );
                    }
                    $( '#save_cardtype_form [name=image_' + type + '_' + number + ']' ).val( '' );
                } else if ( type == 'c' ) {
                    $( this ).find( 'span' ).css( 'background-image', 'url' + $( '#env_static_url' ).val() + 'img/cardtype/cardtype-c.png)' );
                    $( '#save_cardtype_form [name=image_' + type + '_' + number + ']' ).val( '' );
                } else if ( type == 'account' ) {
                    $( this ).find( 'span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/person-default.png)' );
                    $( '#save_cardtype_form [name=image_' + number + ']' ).val( '' );
                } else if ( type == 'image' || type == 'more' ) {
                    $( this ).find( 'span' ).css( 'background-image', 'url(' + $( '#env_static_url' ).val() + 'img/cardtype/image-default.png)' );
                    $( '#save_cardtype_form [name=image_' + number + ']' ).val( '' );
                }
            }
        });
        $( this ).parents( '.upload-image-area' ).find( 'button' ).remove();
    });
    $( document ).on( 'click', '#save_cardtype_form .display-area .upload-area .upload-image-area a', function () {
        if ( !$( this ).parents( '.upload-image-area' ).prev().prop( 'disabled' ) ) {
            var button_number = 1;
            if ( $( this ).parents( '.content-input-area' ).find( '.dropdown input' ).val() == '2' ) {
                button_number = 2;
            } else if ( $( this ).parents( '.content-input-area' ).find( '.dropdown input' ).val() == '3' ) {
                if ( $( this ).parents( '.upload-image-area' ).find( 'input' ).val() == 'a' ) {
                    button_number = 2;
                }
            }
            $( this ).parents( '.upload-area' ).children( 'button' ).each( function( index, value ) {
                if ( index == ( button_number - 1 ) ) {
                    $( this ).trigger( 'click' );
                }
            });
            $( '.trimming-image-modal .upload-button' ).val( $( this ).parent().find( 'input' ).val() );
        }
    });
    $( '.trimming-image-modal .modal-body .drop-delete-button' ).on( 'click', function() {
        reset_trimming( this );
    });
    $( '.trimming-image-modal .upload-button' ).on( 'click', function() {
        var target = $( this );
        $( '#save_cardtype_form .tab-pane' ).each( function( index, value ) {
            if ( $( this ).hasClass( 'active' ) ) {
                var number = $( this ).attr( 'id' ).replace( 'tab', '' );
                $( this ).find( '.display-area .upload-area .upload-image-area' ).each( function( index, value ) {
                    var image_target = $( this );
                    if ( $( this ).find( 'input' ).val() == 'account' || $( this ).find( 'input' ).val() == 'image' ) {
                        $( target ).parents( '.modal' ).find( '.image-trimming-area' ).croppie( 'result', 'base64' ).then( function( base64 ) {
                            $( image_target ).find( 'a' ).remove();
                            $( image_target ).find( 'img' ).remove();
                            $( image_target ).prepend( '<img src="' + base64 + '" style="width: 100%; height: 100%;">' );
                            
                            var html = '<button type="button" class="btn upload-delete-button p-0">';
                            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                            html += '</button>';
                            $( image_target ).prepend( html );
                            $( image_target ).prev().val( base64 );
                        });
                    } else if ( $( target ).val() == $( this ).find( 'input' ).val() ) {
                        $( target ).parents( '.modal' ).find( '.image-trimming-area' ).croppie( 'result', 'base64' ).then( function( base64 ) {
                            $( image_target ).find( 'a' ).remove();
                            $( image_target ).find( 'img' ).remove();
                            if ( $( target ).parents( '.modal' ).attr( 'id' ).indexOf( 'half' ) !== -1 ) {
                                $( image_target ).prepend( '<img src="' + base64 + '" style="height: 100%;">' );
                            } else {
                                $( image_target ).prepend( '<img src="' + base64 + '" style="width: 100%;">' );
                            }

                            var html = '<button type="button" class="btn upload-delete-button p-0">';
                            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross-white.svg">';
                            html += '</button>';
                            $( image_target ).prepend( html );
                            $( image_target ).prev().val( base64 );
                        });
                    }
                });
                $( this ).find( '.cardtype-area .cardtype-image-area .cardtype-image-item' ).each( function( index, value ) {
                    if ( $( target ).val() == $( this ).find( 'input' ).val() ) {
                        var image_target = $( this );
                        $( target ).parents( '.modal' ).find( '.image-trimming-area' ).croppie( 'result', 'base64' ).then( function( base64 ) {
                            $( image_target ).find( 'span' ).css( 'background-image', 'url("' + base64 + '")' );
                        });
                    }
                });
        
                $( target ).next().next().trigger( 'click' );
                reset_trimming( target );
            }
        });
    });
    $( '.trimming-image-modal .cancel-button' ).on( 'click', function() {
        $( this ).next().trigger( 'click' );
        reset_trimming( this );
    });

    $( document ).on( 'click', '#save_cardtype_form .message-area .display-area .content-area .select-button', function () {
        $( '#more_template_modal .cardtype-area img').each( function( index, value ) {
            if ( $( '#save_cardtype_form [name=template_10]' ).val() == '1' ) {
                if ( index == 0 || index == 3 ) {
                    $( this ).addClass( 'd-none' );
                } else if ( index == 1 || index == 2 ) {
                    $( this ).removeClass( 'd-none' );
                }
            } else if ( $( '#save_cardtype_form [name=template_10]' ).val() == '2' ) {
                if ( index == 0 || index == 3 ) {
                    $( this ).removeClass( 'd-none' );
                } else if ( index == 1 || index == 2 ) {
                    $( this ).addClass( 'd-none' );
                }
            }
        });
        $( '#more_template_modal .cardtype-area input').each( function( index, value ) {
            if ( $( '#save_cardtype_form [name=template_10]' ).val() == '1' ) {
                if ( index == 0 ) {
                    $( this ).prop( 'checked', true );
                } else if ( index == 1 ) {
                    $( this ).prop( 'checked', false );
                }
            } else if ( $( '#save_cardtype_form [name=template_10]' ).val() == '2' ) {
                if ( index == 0 ) {
                    $( this ).prop( 'checked', false );
                } else if ( index == 1 ) {
                    $( this ).prop( 'checked', true );
                }
            }
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#more_template_modal [name=more_template]' ).on( 'change', function() {
        $( '#more_template_modal [name=more_template]' ).each( function( index, value ) {
            $( this ).parent().prev().prev().removeClass( 'd-none' );
            $( this ).parent().prev().addClass( 'd-none' );
        });
        $( this ).parent().prev().prev().addClass( 'd-none' );
        $( this ).parent().prev().removeClass( 'd-none' );
    });
    $( '#more_template_modal .cardtype-area img' ).on( 'click', function() {
        $( this ).parent().find( 'input' ).prop( 'checked', true );
        $( '#more_template_modal [name=more_template]' ).each( function( index, value ) {
            $( this ).parent().prev().prev().removeClass( 'd-none' );
            $( this ).parent().prev().addClass( 'd-none' );
        });
        $( this ).parent().find( 'img' ).each( function( index, value ) {
            if ( index == 0 ) {
                $( this ).addClass( 'd-none' );
            } else if ( index == 1 ) {
                $( this ).removeClass( 'd-none' );
            }
        });
    });
    $( '#more_template_modal .select-button' ).on( 'click', function() {
        $( '#save_cardtype_form [name=template_10]' ).val( $( '#more_template_modal [name=more_template]:checked' ).val() );
        $( '#save_cardtype_form [name=template_10]' ).prev().text( $( '#more_template_modal [name=more_template]:checked' ).prev().text() );
    
        $( '#save_cardtype_form .tab-pane.active .display-area .content-area' ).each( function( index, value ) {
            if ( index == 2 ) {
                if ( $( '#save_cardtype_form [name=template_10]' ).val() == '1' ) {
                    $( this ).addClass( 'd-none' );
                    $( this ).find( 'input' ).prop( 'required', false );
                } else if ( $( '#save_cardtype_form [name=template_10]' ).val() == '2' ) {
                    $( this ).removeClass( 'd-none' );
                    $( this ).find( 'input' ).prop( 'required', true );
                }
            }
        });

        $( '#save_cardtype_form .tab-pane.active .cardtype-area' ).remove();
        if ( $( '#save_cardtype_form [name=template_10]' ).val() == '1' ) {
            $( '#save_cardtype_form .tab-pane.active .col-3' ).prepend( append_more_simple() );
        } else if ( $( '#save_cardtype_form [name=template_10]' ).val() == '2' ) {
            $( '#save_cardtype_form .tab-pane.active .col-3' ).prepend( append_more_image() );
        }

        if ( $( '#save_cardtype_form [name=action_label_10]').val() != '' ) {
            $( '#save_cardtype_form .tab-pane.active .cardtype-area .more' ).text( $( '#save_cardtype_form [name=action_label_10]').val() );
        }
        if ( $( '#save_cardtype_form [name=image_10]').val() != '' ) {
            $( '#save_cardtype_form .tab-pane.active .cardtype-area .cardtype-image-area span' ).css( 'background-image', 'url( \'' + $( '#save_cardtype_form [name=image_10]').val() + '\' )' );
        }

        $( this ).next().next().trigger( 'click' );
    });
    $( '#more_template_modal .cancel-button' ).on( 'click', function() {
        $( '#more_template_modal [name=more_template]' ).each( function( index, value ) {
            if ( $( this ).val() == $( '#save_cardtype_form [name=template_10]' ).val() ) {
                $( this ).prop( 'checked', true );
                $( this ).parent().prev().prev().addClass( 'd-none' );
                $( this ).parent().prev().removeClass( 'd-none' );
            } else {
                $( this ).prop( 'checked', false );
                $( this ).parent().prev().prev().removeClass( 'd-none' );
                $( this ).parent().prev().addClass( 'd-none' );
            }
        });
        $( this ).next().trigger( 'click' );
    });
    
    action_preview();
});

function reset_trimming( target ) {
    $( target ).parents( '.modal' ).find( '.image-drop-zone [name=image_file]' ).val( '' );
    $( target ).parents( '.modal' ).find( '.image-drop-zone' ).removeClass( 'd-none' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone' ).addClass( 'd-none' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone .image-trimming-area' ).removeClass( 'croppie-container' );
    $( target ).parents( '.modal' ).find( '.image_trimming_zone .image-trimming-area' ).empty();
    $( '.trimming-image-modal .upload-button' ).removeClass( 'd-block' );
    $( '.trimming-image-modal .upload-button' ).addClass( 'd-none' );
}