var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_richmessage_form' ).length ) {
        $( '#save_richmessage_form' ).parsley();
        $( '#save_richmessage_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_richmessage_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    }

    save_data.richmessage = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richmessage_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_richmessage_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_richmessage_form [name=name]' ).val() );
        form_data.append( 'template', $( '#save_richmessage_form [name=template]' ).val() );
        form_data.append( 'image', $( '#save_richmessage_form [name=upload_image]' ).val() );

        if ( $( '#save_richmessage_form [name=favorite]' ).prop( 'checked' ) ) {
            form_data.append( 'favorite', 1 );
        } else {
            form_data.append( 'favorite', 0 );
        }

        $( '#save_richmessage_form .action-area [name=number]' ).each( function( index, value ) {
            form_data.append( 'type_' + $( this ).val(), $( '#save_richmessage_form [name=type_' + $( this ).val() + ']' ).next().val() );
            if ( $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).length ) {
                form_data.append( 'url_' + $( this ).val(), $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).val() );
            }
            if ( $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).next().length ) {
                if ( check_empty( $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).next().val() ) ) {
                    if ( $( '#save_richmessage_form [name=type_' + $( this ).val() + ']' ).next().val() == '2' ) {
                        form_data.append( 'video_' + $( this ).val(), $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).next().val() );
                    } else if ( $( '#save_richmessage_form [name=type_' + $( this ).val() + ']' ).next().val() == '3' ) {
                        form_data.append( 'question_' + $( this ).val(), $( '#save_richmessage_form [name=url_' + $( this ).val() + ']' ).next().val() );
                    }
                }
            }
            if ( $( '#save_richmessage_form [name=label_' + $( this ).val() + ']' ).length ) {
                form_data.append( 'label_' + $( this ).val(), $( '#save_richmessage_form [name=label_' + $( this ).val() + ']' ).val() );
            }
        });

        return form_data;
    };
    save_success.richmessage = function(modal) {
        $( '#save_check_modal .yes-button' ).val('richmessage');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.richmessage = function(message='') {
        
    };

    delete_data.richmessage = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_richmessage_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.richmessage = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richmessage_form [name=id]' ).val() );
        return form_data;
    };
});