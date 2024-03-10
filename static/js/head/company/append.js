
function append_table_area(data) {
    var image = '';
    if ( check_empty(data.profile.company_logo_image) ) {
        image = '<img class="company-image me-2" src="' + $( '#env_media_url' ).val() + data.profile.company_logo_image + '">';
    } else {
        image = '<img class="company-image me-2" src="' + $( '#env_static_url' ).val() + 'img/user-none.png">';
    }

    var html = '<tr>';
    html += '<td class="p-1"></td>';
    html += '<td class="position-relative p-1">';
    html += '<div class="d-flex justify-content-start align-items-center">';
    html += image;
    html += '<p class="content-title mb-0">' + data.profile.company_name + '</p>';
    html += '</div>';
    html += '<p class="content-date mb-0">#' + data.display_id + '</p>';
    html += '</td>';
    html += '<td class="p-1">';
    html += '<p class="content-title mb-0">' + data.profile.head_family_name + data.profile.head_first_name + '</p>';
    html += '</td>';
    html += '<td class="p-1">';
    html += '<p class="content-title mb-0">' + data.profile.prefecture_name + '</p>';
    html += '</td>';
    html += '<td class="p-1">';
    $.each( data.tag, function( index, value ) {
        html += '<label class="content-tag text-center p-1 mt-1 mb-1">' + value.name + '</label>&nbsp;';
    });
    html += '</td>';
    html += '<td class="text-center p-1">';
    html += '<div class="d-flex justify-content-start align-items-center">';
    html += '<button type="button" value="' + data.display_id + '" class="btn preview-button p-1 me-1">プレビュー</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#offcanvas_company_profile"></button>';
    html += '<div class="dropdown button-area text-center d-inline-block p-0 me-3">';
    html += '<button type="button" class="btn p-0" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-vertical-rounded menu-icon"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu">';
    if ( data.status <= 2 ) {
        html += '<button type="button" class="btn start-button dropdown-item fw-bold text-center p-1 pt-2" value="' + data.display_id + '">アカウント開始</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#start_check_modal"></button>';
        html += '<a href="/company/shop/?login_id=' + data.display_id + '" class="btn dropdown-item fw-bold border-top text-center">企業ログイン</a>';
    } else {
        html += '<a href="/company/shop/?login_id=' + data.display_id + '" class="btn dropdown-item fw-bold text-center">企業ログイン</a>';
    }
    html += '';
    html += '';
    html += '';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}