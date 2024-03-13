var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_cardtype_form' ).length ) {
        $( '#save_cardtype_form' ).parsley();
        $( '#save_cardtype_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_cardtype_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    };

    save_data.cardtype = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_cardtype_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_cardtype_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_cardtype_form [name=name]' ).val() );
        form_data.append( 'type', $( '#save_cardtype_form [name=type]' ).val() );

        var count = 0;
        $( '#save_cardtype_form .tab-area ul li' ).each( function( index, value ) {
            var number = $( this ).find( 'a' ).text();
            if ( number == 'もっと見る' ) {
                if ( $( '#save_cardtype_form [name=template_10]' ).val() == '2' ) {
                    form_data.append( 'image_10', $( '#save_cardtype_form [name=image_10]' ).val() );
                }
                form_data.append( 'template_10', $( '#save_cardtype_form [name=template_10]' ).val() );
                form_data.append( 'action_label_10', $( '#save_cardtype_form [name=action_label_10]' ).val() );

                form_data.append( 'action_type_10', 0 );
                if ( check_empty( $( '#save_cardtype_form [name=action_type_10]' ).next().val() ) ) {
                    form_data.append( 'action_type_10', $( '#save_cardtype_form [name=action_type_10]' ).next().val() );
                    if ( $( '#save_cardtype_form [name=action_type_10]' ).next().val() == '8' ) {
                        form_data.append( 'action_text_10', $( '#save_cardtype_form [name=action_text_10]' ).val() );
                    } else {
                        if ( check_empty( $( '#save_cardtype_form [name=action_url_10]' ).val() ) ) {
                            form_data.append( 'action_url_10', $( '#save_cardtype_form [name=action_url_10]' ).val() );
                        }
                        if ( check_empty( $( '#save_cardtype_form [name=action_url_10]' ).next().val() ) ) {
                            form_data.append( 'action_url_value_10', $( '#save_cardtype_form [name=action_url_10]' ).next().val() );
                        }
                    }
                }
            } else {
                if ( $( '#save_cardtype_form [name=type]' ).val() == '2' || $( '#save_cardtype_form [name=type]' ).val() == '3' ) {
                    form_data.append( 'action_label_1_' + number, $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() );
                    form_data.append( 'action_label_2_' + number, $( '#save_cardtype_form [name=action_2_' + number + ']' ).val() );

                    form_data.append( 'action_type_1_' + number, 0 );
                    if ( check_empty( $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() ) ) {
                        form_data.append( 'action_type_1_' + number, $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() );
                        if ( $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() == '8' ) {
                            form_data.append( 'action_text_1_' + number, $( '#save_cardtype_form [name=action_text_1_' + number + ']' ).val() );
                        } else {
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).val() ) ) {
                                form_data.append( 'action_url_1_' + number, $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).val() );
                            }
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).next().val() ) ) {
                                form_data.append( 'action_url_value_1_' + number, $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).next().val() );
                            }
                        }
                    }
                    form_data.append( 'action_type_2_' + number, 0 );
                    if ( check_empty( $( '#save_cardtype_form [name=action_type_2_' + number + ']' ).next().val() ) ) {
                        form_data.append( 'action_type_2_' + number, $( '#save_cardtype_form [name=action_type_2_' + number + ']' ).next().val() );
                        if ( $( '#save_cardtype_form [name=action_type_2_' + number + ']' ).next().val() == '8' ) {
                            form_data.append( 'action_text_2_' + number, $( '#save_cardtype_form [name=action_text_2_' + number + ']' ).val() );
                        } else {
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_2_' + number + ']' ).val() ) ) {
                                form_data.append( 'action_url_2_' + number, $( '#save_cardtype_form [name=action_url_2_' + number + ']' ).val() );
                            }
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_2_' + number + ']' ).next().val() ) ) {
                                form_data.append( 'action_url_value_2_' + number, $( '#save_cardtype_form [name=action_url_2_' + number + ']' ).next().val() );
                            }
                        }
                    }

                    if ( $( '#save_cardtype_form [name=action_check_1_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'action_label_flg_1_' + number, 1 );
                    } else {
                        form_data.append( 'action_label_flg_1_' + number, 0 );
                    }
                    if ( $( '#save_cardtype_form [name=action_check_2_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'action_label_flg_2_' + number, 1 );
                    } else {
                        form_data.append( 'action_label_flg_2_' + number, 0 );
                    }
                }

                if ( $( '#save_cardtype_form [name=type]' ).val() == '1' || $( '#save_cardtype_form [name=type]' ).val() == '2' ) {
                    form_data.append( 'title_' + number, $( '#save_cardtype_form [name=title_' + number + ']' ).val() );
                    form_data.append( 'image_count_' + number, $( '#save_cardtype_form [name=image_count_' + number + ']' ).val() );
                    form_data.append( 'image_1_' + number, $( '#save_cardtype_form [name=image_a_' + number + ']' ).val() );
                    form_data.append( 'image_2_' + number, $( '#save_cardtype_form [name=image_b_' + number + ']' ).val() );
                    form_data.append( 'image_3_' + number, $( '#save_cardtype_form [name=image_c_' + number + ']' ).val() );
                    form_data.append( 'label_' + number, $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() );
                    form_data.append( 'label_color_' + number, $( '#save_cardtype_form [name=label_color_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'label_flg_' + number, 1 );
                    } else {
                        form_data.append( 'label_flg_' + number, 0 );
                    }
                }

                if ( $( '#save_cardtype_form [name=type]' ).val() == '1' ) {
                    form_data.append( 'description_' + number, $( '#save_cardtype_form [name=description_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=description_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'description_flg_' + number, 1 );
                    } else {
                        form_data.append( 'description_flg_' + number, 0 );
                    }
                    if ( $( '#save_cardtype_form [name=image_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'image_flg_' + number, 1 );
                    } else {
                        form_data.append( 'image_flg_' + number, 0 );
                        form_data.append( 'image_count_' + number, 0 );
                    }
                    form_data.append( 'text_count_' + number, $( '#save_cardtype_form .tab-pane' ).eq(index).find( '.content-text-area' ).length );
                    $( '#save_cardtype_form .tab-pane' ).eq(index).find( '.content-text-area' ).each( function( index ,value ) {
                        form_data.append( 'text_title_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=text_title_' + ( index + 1 ) + '_' + number + ']' ).val() );
                        form_data.append( 'text_text_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).val() );
                        form_data.append( 'text_value_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=text_text_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                        if ( $( '#save_cardtype_form [name=text_check_' + ( index + 1 ) + '_' + number + ']' ).prop( 'checked' ) ) {
                            form_data.append( 'text_flg_' + ( index + 1 ) + '_' + number, 1 );
                        } else {
                            form_data.append( 'text_flg_' + ( index + 1 ) + '_' + number, 0 );
                        }
                    });
                    form_data.append( 'action_count_' + number, $( '#save_cardtype_form .tab-pane' ).eq(index).find( '.content-action-area' ).length );
                    $( '#save_cardtype_form .tab-pane' ).eq(index).find( '.content-action-area' ).each( function( index ,value ) {
                        form_data.append( 'action_label_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_label_' + ( index + 1 ) + '_' + number + ']' ).val() );
                        form_data.append( 'action_button_type_' + ( index + 1 ) + '_' + number, '' );
                        if ( check_empty( $( '#save_cardtype_form [name=action_button_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                            form_data.append( 'action_button_type_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_button_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                        }
                        form_data.append( 'action_text_color_' + ( index + 1 ) + '_' + number, '0' );
                        if ( check_empty( $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                            form_data.append( 'action_text_color_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_text_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                        }
                        form_data.append( 'action_background_color_' + ( index + 1 ) + '_' + number, '0' );
                        if ( check_empty( $( '#save_cardtype_form [name=action_background_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                            form_data.append( 'action_background_color_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_background_color_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                        }
                        form_data.append( 'action_type_' + ( index + 1 ) + '_' + number, 0 );
                        if ( check_empty( $( '#save_cardtype_form [name=action_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                            form_data.append( 'action_type_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                            if ( $( '#save_cardtype_form [name=action_type_' + ( index + 1 ) + '_' + number + ']' ).next().val() == '8' ) {
                                form_data.append( 'action_text_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_text_' + ( index + 1 ) + '_' + number + ']' ).val() );
                            } else {
                                if ( check_empty( $( '#save_cardtype_form [name=action_url_' + ( index + 1 ) + '_' + number + ']' ).val() ) ) {
                                    form_data.append( 'action_url_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_url_' + ( index + 1 ) + '_' + number + ']' ).val() );
                                }
                                if ( check_empty( $( '#save_cardtype_form [name=action_url_' + ( index + 1 ) + '_' + number + ']' ).next().val() ) ) {
                                    form_data.append( 'action_url_value_' + ( index + 1 ) + '_' + number, $( '#save_cardtype_form [name=action_url_' + ( index + 1 ) + '_' + number + ']' ).next().val() );
                                }
                            }
                        }
                        if ( $( '#save_cardtype_form [name=action_check_' + ( index + 1 ) + '_' + number + ']' ).prop( 'checked' ) ) {
                            form_data.append( 'action_flg_' + ( index + 1 ) + '_' + number, 1 );
                        } else {
                            form_data.append( 'action_flg_' + ( index + 1 ) + '_' + number, 0 );
                        }
                    });
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '2' ) {
                    form_data.append( 'place_' + number, $( '#save_cardtype_form [name=place_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=place_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'place_flg_' + number, 1 );
                    } else {
                        form_data.append( 'place_flg_' + number, 0 );
                    }
                    form_data.append( 'plus_' + number, $( '#save_cardtype_form [name=plus_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=plus_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'plus_flg_' + number, 1 );
                    } else {
                        form_data.append( 'plus_flg_' + number, 0 );
                    }
                    form_data.append( 'plus_type_' + number, $( '#save_cardtype_form [name=select_plus_' + number + ']' ).next().val() );
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '3' ) {
                    form_data.append( 'image_' + number, $( '#save_cardtype_form [name=image_' + number + ']' ).val() );
                    form_data.append( 'name_' + number, $( '#save_cardtype_form [name=name_' + number + ']' ).val() );
                    form_data.append( 'tag_1_' + number, $( '#save_cardtype_form [name=tag_input_1_' + number + ']' ).val() );
                    form_data.append( 'tag_2_' + number, $( '#save_cardtype_form [name=tag_input_2_' + number + ']' ).val() );
                    form_data.append( 'tag_3_' + number, $( '#save_cardtype_form [name=tag_input_3_' + number + ']' ).val() );
                    form_data.append( 'tag_color_1_' + number, $( '#save_cardtype_form [name=tag_color_1_' + number + ']' ).val() );
                    form_data.append( 'tag_color_2_' + number, $( '#save_cardtype_form [name=tag_color_2_' + number + ']' ).val() );
                    form_data.append( 'tag_color_3_' + number, $( '#save_cardtype_form [name=tag_color_3_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=tag_check_1_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'tag_flg_1_' + number, 1 );
                    } else {
                        form_data.append( 'tag_flg_1_' + number, 0 );
                    }
                    if ( $( '#save_cardtype_form [name=tag_check_2_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'tag_flg_2_' + number, 1 );
                    } else {
                        form_data.append( 'tag_flg_2_' + number, 0 );
                    }
                    if ( $( '#save_cardtype_form [name=tag_check_3_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'tag_flg_3_' + number, 1 );
                    } else {
                        form_data.append( 'tag_flg_3_' + number, 0 );
                    }
                    form_data.append( 'description_' + number, $( '#save_cardtype_form [name=description_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=description_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'description_flg_' + number, 1 );
                    } else {
                        form_data.append( 'description_flg_' + number, 0 );
                    }
                } else if ( $( '#save_cardtype_form [name=type]' ).val() == '4' ) {
                    form_data.append( 'image_' + number, $( '#save_cardtype_form [name=image_' + number + ']' ).val() );
                    form_data.append( 'label_' + number, $( '#save_cardtype_form [name=label_input_' + number + ']' ).val() );
                    form_data.append( 'label_color_' + number, $( '#save_cardtype_form [name=label_color_' + number + ']' ).val() );
                    if ( $( '#save_cardtype_form [name=label_check_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'label_flg_' + number, 1 );
                    } else {
                        form_data.append( 'label_flg_' + number, 0 );
                    }
                    form_data.append( 'action_label_' + number, $( '#save_cardtype_form [name=action_1_' + number + ']' ).val() );

                    form_data.append( 'action_type_' + number, 0 );
                    if ( check_empty( $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() ) ) {
                        form_data.append( 'action_type_' + number, $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() );
                        if ( $( '#save_cardtype_form [name=action_type_1_' + number + ']' ).next().val() == '8' ) {
                            form_data.append( 'action_text_' + number, $( '#save_cardtype_form [name=action_text_1_' + number + ']' ).val() );
                        } else {
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).val() ) ) {
                                form_data.append( 'action_url_' + number, $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).val() );
                            }
                            if ( check_empty( $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).next().val() ) ) {
                                form_data.append( 'action_url_value_' + number, $( '#save_cardtype_form [name=action_url_1_' + number + ']' ).next().val() );
                            }
                        }
                    }
                    
                    if ( $( '#save_cardtype_form [name=action_check_1_' + number + ']' ).prop( 'checked' ) ) {
                        form_data.append( 'action_label_flg_' + number, 1 );
                    } else {
                        form_data.append( 'action_label_flg_' + number, 0 );
                    }
                }
                count++;
            }
        });
        form_data.append( 'count', count );
        return form_data;
    }
    save_success.cardtype = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'cardtype' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.cardtype = function(message='') {
        
    };

    delete_data.cardtype = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_cardtype_form [name=id]' ).val() );
        return form_data;
    };
    
    copy_data.cardtype = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_cardtype_form [name=id]' ).val() );
        return form_data;
    };
});