$( function() {
    $( '#save_cardtype_form .type-area .template_select_button' ).on( 'click', function() {
        var target = $( this );
        if ( check_empty($( this ).prev().val()) ) {
            $( '#select_cardtype_modal .cardtype-area .col-3' ).each( function( index, value ) {
                if ( Number( $( this ).find( 'input[type=radio]' ).val() ) == Number( $( target ).prev().val() ) ) {
                    $( this ).find( 'img' ).each( function( index, value ) {
                        if ( index == 0 ) {
                            $( this ).addClass( 'd-none' );
                        } else if ( index == 1 ) {
                            $( this ).removeClass( 'd-none' );
                        }
                    });
                    $( this ).find( 'input' ).prop( 'checked', true );
                } else {
                    $( this ).find( 'img' ).each( function( index, value ) {
                        if ( index == 0 ) {
                            $( this ).removeClass( 'd-none' );
                        } else if ( index == 1 ) {
                            $( this ).addClass( 'd-none' );
                        }
                    });
                    $( this ).find( 'input' ).prop( 'checked', false );
                }
            });
        }
        $( this ).next().trigger( 'click' );
    });
    $( '#select_cardtype_modal [name=cardtype]' ).on( 'change', function() {
        $( '#select_cardtype_modal [name=cardtype]' ).each( function( index, value ) {
            $( this ).parent().prev().prev().removeClass( 'd-none' );
            $( this ).parent().prev().addClass( 'd-none' );
        });
        $( this ).parent().prev().prev().addClass( 'd-none' );
        $( this ).parent().prev().removeClass( 'd-none' );
    });
    $( '#select_cardtype_modal .cardtype-area img' ).on( 'click', function() {
        $( this ).parent().find( 'input' ).prop( 'checked', true );
        $( '#select_cardtype_modal [name=cardtype]' ).each( function( index, value ) {
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
    $( '#select_cardtype_modal .select-button' ).on( 'click', function() {
        if ( $( '#save_cardtype_form [name=type]' ).val() == '' ) {
            select_cardtype();
            $( this ).next().next().next().trigger( 'click' );
        } else {
            $( this ).next().trigger( 'click' );
            up_modal();
        }
        create_preview();
        slide_preview();
    });
    $( '#select_cardtype_modal .cancel-button' ).on( 'click', function() {
        $( '#select_cardtype_modal [name=cardtype]' ).each( function( index, value ) {
            $( this ).prop( 'checked', false );
            $( this ).parent().prev().prev().removeClass( 'd-none' );
            $( this ).parent().prev().addClass( 'd-none' );
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#select_cardtype_check_modal .yes-button' ).on( 'click', function() {
        select_cardtype();
        $( '#select_cardtype_check_modal .no-button' ).trigger( 'click' );
        $( '#select_cardtype_modal .cancel-button' ).next().trigger( 'click' );
        $( '#more_template_modal [name=more_template]:eq(0)' ).prop( 'checked', true );
        $( '#more_template_modal .cardtype-area img' ).each( function( index, value ) {
            if ( index == 0 || index == 3 ) {
                $( this ).addClass( 'd-none' );
            } else if ( index == 1 || index == 2 ) {
                $( this ).removeClass( 'd-none' );
            }
        });
        create_preview();
        slide_preview();
    });

    $( document ).on( 'click', '#save_cardtype_form .tab-area .add-card-button', function () {
        if ( $( '#save_cardtype_form .tab-area ul li' ).length < 10 ) {
            if ( $( '#save_cardtype_form .tab-area ul li' ).length == 9 ) {
                if ( $( '#save_cardtype_form .tab-area ul li' ).eq($( '#save_cardtype_form .tab-area ul li' ).length - 1).find( 'a' ).text() != 'もっと見る' ) {
                    return;
                }
            }

            var clone = '';
            var more_flg = false;
            var tab_count = $( '#save_cardtype_form .tab-area ul li' ).length + 1;
            $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
                $( this ).find( 'a' ).removeClass( 'active' );
                if( index == $( '#save_cardtype_form .tab-area ul li' ).length - 1 ) {
                    clone = $( this );
                }
                if ( $( this ).find( 'a' ).text() == 'もっと見る' ) {
                    tab_count = tab_count - 1;
                    more_flg = true;
                }
            });
            if ( !more_flg ) {
                clone = '';
            }

            var html = '<li class="nav-item">';
            html += '<a href="#tab' + tab_count + '" class="nav-link active" data-bs-toggle="tab" role="tab">' + tab_count + '</a>';
            html += '</li>';
            $( '#save_cardtype_form .tab-area ul' ).append( html );
            $( '#save_cardtype_form .tab-area ul' ).append( clone );
            $( '#save_cardtype_form .message-area .tab-content .tab-pane' ).each( function( index, value ) {
                $( this ).removeClass( 'active' );
                if( index == $( '#save_cardtype_form .message-area .tab-content .tab-pane' ).length - 1 ) {
                    if ( more_flg ) {
                        clone = $( this );
                    }
                }
            });
            if ( $( '#save_cardtype_form [name=type]' ).val() == '1' ) {
                $( '#save_cardtype_form .tab-content' ).append( append_announce_card( tab_count ) );
            } else if ( $( '#save_cardtype_form [name=type]' ).val() == '2' ) {
                $( '#save_cardtype_form .tab-content' ).append( append_location_card( tab_count ) );
            } else if ( $( '#save_cardtype_form [name=type]' ).val() == '3' ) {
                $( '#save_cardtype_form .tab-content' ).append( append_person_card( tab_count ) );
            } else if ( $( '#save_cardtype_form [name=type]' ).val() == '4' ) {
                $( '#save_cardtype_form .tab-content' ).append( append_image_card( tab_count ) );
            }
            $( '#save_cardtype_form .tab-content' ).append( clone );
            create_preview();
            slide_preview();
        }
    });
    $( document ).on( 'click', '#save_cardtype_form .tab-area .add-more-card-button', function () {
        $( this ).addClass( 'd-none' );
        $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
            $( this ).find( 'a' ).removeClass( 'active' );
        });

        var html = '<li class="nav-item">';
        html += '<a href="#tab10" class="nav-link" data-bs-toggle="tab" role="tab">もっと見る</a>';
        html += '</li>';
        $( '#save_cardtype_form .tab-area ul' ).append( html );
        $( '#save_cardtype_form .tab-area ul li' ).eq( $( '#save_cardtype_form .tab-area ul li' ).length - 1 ).find( 'a' ).addClass( 'active' );

        $( '#save_cardtype_form .tab-content .tab-pane' ).each( function( index, value ) {
            $( this ).removeClass( 'active' );
        });
        $( '#save_cardtype_form .tab-content' ).append( append_more() );
        $( '#save_cardtype_form .tab-content .tab-pane' ).eq( $( '#save_cardtype_form .tab-content .tab-pane' ).length - 1 ).addClass( 'active' );
        create_preview();
        slide_preview();
    });
    $( document ).on( 'click', '#save_cardtype_form .action-area .copy-card-button', function () {
        if ( $( '#save_cardtype_form .tab-area ul li' ).length < 10 ) {
            if ( $( '#save_cardtype_form .tab-area ul li' ).length == 9 ) {
                if ( $( '#save_cardtype_form .tab-area ul li' ).eq($( '#save_cardtype_form .tab-area ul li' ).length - 1).find( 'a' ).text() != 'もっと見る' ) {
                    return;
                }
            }

            var more_clone = '';
            var more_flg = false;
            var tab_count = $( '#save_cardtype_form .tab-area ul li' ).length + 1;
            $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
                $( this ).find( 'a' ).removeClass( 'active' );
                if( index == $( '#save_cardtype_form .tab-area ul li' ).length - 1 ) {
                    more_clone = $( this );
                }
                if ( $( this ).find( 'a' ).text() == 'もっと見る' ) {
                    tab_count = tab_count - 1;
                    more_flg = true;
                }
            });
            if ( !more_flg ) {
                more_clone = '';
            }

            var html = '<li class="nav-item">';
            html += '<a href="#tab' + tab_count + '" class="nav-link active" data-bs-toggle="tab" role="tab">' + tab_count + '</a>';
            html += '</li>';
            $( '#save_cardtype_form .tab-area ul' ).append( html );
            $( '#save_cardtype_form .tab-area ul' ).append( more_clone );
            var clone = $( '#save_cardtype_form .tab-pane.active' ).clone();
            $( '#save_cardtype_form .tab-content .tab-pane' ).each( function( index, value ) {
                $( this ).removeClass( 'active' );
                if( index == $( '#save_cardtype_form .tab-content .tab-pane' ).length - 1 ) {
                    if ( more_flg ) {
                        more_clone = $( this );
                    }
                }
            });
            $( '#save_cardtype_form .tab-content' ).append( clone );
            var target = $( '#save_cardtype_form .tab-content .tab-pane' ).eq($( '#save_cardtype_form .tab-content .tab-pane' ).length - 1);
            $( target ).attr( 'id', 'tab' + tab_count );
            $( target ).children( 'input' ).val( tab_count );
            $( target ).find( '.action-area button' ).val( tab_count );

            change_tab_number( target, tab_count );
            $( '#save_cardtype_form .tab-content' ).append( more_clone );
            create_preview();
            slide_preview();
        }
    });
    $( document ).on( 'click', '#save_cardtype_form .action-area .delete-card-button', function () {
        var count = $( '#save_cardtype_form .tab-area ul li' ).length;
        var delete_flg = true;
        if ( count == 2 ) {
            $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
                if ( $( this ).find( 'a' ).text() == 'もっと見る' ) {
                    delete_flg = false;
                }
            });
        }
        if ( count != 1 && ( delete_flg || $( this ).val() == '10' ) ) {
            $( '#delete_card_check_modal .yes-button' ).val( $( this ).val() );
            $( this ).next().trigger( 'click' );
        }
    });
    $( '#delete_card_check_modal .yes-button' ).on( 'click', function() {
        var target = $( this );
        var last_flg = false;
        $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
            if ( index == Number( $( target ).val() ) - 1 ) {
                $( this ).remove();
                last_flg = true;
            } else if ( index > Number( $( target ).val() ) - 1 ) {
                if ( $( this ).find( 'a' ).text() != 'もっと見る' ) {
                    var number = Number( $( this ).find( 'a' ).text() ) - 1;
                    $( this ).find( 'a' ).text( number );
                    $( this ).find( 'a' ).attr( 'href', '#tab' + number );
                }
                if ( index == Number( $( target ).val() ) ) {
                    if ( $( this ).find( 'a' ).text() == 'もっと見る' ) {
                        $( '#save_cardtype_form .tab-area ul li' ).eq($( '#save_cardtype_form .tab-area ul li' ).length - 2).find( 'a' ).addClass( 'active' );
                    } else {
                        $( this ).find( 'a' ).addClass( 'active' );
                    }
                }
                last_flg = false;
            }

            if ( $( target ).val() == '10' ) {
                if ( index == $( '#save_cardtype_form .tab-area ul li' ).length - 1 ) {
                    $( this ).remove();
                } else if ( index == $( '#save_cardtype_form .tab-area ul li' ).length - 2 ) {
                    $( this ).find( 'a' ).addClass( 'active' );
                }
                $( '#save_cardtype_form .tab-area .add-more-card-button' ).removeClass( 'd-none' );
                $( '#more_template_modal .cancel-button' ).trigger( 'click' );
            }
        });

        if ( last_flg ) {
            $( '#save_cardtype_form .tab-area ul li' ).eq($( '#save_cardtype_form .tab-area ul li' ).length - 1).find( 'a' ).addClass( 'active' );
        }
        last_flg = false
        $( '#save_cardtype_form .tab-content .tab-pane' ).each( function( index, value ) {
            if ( index == Number( $( target ).val() ) - 1 ) {
                $( this ).remove();
                last_flg = true;
            } else if ( index > Number( $( target ).val() ) - 1 ) {
                if ( $( this ).attr( 'id' ) != 'tab10' ) {
                    var number = Number( $( this ).children( 'input' ).val() ) - 1;
                    $( this ).attr( 'id', 'tab' + number );
                    $( this ).children( 'input' ).val( number );
                    $( this ).find( '.action-area button' ).val( number );
                }
                if ( index == Number( $( target ).val() ) ) {
                    if ( $( this ).attr( 'id' ) == 'tab10' ) {
                        $( '#save_cardtype_form .tab-content .tab-pane' ).eq($( '#save_cardtype_form .tab-content .tab-pane' ).length - 2).addClass( 'active' );
                    } else {
                        $( this ).addClass( 'active' );
                    }
                }
                last_flg = false;

                change_tab_number( $( this ), number );
            }
            if ( $( target ).val() == '10' ) {
                if ( index == $( '#save_cardtype_form .tab-content .tab-pane' ).length - 1 ) {
                    $( this ).remove();
                } else if ( index == $( '#save_cardtype_form .tab-content .tab-pane' ).length - 2 ) {
                    $( this ).addClass( 'active' );
                }
            }
        });

        if ( last_flg ) {
            $( '#save_cardtype_form .tab-content .tab-pane' ).eq($( '#save_cardtype_form .tab-content .tab-pane' ).length - 1).addClass( 'active' );
        }
        $( '#delete_card_check_modal .no-button' ).trigger( 'click' );
    });
    create_preview();
    slide_preview();
});

function select_cardtype() {
    $( '#save_cardtype_form [name=type]' ).val( $( '#select_cardtype_modal [name=cardtype]:checked' ).val() );
    $( '#save_cardtype_form [name=type]' ).next().text( 'カードタイプを変更' );
    $( '#save_cardtype_form [name=type]' ).prev().text( $( '#select_cardtype_modal [name=cardtype]:checked' ).prev().text() );

    var id = $( '#save_cardtype_form [name=id]' ).val()
    $( '#save_cardtype_form .input-area .tab-area' ).remove();
    $( '#save_cardtype_form .input-area .message-area' ).remove();
    $( '#save_cardtype_form .input-area .button-area' ).remove();
    if ( $( '#select_cardtype_modal [name=cardtype]:checked' ).val() == "1" ) {
        $( '#save_cardtype_form .input-area' ).append( append_announce() );
    } else if ( $( '#select_cardtype_modal [name=cardtype]:checked' ).val() == "2" ) {
        $( '#save_cardtype_form .input-area' ).append( append_location() );
    } else if ( $( '#select_cardtype_modal [name=cardtype]:checked' ).val() == "3" ) {
        $( '#save_cardtype_form .input-area' ).append( append_person() );
    } else if ( $( '#select_cardtype_modal [name=cardtype]:checked' ).val() == "4" ) {
        $( '#save_cardtype_form .input-area' ).append( append_image() );
    }
    $( '#save_cardtype_form [name=id]' ).val(id);
}

function change_tab_number( target, number ) {
    $( target ).find( 'div' ).each( function( index, value ) {
        if ( $( this ).attr( 'id' ) != undefined && $( this ).attr( 'id' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'id', $( this ).attr( 'id' ).slice( 0, -1 ) + number );
        }
        if ( $( this ).attr( 'aria-labelledby' ) != undefined && $( this ).attr( 'aria-labelledby' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'aria-labelledby', $( this ).attr( 'aria-labelledby' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( 'label' ).each( function( index, value ) {
        if ( $( this ).attr( 'id' ) != undefined && $( this ).attr( 'id' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'id', $( this ).attr( 'id' ).slice( 0, -1 ) + number );
        }
        if ( $( this ).attr( 'for' ) != undefined && $( this ).attr( 'for' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'for', $( this ).attr( 'for' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( 'p' ).each( function( index, value ) {
        if ( $( this ).attr( 'id' ) != undefined && $( this ).attr( 'id' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'id', $( this ).attr( 'id' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( 'button' ).each( function( index, value ) {
        if ( $( this ).attr( 'id' ) != undefined && $( this ).attr( 'id' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'id', $( this ).attr( 'id' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( 'input' ).each( function( index, value ) {
        if ( $( this ).attr( 'id' ) != undefined && $( this ).attr( 'id' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'id', $( this ).attr( 'id' ).slice( 0, -1 ) + number );
        }
        if ( $( this ).attr( 'name' ) != undefined && $( this ).attr( 'name' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'name', $( this ).attr( 'name' ).slice( 0, -1 ) + number );
        }
        if ( $( this ).attr( 'data-parsley-errors-container' ) != undefined && $( this ).attr( 'data-parsley-errors-container' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'data-parsley-errors-container', $( this ).attr( 'data-parsley-errors-container' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( 'textarea' ).each( function( index, value ) {
        if ( $( this ).attr( 'name' ) != undefined && $( this ).attr( 'name' ).slice( -2 ) != '10' ) {
            $( this ).attr( 'name', $( this ).attr( 'name' ).slice( 0, -1 ) + number );
        }
    });
    $( target ).find( '.parsley-errors-list' ).remove();
    $( target ).find( '.parsley-error' ).removeClass( 'parsley-error' );
}