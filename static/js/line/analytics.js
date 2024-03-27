$( function() {
    liff.init( {
        liffId: $( '#liff_id' ).val(),
    }).then( () => {
        if ( !liff.isLoggedIn() ) {
            window.open('/qrcode/display/' + $( '#shop_id' ).val(),'_self');
        } 
        if ( liff.isInClient() ) {
            var form_data = new FormData();
            form_data.append( 'shop_id', $( '#shop_id' ).val() );
            form_data.append( 'user_id', liff.getContext().userId );
            form_data.append( 'id', $( '#id' ).val() );
            form_data.append( 'number', $( '#number' ).val() );
            form_data.append( 'type', $( '#type' ).val() );
            form_data.append( 'csrfmiddlewaretoken', $( '#csrf_token' ).val() );
            $.ajax({
                'data': form_data,
                'url': $( '#url_form' ).val(),
                'type': 'POST',
                'dataType': 'json',
                'processData': false,
                'contentType': false,
            }).done( function( response ){
                if ( response.url != null && response.url != undefined && response.url != '' ) {
                    if ( response.type == 2 ) {
                        $( 'main' ).removeClass( 'm-3' );
                        $( 'video' ).attr( 'src', response.url );
                        $( '.row' ).removeClass( 'd-none' );
                    } else {
                        window.location.href = response.url;
                    }
                }
                window.addEventListener( "popstate", function(e) {
                    history.pushState( null, null, null );
                    return;
                });
            }).fail( function(){
                liff.closeWindow();
            });
        }
    }).catch( ( err ) => {
        window.open('about:blank','_self').close();
    });
});