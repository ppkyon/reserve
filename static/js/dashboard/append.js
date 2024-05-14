function append_mini_table_area(target, data) {
    if ( $( target ).parents( '.mini-table-paging-area' ).next().next().val() == 'today' ) {
        var image = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.image ) ) {
            image = data.flow.user.profile.image;
        } else if ( check_empty( data.flow.user.display_image ) ) {
            image = data.flow.user.display_image;
        } else {
            image = $( '#env_static_url' ).val() + 'img/user-none.png';
        }
    
        var name = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.name ) ) {
            if ( check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.profile.name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.profile.name;
            }
        } else {
            if ( check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.display_name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.display_name;
            }
        }
        
        var html = '<tr class="position-relative">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.number + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<img src="' + image + '" class="user-image me-2">';
        html += '<p class="d-flex align-items-center content-title mb-0">';
        html += '<span>' + name + '</span>';
        html += '</p>';
        html += '</div>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.flow.user.reserve + '</p>';
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.schedule.offline ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.offline.name + '</p>';
        } else if ( data.flow.user.schedule.online ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.online.name + '</p>';
        }
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.proxy_flg ) {
            html += '<p class="content-title mb-0">未登録</p>';
        } else {
            html += '<p class="content-title mb-0">登録済み</p>';
        }
        html += '</td>';
        html += '<td>';
        html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn action-button">対応</button>';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#edit_step_modal"></button>';
        html += '</td>';
        html += '<td class="text-center">';
        html += '<div class="dropdown d-inline-block p-0">';
        html += '<button type="button" class="btn" data-bs-toggle="dropdown">';
        html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
        html += '</button>';
        html += '<div class="dropdown-menu">';
        html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn dropdown-item dropdown-preview-button fw-bold text-center">プレビュー</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#user_profile_offcanvas"></button>';
        if ( data.flow.user.proxy_flg ) {
            html += '<a href="/temp/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        } else {
            html += '<a href="/user/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        }
        if ( !data.flow.user.proxy_flg ) {
            html += '<a href="/talk/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">1対1トーク</a>';
        }
        if ( !data.flow.user.member_flg ) {
            html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn member-button dropdown-item fw-bold text-center border-top p-1 ps-2 pe-2 pt-2">会員登録</a>';
            html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#member_user_check_modal"></button>';
        }
        html += '</div>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        return html;
    } else if ( $( target ).parents( '.mini-table-paging-area' ).next().next().val() == 'new' ) {
        var image = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.image ) ) {
            image = data.flow.user.profile.image;
        } else if ( check_empty( data.flow.user.display_image ) ) {
            image = data.flow.user.display_image;
        } else {
            image = $( '#env_static_url' ).val() + 'img/user-none.png';
        }
    
        var name = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.name ) ) {
            if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.profile.name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.profile.name;
            }
        } else {
            if ( check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.display_name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.display_name;
            }
        }
        
        var html = '<tr class="position-relative">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.number + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<img src="' + image + '" class="user-image me-2">';
        html += '<p class="d-flex align-items-center content-title mb-0">';
        html += '<span>' + name + '</span>';
        html += '</p>';
        html += '</div>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.flow.user.reserve + '</p>';
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.schedule.offline ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.offline.name + '</p>';
        } else if ( data.flow.user.schedule.online ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.online.name + '</p>';
        }
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.proxy_flg ) {
            html += '<p class="content-title mb-0">未登録</p>';
        } else {
            html += '<p class="content-title mb-0">登録済み</p>';
        }
        html += '</td>';
        html += '<td>';
        html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn check-button">確認</button>';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#check_check_modal"></button>';
        html += '</td>';
        html += '<td class="text-center">';
        html += '<div class="dropdown d-inline-block p-0">';
        html += '<button type="button" class="btn" data-bs-toggle="dropdown">';
        html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
        html += '</button>';
        html += '<div class="dropdown-menu">';
        html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn dropdown-item dropdown-preview-button fw-bold text-center">プレビュー</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#user_profile_offcanvas"></button>';
        if ( data.flow.user.proxy_flg ) {
            html += '<a href="/temp/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        } else {
            html += '<a href="/user/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        }
        if ( !data.flow.user.proxy_flg ) {
            html += '<a href="/talk/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">1対1トーク</a>';
        }
        if ( !data.flow.user.member_flg ) {
            html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn member-button dropdown-item fw-bold text-center border-top p-1 ps-2 pe-2 pt-2">会員登録</a>';
            html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#member_user_check_modal"></button>';
        }
        html += '</div>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        return html;
    } else if ( $( target ).parents( '.mini-table-paging-area' ).next().next().val() == 'after' ) {
        var image = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.image ) ) {
            image = data.flow.user.profile.image;
        } else if ( check_empty( data.flow.user.display_image ) ) {
            image = data.flow.user.display_image;
        } else {
            image = $( '#env_static_url' ).val() + 'img/user-none.png';
        }
    
        var name = '';
        if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.name ) ) {
            if ( check_empty( data.flow.user.profile ) && check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.profile.name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.profile.name;
            }
        } else {
            if ( check_empty( data.flow.user.profile.age ) ) {
                name = data.flow.user.display_name + ' (' + data.flow.user.profile.age + ')';
            } else {
                name = data.flow.user.display_name;
            }
        }
        
        var html = '<tr class="position-relative">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.number + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<img src="' + image + '" class="user-image me-2">';
        html += '<p class="d-flex align-items-center content-title mb-0">';
        html += '<span>' + name + '</span>';
        html += '</p>';
        html += '</div>';
        html += '</td>';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.flow.user.reserve + '</p>';
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.schedule.offline ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.offline.name + '</p>';
        } else if ( data.flow.user.schedule.online ) {
            html += '<p class="content-title mb-0">' + data.flow.user.schedule.online.name + '</p>';
        }
        html += '</td>';
        html += '<td>';
        if ( data.flow.user.proxy_flg ) {
            html += '<p class="content-title mb-0">未登録</p>';
        } else {
            html += '<p class="content-title mb-0">登録済み</p>';
        }
        html += '</td>';
        html += '<td></td>';
        html += '<td class="text-center">';
        html += '<div class="dropdown d-inline-block p-0">';
        html += '<button type="button" class="btn" data-bs-toggle="dropdown">';
        html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
        html += '</button>';
        html += '<div class="dropdown-menu">';
        html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn dropdown-item dropdown-preview-button fw-bold text-center">プレビュー</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#user_profile_offcanvas"></button>';
        if ( data.flow.user.proxy_flg ) {
            html += '<a href="/temp/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        } else {
            html += '<a href="/user/detail/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        }
        if ( !data.flow.user.proxy_flg ) {
            html += '<a href="/talk/?id=' + data.flow.user.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">1対1トーク</a>';
        }
        if ( !data.flow.user.member_flg ) {
            html += '<button type="button" value="' + data.flow.user.display_id + '" class="btn member-button dropdown-item fw-bold text-center border-top p-1 ps-2 pe-2 pt-2">会員登録</a>';
            html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#member_user_check_modal"></button>';
        }
        html += '</div>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        return html;
    } else if ( $( target ).parents( '.mini-table-paging-area' ).next().next().val() == 'line' ) {
        var image = '';
        if ( check_empty( data.profile ) && check_empty( data.profile.image ) ) {
            image = data.profile.image;
        } else if ( check_empty( data.display_image ) ) {
            image = data.display_image;
        } else {
            image = $( '#env_static_url' ).val() + 'img/user-none.png';
        }
    
        var name = '';
        if ( check_empty( data.profile ) && check_empty( data.profile.name ) ) {
            if ( check_empty( data.profile ) && check_empty( data.profile.age ) ) {
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
        
        var html = '<tr class="position-relative">';
        html += '<td>';
        html += '<p class="content-title mb-0">' + data.number + '</p>';
        html += '</td>';
        html += '<td>';
        html += '<div class="d-flex justify-content-start align-items-center">';
        html += '<img src="' + image + '" class="user-image me-2">';
        html += '<p class="d-flex align-items-center content-title mb-0">';
        html += '<span>' + name + '</span>';
        html += '</p>';
        html += '</div>';
        html += '</td>';
        html += '<td>';
        html += '<button type="button" value="' + data.display_id + '" class="btn check-button">確認</button>';
        html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#check_user_modal"></button>';
        html += '</td>';
        html += '<td class="text-center">';
        html += '<div class="dropdown d-inline-block p-0">';
        html += '<button type="button" class="btn" data-bs-toggle="dropdown">';
        html += '<i class="bx bx-dots-horizontal-rounded bx-sm"></i>';
        html += '</button>';
        html += '<div class="dropdown-menu">';
        html += '<button type="button" value="' + data.display_id + '" class="btn dropdown-item dropdown-preview-button fw-bold text-center">プレビュー</button>';
        html += '<button type="button" class="d-none" data-bs-toggle="offcanvas" data-bs-target="#user_profile_offcanvas"></button>';
        if ( data.proxy_flg ) {
            html += '<a href="/temp/detail/?id=' + data.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        } else {
            html += '<a href="/user/detail/?id=' + data.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">詳細</a>';
        }
        if ( !data.proxy_flg ) {
            html += '<a href="/talk/?id=' + data.display_id + '" class="btn dropdown-item fw-bold text-center border-top p-1 pt-2">1対1トーク</a>';
        }
        if ( !data.member_flg ) {
            html += '<button type="button" value="' + data.display_id + '" class="btn member-button dropdown-item fw-bold text-center border-top p-1 ps-2 pe-2 pt-2">会員登録</a>';
            html += '<button type="button" class="up-modal-button d-none" data-bs-toggle="modal" data-bs-target="#member_user_check_modal"></button>';
        }
        html += '</div>';
        html += '</div>';
        html += '</td>';
        html += '</tr>';
        return html;
    }
}