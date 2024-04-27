$(function () {
    $(".slide").on("click", function () {
      $(this).next().slideToggle(300);
      $(this).toggleClass("slide-open", 300);
    });
});