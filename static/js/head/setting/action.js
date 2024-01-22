$( function() {
    $( '#change_email_modal .action-button' ).on( 'click', function() {
        if ( $( '#change_email_form' ).parsley().validate() ) {
            var target = $( this );
            $.ajax({
                'data': change_data['email'](),
                'url': $( '#change_email_check_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    change_success['email']($( target ).next());
                } else {
                    change_error['email'](response.message);
                }
            }).fail( function(){
                change_error['email']('メールアドレスの変更に失敗しました');
            });
        }
    });
    $( '#change_email_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        
        $( '#change_email_check_modal .no-button' ).trigger( 'click' );
        $.ajax({
            'data': change_data['email'](),
            'url': $( '#change_email_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#change_email_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#change_email_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'change_email' );

    $( '#change_password_modal .action-button' ).on( 'click', function() {
        if ( $( '#change_password_form' ).parsley().validate() ) {
            var next = $( this ).next();
            $.ajax({
                'data': change_data['password'](),
                'url': $( '#change_password_check_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    change_success['password'](next);
                } else {
                    change_error['password']('パスワードが間違っています')
                }
            }).fail( function(){
                change_error['password']('パスワードの変更に失敗しました')
            });
        }
    });
    $( '#change_password_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        
        $( '#change_password_check_modal .no-button' ).trigger( 'click' );
        $.ajax({
            'data': change_data['password'](),
            'url': $( '#change_password_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#change_password_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#change_password_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'change_password' );

    $( '.detail-manager-modal .reset-button' ).on( 'click', function() {
        $( '#reset_password_check_modal .yes-button' ).val( $( this ).val() );
        $( this ).next().trigger( 'click' );
        up_modal();
    });
    $( '#reset_password_check_modal .yes-button' ).on( 'click', function() {
        $( this ).prop( 'disabled', true );
        $( '#reset_password_check_modal .no-button' ).trigger( 'click' );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#reset_password_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '#reset_password_success_button' ).trigger( 'click' );
            up_modal();
        }).fail( function(){
            $( '#reset_password_error_button' ).trigger( 'click' );
            up_modal();
        });
    });
    action_reload( 'reset_password' );
});