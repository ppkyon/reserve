function append_table_area(data) {
    var image = '';
    if ( check_empty( data.profile.image ) ) {
        image = data.profile.image;
    } else if ( check_empty( data.display_image ) ) {
        image = data.display_image;
    } else {
        image = $( '#env_static_url' ).val() + 'img/user-none.png';
    }

    var name = '';
    if ( check_empty( data.profile.name ) ) {
        if ( check_empty( data.profile.age ) ) {
            name = data.profile.name + ' (' + data.profile.age + ')';
        } else {
            name = data.profile.name;
        }
    } else {
        if ( check_empty( data.profile.age ) ) {
            name = data.display_name + ' (' + data.profile.age + ')';
        } else {
            name = data.display_name;
        }
    }

    var atelle_id = '-';
    if ( check_empty( data.profile.atelle_id ) ) {
        atelle_id = '#' + data.profile.atelle_id;
    }

    var status = '';
    if ( data.status == 2 ) {
        status = '<p class="content-title mb-0">ブロック</p>';
    } else {
        if ( check_empty( data.active_flow ) ) {
            status = '<p class="content-title mb-0">' + data.active_flow.flow_tab.name + '</p>'
        } else {
            status = '<p class="content-title mb-0">-</p>';
        }
    }

    var tag = '';
    $.each( data.tag, function( index, value ) {
        tag += '<label class="content-tag text-center p-1 mt-1 mb-1">' + value.tag.name + '</label> ';
    });

    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( '00' + ( created_date.getMonth() + 1 ) ).slice(-2) + '月' + ( '00' + created_date.getDate() ).slice(-2) + '日 ' + ( '00' + created_date.getHours() ).slice(-2) + ':' + ( '00' + created_date.getMinutes() ).slice(-2);

    var html = '<tr class="position-relative">';
    html += '<td class="p-1">';
    if ( data.alert ) {
        if ( data.alert.status == 2 ) {
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/notice.png" class="ms-2 notice-image">';
            html += '<label class="notice-text mb-0 p-1 ps-2 pe-2">' + data.alert.text + '</label>';
        } else if ( data.alert.status == 3 ) {
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/warning.svg" class="ms-2 alert-image">';
            html += '<label class="alert-text mb-0 p-1 ps-2 pe-2">' + data.alert.text + '</label>';
        }
    }
    html += '</td>';
    html += '<td class="position-relative p-1">';
    html += '<div class="d-flex justify-content-start align-items-center">';
    html += '<img src="' + image + '" class="user-image me-2">';
    html += '<p class="d-flex align-items-center content-title mb-0">';
    html += '<span>' + name + '</span>';
    if ( data.member_flg ) {
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/member-yes.png" class="ms-1" width="12" height="12"></img>';
    } else {
        html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/member-no.png" class="ms-1" width="12" height="12"></img>';
    }
    html += '</p>';
    html += '</div>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td class="p-1">';
    html += '<p class="content-title mb-0">' + atelle_id + '</p>';
    html += '</td>';
    html += '<td class="p-1">' + status + '</td>';
    html += '<td class="p-1">' + tag + '</td>';
    html += '<td class="text-center p-1">';
    html += '<div class="d-flex justify-content-start align-items-center">';
    html += '<button type="button" value="' + data.display_id + '" class="btn preview-icon-button p-0 me-1" data-bs-toggle="tooltip" data-bs-placement="bottom" title="プレビュー">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/preview.png" class="pt-1 pb-1">';
    html += '</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#user_profile_offcanvas"></button>';
    html += '<a href="/user/detail?id=' + data.display_id + '" class="btn detail-icon-button p-1 me-2" data-bs-toggle="tooltip" data-bs-placement="bottom" title="詳細">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/detail.png">';
    html += '</a>';
    html += '<div class="dropdown button-area text-center d-inline-block p-0 me-3">';
    html += '<button type="button" id="dropdown_menu" class="btn p-0" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-vertical-rounded menu-icon"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu" aria-labelledby="dropdown_menu">';
    html += '<a href="/talk?id=' + data.display_id + '" class="btn edit-button dropdown-item fw-bold text-center">1対1トーク</a>';
    if ( !data.member_flg ) {
        html += '<button type="button" value="' + data.display_id + '" class="btn member-button dropdown-item fw-bold text-center border-top p-1 ps-2 pe-2 pt-2">会員登録</a>';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#member_user_check_modal"></button>';
    }
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}