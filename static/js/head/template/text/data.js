var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_text_form' ).length ) {
        $( '#save_text_form' ).parsley();
        $( '#save_text_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.text = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_text_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_text_form [name=name]' ).val() );
        form_data.append( 'count', $( '#save_text_form [name=number]' ).length );
        $( '#save_text_form [name=number]' ).each( function( index, value ) {
            form_data.append( 'message_type_' + ( index + 1 ), $( '#save_text_form [name=message_type_' + ( index + 1 ) + ']' ).val() );
            if ( $( '#save_text_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '1' ) {
                form_data.append( 'text_' + ( index + 1 ), $( '#save_text_form [name=text_' + ( index + 1 ) + ']' ).html() );
            } else if ( $( '#save_text_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '2' ) {
                form_data.append( 'image_' + ( index + 1 ), $( '#save_text_form [name=upload_image_' + ( index + 1 ) + ']' ).val() );
            } else if ( $( '#save_text_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '3' ) {
                form_data.append( 'video_' + ( index + 1 ), $( '#save_text_form [name=upload_video_' + ( index + 1 ) + ']' ).val() );
            } else if ( $( '#save_text_form [name=message_type_' + ( index + 1 ) + ']' ).val() == '4' ) {
                form_data.append( 'template_' + ( index + 1 ), $( '#save_text_form [name=template_' + ( index + 1 ) + ']' ).val() );
                form_data.append( 'template_type_' + ( index + 1 ), $( '#save_text_form [name=template_type_' + ( index + 1 ) + ']' ).val() );
            }
        });
        return form_data;
    };
    save_success.text = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'text' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.text = function(message='') {
        
    };

    delete_data.text = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_text_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.text = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_text_form [name=id]' ).val() );
        return form_data;
    };
});