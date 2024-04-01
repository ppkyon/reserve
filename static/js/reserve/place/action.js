$( function() {
    $( document ).on( 'click', '.add-course-modal-button', function () {
        $( '#save_course_modal .modal-title' ).text( 'コースを追加' );
        
        $( '#save_course_modal [name=title]' ).val( '' );
        $( '#save_course_modal [name=outline]' ).val( '' );
        $( '#save_course_modal [name=start]' ).val( '' );
        $( '#save_course_modal [name=start]' ).next().val( '' );
        $( '#save_course_modal [name=on_time]' ).val( '' );
        $( '#save_course_modal [name=on_time]' ).next().val( '' );
        $( '#save_course_modal [name=any_day]' ).val( '' );
        $( '#save_course_modal [name=any_day]' ).next().val( '' );
        $( '#save_course_modal [name=any_time]' ).val( '' );
        $( '#save_course_modal [name=any_time]' ).next().val( '' );
        $( '#save_course_modal [name=method]' ).val( '' );
        $( '#save_course_modal [name=method]' ).next().val( '' );

        $( '#save_course_modal [name=deadline]' ).each( function( index, value ) {
            if ( $( this ).val() == '1' ) {
                $( this ).prop( 'checked', true );
            }
        });
        $( '#save_course_modal [name=on_time]' ).prop( 'disabled', false );
        $( '#save_course_modal [name=on_time]' ).removeClass( 'readonly' );
        $( '#save_course_modal [name=any_day]' ).prop( 'disabled', true );
        $( '#save_course_modal [name=any_day]' ).addClass( 'readonly' );
        $( '#save_course_modal [name=any_time]' ).prop( 'disabled', true );
        $( '#save_course_modal [name=any_time]' ).addClass( 'readonly' );

        for ( var i = 1; i <= 7; i ++ ) {
            $( '#save_course_modal [name=business_check_' + i + ']' ).prop( 'checked', false );
        }

        $( '#save_course_modal .add-course-button' ).val( $( this ).val() );
        $( '#save_course_modal .add-course-button' ).removeClass( 'd-none' );
        $( '#save_course_modal .save-course-button' ).addClass( 'd-none' );
        $( this ).next().trigger( 'click' );
    });
    $( document ).on( 'click', '.detail-course-button', function () {
        $( '#save_course_modal .modal-title' ).text( 'コース詳細' );
        
        var table = $( this ).parents( 'tr.position-relative' );
        $( '#save_course_modal [name=title]' ).val( $( table ).find( '.input-course-title' ).val() );
        $( '#save_course_modal [name=outline]' ).val( $( table ).find( '.input-course-outline' ).val() );
        if ( check_empty($( table ).find( '.input-course-start' ).val()) ) {
            $( '#save_course_modal [name=start]' ).val( $( table ).find( '.input-course-start' ).val() + '週間' );
        } else {
            $( '#save_course_modal [name=start]' ).val( '' );
        }
        $( '#save_course_modal [name=start]' ).next().val( $( table ).find( '.input-course-start' ).val() );
        if ( $( table ).find( '.input-course-on-time' ).val() == '1' ) {
            $( '#save_course_modal [name=on_time]' ).val( '直前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '30' ) {
            $( '#save_course_modal [name=on_time]' ).val( '30分前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '60' ) {
            $( '#save_course_modal [name=on_time]' ).val( '1時間前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '90' ) {
            $( '#save_course_modal [name=on_time]' ).val( '1時間30分前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '120' ) {
            $( '#save_course_modal [name=on_time]' ).val( '2時間前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '150' ) {
            $( '#save_course_modal [name=on_time]' ).val( '2時間30分前' );
        } else if ( $( table ).find( '.input-course-on-time' ).val() == '180' ) {
            $( '#save_course_modal [name=on_time]' ).val( '3時間前' );
        } else {
            $( '#save_course_modal [name=on_time]' ).val( '' );
        }
        $( '#save_course_modal [name=on_time]' ).next().val( $( table ).find( '.input-course-on-time' ).val() );
        if ( check_empty($( table ).find( '.input-course-any-day' ).val()) ) {
            $( '#save_course_modal [name=any_day]' ).val( $( table ).find( '.input-course-any-day' ).val() + '日前' );
        } else {
            $( '#save_course_modal [name=any_day]' ).val( '' );
        }
        $( '#save_course_modal [name=any_day]' ).next().val( $( table ).find( '.input-course-any-day' ).val() );
        if ( check_empty($( table ).find( '.input-course-any-time' ).val()) ) {
            $( '#save_course_modal [name=any_time]' ).val( $( table ).find( '.input-course-any-time' ).val() + '時' );
        } else {
            $( '#save_course_modal [name=any_time]' ).val( '' );
        }
        $( '#save_course_modal [name=any_time]' ).next().val( $( table ).find( '.input-course-any-time' ).val() );
        if ( $( table ).find( '.input-course-method' ).val() == '1' ) {
            $( '#save_course_modal [name=method]' ).val( '日数で計算' );
        } else if ( $( table ).find( '.input-course-method' ).val() == '2' ) {
            $( '#save_course_modal [name=method]' ).val( '営業日で計算(休業日を含まない)' );
        }
        $( '#save_course_modal [name=method]' ).next().val( $( table ).find( '.input-course-method' ).val() );

        $( '#save_course_modal [name=deadline]' ).each( function( index, value ) {
            if ( $( this ).val() == $( table ).find( '.input-course-deadline' ).val() ) {
                $( this ).prop( 'checked', true );
            }
        });
        if ( $( table ).find( '.input-course-deadline' ).val() == '1' ) {
            $( '#save_course_modal [name=on_time]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=on_time]' ).removeClass( 'readonly' );
            $( '#save_course_modal [name=any_day]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=any_day]' ).addClass( 'readonly' );
            $( '#save_course_modal [name=any_time]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=any_time]' ).addClass( 'readonly' );
        } else if ( $( table ).find( '.input-course-deadline' ).val() == '2' ) {
            $( '#save_course_modal [name=on_time]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=on_time]' ).addClass( 'readonly' );
            $( '#save_course_modal [name=any_day]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=any_day]' ).removeClass( 'readonly' );
            $( '#save_course_modal [name=any_time]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=any_time]' ).removeClass( 'readonly' );
        }

        for ( var i = 1; i <= 7; i ++ ) {
            if ( $( table ).find( '.input-course-business-check-' + i ).val() == '1' ) {
                $( '#save_course_modal [name=business_check_' + i + ']' ).prop( 'checked', true );
            }
        }

        $( '#save_course_modal .save-course-button' ).val( $( this ).val() );
        $( '#save_course_modal .add-course-button' ).addClass( 'd-none' );
        $( '#save_course_modal .save-course-button' ).removeClass( 'd-none' );
        $( this ).next().trigger( 'click' );
    });

    $( document ).on( 'click', '.delete-course-button', function () {
        $( this ).parents( 'tr.position-relative' ).remove();
    });
    
    $( document ).on( 'change', '#save_course_modal [name=deadline]', function () {
        if ( $( this ).val() == '1' ) {
            $( '#save_course_modal [name=on_time]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=on_time]' ).removeClass( 'readonly' );
            $( '#save_course_modal [name=any_day]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=any_day]' ).addClass( 'readonly' );
            $( '#save_course_modal [name=any_time]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=any_time]' ).addClass( 'readonly' );
        } else if ( $( this ).val() == '2' ) {
            $( '#save_course_modal [name=on_time]' ).prop( 'disabled', true );
            $( '#save_course_modal [name=on_time]' ).addClass( 'readonly' );
            $( '#save_course_modal [name=any_day]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=any_day]' ).removeClass( 'readonly' );
            $( '#save_course_modal [name=any_time]' ).prop( 'disabled', false );
            $( '#save_course_modal [name=any_time]' ).removeClass( 'readonly' );
        }
    });
    $( '#save_course_modal .add-course-button' ).on( 'click', function() {
        if ( $( '#save_course_form' ).parsley().validate() ) {
            var value = $( this ).val();
            $( '.course-table.' + value + ' tbody' ).append( append_course_area(value) );
            $( '#save_course_modal .btn-close' ).trigger( 'click' );
        }
    });
    $( '#save_course_modal .save-course-button' ).on( 'click', function() {
        if ( $( '#save_course_form' ).parsley().validate() ) {
            var value = $( this ).val();
            value = value.split('_');
            var number = value[1];
            value = value[0];

            var table = $( '.course-table.' + value + ' tbody tr' ).eq(Number(number)-1);
            $( table ).find( '.input-course-title' ).val( $( '#save_course_modal [name=title]' ).val() );
            $( table ).find( '.input-course-outline' ).val( $( '#save_course_modal [name=outline]' ).val() );
            $( table ).find( '.input-course-start' ).val( $( '#save_course_modal [name=start]' ).next().val() );
            $( table ).find( '.input-course-deadline' ).val( $( '#save_course_modal [name=deadline]:checked' ).val() );
            $( table ).find( '.input-course-on-time' ).val( $( '#save_course_modal [name=on_time]' ).next().val() );
            $( table ).find( '.input-course-any-day' ).val( $( '#save_course_modal [name=any_day]' ).next().val() );
            $( table ).find( '.input-course-any-time' ).val( $( '#save_course_modal [name=any_time]' ).next().val() );
            $( table ).find( '.input-course-method' ).val( $( '#save_course_modal [name=method]' ).next().val() );

            if ( $( '#save_course_modal [name=business_check_1]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-1' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-1' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_2]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-2' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-2' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_3]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-3' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-3' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_4]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-4' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-4' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_5]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-5' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-5' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_6]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-6' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-6' ).val( '0' );
            }
            if ( $( '#save_course_modal [name=business_check_7]' ).prop( 'checked' ) ) {
                $( table ).find( '.input-course-business-check-7' ).val( '1' );
            } else {
                $( table ).find( '.input-course-business-check-7' ).val( '0' );
            }
            $( '#save_course_modal .btn-close' ).trigger( 'click' );
        }
    });
});