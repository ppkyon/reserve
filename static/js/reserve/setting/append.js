
function append_setting_area(type) {
    var advance_list = [];
    $( '#save_setting_form .setting-list-area' ).each( function( index, value ) {
        if ( !$( this ).hasClass( 'd-none' ) ) {
            $( this ).find( '.input-name' ).each( function( index, value ) {
                advance_list.push({
                    'name': $( this ).val(),
                    'value': $( this ).attr( 'name').replace( 'name_', '' ),
                });
            });
        }
    });

    var count = $( '#' + $( '.save-button' ).next().val() ).find( '.reserve-setting-table' ).children( 'tbody' ).children( 'tr' ).length + 1;
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;
    var html = '<tr style="background-color: #FFF;">';
    html += '<td>';
    html += '<div class="setting-area p-2">';
    html += '<div class="d-flex justify-content-start align-items-stretch p-2">';
    html += '<p class="count-text mt-1 mb-0" style="width: 5%;">' + count + '.</p>';
    html += '<input type="hidden" value="' + random + '">';
    html += '<div class="setting-sp" style="width: 75%;">';
    html += '<div class="d-flex justify-content-start align-items-center mb-1">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">登録名</label>';
    html += '<input type="text" name="name_' + random + '" class="input-text input-name ps-2 pe-2" style="width: 75%;" data-parsley-errors-messages-disabled required>';
    html += '</div>';
    html += '<div class="d-flex align-items-center justify-content-start mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">&nbsp;</label>';
    html += '<p class="description mb-2" style="width: 75%;">登録名は管理画面のみで使用され、ユーザーには表示されません。</p>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">タイトル</label>';
    html += '<input type="text" name="title_' + random + '" class="input-text input-title ps-2 pe-2" style="width: 75%;" data-parsley-errors-messages-disabled required>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">概要</label>';
    html += '<input type="text" name="outline_' + random + '" class="input-text input-outline ps-2 pe-2" style="width: 75%;" data-parsley-errors-messages-disabled>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-start mb-1">';
    html += '<label class="setting-area-tablet mt-2 mb-0" style="width: 15%;">補足</label>';
    html += '<textarea name="note_' + random + '" class="d-block input-textarea ms-0" style="width: 75%;"></textarea>';
    html += '</div>';
    html += '<div class="d-flex align-items-center justify-content-start mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">&nbsp;</label>';
    html += '<p class="description mb-2" style="width: 75%;">タイトル、概要、補足はユーザー画面にも表示されます。</p>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">時間</label>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0" style="width: 22.5%;">';
    html += '<input type="text" name="time_' + random + '" class="input-text input-time input-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly required>';
    html += '<input type="hidden">';
    html += '<div class="dropdown-menu w-100">';
    html += '<button type="button" value="15" class="btn dropdown-item fw-bold text-center">15</button>';
    html += '<button type="button" value="30" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">30</button>';
    html += '<button type="button" value="45" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">45</button>';
    html += '<button type="button" value="60" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">60</button>';
    html += '<button type="button" value="75" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">75</button>';
    html += '<button type="button" value="90" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">90</button>';
    html += '<button type="button" value="105" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">105</button>';
    html += '<button type="button" value="120" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">120</button>';
    html += '<button type="button" value="135" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">135</button>';
    html += '<button type="button" value="150" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">150</button>';
    html += '<button type="button" value="165" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">165</button>';
    html += '<button type="button" value="180" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">180</button>';
    html += '</div>';
    html += '</div>';
    html += '<label class="ps-2 mb-0" style="width: 5%;">分</label>';
    html += '<div class="d-flex justify-content-center align-items-center ps-4">';
    html += '<div class="input-check-wrap text-center mb-0">';
    html += '<input type="checkbox" id="course_flg_' + random + '" name="course_flg_' + random + '" class="input-check input-course-flg">';
    html += '<label for="course_flg_' + random + '" class="input-check-mark position-relative mb-0"></label>';
    html += '</div>';
    html += '<label for="course_flg_' + random + '" class="ps-1 mb-0" style="cursor: pointer;">コース選択</label>';
    html += '</div>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">同時対応数</label>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0" style="width: 22.5%;">';
    html += '<input type="text" name="people_' + random + '" value="" class="input-text input-people input-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly required>';
    html += '<input type="hidden">';
    html += '<div class="dropdown-menu w-100">';
    html += '<button type="button" value="1" class="btn dropdown-item fw-bold text-center">1</button>';
    html += '<button type="button" value="2" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">2</button>';
    html += '<button type="button" value="3" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">3</button>';
    html += '<button type="button" value="4" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">4</button>';
    html += '<button type="button" value="5" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">5</button>';
    html += '<button type="button" value="6" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">6</button>';
    html += '<button type="button" value="7" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">7</button>';
    html += '<button type="button" value="8" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">8</button>';
    html += '<button type="button" value="9" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">9</button>';
    html += '<button type="button" value="10" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">10</button>';
    html += '<button type="button" value="11" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">11</button>';
    html += '<button type="button" value="12" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">12</button>';
    html += '<button type="button" value="13" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">13</button>';
    html += '<button type="button" value="14" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">14</button>';
    html += '<button type="button" value="15" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">15</button>';
    html += '<button type="button" value="16" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">16</button>';
    html += '<button type="button" value="17" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">17</button>';
    html += '<button type="button" value="18" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">18</button>';
    html += '<button type="button" value="19" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">19</button>';
    html += '<button type="button" value="20" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">20</button>';
    html += '<button type="button" value="21" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">21</button>';
    html += '<button type="button" value="22" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">22</button>';
    html += '<button type="button" value="23" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">23</button>';
    html += '<button type="button" value="24" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">24</button>';
    html += '<button type="button" value="25" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">25</button>';
    html += '<button type="button" value="26" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">26</button>';
    html += '<button type="button" value="27" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">27</button>';
    html += '<button type="button" value="28" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">28</button>';
    html += '<button type="button" value="29" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">29</button>';
    html += '<button type="button" value="30" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">30</button>';
    html += '</div>';
    html += '</div>';
    html += '<label class="ps-2 mb-0" style="width: 5%;">人</label>';
    html += '<label class="setting-area-sp ps-4 mb-0" style="width: 20%;">同時施設数</label>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0" style="width: 22.5%;">';
    html += '<input type="text" name="facility_' + random + '" value="" class="input-text input-facility input-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly required>';
    html += '<input type="hidden">';
    html += '<div class="dropdown-menu w-100">';
    html += '<button type="button" value="1" class="btn dropdown-item fw-bold text-center">1</button>';
    html += '<button type="button" value="2" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">2</button>';
    html += '<button type="button" value="3" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">3</button>';
    html += '<button type="button" value="4" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">4</button>';
    html += '<button type="button" value="5" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">5</button>';
    html += '<button type="button" value="6" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">6</button>';
    html += '<button type="button" value="7" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">7</button>';
    html += '<button type="button" value="8" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">8</button>';
    html += '<button type="button" value="9" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">9</button>';
    html += '<button type="button" value="10" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">10</button>';
    html += '<button type="button" value="11" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">11</button>';
    html += '<button type="button" value="12" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">12</button>';
    html += '<button type="button" value="13" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">13</button>';
    html += '<button type="button" value="14" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">14</button>';
    html += '<button type="button" value="15" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">15</button>';
    html += '<button type="button" value="16" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">16</button>';
    html += '<button type="button" value="17" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">17</button>';
    html += '<button type="button" value="18" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">18</button>';
    html += '<button type="button" value="19" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">19</button>';
    html += '<button type="button" value="20" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">20</button>';
    html += '<button type="button" value="21" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">21</button>';
    html += '<button type="button" value="22" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">22</button>';
    html += '<button type="button" value="23" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">23</button>';
    html += '<button type="button" value="24" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">24</button>';
    html += '<button type="button" value="25" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">25</button>';
    html += '<button type="button" value="26" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">26</button>';
    html += '<button type="button" value="27" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">27</button>';
    html += '<button type="button" value="28" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">28</button>';
    html += '<button type="button" value="29" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">29</button>';
    html += '<button type="button" value="30" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">30</button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">回答フォーム</label>';
    html += '<div class="dropdown input-select-dropdown input-question-dropdown d-inline-block p-0" style="width: 45%;">';
    html += '<input type="text" name="question_' + random + '" value="" class="input-text input-question input-select w-100 ps-2 pe-2" data-parsley-errors-messages-disabled readonly>';
    html += '<input type="hidden" value="">';
    html += '</div>';
    html += '<button type="button" value="' + random + '" class="d-none" data-bs-toggle="modal" data-bs-target="#question_modal"></button>';
    html += '<button type="button" value="' + random + '" class="d-none" data-bs-toggle="modal" data-bs-target="#question_modal"></button>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">事前予約</label>';
    html += '<div class="dropdown input-select-dropdown input-advance-dropdown d-inline-block p-0" style="width: 45%;">';
    html += '<input type="text" name="advance_' + random + '" value="" class="input-text input-advance input-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly>';
    html += '<input type="hidden" value="">';
    html += '<div class="dropdown-menu w-100">';
    $.each( advance_list, function( index, value ) {
        if ( index == 0 ) {
            html += '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold ps-2">' + value.name + '</button>';
        } else {
            html += '<button type="button" value="' + value.value + '" class="btn dropdown-item fw-bold border-top p-1 ps-2 pt-2">' + value.name + '</button>';
        }
    });

    html += '</div>';
    html += '</div>';
    html += '</div>';


    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="setting-area-tablet mb-0" style="width: 15%;">予約単位</label>';
    html += '<div class="d-flex align-items-center mb-0">';
    html += '<div class="input-radio-wrap position-relative me-3 mb-1">';
    html += '<label for="reserve_unit_' + random + '_60" class="ps-4 mb-0">1時間毎</label>';
    html += '<input type="radio" id="reserve_unit_' + random + '_60" name="unit_' + random + '" value="60" class="input-radio" data-parsley-multiple="action">';
    html += '<label for="reserve_unit_' + random + '_60" class="input-radio-mark mb-0"></label>';
    html += '</div>';                                                                                                                                                                                                                                                                                                                                                                    
    html += '<div class="input-radio-wrap position-relative me-3 mb-1">';
    html += '<label for="reserve_unit_' + random + '_30" class="ps-4 mb-0">30分毎</label>';
    html += '<input type="radio" id="reserve_unit_' + random + '_30" name="unit_' + random + '" value="30" class="input-radio"  data-parsley-multiple="action">';
    html += '<label for="reserve_unit_' + random + '_30" class="input-radio-mark mb-0"></label>';
    html += '</div>';
    html += '<div class="input-radio-wrap position-relative mb-1">';
    html += '<label for="reserve_unit_' + random + '_15" class="ps-4 mb-0">15分毎</label>';
    html += '<input type="radio" id="reserve_unit_' + random + '_15" name="unit_' + random + '" value="15" class="input-radio" data-parsley-multiple="action">';
    html += '<label for="reserve_unit_' + random + '_15" class="input-radio-mark mb-0"></label>';
    
    
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div style="width: 20%;">';
    html += '<div class="d-flex justify-content-end align-items-start flex-column h-100">';
    html += '<button type="button" value="interview" class="btn delete-item-button ms-auto me-2">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_item_check_modal"></button>';
    html += '<div class="pin-area d-flex align-items-center mt-auto me-1 mb-2">';
    html += '<span class="me-1">非表示</span>';
    html += '<input id="check_pin_' + random + '" type="checkbox" name="display_flg_' + random + '" class="input-required" value="1" checked>';
    html += '<label for="check_pin_' + random + '" class="d-block position-relative mb-0"></label>';
    html += '<span class="ms-2">表示</span>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    if ( type == 'online' ) {
        html += '<div class="row">';
        html += '<div class="col-12">';
        html += '<div class="d-flex justify-content-start align-items-center ms-3">';
        html += '<button type="button" value="' + random + '" class="btn main-button add-meeting-button plus p-0 ps-3 mb-2">ミーティングURLを追加する</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#add_meeting_modal"></button>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '<div class="row">';
        html += '<div class="col-12">';
        html += '<div class="mini-table-area meeting-table-area meeting-table-area-sp ms-3 mb-2" style="width: 95%;">';
        html += '<table class="table reserve-meeting-table reserve-meeting-table-sp mb-0">';
        html += '<thead>';
        html += '<tr>';
        html += '<th style="width: 20%;">ミーティング名</th>';
        html += '<th style="width: 20%;">ミーティングURL</th>';
        html += '<th class="mini-table-date-tablet" style="width: 17.5%;">期限日</th>';
        html += '<th class="mini-table-status-tablet" style="width: 15%;">ステータス</th>';
        html += '<th style="width: 20%;">プラットフォーム</th>';
        html += '<th style="width: 7.5%;"></th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody></tbody>';
        html += '</table>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
    }
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}

function append_meeting_area(target) {
    var now_date = new Date();
    var limit_date = new Date( $( '#save_meeting_form [name=create_date]' ).val() );
    limit_date.setDate( limit_date.getDate() + 90 );
    var number = $( target ).find( '.meeting-table-area table tbody tr' ).length + 1;

    var html = '<tr class="position-relative">';
    html += '<td class="position-relative">';
    html += '<input type="text" value="' + $( '#save_meeting_form [name=name]' ).val() + '" class="input-text input-meeting-name readonly ps-2 pe-2" style="width: 100%;" readonly>';
    html += '</td>';
    html += '<td class="position-relative">';
    html += '<input type="text" value="' + $( '#save_meeting_form [name=url]' ).val() + '" class="input-text input-meeting-url readonly ps-2 pe-2" style="width: 75%;" readonly>';
    html += '<i class="bx bx-copy copy-icon ms-1"></i>';
    html += '<div class="copy-toast-area">';
    html += '<div class="toast align-items-center copy-toast">';
    html += '<div class="toast-body text-center">コピーしました</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '<td>';
    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
        if ( check_empty( $( '#save_meeting_form [name=create_date]' ).val() ) ) {
            html += '<input type="text" value="' + limit_date.getFullYear() + '/' + ( limit_date.getMonth() + 1 ) + '/' + limit_date.getDate() + '" class="input-text input-meeting-limit w-100 readonly ps-2 pe-2" readonly>';
            html += '<input type="hidden" value="' + $( '#save_meeting_form [name=create_date]' ).val() + '" class="input-meeting-start">';
        } else {
            html += '<input type="text" value="-" class="input-text input-meeting-limit w-100 readonly ps-2 pe-2" readonly>';
            html += '<input type="hidden" value="" class="input-meeting-start">';
        }
    } else {
        html += '<input type="text" value="-" class="input-text input-meeting-limit w-100 readonly ps-2 pe-2" readonly>';
        html += '<input type="hidden" value="" class="input-meeting-start">';
    }
    html += '</td>';
    html += '<td>';
    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
        if ( now_date > limit_date ) {
            html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/warning.svg" class="me-2 alert-image">';
            html += '<label class="alert-text mb-0 p-1 ps-2 pe-2" style="top: -40%; left: 43.3%; z-index: 1000;">期限切れです。ミーティングURLを<br>削除してください。</label>';
            html += '<span style="color: #FF0000;">期限切れ</span>';
            html += '<input type="hidden" value="1" class="input-meeting-status">';
        } else {
            html += '<span>使用可能</span>';
            html += '<input type="hidden" value="0" class="input-meeting-status">';
        }
    } else {
        html += '<span>使用可能</span>';
        html += '<input type="hidden" value="0" class="input-meeting-status">';
    }
    html += '</td>';
    html += '<td>';
    if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '1' ) {
        html += '<span>LINEミーティング</span>';
        html += '<input type="hidden" value="1" class="input-meeting-platform">';
        html += '<input type="hidden" value="" class="input-meeting-platform-text">';
    } else if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '2' ) {
        html += '<span>Zoom</span>';
        html += '<input type="hidden" value="2" class="input-meeting-platform">';
        html += '<input type="hidden" value="" class="input-meeting-platform-text">';
    } else if ( $( '#save_meeting_form [name=platform]:checked' ).val() == '9' ) {
        html += '<span>' + $( '#save_meeting_form [name=platform_text]' ).val() + '</span>';
        html += '<input type="hidden" value="9" class="input-meeting-platform">';
        html += '<input type="hidden" value="' + $( '#save_meeting_form [name=platform_text]' ).val() + '" class="input-meeting-platform-text">';
    }
    html += '</td>';
    html += '<td>';
    html += '<div class="dropdown d-inline-block p-0">';
    html += '<button type="button" class="btn ps-0" data-bs-toggle="dropdown">';
    html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
    html += '</button>';
    html += '<div class="dropdown-menu">';
    html += '<button type="button" value="' + $( target ).find( '.count-text' ).next().val() + '_' + number + '" class="btn dropdown-item detail-meeting-button fw-bold text-center">詳細</button>';
    html += '<button type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#save_meeting_modal"></button>';
    html += '<button type="button" class="btn dropdown-item delete-meeting-button fw-bold text-center border-top p-1 pt-2">削除</button>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}