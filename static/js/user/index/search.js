$( function() {
    $( document ).on( 'click', '#search_user_modal .reset-button', function () {
        $( '#search_user_modal input[type=text]' ).val( '' );
        $( '#search_user_modal input[type=hidden]' ).val( '' );
        $( '#search_user_modal input[type=checkbox]' ).prop( 'checked', false );
    });
    $( document ).on( 'click', '#search_user_modal .yes-button', function () {
        var form_data = new FormData();
        form_data.append( 'name', $( '#search_user_modal input[name=name]' ).val() );
        form_data.append( 'kana', $( '#search_user_modal input[name=kana]' ).val() );
        form_data.append( 'phone', $( '#search_user_modal input[name=phone]' ).val() );
        form_data.append( 'email', $( '#search_user_modal input[name=email]' ).val() );
        form_data.append( 'age_from', $( '#search_user_modal input[name=age_from]' ).val() );
        form_data.append( 'age_to', $( '#search_user_modal input[name=age_to]' ).val() );
        form_data.append( 'date_from', $( '#search_user_modal input[name=date_from]' ).val() );
        form_data.append( 'date_to', $( '#search_user_modal input[name=date_to]' ).val() );
        form_data.append( 'id_from', $( '#search_user_modal input[name=id_from]' ).val() );
        form_data.append( 'id_to', $( '#search_user_modal input[name=id_to]' ).val() );
        form_data.append( 'sex', $( '#search_user_modal input[name=sex]' ).next().val() );
        form_data.append( 'member', $( '#search_user_modal input[name=member]' ).next().val() );

        var tag = [];
        $( '#search_user_modal input[name=tag]:checked' ).each( function( index, value ) {
            tag.push( $( this ).val() );
        });
        form_data.append( 'tag', tag );
        var flow = [];
        $( '#search_user_modal input[name=flow]:checked' ).each( function( index, value ) {
            flow.push( $( this ).val() );
        });
        form_data.append( 'flow', flow );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#search_user_form' ).attr( 'action' ),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            location.reload();
        }).fail( function(){
            location.reload();
        });
    });
    $( document ).on( 'click', '.search-box .delete-button', function () {
        var form_data = new FormData();
        form_data.append( 'item', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#delete_search_user_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            location.reload();
        }).fail( function(){
            location.reload();
        });
    });
});