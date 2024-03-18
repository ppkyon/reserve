var save_data = new Array();
var save_success = new Array();
var save_error = new Array();
var delete_data = new Array();
var copy_data = new Array();

$( function() {
    if ( $( '#save_question_form' ).length ) {
        $( '#save_question_form' ).parsley();
        $( '#save_question_form' ).parsley().options.requiredMessage = "入力してください";
        $( '#save_question_form' ).parsley().options.typeMessage = "正しい形式で入力してください";
    }

    save_data.question = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_question_form [name=id]' ).val() );
        form_data.append( 'title', $( '#save_question_form [name=title]' ).val() );
        form_data.append( 'name', $( '#save_question_form [name=name]' ).val() );
        form_data.append( 'description', $( '#save_question_form [name=description]' ).val() );
        form_data.append( 'color', $( '#save_question_form [name=color]' ).val() );
        form_data.append( 'count', $( '#save_question_form .display-area' ).length );
        if ( $( '#save_question_form [name=favorite]' ).prop( 'checked' ) ) {
            form_data.append( 'favorite', 1 );
        } else {
            form_data.append( 'favorite', 0 );
        }
        $( '#save_question_form .display-area' ).each( function( index, value ) {
            var number = index + 1;
            form_data.append( 'number', number );
            form_data.append( 'title_' + number, $( this ).find( '.input-name' ).val() );
            form_data.append( 'description_' + number, $( this ).find( '.input-description' ).val() );
            if ( $( this ).find( '.item-area .col-6' ).length - 1 >= 0 ) {
                if ( !$( this ).find( '.item-area .col-6' ).eq(0).find( 'input' ).prop( 'disabled' ) ) {
                    form_data.append( 'choice_count_' + number, $( this ).find( '.item-area .col-6' ).length - 1 );
                } else {
                    form_data.append( 'choice_count_' + number, 0 );
                }
            } else {
                form_data.append( 'choice_count_' + number, 0 );
            }
            if ( $( this ).find( '.input-required' ).prop( 'checked' ) ) {
                form_data.append( 'required_' + number, 1 );
            } else {
                form_data.append( 'required_' + number, 0 );
            }

            if ( $( this ).find( '.item-area .col-6' ).length - 1 > 0 ) {
                $( this ).find( '.item-area .col-6' ).each( function( index, value ) {
                    if ( !$( this ).find( 'input' ).prop( 'disabled' ) ) {
                        form_data.append( 'choice_text_' + number + '_' + ( index + 1 ), $( this ).find( 'input' ).val() );
                    }
                });
            }
            
            form_data.append( 'type_' + number, $( this ).find( '.input-type' ).next().val() );
            if ( $( this ).find( '.input-type' ).next().val() == '51' ) {
                var count = 0;
                $( this ).find( '.item-area .col-6' ).each( function( index, value ) {
                    if ( $( this ).find( 'input' ).val() != null && $( this ).find( 'input' ).val() != undefined && $( this ).find( 'input' ).val() != '' ) {
                        form_data.append( 'choice_text_' + number + '_' + ( index + 1 ), $( this ).find( 'input' ).val() );
                        count++;
                    }
                });
                form_data.append( 'choice_count_' + number, count );
            }

            if ( check_empty( $( this ).find( '.input-question' ).next().val() ) ) {
                form_data.append( 'choice_type_' + number, $( this ).find( '.input-question' ).next().val() );
            } else {
                form_data.append( 'choice_type_' + number, 0 );
            }
        });

        return form_data;
    };
    save_success.question = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'question' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.question = function( message='' ) {
        
    };

    delete_data.question = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#delete_question_form [name=id]' ).val() );
        return form_data;
    };

    copy_data.question = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '#save_question_form [name=id]' ).val() );
        return form_data;
    };
});