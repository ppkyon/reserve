function append_order_button() {
    $( '.input-area .display-area' ).each( function( index, value ) {
        $( this ).find( '.order-up-button' ).remove();
        $( this ).find( '.order-down-button' ).remove();
        if ( index == 0 ) {
            var html = '<button type="button" class="btn order-down-button d-flex ms-4 p-0">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/order-down.svg">';
            html += '</button>';
            $( this ).find( '.action-area' ).append( html );
        } else if ( index == $( '.input-area .display-area' ).length - 1 ) {
            var html = '<button type="button" class="btn order-up-button d-flex ms-4 p-0">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/order-up.svg">';
            html += '</button>';
            $( this ).find( '.action-area' ).append( html );
        } else {
            var html = '<button type="button" class="btn order-up-button d-flex ms-4 p-0">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/order-up.svg">';
            html += '</button>';
            html += '<button type="button" class="btn order-down-button d-flex ms-2 p-0">';
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/order-down.svg">';
            html += '</button>';
            $( this ).find( '.action-area' ).append( html );
        }
    });
}

function append_setting_area() {
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;
    var html = '<div class="display-area d-flex align-items-start position-relative p-1 mb-2">';
    html += '<div class="content-area p-2">';
    html += '<div class="top-area d-flex justify-content-start align-items-center mb-0">';
    html += '<p class="input-label mb-0">設問項目</p>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0">';
    html += '<input type="text" class="input-text input-select input-type ps-2 pe-2" style="width: 10rem;" placeholder="設問項目" data-bs-toggle="dropdown" data-parsley-error-message="選択してください" data-parsley-errors-container="#error_select_item_' + random + '" readonly required>';
    html += '<input type="hidden">';
    html += '<div class="dropdown-menu">';
    html += '<button type="button" value="1" class="btn dropdown-item fw-bold">氏名</button>';
    html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">フリガナ</button>';
    html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">年齢</button>';
    html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">性別</button>';
    html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">電話番号</button>';
    html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">メールアドレス</button>';
    html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">生年月日</button>';
    html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">住所</button>';
    html += '<button type="button" value="9" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">プロフィール写真</button>';
    html += '<button type="button" value="10" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">画像</button>';
    html += '<button type="button" value="11" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
    html += '<button type="button" value="51" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約形式</button>';
    html += '<button type="button" value="52" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約日程</button>';
    html += '<button type="button" value="53" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約可能日</button>';
    html += '<button type="button" value="54" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約日程再調整</button>';
    html += '<button type="button" value="99" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設問</button>';
    html += '</div>';
    html += '</div>';
    html += '<p class="input-label ms-3 mb-0">タイトル</p>';
    html += '<input type="text" class="input-text input-select input-name ps-2 pe-2" style="width: 15rem;" placeholder="タイトルを入力" data-parsley-errors-container="#error_item_title_' + random + '" required>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<div id="error_select_item_' + random + '" style="margin-left: 4.4rem; width: 10rem;"></div>';
    html += '<div id="error_item_title_' + random + '" style="margin-left: 5.4rem;"></div>';
    html += '</div>';
    html += '<div class="sub-area d-flex justify-content-start align-items-center">';
    html += '<p class="input-label mb-0">補足</p>';
    html += '<input type="text" class="input-text input-select input-description ps-2 pe-2" style="width: 30.5rem;" placeholder="補足を入力">';
    html += '</div>';
    html += '</div>';
    html += '<div class="action-area p-2 d-flex justify-content-between align-items-center mb-2">';
    html += '<div class="pin-area d-flex align-items-center me-1">';
    html += '<span class="me-1">必須</span>';
    html += '<input id="check_pin_' + random + '" type="checkbox" value="1" class="input-required" checked>';
    html += '<label for="check_pin_' + random + '" class="d-block position-relative mb-0"></label>';
    html += '</div>';
    html += '<button type="button" class="btn copy-item-button ms-3 me-2 p-0">';
    html += '<i class="bx bx-copy-alt"></i>';
    html += '</button>';
    html += '<button type="button" class="btn delete-item-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_item_check_modal"></button>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_reserve_type_area() {
    var html = '<div class="type-area d-flex justify-content-start align-items-center mt-2 mb-2">';
    html += '<p class="input-label mb-0">種類を選択</p>';
    html += '<input type="text" class="input-text input-select input-question readonly ps-2 pe-2" value="ラジオボタン" style="width: 10rem;" disabled>';
    html += '</div>';
    html += '<div class="item-area mt-2 mb-2">';
    html += '<div class="row">';
    html += '<div class="col-6 mb-2">';
    html += '<span>1.</span>';
    html += '<input type="text" value="対面" class="ps-1 ms-1" disabled>';
    html += '<button type="button" class="btn delete-offline-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<span>2.</span>';
    html += '<input type="text" value="オンライン" class="ps-1 ms-1" disabled>';
    html += '<button type="button" class="btn delete-online-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_reserve_date_area() {
    var html = '<div class="type-area d-flex justify-content-start align-items-center mt-2 mb-2">';
    html += '<p class="input-label mb-0">種類を選択</p>';
    html += '<input type="text" class="input-text input-select input-question readonly ps-2 pe-2" value="ラジオボタン" style="width: 10rem;" disabled>';
    html += '</div>';
    html += '<div class="item-area mt-2 mb-2">';
    html += '<div class="row">';
    html += '<div class="col-6 mb-2">';
    html += '<span>1.</span>';
    html += '<input type="text" value="〇年〇月〇日 〇時〇分" class="ps-1 ms-1" disabled>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<span>2.</span>';
    html += '<input type="text" value="〇年〇月〇日 〇時〇分" class="ps-1 ms-1" disabled>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_reserve_best_area() {
    var html = '<div class="type-area d-flex justify-content-start align-items-center mt-2 mb-2">';
    html += '<p class="input-label mb-0">種類を選択</p>';
    html += '<input type="text" class="input-text input-select input-question readonly ps-2 pe-2" value="日時" style="width: 10rem;" disabled>';
    html += '</div>';
    html += '<div class="item-area mt-2 mb-2">';
    html += '<div class="row">';
    html += '<div class="col-6 mb-2">';
    html += '<span>1.</span>';
    html += '<input type="text" class="ps-1 ms-1">';
    html += '<button type="button" class="btn delete-list-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_list_check_modal"></button>';
    html += '</div>';
    html += '</div>';
    html += '<div class="row">';
    html += '<div class="col-6 d-flex justify-content-start align-items-center">';
    html += '<button type="button" class="btn add-list-button d-flex justify-content-start align-items-center p-0">';
    html += '<i class="bx bx-plus me-1"></i>';
    html += '<p class="mb-0">リストを追加する</p>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_question_type_area() {
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;
    var html = '<div class="type-area d-flex justify-content-start align-items-center mt-2 mb-2">';
    html += '<p class="input-label mb-0">種類を選択</p>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0">';
    html += '<input type="text" class="input-text input-select input-question ps-2 pe-2" style="width: 10rem;" placeholder="種類を選択" data-bs-toggle="dropdown" data-parsley-error-message="選択してください" readonly required>';
    html += '<input type="hidden">';
    html += '<div class="dropdown-menu" aria-labelledby="type">';
    html += '<button type="button" value="1" class="btn dropdown-item fw-bold">フリーテキスト</button>';
    html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">ラジオボタン</button>';
    html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">チェックボックス</button>';
    html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">プルダウン</button>';
    html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">日付</button>';
    html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">時間</button>';
    html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">日時</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="item-area mt-2 mb-2">';
    html += '<div class="row">';
    html += '<div class="col-6 mb-2">';
    html += '<span>1.</span>';
    html += '<input type="text" class="ps-1 ms-1" data-parsley-errors-container="#error_list_item_' + random + '" required>';
    html += '<button type="button" class="btn delete-list-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_list_check_modal"></button>';
    html += '<div id="error_list_item_' + random + '" class="ms-2"></div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="row">';
    html += '<div class="col-6 d-flex justify-content-start align-items-center">';
    html += '<button type="button" class="btn add-list-button d-flex justify-content-start align-items-center p-0">';
    html += '<i class="bx bx-plus me-1"></i>';
    html += '<p class="mb-0">リストを追加する</p>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_item_area(required_flg) {
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;
    var html = '<div class="item-area mt-2 mb-2">';
    html += '<div class="row">';
    html += '<div class="col-6 mb-2">';
    html += '<span>1.</span>';
    if ( required_flg ) {
        html += '<input type="text" class="ps-1 ms-1" data-parsley-errors-container="#error_list_item_' + random + '" required>';
    } else {
        html += '<input type="text" class="ps-1 ms-1">';
    }
    html += '<button type="button" class="btn delete-list-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_list_check_modal"></button>';
    if ( required_flg ) {
        html += '<div id="error_list_item_' + random + '" class="ms-2"></div>';
    }
    html += '</div>';
    html += '</div>';
    html += '<div class="row">';
    html += '<div class="col-6 d-flex justify-content-start align-items-center">';
    html += '<button type="button" class="btn add-list-button d-flex justify-content-start align-items-center p-0">';
    html += '<i class="bx bx-plus me-1"></i>';
    html += '<p class="mb-0">リストを追加する</p>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}

function append_list_area(target) {
    var count = $( target ).parents( '.item-area' ).find( '.col-6' ).length;
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;
    var type = $( target ).parents( '.content-area' ).find( '.type-area input[type=hidden]' ).val();

    var html = '<div class="col-6 mb-2">';
    html += '<span>' + count + '.</span>';
    if ( type == '2' || type == '3' || type == '4' ) {
        html += '<input type="text" class="ps-1 ms-1" data-parsley-errors-container="#error_list_item_' + random + '" required>';
    } else {
        html += '<input type="text" class="ps-1 ms-1">';
    }
    html += '<button type="button" class="btn delete-list-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_list_check_modal"></button>';
    if ( type == '2' || type == '3' || type == '4' ) {
        html += '<div id="error_list_item_' + random + '" class="ms-2"></div>';
    }
    html += '</div>';
    return html;
}

function append_delete_offline() {
    var html = '<div class="col-6 mb-2">';
    html += '<span>1. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="オンライン" disabled>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<button type="button" class="btn add-offline-button d-flex justify-content-start align-items-center p-0">';
    html += '<i class="bx bx-plus me-1"></i>';
    html += '<p class="mb-0">対面を追加する</p>';
    html += '</button>';
    html += '</div>';
    return html;
}
function append_delete_online() {
    var html = '<div class="col-6 mb-2">';
    html += '<span>1. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="対面" disabled>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<button type="button" class="btn add-online-button d-flex justify-content-start align-items-center p-0">';
    html += '<i class="bx bx-plus me-1"></i>';
    html += '<p class="mb-0">オンラインを追加する</p>';
    html += '</button>';
    html += '</div>';
    return html;
}
function append_add_offline() {
    var html = '<div class="col-6 mb-2">';
    html += '<span>1. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="対面" disabled>';
    html += '<button type="button" class="btn delete-offline-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<span>2. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="オンライン" disabled>';
    html += '<button type="button" class="btn delete-online-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    return html;
}
function append_add_online() {
    var html = '<div class="col-6 mb-2">';
    html += '<span>1. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="対面" disabled>';
    html += '<button type="button" class="btn delete-offline-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    html += '<div class="col-6 mb-2">';
    html += '<span>2. </span>';
    html += '<input type="text" class="ps-1 ms-1" value="オンライン" disabled>';
    html += '<button type="button" class="btn delete-online-button ms-2 me-2 p-0">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '</div>';
    return html;
}



function append_table_area(data) {
    var item = '';
    $.each( data.item, function( index, value ) {
        if ( index < 3 ) {
            if ( value.type == 1 ) {
                item += '<p class="content-title mb-0">氏名</p>';
            } else if ( value.type == 2 ) {
                item += '<p class="content-title mb-0">フリガナ</p>';
            } else if ( value.type == 3 ) {
                item += '<p class="content-title mb-0">年齢</p>';
            } else if ( value.type == 4 ) {
                item += '<p class="content-title mb-0">性別</p>';
            } else if ( value.type == 5 ) {
                item += '<p class="content-title mb-0">電話番号</p>';
            } else if ( value.type == 6 ) {
                item += '<p class="content-title mb-0">メールアドレス</p>';
            } else if ( value.type == 7 ) {
                item += '<p class="content-title mb-0">生年月日</p>';
            } else if ( value.type == 8 ) {
                item += '<p class="content-title mb-0">住所</p>';
            } else if ( value.type == 9 ) {
                item += '<p class="content-title mb-0">プロフィール写真</p>';
            } else if ( value.type == 10 ) {
                item += '<p class="content-title mb-0">画像</p>';
            } else if ( value.type == 11 ) {
                item += '<p class="content-title mb-0">動画</p>';
            } else if ( value.type == 51 ) {
                item += '<p class="content-title mb-0">予約形式</p>';
            } else if ( value.type == 52 ) {
                item += '<p class="content-title mb-0">予約日程</p>';
            } else if ( value.type == 53 ) {
                item += '<p class="content-title mb-0">予約可能日</p>';
            } else if ( value.type == 54 ) {
                item += '<p class="content-title mb-0">予約日程再調整</p>';
            } else if ( value.type == 99 ) {
                item += '<p class="content-title mb-0">設問</p>';
            }
        }
    });
    if ( data.count > 3 ) {
        item += '<p class="content-title mb-0">...</p>';
    }

    var button = '<a href="/head/question/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.title + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '</td>';
    html += '<td>' + item + '</td>';
    html += '<td>';
    html += '<p class="content-title mb-0">' + data.count + '</p>';
    html += '</td>';
    html += '<td>';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += button;
    html += '</td>';
    html += '</tr>';
    return html;
}