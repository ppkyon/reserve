$( function() {
    $( '.table-control-area .search-input' ).on( 'keyup', function() {
        var form_data = new FormData();
        form_data.append( 'text', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#table_search_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            var total = 0;
            $( '.table-area .table tbody' ).empty();
            $.each( response, function( index, value ) {
                $( '.table-area .table tbody' ).append( append_table_area(value) );
                total = value.total;
            });
            $( '#table_total_count' ).val( total );
            append_paging_area(1, total);
        }).fail( function(){
            
        });
    });

    $( '.table-control-area .input-select-table-number-dropdown .dropdown-menu button' ).on( 'click', function() {
        var form_data = new FormData();
        form_data.append( 'number', $( this ).val() );
        form_data.append( 'url', location.pathname );
        $.ajax({
            'data': form_data,
            'url': $( '#table_number_url' ).val(),
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

    $( document ).on( 'click', '.table-paging-area ul li button', function () {
        $( '.table-area .table tbody' ).css( 'opacity', '0' );
        $( '.table-loader-area' ).css( 'opacity', '1' );
        
        var target = Number($( this ).val());

        var form_data = new FormData();
        form_data.append( 'shop_id', $( '#login_shop_id' ).val() );
        form_data.append( 'page', target );
        $.ajax({
            'data': form_data,
            'url': $( '#table_paging_url' ).val(),
            'type': 'POST',
            'dataType': 'json',
            'processData': false,
            'contentType': false,
        }).done( function( response ){
            setTimeout( function() {
                $( '.table-area .table tbody' ).empty();
                $.each( response, function( index, value ) {
                    $( '.table-area .table tbody' ).append( append_table_area(value) );
                });
                append_paging_area(Number(target), Number($( '#table_total_count' ).val()));
                $( '.table-area .table tbody' ).css( 'opacity', '1' );
                $( '.table-loader-area' ).css( 'opacity', '0' );
            }, 750 );
        }).fail( function(){
            setTimeout( function() {
                $( '.table-area .table tbody' ).css( 'opacity', '1' );
                $( '.table-loader-area' ).css( 'opacity', '0' );
            }, 750 );
        });
    });
});

function append_paging_area( target, total ) {
    var number = Number($( '#table_number' ).val());
    var page = Math.ceil( total / number );

    var start = number * ( target - 1 ) + 1;
    var end = number * target;
    if ( end > total ) {
        end = total;
    }
    
    $( '.table-paging-area div' ).empty();
    if ( total != 0 ) {
        var html = '<p class="me-3 mb-0">ALL DATA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + start + ' - ' + end + ' / ' + total + '</p>';
        html += '<ul class="pagination d-flex m-0 p-0"></ul>';
        $( '.table-paging-area div' ).append(html);
    
        html = '';
        if ( page != 1 || end < total ) {
            if ( target == 1 ) {
                html += '<li class="page-item d-inline active">';
                html += '<button type="button" value="1" class="btn d-flex justify-content-center align-items-center position-relative" disabled>';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/paging-left.svg">';
                html += '</button>';
                html += '</li>';
            } else {
                html += '<li class="page-item d-inline">';
                html += '<button type="button" value="' + ( target - 1 ) + '" class="btn d-flex justify-content-center align-items-center position-relative">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/paging-left.svg">';
                html += '</button>';
                html += '</li>';
            }
    
            if ( page > 5 && target > 3 ) {
                if ( ( page - 2 ) < target ) {
                    for ( var i = ( page - 4 ); i <= page; i++ ) {
                        if ( target == i ) {
                            html += '<li class="page-item d-inline active">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative" disabled>';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        } else {
                            html += '<li class="page-item d-inline">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative">';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        }
                    }
                } else {
                    for ( var i = ( target - 2 ); i <= ( target + 2 ); i++ ) {
                        if ( target == i ) {
                            html += '<li class="page-item d-inline active">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative" disabled>';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        } else {
                            html += '<li class="page-item d-inline">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative">';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        }
                    }
                }
            } else {
                if ( target == 1 ) {
                    html += '<li class="page-item d-inline active">';
                    html += '<button type="button" value="1" class="btn d-flex justify-content-center align-items-center position-relative" disabled>1</button>';
                    html += '</li>';
                } else {
                    html += '<li class="page-item d-inline">';
                    html += '<button type="button" value="1" class="btn d-flex justify-content-center align-items-center position-relative">1</button>';
                    html += '</li>';
                }
                if ( target == 2 ) {
                    html += '<li class="page-item d-inline active">';
                    html += '<button type="button" value="2" class="btn d-flex justify-content-center align-items-center position-relative" disabled>2</button>';
                    html += '</li>';
                } else {
                    html += '<li class="page-item d-inline">';
                    html += '<button type="button" value="2" class="btn d-flex justify-content-center align-items-center position-relative">2</button>';
                    html += '</li>';
                }
                for ( var i = 3; i <= 5; i++ ) {
                    if ( page >= i ) {
                        if ( target == i ) {
                            html += '<li class="page-item d-inline active">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative" disabled>';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        } else {
                            html += '<li class="page-item d-inline">';
                            html += '<button type="button" value="' + i + '" class="btn d-flex justify-content-center align-items-center position-relative">';
                            html += i;
                            html += '</button>';
                            html += '</li>';
                        }
                    }
                }
            }
    
            if ( page == target ) {
                html += '<li class="page-item d-inline active">';
                html += '<button type="button" value="' + ( target + 1 ) + '" class="btn d-flex justify-content-center align-items-center position-relative" disabled>';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/paging-right.svg">';
                html += '</li>';
            } else {
                html += '<li class="page-item d-inline">';
                html += '<button type="button" value="' + ( target + 1 ) + '" class="btn d-flex justify-content-center align-items-center position-relative">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/paging-right.svg">';
                html += '</li>';
            }
        }
        $( '.table-paging-area div ul' ).append(html);
    } else {
        var html = '<p class="me-3 mb-0">ALL DATA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 - 0 / 0</p>';
        html += '<ul class="pagination d-flex m-0 p-0"></ul>';
        $( '.table-paging-area div' ).append(html);
    }
}