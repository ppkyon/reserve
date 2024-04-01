
function append_facility_area() {
    var count = $( '#' + $( '.save-button' ).next().val() ).find( '.facility-setting-table' ).children( 'tbody' ).children( 'tr' ).length;
    var random = Math.floor( Math.random() * ( ( 99999999 + 1 ) - 10000000 ) ) + 2;

    var html = '<tr style="background-color: #FFF;">';
    html += '<td>';
    html += '<div class="facility-area p-2">';
    html += '<div class="d-flex justify-content-start align-items-stretch p-2">';
    html += '<p class="count-text mt-1 mb-0" style="width: 5%;">' + ( count + 1 ) + '.</p>';
    html += '<input type="hidden" value="' + random + '"></input>';
    html += '<div style="width: 75%;">';
    html += '<div class="d-flex justify-content-start align-items-center mb-2">';
    html += '<label class="mb-0" style="width: 15%;">設備名</label>';
    html += '<input type="text" name="name_' + random + '" class="input-text input-name ps-2 pe-2" style="width: 75%;" data-parsley-errors-messages-disabled required>';
    html += '</div>';
    html += '<div class="d-flex justify-content-start align-items-center mb-1">';
    html += '<label class="mb-0" style="width: 15%;">受付可能数</label>';
    html += '<div class="dropdown input-select-dropdown d-inline-block p-0" style="width: 22.5%;">';
    html += '<input type="text" name="count_' + random + '" class="input-text input-select input-count display-result-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly required>';
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
    html += '<label class="ps-4 mb-0" style="width: 20%;">振り分け順</label>';
    html += '<div class="dropdown input-select-dropdown input-order-dropdown d-inline-block p-0" style="width: 22.5%;">';
    html += '<input type="text" name="order_' + random + '" value="' + ( count + 1 ) + '" class="input-text input-select input-order display-result-select w-100 ps-2 pe-2" data-bs-toggle="dropdown" data-parsley-errors-messages-disabled readonly required>';
    html += '<div class="dropdown-menu w-100">';
    for ( var i = 1; i <= count; i++ ) {
        if ( i == 1 ) {
            html += '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center">' + i + '</button>';
        } else {
            html += '<button type="button" value="' + i + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">' + i + '</button>';
        }
    }
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '<div style="width: 20%;">';
    html += '<div class="d-flex justify-content-end align-items-start">';
    html += '<button type="button" value="facility" class="btn delete-item-button ms-auto me-2">';
    html += '<img src="' + $( '#env_static_url' ).val() + 'img/icon/cross.svg">';
    html += '</button>';
    html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#delete_item_check_modal"></button>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</td>';
    html += '</tr>';
    return html;
}