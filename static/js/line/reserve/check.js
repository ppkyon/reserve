$( function(){
    $( '.button-area .reserve-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.check-area' ).addClass( 'd-none' );

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '[name=shop_id]' ).val() );
        form_data.append( 'user_id', liff.getContext().userId );
        form_data.append( 'setting_id', $( '.date-area [name=select_setting]' ).next().val() );
        form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#send_reserve_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '.loader-area' ).css( 'opacity', '0' );
                $( '.loader-area' ).addClass( 'd-none' );
                $( '.end-area' ).removeClass( 'd-none' );
            }, 750 );
        }).fail( function(){
        
        });
    });

    $( '.menu-area .place-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.place-area' ).addClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.place-area' ).removeClass( 'd-none' );
        }, 750 );
    });
    $( '.menu-area .course-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.place-area' ).addClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.course-area' ).removeClass( 'd-none' );
        }, 750 );
    });
    $( '.menu-area .date-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.place-area' ).addClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
        $( '.question-area' ).addClass( 'd-none' );
        $( '.check-area' ).addClass( 'd-none' );
        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.date-area' ).removeClass( 'd-none' );
        }, 750 );
    });

    $( '.button-area .close-button, .reserveform .error-area .close-button' ).on( 'click', function() {
        liff.closeWindow();
    });
});