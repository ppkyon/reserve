function append_template_area( value ) {
    if ( Number(value) < 7 ) {
        $( '#save_richmenu_form .template-area' ).css( 'padding-top', '65%' );
    } else {
        $( '#save_richmenu_form .template-area' ).css( 'padding-top', '32.5%' );
    }
    $( '#save_richmenu_form .template-area img' ).remove();
    if ( !$( '#save_richmenu_form .template-area p' ).length ) {
        $( '#save_richmenu_form .template-area' ).append( '<p class="text-muted mb-0">テンプレートを選択して、背景画像をアップロードしてください。</p>' );
    }
    $( '#save_richmenu_form [name=upload_image]' ).val( '' );
    create_preview();

    var html = '';
    $( '#save_richmenu_form .template-area table' ).remove();
    if ( value == '0' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="c">C';
        html += '</td>';
        html += '</tr>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="d">D';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="e">E';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="f">F';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '1' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="c">C';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="d">D';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '2' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td colspan="3">';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '</tr>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="c">C';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="d">D';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '3' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tr>';
        html += '<td rowspan="2" style="width: 66.7%">';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td style="width: 33.3%">';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '<tr class="border-top border-primary">';
        html += '<td style="width: 33.3%">';
        html += '<input type="hidden" value="c">C';
        html += '</td>';
        html += '</tr>';
        html += '</table>';
    } else if ( value == '4' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '</tr>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '5' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '6' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '7' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="c">C';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '8' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td style="width: 33.3%;">';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td style="width: 66.7%;">';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '9' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td style="width: 66.7%;">';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td style="width: 33.3%;">';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '10' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '<td>';
        html += '<input type="hidden" value="b">B';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    } else if ( value == '11' ) {
        html += '<table class="text-center text-white h-100">';
        html += '<tbody>';
        html += '<tr>';
        html += '<td>';
        html += '<input type="hidden" value="a">A';
        html += '</td>';
        html += '</tr>';
        html += '</tbody>';
        html += '</table>';
    }
    $( '#save_richmenu_form .template-area' ).append( html );
}

function append_action_area( value ) {
    var add_count = 1;
    if ( value == '4' || value == '5' || value == '8' || value == '9' || value == '10' ) {
        add_count = 2;
    } else if ( value == '3' || value == '7' ) {
        add_count = 3;
    } else if ( value == '1' || value == '2' ) {
        add_count = 4;
    } else if ( value == '0' ) {
        add_count = 6;
    }

    var now_count = $( '#save_richmenu_form .action-area' ).length;
    $( '#save_richmenu_form .action-area' ).each( function( index, value ) {
        if ( index >= add_count ) {
            $( this ).remove();
        }
    });

    var html = '';
    for ( var i = 1; i < add_count; i++ ) {
        if ( i >= now_count ) {
            if ( i == 1 ) {
                html = '';
                html += '<div class="action-area d-flex flex-column position-relative p-1 mb-2">';
                html += '<div class="number-area d-flex justify-content-start align-items-center pb-3">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/than-green.svg" class="mt-1 ms-2">';
                html += '<p class="ms-2 mb-0">B</p>';
                html += '<input type="hidden" name="number" value="b">';
                html += '</div>';
                html += '<div class="content-area-wrap">';
                html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
                html += '<label class="ms-5 mb-3">タイプ</label>';
                html += '<div class="dropdown input-select-dropdown d-inline-block p-0 ms-3">';
                html += '<input type="text" name="type_b" class="input-text input-select ps-2 pe-2" placeholder="選択" data-bs-toggle="dropdown" data-parsley-errors-container="#error_type_b" data-parsley-error-message="選択してください" readonly required>';
                html += '<input type="hidden">';
                html += '<div class="dropdown-menu">';
                html += '<button type="button" value="1" class="btn dropdown-item fw-bold">リンク</button>';
                html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
                html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">回答フォーム</button>';
                html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約フォーム</button>';
                html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約履歴ページ</button>';
                html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">オンラインURL</button>';
                html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">会社概要</button>';
                html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">テキスト</button>';
                html += '<button type="button" value="0" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設定なし</button>';
                html += '</div>';
                html += '</div>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_question_modal"></button>';
                html += '</div>';
                html += '<div class="content-error-area d-flex justify-content-start align-items-start pb-0">';
                html += '<label class="mb-0" style="margin-left: 9.5rem; font-size: 0.1rem;">&nbsp;</label>';
                html += '<div id="error_type_b" class="ms-3 mb-3"></div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            } else if ( i == 2 ) {
                html = '';
                html += '<div class="action-area d-flex flex-column position-relative p-1 mb-2">';
                html += '<div class="number-area d-flex justify-content-start align-items-center pb-3">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/than-green.svg" class="mt-1 ms-2">';
                html += '<p class="ms-2 mb-0">C</p>';
                html += '<input type="hidden" name="number" value="c">';
                html += '</div>';
                html += '<div class="content-area-wrap">';
                html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
                html += '<label class="ms-5 mb-3">タイプ</label>';
                html += '<div class="dropdown input-select-dropdown d-inline-block p-0 ms-3">';
                html += '<input type="text" name="type_c" class="input-text input-select ps-2 pe-2" placeholder="選択" data-bs-toggle="dropdown" data-parsley-errors-container="#error_type_c" data-parsley-error-message="選択してください" readonly required>';
                html += '<input type="hidden">';
                html += '<div class="dropdown-menu">';
                html += '<button type="button" value="1" class="btn dropdown-item fw-bold">リンク</button>';
                html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
                html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">回答フォーム</button>';
                html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約フォーム</button>';
                html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約履歴ページ</button>';
                html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">オンラインURL</button>';
                html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">会社概要</button>';
                html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">テキスト</button>';
                html += '<button type="button" value="0" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設定なし</button>';
                html += '</div>';
                html += '</div>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_question_modal"></button>';
                html += '</div>';
                html += '<div class="content-error-area d-flex justify-content-start align-items-start pb-0">';
                html += '<label class="mb-0" style="margin-left: 9.5rem; font-size: 0.1rem;">&nbsp;</label>';
                html += '<div id="error_type_c" class="ms-3 mb-3"></div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            } else if ( i == 3 ) {
                html = '';
                html += '<div class="action-area d-flex flex-column position-relative p-1 mb-2">';
                html += '<div class="number-area d-flex justify-content-start align-items-center pb-3">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/than-green.svg" class="mt-1 ms-2">';
                html += '<p class="ms-2 mb-0">D</p>';
                html += '<input type="hidden" name="number" value="d">';
                html += '</div>';
                html += '<div class="content-area-wrap">';
                html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
                html += '<label class="ms-5 mb-3">タイプ</label>';
                html += '<div class="dropdown input-select-dropdown d-inline-block p-0 ms-3">';
                html += '<input type="text" name="type_d" class="input-text input-select ps-2 pe-2" placeholder="選択" data-bs-toggle="dropdown" data-parsley-errors-container="#error_type_d" data-parsley-error-message="選択してください" readonly required>';
                html += '<input type="hidden">';
                html += '<div class="dropdown-menu">';
                html += '<button type="button" value="1" class="btn dropdown-item fw-bold">リンク</button>';
                html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
                html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">回答フォーム</button>';
                html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約フォーム</button>';
                html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約履歴ページ</button>';
                html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">オンラインURL</button>';
                html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">会社概要</button>';
                html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">テキスト</button>';
                html += '<button type="button" value="0" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設定なし</button>';
                html += '</div>';
                html += '</div>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_question_modal"></button>';
                html += '</div>';
                html += '<div class="content-error-area d-flex justify-content-start align-items-start pb-0">';
                html += '<label class="mb-0" style="margin-left: 9.5rem; font-size: 0.1rem;">&nbsp;</label>';
                html += '<div id="error_type_d" class="ms-3 mb-3"></div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            } else if ( i == 4 ) {
                html = '';
                html += '<div class="action-area d-flex flex-column position-relative p-1 mb-2">';
                html += '<div class="number-area d-flex justify-content-start align-items-center pb-3">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/than-green.svg" class="mt-1 ms-2">';
                html += '<p class="ms-2 mb-0">E</p>';
                html += '<input type="hidden" name="number" value="e">';
                html += '</div>';
                html += '<div class="content-area-wrap">';
                html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
                html += '<label class="ms-5 mb-3">タイプ</label>';
                html += '<div class="dropdown input-select-dropdown d-inline-block p-0 ms-3">';
                html += '<input type="text" name="type_e" class="input-text input-select ps-2 pe-2" placeholder="選択" data-bs-toggle="dropdown" data-parsley-errors-container="#error_type_e" data-parsley-error-message="選択してください" readonly required>';
                html += '<input type="hidden">';
                html += '<div class="dropdown-menu">';
                html += '<button type="button" value="1" class="btn dropdown-item fw-bold">リンク</button>';
                html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
                html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">回答フォーム</button>';
                html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約フォーム</button>';
                html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約履歴ページ</button>';
                html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">オンラインURL</button>';
                html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">会社概要</button>';
                html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">テキスト</button>';
                html += '<button type="button" value="0" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設定なし</button>';
                html += '</div>';
                html += '</div>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_question_modal"></button>';
                html += '</div>';
                html += '<div class="content-error-area d-flex justify-content-start align-items-start pb-0">';
                html += '<label class="mb-0" style="margin-left: 9.5rem; font-size: 0.1rem;">&nbsp;</label>';
                html += '<div id="error_type_e" class="ms-3 mb-3"></div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            } else if ( i == 5 ) {
                html = '';
                html += '<div class="action-area d-flex flex-column position-relative p-1 mb-2">';
                html += '<div class="number-area d-flex justify-content-start align-items-center pb-3">';
                html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/than-green.svg" class="mt-1 ms-2">';
                html += '<p class="ms-2 mb-0">F</p>';
                html += '<input type="hidden" name="number" value="f">';
                html += '</div>';
                html += '<div class="content-area-wrap">';
                html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
                html += '<label class="ms-5 mb-3">タイプ</label>';
                html += '<div class="dropdown input-select-dropdown d-inline-block p-0 ms-3">';
                html += '<input type="text" name="type_f" class="input-text input-select ps-2 pe-2" placeholder="選択" data-bs-toggle="dropdown" data-parsley-errors-container="#error_type_f" data-parsley-error-message="選択してください" readonly required>';
                html += '<input type="hidden">';
                html += '<div class="dropdown-menu">';
                html += '<button type="button" value="1" class="btn dropdown-item fw-bold">リンク</button>';
                html += '<button type="button" value="2" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">動画</button>';
                html += '<button type="button" value="3" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">回答フォーム</button>';
                html += '<button type="button" value="4" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約フォーム</button>';
                html += '<button type="button" value="5" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">予約履歴ページ</button>';
                html += '<button type="button" value="6" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">オンラインURL</button>';
                html += '<button type="button" value="7" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">会社概要</button>';
                html += '<button type="button" value="8" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">テキスト</button>';
                html += '<button type="button" value="0" class="btn dropdown-item fw-bold border-top p-1 ps-4 pt-2">設定なし</button>';
                html += '</div>';
                html += '</div>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_template_video_modal"></button>';
                html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#head_question_modal"></button>';
                html += '</div>';
                html += '<div class="content-error-area d-flex justify-content-start align-items-start pb-0">';
                html += '<label class="mb-0" style="margin-left: 9.5rem; font-size: 0.1rem;">&nbsp;</label>';
                html += '<div id="error_type_f" class="ms-3 mb-3"></div>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            }
        }
        if ( html != '' ) {
            $( '#save_richmenu_form .message-area .action-area-wrap' ).append( html );
        }
    }
}

function append_content_area( target, value ) {
    $( target ).parents( '.action-area' ).find( '.content-area-wrap .content-area' ).each( function( index, value ) {
        if ( index > 0 ) {
            $( this ).remove();
        }
    });

    if ( $( target ).val() != '0' ) {
        var html = '';
        if ( $( target ).val() == '8' ) {
            html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
            html += '<label class="ms-5 mb-3"></label>';
            html += '<div class="p-0 mb-3 ms-3">';
            html += '<p class="description mb-0">キーワード応答で設定したテキストを含む、すべてのテキストを設定できます（50文字以内）。</p>';
            html += '</div>';
            html += '</div>';
            html += '<div class="content-area d-flex justify-content-start pb-0">';
            html += '<label class="ms-5 mt-1 mb-3"></label>';
            html += '<div class="p-0 mb-3 ms-3">';
            html += '<textarea name="text_' + value + '" class="d-block input-textarea" placeholder="テキストを入力" maxlength="50" data-parsley-maxlength="50" required></textarea>';
            html += '</div>';
            html += '</div>';
        } else {
            html += '<div class="content-area d-flex justify-content-start align-items-center pb-0">';
            html += '<label class="ms-5 mb-3"></label>';
            html += '<div class="p-0 mb-3 ms-3">';
            html += '<input type="text" name="url_' + value + '" class="input-text input-select ps-2 pe-2" placeholder="URLを入力" required>';
            html += '<input type="hidden">';
            html += '</div>';
            html += '</div>';
            html += '<div class="content-area d-flex justify-content-start pb-0">';
            html += '<label class="ms-5 mt-1 mb-3">アクションラベル</label>';
            html += '<div class="p-0 mb-3 ms-3">';
            html += '<textarea name="label_' + value + '" class="d-block input-textarea" placeholder="アクションラベルを入力" maxlength="20" data-parsley-maxlength="20" required></textarea>';
            html += '</div>';
            html += '</div>';
        }
        $( target ).parents( '.action-area' ).find( '.content-area-wrap' ).append( html );
    }
}



function append_table_area(data) {
    var action = '';
    $.each( data.item, function( index, value ) {
        if ( value.type == 1 || value.type == 2 || value.type == 3 || value.type == 4 || value.type == 5 || value.type == 6 || value.type == 7 ) {
            action += '<p class="content-title mb-0">' + value.url + '</p>';
        } else if ( value.type == 8 ) {
            action += '<p class="content-title mb-0">' + value.text + '</p>';
        }
    });
    var created_date = new Date( data.created_at );
    created_date = created_date.getFullYear() + '年' + ( created_date.getMonth() + 1 ) + '月' + created_date.getDate() + '日 ' + created_date.getHours() + ':' + created_date.getMinutes();

    var html = '<tr>';
    html += '<td class="text-center">';
    if ( check_empty( data.image ) ) {
        html += '<img class="content-image me-2" src="' + $( '#env_media_url' ).val() + data.image + '">';
    } else {
        html += '<img class="content-image me-2" src="' + $( '#env_static_url' ).val() + 'img/image-none.png">';
    }
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<p class="content-title mb-0">' + data.name + '</p>';
    html += '<p class="content-date mb-0">' + created_date + '</p>';
    html += '</td>';
    html += '<td>';
    html += action;
    html += '</td>';
    html += '<td>';
    html += '<input type="hidden" name="id" value="' + data.display_id + '">';
    html += '<a href="/head/richmenu/edit/?id=' + data.display_id + '" class="btn detail-button p-1">詳細</a>';
    html += '</td>';
    html += '</tr>';
    return html;
}