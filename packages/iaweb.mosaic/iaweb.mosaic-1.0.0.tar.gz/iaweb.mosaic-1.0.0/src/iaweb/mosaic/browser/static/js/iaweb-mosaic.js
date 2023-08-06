(function ($) {

  function getGridSize(limit) {
    var number = limit;
    if (window.innerWidth < 900) {
      number = 3;
    }
    if (window.innerWidth < 600) {
      number = 2;
    }
    if (window.innerWidth < 480) {
      number = 1;
    }
    return number;
  }

  $(".flexslider").each(function () {
    var limit = $(this).attr("data-slider");
    $(this).flexslider({
      animation: "slide",
      animationLoop: false,
      itemWidth: 210,
      itemMargin: 5,
      minItems: getGridSize(limit),
      maxItems: getGridSize(limit),
      start: function (slider) {
        $("body").removeClass("loading");
      }
    });
  });

})(jQuery);