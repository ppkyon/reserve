
function append_table_area(data) {
    var valid_icon = '<td class="position-relative">';
    valid_icon += '<form class="valid-form" action="/head/flow/valid/" method="POST" enctype="multipart/form-data" data-parsley-focus="none">';
    valid_icon += '<input type="hidden" name="id" value="' + data.display_id + '">';
    valid_icon += '</form>';
    valid_icon += '<div class="flg-area">';
    if ( data.valid ) {
        valid_icon += '<input id="valid_' + data.display_id + '" type="checkbox" name="valid_flg" value="1" class="d-none" checked>';
    } else {
        valid_icon += '<input id="valid_' + data.display_id + '" type="checkbox" name="valid_flg" value="1" class="d-none">';
    }
    valid_icon += '<label for="valid_' + data.display_id + '" class="d-block position-relative mb-0" style="width: 35px;"></label>';
    valid_icon += '</div>';
    valid_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#valid_on_modal"></button>';
    valid_icon += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#valid_off_modal"></button>';
    valid_icon += '</td>';

    var button = '<a href="/head/flowchart/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.description + '</p>';
    html += '</td>';
    html += valid_icon;
    html += '<td>';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}