var delete_data = new Array();

$( function() {
    $( '.table-control-area .add-tag-button' ).on( 'click', function() {
        if ( $( '.table-area .genre-table .active' ).length ) {
            $( '.table-area .tag-table tr' ).each( function() {
                $( this ).css( 'background-color', '#FFF' );
                $( this ).removeClass( 'active' );
            });
            $( '.table-area .tag-table tbody' ).prepend( append_tag() );
            $( '.table-area .tag-table input[type="text"]' ).focus();
        }
    });

    $( '.table-control-area .tag-search' ).on( 'keyup', function() {
        var target = $( '.table-area .genre-table .active' )
        var form_data = new FormData();
        form_data.append( 'id', $( target ).children( 'input' ).val() );
        form_data.append( 'text', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#search_tag_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            append_tag_list( response, target );
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.table-area .tag-table tbody tr', function () {
        if ( !$( this ).hasClass( 'active' ) ) {
            $( this ).parent().find( 'tr' ).each( function( index, value ) {
                $( this ).css( 'background-color', '#FFF' );
                $( this ).removeClass( 'active' );
            });
            $( this ).css( 'background-color', '' );
            $( this ).addClass( 'active' );
        }
    });

    $( document ).on( 'blur', '.table-area .tag-table input[type="text"]', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'id', $( this ).parents( 'tr' ).children( 'input' ).val() );
        form_data.append( 'genre', $( '.table-area .genre-table .active' ).children( 'input' ).val() );
        form_data.append( 'name', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_tag_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( response.id == '' ) {
                $( target ).parents( 'tr' ).remove();
                $( '.table-area .tag-table tbody tr' ).eq(0).addClass( 'active' );
                $( '.table-area .tag-table tbody tr' ).eq(0).css( 'background-color', '' );
            } else {
                $( target ).parents( 'tr' ).children( 'input' ).val( response.id );
                $( target ).parents( 'tr' ).find( 'form' ).eq(1).attr( 'id', 'delete_tag_' + response.id + '_form' );
                $( target ).parents( 'tr' ).find( 'form [name=id]' ).val( response.id );
                $( target ).parents( 'tr' ).find( '.dropdown' ).children( 'button' ).attr( 'id', 'dropdown_' + response.id );
                $( target ).parents( 'tr' ).find( '.dropdown .dropdown-menu' ).attr( 'aria-labelledby', 'dropdown_' + response.id );
                $( target ).parents( 'tr' ).find( '.dropdown .dropdown-menu .delete-button' ).val( 'tag_' + response.id );
                $( target ).parent().append( '<p class="content-title mb-0">' + $( target ).val() + '</p>' );
                $( target ).parent().next().empty();
                $( target ).parent().next().append( '<p class="content-title mb-0">' + response.date + '</p>' );

                var genre = $( '.table-area .genre-table .active td' ).eq(0).find( 'p' ).text().split( '(' )[0];
                var count = $( '.table-area .tag-table tbody tr' ).length - $( '.modal .table-area .tag-table tbody tr' ).length;
                $( '.table-area .genre-table .active td' ).eq(0).find( 'p' ).text( genre + '(' + count + ')' );
                $( target ).remove();
            }
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.table-area .tag-table .dropdown .edit-button', function () {
        var text = $( this ).parents( 'tr' ).find( 'td' ).eq(0).find( 'p' ).text();
        $( this ).parents( 'tr' ).find( 'td' ).eq(0).append( '<input type="text" class="input-text" value="' + text + '">' );
        $( this ).parents( 'tr' ).find( 'td' ).eq(0).find( 'p' ).remove();
        $( '.table-area .tag-table input[type="text"]' ).focus();
    });
    
    $( document ).on( 'click', '.table-area .tag-table .dropdown .delete-button', function () {
        $( '#delete_check_modal .modal-body .col-12 .modal-description-area' ).remove();
    });


    delete_data.tag = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_tag_' + id + '_form [name=id]' ).val() );
        return form_data;
    };
});