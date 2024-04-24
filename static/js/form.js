var week = ['日', '月', '火', '水', '木', '金', '土'];

$( function() {
    $( document ).on( 'click', '.input-select-dropdown .dropdown-item', function () {
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).val( $( this ).text() );
        $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).val( $( this ).val() );
    });
    $( document ).on( 'click', '.input-manager-select-dropdown .dropdown-item', function () {
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).val( $( this ).find( 'span' ).text() );
        if ( $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).length ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).val( $( this ).val() );
        }
    });
    $( document ).on( 'click', '.input-color-select-dropdown .dropdown-item', function () {
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).attr( 'placeholder', '' );
        $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).prev().remove();
        if ( $( this ).val() == '0' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #fff; background-color: #666f86; border-radius: 50%;"></label>' );
        } else if ( $( this ).val() == '1' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #666f86; background-color: #fff; border: 1px solid #666f86; border-radius: 50%;"></label>' );
        } else if ( $( this ).val() == '2' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #fff; background-color: #eb4e3d; border-radius: 50%;"></label>' );
        } else if ( $( this ).val() == '3' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #fff; background-color: #ed8537; border-radius: 50%;"></label>' );
        } else if ( $( this ).val() == '4' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #fff; background-color: #00B900; border-radius: 50%;"></label>' );
        } else if ( $( this ).val() == '5' ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=text]' ).before( '<label class="btn mb-0" style="position: absolute; top: 15%; left: 15%; width: 26px; height: 26px; color: #fff; background-color: #5b82db; border-radius: 50%;"></label>' );
        }
        if ( $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).length ) {
            $( this ).parents( '.dropdown' ).find( 'input[type=hidden]' ).val( $( this ).val() );
        }
    });
});