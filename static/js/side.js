$(function () {
    $(".slide").on("click", function () {
      $(this).next().slideToggle(300);
      $(this).toggleClass("slide-open", 300);
    });

    if ($('.slide-user li').hasClass('active')) {
      $('.slide-user').addClass("slide-active");
      $('.slide-user-area').addClass("active-cursor");
    } else {
      $('.slide-user').removeClass("slide-active");
      $('.slide-user-area').removeClass("active-cursor");
    };

    if ($('.slide-template li').hasClass('active')) {
      $('.slide-template').addClass("slide-active");
      $('.slide-template-area').addClass("active-cursor");
    } else {
      $('.slide-template').removeClass("slide-active");
      $('.slide-template-area').removeClass("active-cursor");
    }

    if ($('.slide-setting li').hasClass('active')) {
      $('.slide-setting').addClass("slide-active");
      $('.slide-setting-area').addClass("active-cursor");
    } else {
      $('.slide-setting').removeClass("slide-active");
      $('.slide-setting-area').removeClass("active-cursor");
    }


});