function open_question_modal(target, number){
    var form_data = new FormData();
    $.ajax({
        'data': form_data,
        'url': $( '#get_question_list_url' ).val(),
        'type': 'POST',
        'dataType': 'json',
        'processData': false,
        'contentType': false,
    }).done( function( response ){
        $( '#question_modal .table-area tbody' ).empty();
        if ( response.length > 0 ) {
            $.each( response, function( index, value ) {
                $( '#question_modal .table-area tbody' ).append( append_question_data(value) );
            });
            $( '#question_modal .table-area tbody button' ).val( number );
            $( '#question_modal .table-area' ).removeClass( 'd-none' );
            $( '#question_modal .notice-area' ).addClass( 'd-none' );
        } else {
            $( '#question_modal .table-area' ).addClass( 'd-none' );
            $( '#question_modal .notice-area' ).removeClass( 'd-none' );
        }
        $( target ).parents( '.dropdown' ).next().next().trigger( 'click' );
    }).fail( function(){
        
    });
}

function append_question_data(data) {
    var action = '';
    $.each( data.item, function( index, value ) {
        if ( index < 3 ) {
            if ( value.type == 1 ) {
                action += '<p class="content-title mb-0">氏名</p>';
            } else if ( value.type == 2 ) {
                action += '<p class="content-title mb-0">フリガナ</p>';
            } else if ( value.type == 3 ) {
                action += '<p class="content-title mb-0">年齢</p>';
            } else if ( value.type == 4 ) {
                action += '<p class="content-title mb-0">性別</p>';
            } else if ( value.type == 5 ) {
                action += '<p class="content-title mb-0">電話番号</p>';
            } else if ( value.type == 6 ) {
                action += '<p class="content-title mb-0">メールアドレス</p>';
            } else if ( value.type == 7 ) {
                action += '<p class="content-title mb-0">生年月日</p>';
            } else if ( value.type == 8 ) {
                action += '<p class="content-title mb-0">住所</p>';
            } else if ( value.type == 9 ) {
                action += '<p class="content-title mb-0">プロフィール写真</p>';
            } else if ( value.type == 10 ) {
                action += '<p class="content-title mb-0">画像</p>';
            } else if ( value.type == 11 ) {
                action += '<p class="content-title mb-0">動画</p>';
            } else if ( value.type == 51 ) {
                action += '<p class="content-title mb-0">予約形式</p>';
            } else if ( value.type == 52 ) {
                action += '<p class="content-title mb-0">予約日程</p>';
            } else if ( value.type == 53 ) {
                action += '<p class="content-title mb-0">予約可能日</p>';
            } else if ( value.type == 54 ) {
                action += '<p class="content-title mb-0">予約日程再調整</p>';
            } else if ( value.type == 99 ) {
                action += '<p class="content-title mb-0">設問</p>';
            }
        }
    });
    if ( data.count > 3 ) {
        action += '<p class="content-title mb-0">...</p>';
    }
    
    var button = '<button type="button" class="btn detail-button p-1" style="background-color: #00b074;">選択</button>';
    button += '<input type="hidden" value="' + data.display_id + '">';
    button += '<input type="hidden" value="' + data.name + '">';

    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.title + '</p>';
    html += '</td>';
    html += '<td>' + action + '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.count + '</p>';
    html += '</td>';
    html += '<td>' + button + '</td>';
    html += '</tr>';
    return html;
}