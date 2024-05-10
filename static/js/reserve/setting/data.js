var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    flatpickr( '#meeting_create_date', {
        "locale": "ja",
        dateFormat : 'Y/m/d',
    });

    if ( $( '#save_setting_form' ).length ) {
        $( '#save_setting_form' ).parsley();
        $( '#save_setting_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.setting = function() {
        var form_data = new FormData();
        form_data.append( 'id', $( '.save-button' ).next().val() );
        form_data.append( 'count', $( '#' + $( '.save-button' ).next().val() ).find( '.reserve-setting-table' ).children( 'tbody' ).children( 'tr' ).length );

        $( '#' + $( '.save-button' ).next().val() ).find( '.reserve-setting-table' ).children( 'tbody' ).children( 'tr' ).each( function( index, value ) {
            var random = $( this ).find( '.count-text' ).next().val();
            form_data.append( 'random_' + ( index + 1 ), random );
            form_data.append( 'title_' + ( index + 1 ), $( this ).find( 'input[name=title_' + random + ']' ).val() );
            form_data.append( 'name_' + ( index + 1 ), $( this ).find( 'input[name=name_' + random + ']' ).val() );
            form_data.append( 'outline_' + ( index + 1 ), $( this ).find( 'input[name=outline_' + random + ']' ).val() );
            form_data.append( 'note_' + ( index + 1 ), $( this ).find( '[name=note_' + random + ']' ).val() );
            form_data.append( 'time_' + ( index + 1 ), $( this ).find( 'input[name=time_' + random + ']' ).next().val() );
            form_data.append( 'people_' + ( index + 1 ), $( this ).find( 'input[name=people_' + random + ']' ).next().val() );
            form_data.append( 'facility_' + ( index + 1 ), $( this ).find( 'input[name=facility_' + random + ']' ).next().val() );
            form_data.append( 'question_' + ( index + 1 ), $( this ).find( 'input[name=question_' + random + ']' ).next().val() );
            form_data.append( 'advance_' + ( index + 1 ), $( this ).find( 'input[name=advance_' + random + ']' ).next().val() );
            form_data.append( 'unit_' + ( index + 1 ), $( this ).find( 'input[name=unit_' + random + ']:checked' ).val() );
            if ( $( this ).find( 'input[name=display_flg_' + random + ']' ).prop( 'checked' ) ) {
                form_data.append( 'display_flg_' + ( index + 1 ), 1 );
            } else {
                form_data.append( 'display_flg_' + ( index + 1 ), 0 );
            }
            if ( $( this ).find( 'input[name=course_flg_' + random + ']' ).prop( 'checked' ) ) {
                form_data.append( 'course_flg_' + ( index + 1 ), 1 );
            } else {
                form_data.append( 'course_flg_' + ( index + 1 ), 0 );
            }

            form_data.append( 'meeting_count_' + ( index + 1 ), $( this ).find( '.meeting-table-area table tbody tr' ).length );
            $( this ).find( '.meeting-table-area table tbody tr' ).each( function( meeting_index, meeting_value ) {
                form_data.append( 'meeting_name_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-name' ).val() );
                form_data.append( 'meeting_url_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-url' ).val() );
                form_data.append( 'meeting_platform_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-platform' ).val() );
                form_data.append( 'meeting_platform_text_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-platform-text' ).val() );
                form_data.append( 'meeting_start_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-start' ).val() );
                form_data.append( 'meeting_status_' + ( index + 1 ) + '_' + ( meeting_index + 1 ), $( this ).find( '.input-meeting-status' ).val() );
            });
        });
        return form_data;
    }
    save_success.setting = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'setting' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.setting = function( message='' ) {
        
    };
});