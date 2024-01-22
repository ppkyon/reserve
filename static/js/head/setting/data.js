var change_data = new Array();
var change_success = new Array();
var change_error = new Array();
var add_data = new Array();
var add_success = new Array();
var add_error = new Array();
var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();

$( function() {
    $( '#change_email_form' ).parsley();
    $( '#change_email_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#change_email_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    $( '#change_password_form' ).parsley();
    $( '#change_password_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#change_password_form' ).parsley().options.equaltoMessage = "パスワードが一致していません";
    $( '#change_password_form' ).parsley().options.minlengthMessage = "8文字以上で入力してください";
    
    $( '#add_manager_form' ).parsley();
    $( '#add_manager_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#add_manager_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    change_data.email = function() {
        var form_data = new FormData();
        form_data.append( 'email', $( '#change_email_form [name=email]' ).val() );
        form_data.append( 'password', $( '#change_email_form [name=password]' ).val() );
        return form_data;
    };
    change_success.email = function(modal) {
        $( '#change_email_form .error-message-area' ).removeClass( 'd-block' );
        $( '#change_email_form .error-message-area' ).addClass( 'd-none' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    change_error.email = function(message='') {
        $( '#change_email_form .error-message' ).text( message );
        $( '#change_email_form .error-message-area' ).removeClass( 'd-none' );
        $( '#change_email_form .error-message-area' ).addClass( 'd-block' );
    };

    change_data.password = function() {
        var form_data = new FormData();
        form_data.append( 'now_password', $( '#change_password_form [name=now_password]' ).val() );
        form_data.append( 'new_password', $( '#change_password_form [name=new_password]' ).val() );
        return form_data;
    };
    change_success.password = function(modal) {
        $( '#change_password_form .error-message-area' ).removeClass( 'd-block' );
        $( '#change_password_form .error-message-area' ).addClass( 'd-none' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    change_error.password = function(message='') {
        $( '#change_password_form .error-message' ).text( message );
        $( '#change_password_form .error-message-area' ).removeClass( 'd-none' );
        $( '#change_password_form .error-message-area' ).addClass( 'd-block' );
    };

    add_data.manager = function() {
        var form_data = new FormData();
        form_data.append( 'email', $( '#add_manager_form [name=email]' ).val() );
        form_data.append( 'authority', $( '#add_manager_form [name=authority]:checked' ).val() );
        return form_data;
    };
    add_success.manager = function(modal) {
        $( '#add_manager_modal .error-message-area' ).removeClass( 'd-block' );
        $( '#add_manager_modal .error-message-area' ).addClass( 'd-none' );
        if ( $( '#add_manager_check_description' ).val() == 'True' ) {
            $( '#add_check_modal .modal-description-area' ).removeClass( 'd-none' );
        } else {
            $( '#add_check_modal .modal-description-area' ).addClass( 'd-none' );
        }
        $( '#add_check_modal .yes-button' ).val( 'manager' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    add_error.manager = function(message='') {
        $( '#add_manager_modal .error-message' ).text( message );
        $( '#add_manager_modal .error-message-area' ).removeClass( 'd-none' );
        $( '#add_manager_modal .error-message-area' ).addClass( 'd-block' );
    };

    save_data.manager = function() {
        var form_data = new FormData();
        form_data.append( 'image_file', $( '#save_manager_form [name=image_file]' )[0].files[0] );
        form_data.append( 'family_name', $( '#save_manager_form [name=family_name]' ).val() );
        form_data.append( 'first_name', $( '#save_manager_form [name=first_name]' ).val() );
        form_data.append( 'family_name_kana', $( '#save_manager_form [name=family_name_kana]' ).val() );
        form_data.append( 'first_name_kana', $( '#save_manager_form [name=first_name_kana]' ).val() );
        form_data.append( 'phone_number', $( '#save_manager_form [name=phone_number]' ).val() );
        form_data.append( 'department', $( '#save_manager_form [name=department]' ).val() );
        form_data.append( 'job', $( '#save_manager_form [name=job]' ).val() );
        form_data.append( 'work', $( '#save_manager_form [name=work]' ).val() );
        if ( check_empty( $( '#save_manager_form [name=age]' ).next().val() ) ) {
            form_data.append( 'age', $( '#save_manager_form [name=age]' ).next().val() );
        } else {
            form_data.append( 'age', '0' );
        }
        if ( check_empty( $( '#save_manager_form [name=sex]' ).next().val() ) ) {
            form_data.append( 'sex', $( '#save_manager_form [name=sex]' ).next().val() );
        } else {
            form_data.append( 'sex', '0' );
        }
        return form_data;
    };
    save_success.manager = function(modal) {
        $( '#save_check_modal .yes-button' ).val('manager');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.manager = function(message='') {
        
    };

    delete_data.manager = function(id) {
        if ( id ) {
            var form_data = new FormData();
            form_data.append( 'id', $( '#delete_manager_' + id + '_form [name=id]' ).val() );
            return form_data;
        } else {
            var form_data = new FormData();
            form_data.append( 'id', $( '#delete_manager_form [name=id]' ).val() );
            return form_data;
        }
    };

    save_data.authority = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_authority_' + id + '_form [name=id]' ).val() );
        form_data.append( 'authority', $( '#save_authority_' + id + '_form [name=authority]:checked' ).val() );
        return form_data;
    };
    save_success.authority = function(modal, value) {
        $( '#save_check_modal .yes-button' ).val(value);
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.authority = function(id, message='') {
        
    };
});