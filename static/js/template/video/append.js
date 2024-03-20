
function append_table_area(data) {
    var size = '';
    if ( data.video_size >= 1000000 ) {
        size = Math.ceil( data.video_size / 1000000 ) + 'MB';
    } else if ( data.video_size >= 1000 ) {
        size = Math.ceil( data.video_size / 1000 ) + 'KB';
    } else {
        size = data.video_size + 'B';
    }
    var button = '<a href="/template/video/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center">';
    html += '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + data.video_thumbnail + '">';
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.video_display_time + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + size + '</p>';
    html += '</td>';
    html += '<td>';
    if ( data.use_flg ) {
        html += '<p class="content-title mb-0">使用中</p>';
    } else {
        html += '<p class="content-title mb-0">-</p>';
    }
    html += '</td>';
    html += '<td>';
    html += '<form id="favorite_form" action="/template/video/favorite/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += '</form>';
    if ( data.favorite_flg ) {
        html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    } else {
        html += '<img class="favorite-icon" src="' + $( '#env_static_url' ).val() + 'img/icon/star.svg">';
        html += '<img class="favorite-icon d-none" src="' + $( '#env_static_url' ).val() + 'img/icon/star-color.svg">';
    }
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_on_modal"></button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#favorite_off_modal"></button>';
    html += '</td>';
    html += '<td>';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}