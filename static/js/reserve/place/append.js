function append_course_area(value) {
    var number = $( '.course-table.' + value + ' tbody tr' ).length + 1;
    var html = '<tr class="position-relative">';
    html += '<td class="position-relative">';
    html += '<input type="text" value="' + $( '#save_course_modal [name=title]' ).val() + '" class="input-text input-course-title readonly ps-2 pe-2" style="width: 100%;" readonly>';
    html += '<input type="hidden" class="input-course-id" value=""></input>';
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<input type="text" value="' + $( '#save_course_modal [name=outline]' ).val() + '" class="input-text input-course-outline readonly ps-2 pe-2" style="width: 100%;" readonly>';
    html += '</td>';
    html += '<td>';
    html += '<div class="dropdown d-inline-block p-0">';
    html += '<button type="button" class="btn ps-0" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu">';
    html += '<button type="button" value="' + value + '_' + number + '" class="btn dropdown-item detail-course-button fw-bold text-center">詳細</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#save_course_modal"></button>';
    html += '<button type="button" value="' + value + '_' + number + '" class="btn dropdown-item delete-course-button fw-bold text-center border-top p-1 pt-2">削除</button>';
    html += '</div>';
    html += '</div>';
    html += '<input type="hidden" class="input-course-start" value="' + $( '#save_course_modal [name=start]' ).next().val() + '">';
    html += '<input type="hidden" class="input-course-deadline" value="' + $( '#save_course_modal [name=deadline]:checked' ).val() + '">';
    html += '<input type="hidden" class="input-course-on-time" value="' + $( '#save_course_modal [name=on_time]' ).next().val() + '">';
    html += '<input type="hidden" class="input-course-any-day" value="' + $( '#save_course_modal [name=any_day]' ).next().val() + '">';
    html += '<input type="hidden" class="input-course-any-time" value="' + $( '#save_course_modal [name=any_time]' ).next().val() + '">';
    html += '<input type="hidden" class="input-course-method" value="' + $( '#save_course_modal [name=method]' ).next().val() + '">';
    if ( $( '#save_course_modal [name=business_check_1]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-1" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-1" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_2]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-2" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-2" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_3]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-3" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-3" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_4]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-4" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-4" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_5]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-5" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-5" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_6]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-6" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-6" value="0">';
    }
    if ( $( '#save_course_modal [name=business_check_7]' ).prop( 'checked' ) ) {
        html += '<input type="hidden" class="input-course-business-check-7" value="1">';
    } else {
        html += '<input type="hidden" class="input-course-business-check-7" value="0">';
    }
    html += '</td>';
    html += '</tr>';
    return html;
}