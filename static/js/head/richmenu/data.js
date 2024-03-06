var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_richmenu_form' ).length ) {
        $( '#save_richmenu_form' ).parsley();
        $( '#save_richmenu_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_richmenu_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    }

    save_data.richmenu = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richmenu_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_richmenu_form [name=name]' ).val() );

        form_data.append( 'menu_type', $( '#save_richmenu_form [name=menu_type]:checked' ).val() );
        form_data.append( 'menu_flg', $( '#save_richmenu_form [name=menu_flg]:checked' ).val() );
        form_data.append( 'menu_text', $( '#save_richmenu_form [name=menu_text]' ).val() );

        form_data.append( 'template', $( '#save_richmenu_form [name=template]' ).val() );
        form_data.append( 'image', $( '#save_richmenu_form [name=upload_image]' ).val() );

        $( '#save_richmenu_form .action-area [name=number]' ).each( function( index, value ) {
            form_data.append( 'type_' + $( this ).val(), $( '#save_richmenu_form [name=type_' + $( this ).val() + ']' ).next().val() );
            if ( $( '#save_richmenu_form [name=url_' + $( this ).val() + ']' ).length ) {
                form_data.append( 'url_' + $( this ).val(), $( '#save_richmenu_form [name=url_' + $( this ).val() + ']' ).val() );
            }
            if ( $( '#save_richmenu_form [name=type_' + $( this ).val() + ']' ).next().val() == '2' ) {
                form_data.append( 'video_' + $( this ).val(), $( '#save_richmenu_form [name=url_' + $( this ).val() + ']' ).next().val() );
            } else if ( $( '#save_richmenu_form [name=type_' + $( this ).val() + ']' ).next().val() == '3' ) {
                form_data.append( 'question_' + $( this ).val(), $( '#save_richmenu_form [name=url_' + $( this ).val() + ']' ).next().val() );
            }
            if ( $( '#save_richmenu_form [name=label_' + $( this ).val() + ']' ).length ) {
                form_data.append( 'label_' + $( this ).val(), $( '#save_richmenu_form [name=label_' + $( this ).val() + ']' ).val() );
            }
            if ( $( '#save_richmenu_form [name=text_' + $( this ).val() + ']' ).length ) {
                form_data.append( 'text_' + $( this ).val(), $( '#save_richmenu_form [name=text_' + $( this ).val() + ']' ).val() );
            }
        });
        return form_data;
    };
    save_success.richmenu = function(modal) {
        $( '#save_check_modal .yes-button' ).val('richmenu');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.richmenu = function(message='') {
        
    };

    delete_data.richmenu = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_richmenu_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.richmenu = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richmenu_form [name=id]' ).val() );
        return form_data;
    };
});