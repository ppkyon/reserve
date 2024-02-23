var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    save_data.greeting = function() {
        var form_data = new FormData();
        form_data.append( 'count', $( '#save_greeting_form [name=number]' ).length );
        $( '#save_greeting_form [name=number]' ).each( function( index, value ) {
            form_data.append( 'message_type_' + ( index + 1 ), $( '#save_greeting_form [name=message_type_' + ( index + 1 ) + ']' ).val() );
            if ( $( '#save_greeting_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '1' ) {
                form_data.append( 'text_' + ( index + 1 ), $( '#save_greeting_form [name=text_' + ( index + 1 ) + ']' ).html() );
            } else if ( $( '#save_greeting_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '2' ) {
                form_data.append( 'image_' + ( index + 1 ), $( '#save_greeting_form [name=upload_image_' + ( index + 1 ) + ']' ).val() );
            } else if ( $( '#save_greeting_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '3' ) {
                form_data.append( 'video_' + ( index + 1 ), $( '#save_greeting_form [name=upload_video_' + ( index + 1 ) + ']' ).val() );
            } else if ( $( '#save_greeting_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '4' ) {
                form_data.append( 'template_' + ( index + 1 ), $( '#save_greeting_form [name=template_' + ( index + 1 ) + ']' ).val() );
            }
        });
        return form_data;
    };
    save_success.greeting = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'greeting' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.greeting = function(message='') {
        
    };
});