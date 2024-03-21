function append_genre() {
    var html = '<tr class="active">';
    html += '<input type="hidden" value="">';
    html += '<td>';
    html += '<div class="d-flex justify-content-start align-items-center">';
    html += '<i class="bx bx-folder folder-icon me-1"></i>';
    html += '<input type="text" class="input-text">';
    html += '</div>';
    html += '</td>';
    html += '<td>';
    html += '<div class="d-flex justify-content-center align-items-center">';
    html += '<form id="favorite_text_form" action="/tag/genre/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="">';
    html += '</form>';
    html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
    html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_on_modal"></button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_off_modal"></button>';
    html += '</div>';
    html += '</td>';
    html += '<td>';
    html += '<div class="d-flex justify-content-center align-items-center">';
    html += '<div class="dropdown d-inline-block p-0">';
    html += '<button type="button" id="dropdown" class="btn" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-horizontal-rounded menu-icon"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu" aria-labelledby="dropdown">';
    html += '<button type="button" class="btn dropdown-item edit-button fw-bold text-center">編集</button>';
    html += '<button type="button" class="btn dropdown-item fw-bold delete-button text-center border-top p-1 pt-2" value="genre" data-bs-toggle="modal" data-bs-target="#delete_check_modal">削除</button>';
    html += '<form id="delete_genre_form" action="/tag/genre/delete/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="">';
    html += '</form>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}

function append_tag() {
    var genre = $( '.table-area .genre-table .active td' ).eq(0).find( 'p' ).text().split( '(' )[0];
    var html = '<tr class="active">';
    html += '<input type="hidden" value="">';
    html += '<td>';
    html += '<input type="text" class="input-text">';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0"></p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="genre-mark text-center mb-0">' + genre + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<div class="d-flex justify-content-center align-items-center">';
    html += '<form id="favorite_text_form" action="/tag/tag/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="">';
    html += '</form>';
    html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
    html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_on_modal"></button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_off_modal"></button>';
    html += '</div>';
    html += '</td>';
    html += '<td>';
    html += '<div class="d-flex justify-content-center align-items-center">';
    html += '<div class="dropdown d-inline-block p-0">';
    html += '<button type="button" id="dropdown" class="btn" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-horizontal-rounded menu-icon"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu" aria-labelledby="dropdown">';
    html += '<button type="button" class="btn dropdown-item edit-button fw-bold text-center">編集</button>';
    html += '<button type="button" class="btn dropdown-item delete-button fw-bold text-center border-top p-1 pt-2" value="tag" data-bs-toggle="modal" data-bs-target="#delete_check_modal">削除</button>';
    html += '<form id="delete_tag_form" action="/tag/tag/delete/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="">';
    html += '</form>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}

function append_tag_list( response, target ) {

    var genre = $( target ).find( 'td' ).eq(0).find( 'p' ).text().split( '(' )[0];

    $( '.table-area .tag-table tbody' ).empty();
    $.each( response, function( index, value ) {
        var favorite_icon = '';
        if ( value.favorite_flg ) {
            favorite_icon = '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
            favorite_icon += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
        } else {
            favorite_icon = '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
            favorite_icon += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
        }
        favorite_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_on_modal"></button>';
        favorite_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_off_modal"></button>';

        if ( index == 0 ) {
            var html = '<tr class="active">';
            html += '<input type="hidden" value="' + value.display_id + '">';
            html += '<td>';
            html += '<p class="content-title mb-0">' + value.name + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<p class="content-title mb-0">' + value.display_date + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<p class="genre-mark text-center mb-0">' + genre + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<div class="d-flex justify-content-center align-items-center">';
            html += '<form id="favorite_text_form" action="/tag/tag/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
            html += '<input type="hidden" name="id" value="' + value.display_id + '">';
            html += '</form>';
            html += favorite_icon;
            html += '</div>';
            html += '</td>';
            html += '<td>';
            html += '<div class="d-flex justify-content-center align-items-center">';
            html += '<div class="dropdown d-inline-block p-0">';
            html += '<button type="button" id="dropdown_' + value.display_id + '" class="btn" data-bs-toggle="dropdown">';
            html += '<i class="bx bx-dots-horizontal-rounded menu-icon"></i>';
            html += '</button>';
            html += '<div class="dropdown-menu" aria-labelledby="dropdown_' + value.display_id + '">';
            html += '<button type="button" class="btn dropdown-item edit-button fw-bold text-center">編集</button>';
            html += '<button type="button" class="btn dropdown-item delete-button fw-bold text-center border-top p-1 pt-2" value="tag_' + value.display_id + '" data-bs-toggle="modal" data-bs-target="#delete_check_modal">削除</button>';
            html += '<form id="delete_tag_' + value.display_id + '_form" action="/tag/tag/delete/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
            html += '<input type="hidden" name="id" value="' + value.display_id + '">';
            html += '</form>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            html += '</td>';
            html += '</tr>';
            $( '.table-area .tag-table tbody' ).append( html );
        } else {
            var html = '<tr style="background-color: #FFF;">';
            html += '<input type="hidden" value="' + value.display_id + '">';
            html += '<td>';
            html += '<p class="content-title mb-0">' + value.name + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<p class="content-title mb-0">' + value.display_date + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<p class="genre-mark text-center mb-0">' + genre + '</p>';
            html += '</td>';
            html += '<td>';
            html += '<div class="d-flex justify-content-center align-items-center">';
            html += '<form id="favorite_text_form" action="/tag/tag/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
            html += '<input type="hidden" name="id" value="' + value.display_id + '">';
            html += '</form>';
            html += favorite_icon;
            html += '</div>';
            html += '</td>';
            html += '<td>';
            html += '<div class="d-flex justify-content-center align-items-center">';
            html += '<div class="dropdown d-inline-block p-0">';
            html += '<button type="button" id="dropdown_' + value.display_id + '" class="btn" data-bs-toggle="dropdown">';
            html += '<i class="bx bx-dots-horizontal-rounded menu-icon"></i>';
            html += '</button>';
            html += '<div class="dropdown-menu" aria-labelledby="dropdown_' + value.display_id + '">';
            html += '<button type="button" class="btn dropdown-item edit-button fw-bold text-center">編集</button>';
            html += '<button type="button" class="btn dropdown-item delete-button fw-bold text-center border-top p-1 pt-2" value="tag_' + value.display_id + '" data-bs-toggle="modal" data-bs-target="#delete_check_modal">削除</button>';
            html += '<form id="delete_tag_' + value.display_id + '_form" action="/tag/tag/delete/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
            html += '<input type="hidden" name="id" value="' + value.display_id + '">';
            html += '</form>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            html += '</td>';
            html += '</tr>';
            $( '.table-area .tag-table tbody' ).append( html );
        }
    });
}