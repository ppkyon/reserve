$( function() {
    $( document ).on( 'change', '#save_basic_form [name=deadline]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#save_basic_form [name=on_time]' ).prop( 'disabled', false );
            $( '#save_basic_form [name=on_time]' ).removeClass( 'readonly' );
            $( '#save_basic_form [name=any_day]' ).prop( 'disabled', true );
            $( '#save_basic_form [name=any_day]' ).addClass( 'readonly' );
            $( '#save_basic_form [name=any_time]' ).prop( 'disabled', true );
            $( '#save_basic_form [name=any_time]' ).addClass( 'readonly' );
        } else if ( $( this ).val() == '2' ) {
            $( '#save_basic_form [name=on_time]' ).prop( 'disabled', true );
            $( '#save_basic_form [name=on_time]' ).addClass( 'readonly' );
            $( '#save_basic_form [name=any_day]' ).prop( 'disabled', false );
            $( '#save_basic_form [name=any_day]' ).removeClass( 'readonly' );
            $( '#save_basic_form [name=any_time]' ).prop( 'disabled', false );
            $( '#save_basic_form [name=any_time]' ).removeClass( 'readonly' );
        }
    });
});