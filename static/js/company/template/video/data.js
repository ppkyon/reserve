var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_video_form' ).length ) {
        $( '#save_video_form' ).parsley();
        $( '#save_video_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.video = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_video_form [name=id]' ).val() );
        form_data.append( 'name', $( '#save_video_form [name=name]' ).val() );
        form_data.append( 'video', $( '#save_video_form [name=upload_video]' ).val() );
        form_data.append( 'size', $( '#save_video_form [name=size]' ).val() );
        return form_data;
    };
    save_success.video = function(modal) {
        $( '#save_check_modal .yes-button' ).val('video');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.video = function(message='') {
        
    };

    delete_data.video = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_video_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.video = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_video_form [name=id]' ).val() );
        return form_data;
    };
});