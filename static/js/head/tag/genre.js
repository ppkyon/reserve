var delete_data = new Array();

$( function() {
    $( document ).on( 'click', '.table-control-area .add-genre-button', function () {
        $( '.table-area .tag-table tbody' ).empty();
        $( '.table-area .genre-table tr' ).each( function() {
            $( this ).css( 'background-color', '#FFF' );
            $( this ).removeClass( 'active' );
        });
        $( '.table-area .genre-table tbody' ).prepend( append_genre() );
        $( '.table-area .genre-table input[type="text"]' ).focus();
    });

    $( document ).on( 'click', '.table-area .genre-table tbody tr', function () {
        if ( !$( this ).hasClass( 'active' ) ) {

            $( this ).parent().find( 'tr' ).each( function( index, value ) {
                $( this ).css( 'background-color', '#FFF' );
                $( this ).removeClass( 'active' );
            });
            $( this ).css( 'background-color', '' );
            $( this ).addClass( 'active' );

            $( '.table-area .tag-table tbody' ).css( 'opacity', '0' );
            $( '.table-loader-area' ).css( 'opacity', '1' );
    
            var target = $( this )
            var form_data = new FormData();
            form_data.append( 'id', $( this ).children( 'input' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#get_genre_url' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                setTimeout( function() {
                    append_tag_list( response, target );
                    $( '.table-area .tag-table tbody' ).css( 'opacity', '1' );
                    $( '.table-loader-area' ).css( 'opacity', '0' );
                }, 750 );
            }).fail( function(){
                setTimeout( function() {
                    $( '.table-area .tag-table tbody' ).css( 'opacity', '1' );
                    $( '.table-loader-area' ).css( 'opacity', '0' );
                }, 750 );
            });
        }
    });

    $( document ).on( 'blur', '.table-area .genre-table input[type="text"]', function () {
        var target = $( this );
        var form_data = new FormData();
        form_data.append( 'shop_id', $( '#login_shop_id' ).val() );
        form_data.append( 'id', $( this ).parents( 'tr' ).children( 'input' ).val() );
        form_data.append( 'name', $( this ).val() );
        $.ajax({
            'data': form_data,
            'url': $( '#save_genre_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            if ( response.id == '' ) {
                $( target ).parents( 'tr' ).remove();
                $( '.table-area .genre-table tbody tr' ).eq(0).addClass( 'active' );
                $( '.table-area .genre-table tbody tr' ).eq(0).css( 'background-color', '' );
            } else {
                $( target ).parents( 'tr' ).children( 'input' ).val( response.id );
                $( target ).parents( 'tr' ).find( 'form' ).eq(1).attr( 'id', 'delete_genre_' + response.id + '_form' );
                $( target ).parents( 'tr' ).find( 'form [name=id]' ).val( response.id );
                $( target ).parents( 'tr' ).find( '.dropdown' ).children( 'button' ).attr( 'id', 'dropdown_' + response.id );
                $( target ).parents( 'tr' ).find( '.dropdown .dropdown-menu' ).attr( 'aria-labelledby', 'dropdown_' + response.id );
                $( target ).parents( 'tr' ).find( '.dropdown .dropdown-menu .delete-button' ).val( 'genre_' + response.id );
                $( target ).parent().append( '<p class="content-title mb-0">' + $( target ).val() + '(' + response.count + ')</p>' );
                $( target ).remove();
            }
        }).fail( function(){
            
        });
    });

    $( document ).on( 'click', '.table-area .genre-table .dropdown .edit-button', function () {
        var text = $( this ).parents( 'tr' ).find( 'td' ).eq(0).find( 'p' ).text().split( '(' )[0];
        $( this ).parents( 'tr' ).find( 'td' ).eq(0).children( 'div' ).append( '<input type="text" class="input-text" value="' + text + '">' );
        $( this ).parents( 'tr' ).find( 'td' ).eq(0).find( 'p' ).remove();
        $( '.table-area .genre-table input[type="text"]' ).focus();
    });

    $( document ).on( 'click', '.table-area .genre-table .dropdown .delete-button', function () {
        $( '#delete_check_modal .modal-body .col-12 .modal-description-area' ).remove();
        $( '#delete_check_modal .modal-body .col-12' ).append( '<div class="modal-description-area ps-3 pe-3"><p class="modal-description mb-0">このジャンルに属するタグもすべて削除されます。</p></div>' );
    });

    delete_data.genre = function(id) {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_genre_' + id + '_form [name=id]' ).val() );
        return form_data;
    };
});