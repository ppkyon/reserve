var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_richvideo_form' ).length ) {
        $( '#save_richvideo_form' ).parsley();
        $( '#save_richvideo_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_richvideo_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    };

    save_data.richvideo = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richvideo_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_richvideo_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_richvideo_form [name=name]' ).val() );
        form_data.append( 'video', $( '#save_richvideo_form [name=upload_video]' ).val() );
        form_data.append( 'display', $( '#save_richvideo_form [name=action]:checked' ).val() );
        if ( $( '#save_richvideo_form [name=favorite]' ).prop( 'checked' ) ) {
            form_data.append( 'favorite', 1 );
        } else {
            form_data.append( 'favorite', 0 );
        }
        if ( $( '#save_richvideo_form [name=action]:checked' ).val() == '1' ) {
            form_data.append( 'url', $( '#save_richvideo_form [name=url]' ).val() );
            form_data.append( 'text', $( '#save_richvideo_form [name=text]:checked' ).val() );

            if ( $( '#save_richvideo_form [name=text]:checked' ).val() == '12' ) {
                form_data.append( 'custom', $( '#save_richvideo_form [name=custom]' ).val() );
            }
        }
        form_data.append( 'size', $( '#save_richvideo_form [name=size]' ).val() );
        return form_data;
    };
    save_success.richvideo = function(modal) {
        $( '#save_check_modal .yes-button' ).val('richvideo');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.richvideo = function(message='') {
        
    };

    delete_data.richvideo = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_richvideo_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.richvideo = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_richvideo_form [name=id]' ).val() );
        return form_data;
    };
});