var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    save_data.company = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_company_form [name=id]' ).val() );
        form_data.append( 'company_name', $( '#save_company_form [name=company_name]' ).val() );
        form_data.append( 'head_family_name', $( '#save_company_form [name=head_family_name]' ).val() );
        form_data.append( 'head_first_name', $( '#save_company_form [name=head_first_name]' ).val() );
        form_data.append( 'head_family_name_kana', $( '#save_company_form [name=head_family_name_kana]' ).val() );
        form_data.append( 'head_first_name_kana', $( '#save_company_form [name=head_first_name_kana]' ).val() );
        form_data.append( 'company_postcode', $( '#save_company_form [name=company_postcode]' ).val() );
        form_data.append( 'company_prefecture', $( '#save_company_form [name=company_prefecture]' ).next().val() );
        form_data.append( 'company_address', $( '#save_company_form [name=company_address]' ).val() );
        form_data.append( 'company_phone_number', $( '#save_company_form [name=company_phone_number]' ).val() );
        form_data.append( 'head_email', $( '#save_company_form [name=head_email]' ).val() );
        form_data.append( 'memo', $( '#save_company_form [name=memo]' ).val() );
        var tag = [];
        $( '#save_company_form [name="tag[]"]' ).each( function( index, value ) {
            tag.push( $( this ).val() );
        });
        form_data.append( 'tag[]', tag );
        return form_data;
    };
    save_success.company = function(modal) {
        $( '#save_check_modal .yes-button' ).val('company');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.company = function(message='') {
        
    };

    $( '#add_company_form' ).parsley();
    $( '#add_company_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#add_company_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    $( '#save_company_form' ).parsley();
    $( '#save_company_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#save_company_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    $( '#save_company_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
});