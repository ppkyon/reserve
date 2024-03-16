$( function() {
    $( '#save_flow_form .title-area .select-button' ).on( 'click', function() {
        var target = $( this );
        if ( check_empty($( target ).prev().val()) ) {
            $( '#select_flow_modal .flow-area input' ).each( function( index, value ) {
                if ( $( this ).val() == Number( $( target ).prev().val() ) ) {
                    $( this ).prop( 'checked', true );
                } else {
                    $( this ).prop( 'checked', false );
                }
            });
        }
        $( this ).next().trigger( 'click' );
    });
    $( '#select_flow_modal .select-button' ).on( 'click', function() {
        if ( check_empty($( '#save_flow_form [name=flow]' ).val()) ) {
            $( this ).next().trigger( 'click' );
            up_modal();
        } else {
            select_flow();
            $( this ).next().next().next().trigger( 'click' );
        }
    });
    $( '#select_flow_modal .cancel-button' ).on( 'click', function() {
        $( '#select_flow_modal [name=flow]' ).each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#select_flow_check_modal .yes-button' ).on( 'click', function() {
        select_flow();
        $( '#select_flow_check_modal .no-button' ).trigger( 'click' );
        $( '#select_flow_modal .cancel-button' ).next().trigger( 'click' );
    });

    $( document ).on( 'click', '#save_flow_form .chart-area .action-reminder-button', function () {
        $( this ).parent().addClass( 'target' );
        $( '#action_reminder_modal .modal-body [name=action_reminder_date]' ).val( $( '#save_flow_form .target [name=reminder_action_date]' ).val() );
        $( '#action_reminder_modal .modal-body [name=action_reminder_time]' ).val( $( '#save_flow_form .target [name=reminder_action_time]' ).val() );
        $( '#action_reminder_modal .modal-body [name=action_reminder_template]' ).val( $( '#save_flow_form .target [name=reminder_action_template]' ).val() );
        $( '#action_reminder_modal .modal-body [name=action_reminder_template_item]' ).val( $( '#save_flow_form .target [name=reminder_action_template_item]' ).val() );
        $( '#action_reminder_modal .modal-body [name=action_reminder_template_item_name]' ).val( $( '#save_flow_form .target [name=reminder_action_template_item_name]' ).val() );

        $( '#action_reminder_modal input[type=text]' ).each( function( index, value ) {
            $( this ).prop( 'disabled', true );
            $( this ).css( 'background-color', '-internal-light-dark(rgba(239, 239, 239, 0.3), rgba(59, 59, 59, 0.3));' );
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#action_reminder_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( '#action_reminder_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#save_flow_form .target' ).removeClass( 'target' );
        $( '#action_reminder_modal .modal-header button' ).trigger( 'click' );
    });
    $( '#action_reminder_modal' ).on( 'hidden.bs.modal', function () {
        $( '#action_reminder_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#save_flow_form .target' ).removeClass( 'target' );
        $( '#action_reminder_modal .modal-header button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '#save_flow_form .chart-area .action-message-button', function () {
        $( this ).parent().addClass( 'target' );
        $( '#action_message_modal .modal-body [name=action_message_timer]' ).each( function( index, value ) {
            if ( $( '#save_flow_form .target [name=message_action_template_timer]' ).val() == $( this ).val() ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        
        if ( $( '#save_flow_form .target [name=message_action_template_timer]' ).val() == '1' ) {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'disabled', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'required', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'disabled', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'required', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'required', false );
        } else if ( $( '#save_flow_form .target [name=message_action_template_timer]' ).val() == '2' ) {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'disabled', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'required', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'disabled', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'required', true );
        } else {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'required', false );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'disabled', true );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'required', false );
        }

        $( '#action_message_modal .modal-body [name=action_message_template]' ).val( $( '#save_flow_form .target [name=message_action_template]' ).val() );
        $( '#action_message_modal .modal-body [name=action_message_template_item]' ).val( $( '#save_flow_form .target [name=message_taction_emplate_item]' ).val() );
        $( '#action_message_modal .modal-body [name=action_message_template_item_name]' ).val( $( '#save_flow_form .target [name=message_action_template_item_name]' ).val() );

        if ( $( '#save_flow_form .target [name=message_action_template_timer]' ).val() == '1' ) {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).val( $( '#save_flow_form .target [name=message_action_timer_date]' ).val() );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).val( $( '#save_flow_form .target [name=message_action_timer_time]' ).val() );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).val( '' );
        } else if ( $( '#save_flow_form .target [name=message_action_template_timer]' ).val() == '2' ) {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).val( $( '#save_flow_form .target [name=message_action_timer_date]' ).val() );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).val( $( '#save_flow_form .target [name=message_action_timer_time]' ).val() );
        } else {
            $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).val( '' );
            $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).val( '' );
        }

        $( '#action_message_modal input[type=text]' ).each( function( index, value ) {
            $( this ).prop( 'disabled', true );
            $( this ).css( 'background-color', '-internal-light-dark(rgba(239, 239, 239, 0.3), rgba(59, 59, 59, 0.3));' );
        });
        $( '#action_message_modal input[type=radio]' ).each( function( index, value ) {
            $( this ).prop( 'disabled', true );
        });
        $( this ).next().trigger( 'click' );
    });
    $( '#action_message_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( '#action_message_modal .modal-body input[type=radio]').each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#action_message_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'required', false );

        $( '#save_flow_form .target' ).removeClass( 'target' );
        $( '#action_message_modal .modal-header button' ).trigger( 'click' );
    });
    $( '#action_message_modal' ).on( 'hidden.bs.modal', function () {
        $( '#action_message_modal .modal-body input[type=radio]').each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#action_message_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_date]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_date_time]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress]' ).prop( 'required', false );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'disabled', true );
        $( '#action_message_modal .modal-body [name=action_message_timer_progress_time]' ).prop( 'required', false );

        $( '#save_flow_form .target' ).removeClass( 'target' );
        $( '#action_message_modal .modal-header button' ).trigger( 'click' );
    });

    $( document ).on( 'click', '#save_flow_form .chart-area .chart-bar .timer-icon', function () {
        $( this ).parent().addClass( 'target' );
        $( '#timer_modal .modal-body [name=timer]' ).each( function( index, value ) {
            if ( $( '#save_flow_form .target [name=timer]' ).val() == $( this ).val() ) {
                $( this ).prop( 'checked', true );
            } else {
                $( this ).prop( 'checked', false );
            }
        });
        if ( $( '#save_flow_form .target [name=timer]' ).val() == '1' ) {
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'disabled', false );
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'required', true );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'disabled', false );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'required', true );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'required', false );
        } else if ( $( '#save_flow_form .target [name=timer]' ).val() == '2' ) {
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'disabled', false );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'required', true );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'disabled', false );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'required', true );
        } else {
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'required', false );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'disabled', true );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'required', false );
        }
        

        if ( $( '#save_flow_form .target [name=timer]' ).val() == '1' ) {
            $( '#timer_modal .modal-body [name=timer_date]' ).val( $( '#save_flow_form .target [name=timer_date]' ).val() );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).val( $( '#save_flow_form .target [name=timer_time]' ).val() );
            $( '#timer_modal .modal-body [name=timer_progress]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).val( '' );
        } else if ( $( '#save_flow_form .target [name=timer]' ).val() == '2' ) {
            $( '#timer_modal .modal-body [name=timer_date]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_progress]' ).val( $( '#save_flow_form .target [name=timer_date]' ).val() );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).val( $( '#save_flow_form .target [name=timer_time]' ).val() );
        } else {
            $( '#timer_modal .modal-body [name=timer_date]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_date_time]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_progress]' ).val( '' );
            $( '#timer_modal .modal-body [name=timer_progress_time]' ).val( '' );
        }
        $( this ).next().trigger( 'click' );
    });
    $( '#timer_modal .modal-footer .cancel-button' ).on( 'click', function() {
        $( '#timer_modal .modal-body input[type=radio]').each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#timer_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'required', false );
        
        $( '#save_flow_form .target' ).removeClass( 'target' );
        $( '#timer_modal .modal-header button' ).trigger( 'click' );
    });
    $( '#timer_modal' ).on( 'hidden.bs.modal', function () {
        $( '#timer_modal .modal-body input[type=radio]').each( function( index, value ) {
            $( this ).prop( 'checked', false );
        });
        $( '#timer_modal .modal-body input[type=text]').each( function( index, value ) {
            $( this ).val( '' );
        });
        $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_date]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_date_time]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_progress]' ).prop( 'required', false );
        $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'disabled', true );
        $( '#timer_modal .modal-body [name=timer_progress_time]' ).prop( 'required', false );
        
        $( '#save_flow_form .target' ).removeClass( 'target' );
    });
});

function select_flow(){
    $( '#save_flow_form [name=flow]' ).val( $( '#select_flow_modal [name=flow]:checked' ).val() );
    $( '#save_flow_form [name=flow]' ).next().text( 'フローを変更' );
    $( '#save_flow_form [name=flow]' ).prev().text( $( '#select_flow_modal [name=flow]:checked' ).prev().text() );
    $( '#save_flow_form [name=flow]' ).prev().removeClass( 'd-none' );

    $( '#save_flow_form .card-area .tab-area .nav' ).empty();
    $( '#save_flow_form .card-area .chart-area .tab-content' ).empty();
    $( '#save_flow_form .card-area .tab-area' ).css( 'opacity', '0' );
    $( '#save_flow_form .card-area .chart-area' ).css( 'opacity', '0' );
    $( '.table-loader-area' ).css( 'opacity', '1' );

    var form_data = new FormData();
    form_data.append( 'id', $( '#select_flow_modal [name=flow]:checked' ).val() );
    $.ajax({
        'data': form_data,
        'url': $( '#get_head_flow_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        var last_tab = null;
        $.each( response.tab, function( index, value ) {
            var last_line = null;
            if ( index == 0 ) {
                var html = '<li class="nav-item me-1">';
                html += '<a class="nav-link active" href="#' + value.value + '" data-bs-toggle="tab">' + value.name + '</a>';
                html += '</li>';
                $( '#save_flow_form .card-area .tab-area .nav' ).append( html );

                html = '<div id="' + value.value + '" class="tab-pane active">';
                html += '<table>';
                html += '<tbody>';
                html += '</tbody>';
                html += '</table>';
                html += '</div>';
                $( '#save_flow_form .card-area .chart-area .tab-content' ).append( html );
            } else {
                var html = '<li class="nav-item me-1">';
                html += '<a class="nav-link" href="#' + value.value + '" data-bs-toggle="tab">' + value.name + '</a>';
                html += '</li>';
                $( '#save_flow_form .card-area .tab-area .nav' ).append( html );

                html = '<div id="' + value.value + '" class="tab-pane">';
                html += '<table>';
                html += '<tbody>';
                html += '</tbody>';
                html += '</table>';
                html += '</div>';
                $( '#save_flow_form .card-area .chart-area .tab-content' ).append( html );
            }
            $.each( value.item, function( item_index, item_value ) {
                if ( last_line != item_value.y ) {
                    $( '#save_flow_form .card-area .chart-area .tab-content #' + value.value + ' tbody' ).append( '<tr></tr>' );
                    last_line = item_value.y;
                }
                $( '#save_flow_form .card-area .chart-area .tab-content #' + value.value + ' tbody tr' ).eq(item_value.y-1).append( append_flow( item_value ) );
            });
        });
        setTimeout( function() {
            $( '.table-loader-area' ).css( 'opacity', '0' );
            $( '#save_flow_form .card-area .tab-area' ).css( 'opacity', '1' );
            $( '#save_flow_form .card-area .chart-area' ).css( 'opacity', '1' );
        }, 750 );
    }).fail( function(){
        
    });
}