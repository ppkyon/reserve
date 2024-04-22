$( function() {
    $( '#check_pin' ).on( 'change', function() {
        var form_data = new FormData();
        form_data.append( 'user_id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        if ( $( '#check_pin' ).prop( 'checked' ) ) {
            form_data.append( 'pin_flg', 1 );
        } else {
            form_data.append( 'pin_flg', 0 );
        }
        $.ajax({
            'data': form_data,
            'url': $( '#change_pin_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( $( '#check_pin' ).prop( 'checked' ) ) {
                $( '.user-area .user-area-id' ).each( function( index, element ){
                    if( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                        $( this ).next().find( '.pin-area' ).removeClass( 'd-none' );
                    }
                });
            } else {
                $( '.user-area .user-area-id' ).each( function( index, element ){
                    if( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                        $( this ).next().find( '.pin-area' ).addClass( 'd-none' );
                    }
                });
            }
            create_user_list(response);
        }).fail( function(){
            
        });
    });

    $( '.select_status_button' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'user_id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'status', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#chenge_status_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if( response.status == null ) {
                $( '#select_status' ).addClass( 'readonly' );
                $( '.user-area .user-area-id' ).each( function( index, value ){
                    if ( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                        $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).text( '' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'danger' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'complete' );
                    }
                });
            } else {
                if ( response.status.status == 0 ) {
                    $( '#select_status' ).addClass( 'readonly' );
                    $( '.user-area .user-area-id' ).each( function( index, value ){
                        if ( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                            $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).text( '' );
                            $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'danger' );
                            $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'complete' );
                            $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).addClass( 'd-none' );
                        }
                    });
                } else {
                    $( '#select_status' ).removeClass( 'readonly' );
                    $( '.user-area .user-area-id' ).each( function( index, value ){
                        if ( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                            if ( response.status.status == "1" ) {
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).text( '要対応' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).addClass( 'danger' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'complete' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'd-none' );
                            } else if ( response.status.status == "2" ) {
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).text( '対応済み' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'danger' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).addClass( 'complete' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'd-none' );
                            } else {
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).text( '' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'danger' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).removeClass( 'complete' );
                                $( this ).next().find( '.info-area .status-area span:nth-child(1)' ).addClass( 'd-none' );
                            }
                        }
                    });
                }
            }
        }).fail( function(){
            
        });
    });

    $( '.select_manager_button' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'user_id', $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() );
        form_data.append( 'manager_id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#change_manager_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if( response.manager_profile == null ) {
                $( '#select_manager' ).addClass( 'readonly' );
                $( '.user-area .user-area-id' ).each( function( index, value ){
                    if ( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).text( '' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).removeClass( 'manager' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).removeClass( 'ms-1' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).addClass( 'd-none' );
                    }
                });
            } else {
                $( '#select_manager' ).removeClass( 'readonly' );
                $( '.user-area .user-area-id' ).each( function( index, value ){
                    if ( $( this ).val() == $( '#send_' + $( '#send_id' ).val() + '_form [name=id]' ).val() ) {
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).text( response.manager_profile.family_name + ' ' + response.manager_profile.first_name );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).addClass( 'manager' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).addClass( 'ms-1' );
                        $( this ).next().find( '.info-area .status-area span:nth-child(2)' ).removeClass( 'd-none' );
                    }
                });
            }
        }).fail( function(){
            
        });
    });
});