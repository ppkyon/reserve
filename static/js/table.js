$( function() {
    $( '.table-area .table .sort-area' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'target', $( this ).find( 'button' ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#table_sort_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            window.location.reload();
        }).fail( function(){
            window.location.reload();
        });
    });
    
    $( document ).on( 'click', '.table-area .table tbody tr', function () {
        if ( !$( this ).parents( '.table' ).hasClass( 'parent-table' ) && !$( this ).parents( '.table' ).hasClass( 'children-table' ) ) {
            if ( $( this ).parents( '.table' ).length ) {
                $( '.table-area .table tbody tr' ).each( function() {
                    $( this ).removeClass( 'active' );
                });
                $( this ).addClass( 'active' );
            }
        }
    });

    $( document ).on( 'click', '.table-area .table tbody .favorite-icon', function () {
        if ( $( this ).parent().find( 'form' ).length ) {
            var target = $( this );
            var form_data = new FormData();
            form_data.append( 'id', $( this ).parents( 'td' ).find( 'form [name=id]' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( this ).parents( 'td' ).find( 'form' ).attr( 'action' ),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                $( target ).parent().find( 'img' ).each( function( index, value ) {
                    if ( response.check ) {
                        if ( index == 0 ) {
                            $( this ).addClass( 'd-none' );
                        } else if ( index == 1 ) {
                            $( this ).removeClass( 'd-none' );
                        }
                    } else {
                        if ( index == 0 ) {
                            $( this ).removeClass( 'd-none' );
                        } else if ( index == 1 ) {
                            $( this ).addClass( 'd-none' );
                        }
                    }
                });
                $( target ).parent().find( 'button' ).each( function( index, value ) {
                    if ( response.check ) {
                        if ( index == 0 ) {
                            $( this ).trigger( 'click' );
                        }
                    } else {
                        if ( index == 1 ) {
                            $( this ).trigger( 'click' );
                        }
                    }
                });
            }).fail( function(){
                window.location.reload();
            });
        }
    });
});