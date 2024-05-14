var save_data = new Array();
var save_success = new Array();
var save_error = new Array();

$( function() {
    if ( $( '#save_place_form' ).length ) {
        $( '#save_place_form' ).parsley();
        $( '#save_place_form' ).parsley().options.requiredMessage = "入力してください";
    }
    if ( $( '#save_course_form' ).length ) {
        $( '#save_course_form' ).parsley();
        $( '#save_course_form' ).parsley().options.requiredMessage = "入力してください";
    }

    save_data.place = function() {
        var form_data = new FormData();
        form_data.append( 'offline_name', $( '#save_place_form [name=offline_name]' ).val() );
        form_data.append( 'offline_outline', $( '#save_place_form [name=offline_outline]' ).val() );
        form_data.append( 'online_name', $( '#save_place_form [name=online_name]' ).val() );
        form_data.append( 'online_outline', $( '#save_place_form [name=online_outline]' ).val() );

        form_data.append( 'offline_course_count', $( '#save_place_form .course-table.offline tbody tr' ).length );
        $( '#save_place_form .course-table.offline tbody tr' ).each( function( index ,value ) {
            form_data.append( 'offline_course_id_' + (index+1), $( this ).find( '.input-course-id' ).val() );
            form_data.append( 'offline_course_title_' + (index+1), $( this ).find( '.input-course-title' ).val() );
            form_data.append( 'offline_course_outline_' + (index+1), $( this ).find( '.input-course-outline' ).val() );
            form_data.append( 'offline_course_start_' + (index+1), $( this ).find( '.input-course-start' ).val() );
            form_data.append( 'offline_course_deadline_' + (index+1), $( this ).find( '.input-course-deadline' ).val() );
            form_data.append( 'offline_course_on_time_' + (index+1), $( this ).find( '.input-course-on-time' ).val() );
            form_data.append( 'offline_course_any_day_' + (index+1), $( this ).find( '.input-course-any-day' ).val() );
            form_data.append( 'offline_course_any_time_' + (index+1), $( this ).find( '.input-course-any-time' ).val() );
            form_data.append( 'offline_course_method_' + (index+1), $( this ).find( '.input-course-method' ).val() );
            form_data.append( 'offline_course_business_check_1_' + (index+1), $( this ).find( '.input-course-business-check-1' ).val() );
            form_data.append( 'offline_course_business_check_2_' + (index+1), $( this ).find( '.input-course-business-check-2' ).val() );
            form_data.append( 'offline_course_business_check_3_' + (index+1), $( this ).find( '.input-course-business-check-3' ).val() );
            form_data.append( 'offline_course_business_check_4_' + (index+1), $( this ).find( '.input-course-business-check-4' ).val() );
            form_data.append( 'offline_course_business_check_5_' + (index+1), $( this ).find( '.input-course-business-check-5' ).val() );
            form_data.append( 'offline_course_business_check_6_' + (index+1), $( this ).find( '.input-course-business-check-6' ).val() );
            form_data.append( 'offline_course_business_check_7_' + (index+1), $( this ).find( '.input-course-business-check-7' ).val() );
        });
        form_data.append( 'online_course_count', $( '#save_place_form .course-table.online tbody tr' ).length );
        $( '#save_place_form .course-table.online tbody tr' ).each( function( index ,value ) {
            form_data.append( 'online_course_id_' + (index+1), $( this ).find( '.input-course-id' ).val() );
            form_data.append( 'online_course_title_' + (index+1), $( this ).find( '.input-course-title' ).val() );
            form_data.append( 'online_course_outline_' + (index+1), $( this ).find( '.input-course-outline' ).val() );
            form_data.append( 'online_course_start_' + (index+1), $( this ).find( '.input-course-start' ).val() );
            form_data.append( 'online_course_deadline_' + (index+1), $( this ).find( '.input-course-deadline' ).val() );
            form_data.append( 'online_course_on_time_' + (index+1), $( this ).find( '.input-course-on-time' ).val() );
            form_data.append( 'online_course_any_day_' + (index+1), $( this ).find( '.input-course-any-day' ).val() );
            form_data.append( 'online_course_any_time_' + (index+1), $( this ).find( '.input-course-any-time' ).val() );
            form_data.append( 'online_course_method_' + (index+1), $( this ).find( '.input-course-method' ).val() );
            form_data.append( 'online_course_business_check_1_' + (index+1), $( this ).find( '.input-course-business-check-1' ).val() );
            form_data.append( 'online_course_business_check_2_' + (index+1), $( this ).find( '.input-course-business-check-2' ).val() );
            form_data.append( 'online_course_business_check_3_' + (index+1), $( this ).find( '.input-course-business-check-3' ).val() );
            form_data.append( 'online_course_business_check_4_' + (index+1), $( this ).find( '.input-course-business-check-4' ).val() );
            form_data.append( 'online_course_business_check_5_' + (index+1), $( this ).find( '.input-course-business-check-5' ).val() );
            form_data.append( 'online_course_business_check_6_' + (index+1), $( this ).find( '.input-course-business-check-6' ).val() );
            form_data.append( 'online_course_business_check_7_' + (index+1), $( this ).find( '.input-course-business-check-7' ).val() );
        });
        return form_data;
    }
    save_success.place = function(modal) {
        $( '#save_check_modal .yes-button' ).val( 'place' );
        $( modal ).trigger( 'click' );
        up_modal();
    };
    save_error.place = function( message='' ) {
        
    };
});