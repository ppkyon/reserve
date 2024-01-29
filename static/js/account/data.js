$( function() {
    if ( $( '#save_company_account_form' ).length ) {
        $( '#save_company_account_form' ).parsley();
        $( '#save_company_account_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_company_account_form' ).parsley().options.patternMessage = "正しい形式で入力してください";
        $( '#save_company_account_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    }
});