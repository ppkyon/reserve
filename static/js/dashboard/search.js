$( function() {
    $( document ).on( 'click', '#search_today_modal .reset-button', function () {
        $( '#search_today_modal input[type=text]' ).val( '' );
        $( '#search_today_modal input[type=hidden]' ).val( '' );
        $( '#search_today_modal input[type=checkbox]' ).prop( 'checked', false );
    });
    $( document ).on( 'click', '#search_new_modal .reset-button', function () {
        $( '#search_new_modal input[type=text]' ).val( '' );
        $( '#search_new_modal input[type=hidden]' ).val( '' );
        $( '#search_new_modal input[type=checkbox]' ).prop( 'checked', false );
    });
    $( document ).on( 'click', '#search_after_modal .reset-button', function () {
        $( '#search_after_modal input[type=text]' ).val( '' );
        $( '#search_after_modal input[type=hidden]' ).val( '' );
        $( '#search_after_modal input[type=checkbox]' ).prop( 'checked', false );
    });

    $( document ).on( 'click', '#search_today_modal .yes-button', function () {
        var form_data = new FormData();
        form_data.append( 'name', $( '#search_today_modal input[name=name]' ).val() );
        form_data.append( 'kana', $( '#search_today_modal input[name=kana]' ).val() );
        form_data.append( 'phone', $( '#search_today_modal input[name=phone]' ).val() );
        form_data.append( 'email', $( '#search_today_modal input[name=email]' ).val() );
        form_data.append( 'age_from', $( '#search_today_modal input[name=age_from]' ).val() );
        form_data.append( 'age_to', $( '#search_today_modal input[name=age_to]' ).val() );
        form_data.append( 'time_from', $( '#search_today_modal input[name=date_from]' ).val() );
        form_data.append( 'time_to', $( '#search_today_modal input[name=date_to]' ).val() );
        form_data.append( 'sex', $( '#search_today_modal input[name=sex]' ).next().val() );
        form_data.append( 'member', $( '#search_today_modal input[name=member]' ).next().val() );
        form_data.append( 'line', $( '#search_today_modal input[name=line]' ).next().val() );
        var flow = [];
        $( '#search_today_modal input[name=flow]:checked' ).each( function( index, value ) {
            flow.push( $( this ).val() );
        });
        form_data.append( 'flow', flow );
        var manager = [];
        $( '#search_today_modal input[name=manager]:checked' ).each( function( index, value ) {
            manager.push( $( this ).val() );
        });
        form_data.append( 'manager', manager );
        var facility = [];
        $( '#search_today_modal input[name=facility]:checked' ).each( function( index, value ) {
            facility.push( $( this ).val() );
        });
        form_data.append( 'facility', facility );
        var place = [];
        $( '#search_today_modal input[name=place]:checked' ).each( function( index, value ) {
            place.push( $( this ).val() );
        });
        form_data.append( 'place', place );
        form_data.append( 'url', location.pathname );
        form_data.append( 'page', 'today' );
        $.ajax({
            'data': form_data,
            'url': $( '#search_today_form' ).attr( 'action' ),
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
    $( document ).on( 'click', '#search_new_modal .yes-button', function () {
        var form_data = new FormData();
        form_data.append( 'name', $( '#search_new_modal input[name=name]' ).val() );
        form_data.append( 'kana', $( '#search_new_modal input[name=kana]' ).val() );
        form_data.append( 'phone', $( '#search_new_modal input[name=phone]' ).val() );
        form_data.append( 'email', $( '#search_new_modal input[name=email]' ).val() );
        form_data.append( 'age_from', $( '#search_new_modal input[name=age_from]' ).val() );
        form_data.append( 'age_to', $( '#search_new_modal input[name=age_to]' ).val() );
        form_data.append( 'datetime_from', $( '#search_new_modal input[name=date_from]' ).val() );
        form_data.append( 'datetime_to', $( '#search_new_modal input[name=date_to]' ).val() );
        form_data.append( 'create_from', $( '#search_new_modal input[name=create_from]' ).val() );
        form_data.append( 'create_to', $( '#search_new_modal input[name=create_to]' ).val() );
        form_data.append( 'sex', $( '#search_new_modal input[name=sex]' ).next().val() );
        form_data.append( 'member', $( '#search_new_modal input[name=member]' ).next().val() );
        form_data.append( 'line', $( '#search_new_modal input[name=line]' ).next().val() );
        form_data.append( 'change', $( '#search_new_modal input[name=change]' ).next().val() );
        var flow = [];
        $( '#search_new_modal input[name=flow]:checked' ).each( function( index, value ) {
            flow.push( $( this ).val() );
        });
        form_data.append( 'flow', flow );
        var manager = [];
        $( '#search_new_modal input[name=manager]:checked' ).each( function( index, value ) {
            manager.push( $( this ).val() );
        });
        form_data.append( 'manager', manager );
        var facility = [];
        $( '#search_new_modal input[name=facility]:checked' ).each( function( index, value ) {
            facility.push( $( this ).val() );
        });
        form_data.append( 'facility', facility );
        var place = [];
        $( '#search_new_modal input[name=place]:checked' ).each( function( index, value ) {
            place.push( $( this ).val() );
        });
        form_data.append( 'place', place );
        form_data.append( 'url', location.pathname );
        form_data.append( 'page', 'new' );
        $.ajax({
            'data': form_data,
            'url': $( '#search_new_form' ).attr( 'action' ),
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
    $( document ).on( 'click', '#search_after_modal .yes-button', function () {
        var form_data = new FormData();
        form_data.append( 'name', $( '#search_after_modal input[name=name]' ).val() );
        form_data.append( 'kana', $( '#search_after_modal input[name=kana]' ).val() );
        form_data.append( 'phone', $( '#search_after_modal input[name=phone]' ).val() );
        form_data.append( 'email', $( '#search_after_modal input[name=email]' ).val() );
        form_data.append( 'age_from', $( '#search_after_modal input[name=age_from]' ).val() );
        form_data.append( 'age_to', $( '#search_after_modal input[name=age_to]' ).val() );
        form_data.append( 'datetime_from', $( '#search_after_modal input[name=date_from]' ).val() );
        form_data.append( 'datetime_to', $( '#search_after_modal input[name=date_to]' ).val() );
        form_data.append( 'create_from', $( '#search_after_modal input[name=create_from]' ).val() );
        form_data.append( 'create_to', $( '#search_after_modal input[name=create_to]' ).val() );
        form_data.append( 'sex', $( '#search_after_modal input[name=sex]' ).next().val() );
        form_data.append( 'member', $( '#search_after_modal input[name=member]' ).next().val() );
        form_data.append( 'line', $( '#search_after_modal input[name=line]' ).next().val() );
        var flow = [];
        $( '#search_after_modal input[name=flow]:checked' ).each( function( index, value ) {
            flow.push( $( this ).val() );
        });
        form_data.append( 'flow', flow );
        var manager = [];
        $( '#search_after_modal input[name=manager]:checked' ).each( function( index, value ) {
            manager.push( $( this ).val() );
        });
        form_data.append( 'manager', manager );
        var facility = [];
        $( '#search_after_modal input[name=facility]:checked' ).each( function( index, value ) {
            facility.push( $( this ).val() );
        });
        form_data.append( 'facility', facility );
        var place = [];
        $( '#search_after_modal input[name=place]:checked' ).each( function( index, value ) {
            place.push( $( this ).val() );
        });
        form_data.append( 'place', place );
        form_data.append( 'url', location.pathname );
        form_data.append( 'page', 'after' );
        $.ajax({
            'data': form_data,
            'url': $( '#search_after_form' ).attr( 'action' ),
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

    $( document ).on( 'click', '.search-box .delete-today-button', function () {
        var form_data = new FormData();
        form_data.append( 'page', 'today' );
        form_data.append( 'item', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#delete_search_today_url' ).val(),
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
    $( document ).on( 'click', '.search-box .delete-new-button', function () {
        var form_data = new FormData();
        form_data.append( 'page', 'new' );
        form_data.append( 'item', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#delete_search_new_url' ).val(),
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
    $( document ).on( 'click', '.search-box .delete-after-button', function () {
        var form_data = new FormData();
        form_data.append( 'page', 'after' );
        form_data.append( 'item', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#delete_search_after_url' ).val(),
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