$("#mainMenu .dropdown-menu").hover(function(){
  $(this).prev().parent().addClass("menu-border");

  },
  function(){
  $(this).prev().parent().removeClass("menu-border");
}
);
$("#mainMenu a.dropdown-toggle").click(function(event) {
  if ($(this).hasClass("show")) {
    // If the class 'show' is already present, remove it
    $(this).removeClass("show");
    $(this).next().removeClass("show");
    $(this).parent().removeClass("menu-border");
    $(this).attr("aria-expanded", "false");
  } else {
    // If the class 'show' is not present, add it
    $(this).addClass("show");
    $(this).next().addClass("show");
    $(this).parent().addClass("menu-border");
    $(this).attr("aria-expanded", "true");
  }
});

$("#mainMenu a.dropdown-toggle").focusin(function(){
$("#mainMenu .show").removeClass("show");
$("#mainMenu li.menu-border").removeClass("menu-border");
$("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
});


//Adds hover 
$("#mainMenu a.dropdown-toggle").hover(function(){
  $(this).addClass("show");
  $(this).next().addClass("show");
  $(this).parent().addClass("menu-border");
  $(this).attr("aria-expanded", "true");

  },
  function(){
    $(this).removeClass("show");
    $(this).next().removeClass("show");
    $(this).parent().removeClass("menu-border");
    $(this).attr("aria-expanded", "false");
}
);