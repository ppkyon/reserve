$( function(){
    $( '.button-area .reserve-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.history-check-area' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'flow_id', $( '.history-area .history-content-area.select' ).find( 'input[name=flow]' ).val() );
        form_data.append( 'schedule_id', $( '.history-area .history-content-area.select' ).find( 'input[name=schedule]' ).val() );
        form_data.append( 'year', $( this ).val().substring( 0, $( this ).val().indexOf('年') ) );
        form_data.append( 'month', $( this ).val().substring( $( this ).val().indexOf('年')+1, $( this ).val().indexOf('月') ) );
        form_data.append( 'day', $( this ).val().substring( $( this ).val().indexOf('月')+1, $( this ).val().indexOf('日') ) );
        form_data.append( 'hour', $( this ).val().substring( $( this ).val().indexOf(')')+2, $( this ).val().indexOf(':') ) );
        form_data.append( 'minute', $( this ).val().substring( $( this ).val().indexOf(':')+1, $( this ).val().indexOf('～') ) );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_reserve_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( response.error ) {
                setTimeout( function() {
                    $( '.loader-area' ).css( 'opacity', '0' );
                    $( '.loader-area' ).addClass( 'd-none' );
                    $( '.fail-area' ).removeClass( 'd-none' );
                }, 750 );
            } else {
                setTimeout( function() {
                    $( '.loader-area' ).css( 'opacity', '0' );
                    $( '.loader-area' ).addClass( 'd-none' );
                    $( '.history-end-area' ).removeClass( 'd-none' );
                }, 750 );
            }
        }).fail( function(){
        
        });
    });
    $( '.button-area .question-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.question-check-area' ).addClass( 'd-none' );
        
        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'question_id', $( '.question-area .content-area #question_id' ).val() );
        if ( check_empty($( '.question-area .content-area #question_id' ).val()) ) {
            $.each( $( '#question_form' ).serialize().split( '&' ), function( index, value ) {
                var question_answer = value.split( '=' );
                form_data.append( question_answer[0], question_answer[1].replace('歳', '') );
            });
        }
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_question_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.question-end-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
        
        });
    });

    $( '.menu-area .history-icon' ).on( 'click', function() {
        $( '.history-area .history-content-area' ).each( function( index, value ) {
            $( this ).removeClass( 'select' );
        });
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.history-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.history-check-area' ).addClass( 'd-none' );
        $( '.question-check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.history-area' ).removeClass( 'd-none' );
        }, 750 );
    });
    $( '.menu-area .date-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.history-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.history-check-area' ).addClass( 'd-none' );
        $( '.question-check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.date-area' ).removeClass( 'd-none' );
        }, 750 );
    });
    $( '.menu-area .question-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.history-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.history-check-area' ).addClass( 'd-none' );
        $( '.question-check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.question-area' ).removeClass( 'd-none' );
        }, 750 );
    });
    
    $( '.button-area .close-button, .error-area .close-button' ).on( 'click', function() {
        liff.closeWindow();
    });
    $( '.fail-area .reload-button' ).on( 'click', function() {
        location.reload();
    });
});