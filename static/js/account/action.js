$( function() {
    $( document ).on( 'click', '.input-area .input-text-area .dropdown .dropdown-menu button', function () {
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).val( $( this ).text() );
        $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).val( $( this ).val() );
    });
    $( document ).on( 'keyup', '[name=company_postcode]', function () {
        AjaxZip3.zip2addr( 'company_postcode', '', 'company_prefecture', 'company_address' );
    });

    $( document ).on( 'change', '[name=head_manager_check]', function () {
        if ( $( this ).prop( 'checked' ) ) {
            $( '[name=manager_family_name]' ).prop( 'disabled', true );
            $( '[name=manager_family_name]' ).prop( 'required', false );
            $( '[name=manager_family_name]' ).val( '' );
            $( '[name=manager_first_name]' ).prop( 'disabled', true );
            $( '[name=manager_first_name]' ).prop( 'required', false );
            $( '[name=manager_first_name]' ).val( '' );
            $( '[name=manager_family_name_kana]' ).prop( 'disabled', true );
            $( '[name=manager_family_name_kana]' ).prop( 'required', false );
            $( '[name=manager_family_name_kana]' ).val( '' );
            $( '[name=manager_first_name_kana]' ).prop( 'disabled', true );
            $( '[name=manager_first_name_kana]' ).prop( 'required', false );
            $( '[name=manager_first_name_kana]' ).val( '' );
            $( '[name=manager_department]' ).prop( 'disabled', true );
            $( '[name=manager_department]' ).prop( 'required', false );
            $( '[name=manager_department]' ).val( '' );
            $( '[name=manager_phone_number]' ).prop( 'disabled', true );
            $( '[name=manager_phone_number]' ).prop( 'required', false );
            $( '[name=manager_phone_number]' ).val( '' );
            $( '[name=manager_email]' ).prop( 'disabled', true );
            $( '[name=manager_email]' ).prop( 'required', false );
            $( '[name=manager_email]' ).val( '' );
            $( this ).parents( '.input-area' ).find( '.account-image-button' ).prop( 'disabled', true );
            $( this ).parents( '.input-area' ).find( '.input-text-area .image-file-name' ).addClass( 'd-none' );
            $( this ).parents( '.input-area' ).find( '.input-text-area .image-file-name' ).text( '' );
            $( this ).parents( '.input-area' ).find( '.input-text-area .upload-image-area input[type=hidden]' ).val( '' );
            $( this ).parents( '.input-area' ).find( '.input-text-area .image-delete-button' ).addClass( 'd-none' );
        } else {
            $( '[name=manager_family_name]' ).prop( 'disabled', false );
            $( '[name=manager_family_name]' ).prop( 'required', true );
            $( '[name=manager_first_name]' ).prop( 'disabled', false );
            $( '[name=manager_first_name]' ).prop( 'required', true );
            $( '[name=manager_family_name_kana]' ).prop( 'disabled', false );
            $( '[name=manager_family_name_kana]' ).prop( 'required', true );
            $( '[name=manager_first_name_kana]' ).prop( 'disabled', false );
            $( '[name=manager_first_name_kana]' ).prop( 'required', true );
            $( '[name=manager_department]' ).prop( 'disabled', false );
            $( '[name=manager_department]' ).prop( 'required', true );
            $( '[name=manager_phone_number]' ).prop( 'disabled', false );
            $( '[name=manager_phone_number]' ).prop( 'required', true );
            $( '[name=manager_email]' ).prop( 'disabled', false );
            $( '[name=manager_email]' ).prop( 'required', true );
            $( this ).parents( '.input-area' ).find( '.account-image-button' ).prop( 'disabled', false );
        }
    });

    $( document ).on( 'click', '.input-select-work-parent .dropdown-menu button', function () {
        var form_data = new FormData();
        form_data.append( 'value', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#get_work_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            $( '.input-select-work-child input' ).val( '' );
            $( '.input-select-work-child .dropdown-menu' ).empty();
            $.each( response, function( index, value ) {
                var html = '';
                if ( index == 0 ) {
                    html += '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold p-1 ps-2">' + value.name + '</button>';
                } else {
                    html += '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold border-top p-1 ps-2 pt-2">' + value.name + '</button>';
                }
                $( '.input-select-work-child .dropdown-menu' ).append( html );
            });
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.add-tag-button', function () {
        var number = $( '.input-area .input-text-area .input-text-tag-genre' ).length + 1;
        $( '[name=tag_count]' ).val( number );

        var genre = '<div class="input-text-tag-genre d-inline-block p-0" style="width: 85%;">';
        genre += '<input type="text" name="tag_genre_' + number + '" class="input-text ps-2 pe-2" placeholder="ジャンル">';
        genre += '</div>';

        var tag = '<div class="input-text-tag d-inline-block p-0" style="width: 85%;">';
        tag += '<input type="text" name="tag_' + number + '" class="input-text ps-2 pe-2" placeholder="タグ名">';
        tag += '</div>';

        var html = '<div class="input-area">';
        html += '<div class="d-flex justify-content-start align-items-center ps-2 mb-3">';
        html += '<label class="input-label mb-0"></label>';
        html += '<div class="input-text-area">';
        html += '<div class="d-flex justify-content-start align-items-center" style="width: 92%;">' + genre + tag + '</div>';
        html += '</div>';
        html += '<button type="button" class="btn add-tag-button d-flex justify-content-start align-items-center p-0"></button>';
        html += '</div>';
        html += '</div>';
        $( '.legal-link-area' ).before( html );
    });

    $( '.modal .legal-area' ).scroll( function() {
        var height = $( this ).get(0).scrollHeight;
        var scroll = $( this ).scrollTop() + $( '#legal_modal .modal-body' ).height();
        
        if( height <= scroll ){
            $( '#legal_check' ).prop( 'disabled', false );
            $( '#legal_check' ).prev().removeClass( 'disabled' );
            $( '#legal_check' ).next().removeClass( 'disabled' );
        }
    });
    $( '.modal .close-button' ).on( 'click', function() {
        if ( $( '#legal_check' ).prop( 'checked' ) ) {
            $( '#check_button' ).prop( 'disabled', false );
        } else {
            $( '#check_button' ).prop( 'disabled', true );
        }
        $( this ).next().trigger( 'click' );
    });

    $( '.button-area .check-button' ).on( 'click', function() {
        $( '.error-message-area' ).each( function( index, value ) {
            $( this ).remove();
        });
        if ( $( '#save_company_account_form' ).parsley().validate() ) {
            var form_data = new FormData();
            form_data.append( 'head_email', $( '#save_company_account_form [name=head_email]' ).val() );
            form_data.append( 'manager_email', $( '#save_company_account_form [name=manager_email]' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#check_email_url' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.check ) {
                    $( '#save_company_account_form' ).submit();
                } else {
                    var html = '<div class="error-message-area text-center">';
                    html += '<p class="error-message mt-2 mb-2">メールアドレスが既に登録されています</p>';
                    html += '</div>';
                    $( '.status-area' ).after(html);
                    $( window ).scrollTop(0);
                }
            }).fail( function(){
                
            });
        }
    });
    $( '.button-area .save-button' ).on( 'click', function() {
        $( '#save_company_account_form' ).attr( 'action', '/account/company/end/' );
        $( '#save_company_account_form' ).submit();
    });
    $( '.button-area .back-button' ).on( 'click', function() {
        $( '#save_company_account_form' ).attr( 'action', '/account/company/?id=' + $( '#save_company_account_form [name=id]' ).val() );
        $( '#save_company_account_form' ).submit();
    });
});