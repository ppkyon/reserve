var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    save_data.shop = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_shop_form [name=id]' ).val() );
        form_data.append( 'shop_name', $( '#save_shop_form [name=shop_name]' ).val() );
        form_data.append( 'head_family_name', $( '#save_shop_form [name=head_family_name]' ).val() );
        form_data.append( 'head_first_name', $( '#save_shop_form [name=head_first_name]' ).val() );
        form_data.append( 'head_family_name_kana', $( '#save_shop_form [name=head_family_name_kana]' ).val() );
        form_data.append( 'head_first_name_kana', $( '#save_shop_form [name=head_first_name_kana]' ).val() );
        form_data.append( 'shop_postcode', $( '#save_shop_form [name=shop_postcode]' ).val() );
        form_data.append( 'shop_prefecture', $( '#save_shop_form [name=shop_prefecture]' ).next().val() );
        form_data.append( 'shop_address', $( '#save_shop_form [name=shop_address]' ).val() );
        form_data.append( 'shop_phone_number', $( '#save_shop_form [name=shop_phone_number]' ).val() );
        form_data.append( 'memo', $( '#save_shop_form [name=memo]' ).val() );
        var tag = [];
        $( '#save_shop_form [name="tag[]"]' ).each( function( index, value ) {
            tag.push( $( this ).val() );
        });
        form_data.append( 'tag[]', tag );
        return form_data;
    };
    save_success.shop = function(modal) {
        $( '#save_check_modal .yes-button' ).val('shop');
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.shop = function(message='') {
        
    };

    $( '#add_shop_form' ).parsley();
    $( '#add_shop_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#add_shop_form' ).parsley().options.typeMessage = "正しい形式で入力してください";

    $( '#save_shop_form' ).parsley();
    $( '#save_shop_form' ).parsley().options.requiredMessage = "入力してください";
    $( '#save_shop_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    $( '#save_shop_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
});