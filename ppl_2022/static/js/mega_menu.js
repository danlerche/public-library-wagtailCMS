$("#mainMenu .dropdown-menu").hover(function(){
  $(this).addClass("show");
  $(this).prev().addClass("show");
  $(this).prev().attr("aria-expanded", "true");
  $(this).prev().parent().addClass("menu-border");

  },
  function(){
  $(this).removeClass("show");
  $(this).prev().removeClass("show");
  $(this).prev().parent().removeClass("menu-border");
}
);
$("#mainMenu a.dropdown-toggle").click(function(event){
  $(this).removeClass("show");
  $("#mainMenu .dropdown-menu").removeClass("show");
});

$("#mainMenu a.dropdown-toggle").hover(function(){
  $(this).addClass("show");
  $(this).parent().addClass("menu-border");
  $(this).next().addClass("show");
  $("#mainMenu a.show").attr("aria-expanded", "true");
  $(this).focus();
}
);
$("#mainMenu a.dropdown-toggle").mouseout(function(){
  $(this).removeClass("show");
  $(this).parent().removeClass("menu-border");
  $(this).next().removeClass("show");
  $(this).attr("aria-expanded", "false");
  $("#mainMenu a").blur();

});
$("#mainMenu a.dropdown-toggle").focusin(function(){
$("#mainMenu .show").removeClass("show");
$("#mainMenu li.menu-border").removeClass("menu-border");
$("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
$(this).addClass("show");
$(this).parent().addClass("menu-border");
$(this).attr("aria-expanded", "true");
$(this).next().addClass("show");
});
$("#searchBox #searchForm input").focusin(function(){
$("#mainMenu .show").removeClass("show");
$("#mainMenu li.menu-border").removeClass("menu-border");
$("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
});
$("#logoArea a.navbar-brand").focusin(function(){
$("#mainMenu .show").removeClass("show");
$("#mainMenu li.menu-border").removeClass("menu-border");
$("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
});
//jQuery detect user pressing enter
$("#mainMenu a.dropdown-toggle").click(function(event){
  $(this).addClass("show");
  $(this).next().addClass("show");
});