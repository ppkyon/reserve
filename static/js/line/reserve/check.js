$( function(){
    $( '.button-area .reserve-button' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.check-area' ).addClass( 'd-none' );

        setTimeout( function() {
            $( '.loader-area' ).css( 'opacity', '0' );
            $( '.loader-area' ).addClass( 'd-none' );
            $( '.end-area' ).removeClass( 'd-none' );
        }, 750 );
    });

    $( '.menu-area .place-icon' ).on( 'click', function() {
        $( '.loader-area' ).css( 'opacity', '1' );
        $( '.loader-area' ).removeClass( 'd-none' );
        $( '.place-area' ).addClass( 'd-none' );
        $( '.course-area' ).addClass( 'd-none' );
        $( '.date-area' ).addClass( 'd-none' );
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