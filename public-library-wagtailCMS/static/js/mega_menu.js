//click function
$("#mainMenu a.dropdown-toggle").click(function(event) {
  if ($(this).hasClass("show")) {
    // If the class 'show' is already present, remove it
    $("#mainMenu .show").removeClass("show");
    $("#mainMenu li.menu-border").removeClass("menu-border");
    $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");

  } else if (!$(this).hasClass("show")) {
    // If the class 'show' is not present, add it
    $("#mainMenu .show").removeClass("show");
    $("#mainMenu li.menu-border").removeClass("menu-border");
    $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
    $(this).addClass("show");
    $(this).next().addClass("show");
    $(this).parent().addClass("menu-border");
    $(this).attr("aria-expanded", "true");
  }
});


//spacebar triggers
$("#mainMenu a.dropdown-toggle").keydown(function(event) {
  if (event.which === 32 && $(this).hasClass("show")) {
    // If the class 'show' is already present and spacebar is pressed, remove the show class
    event.preventDefault();
    $("#mainMenu .show").removeClass("show");
    $("#mainMenu li.menu-border").removeClass("menu-border");
    $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
  } else if (event.which === 32 && !$(this).hasClass("show")) {
    // If the class 'show' is not present and spacebar is pressed, add the show class
    event.preventDefault();
    $("#mainMenu .show").removeClass("show");
    $("#mainMenu li.menu-border").removeClass("menu-border");
    $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
    $(this).addClass("show");
    $(this).next().addClass("show");
    $(this).parent().addClass("menu-border");
    $(this).attr("aria-expanded", "true");
  }
});

//use Esc key to close menu items
$("#mainMenu a.dropdown-toggle").keydown(function(event) {
    // Check if the pressed key is the escape key (key code 27)
    if (event.which === 27) { 
        var aria_exp_true = $('[aria-expanded="true"]');
        if (aria_exp_true.length > 0) {
    $("#mainMenu .show").removeClass("show");
    $("#mainMenu li.menu-border").removeClass("menu-border");
    $(this).attr("aria-expanded", "false");
    $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
}
    }
});

//use Esc key to close menu items when delving into the submenus
$("#mainMenu .menu-child-links a.menu-link").keydown(function(event) {
    // Check if the pressed key is the escape key (key code 27)
    if (event.which === 27) {
      $("#mainMenu .show").focus();
      $("#mainMenu .show").removeClass("show");
      $("#mainMenu li.menu-border").removeClass("menu-border");
      $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
    }
});

//closes the menu if clicked outside the menu area
$(document).click(function(event) {
    // Check if the clicked element is not within the div with id "yourDiv"
    if (!$(event.target).closest('#mainMenu a.dropdown-toggle').length) {
        // Code to execute when clicked outside the div
        $("#mainMenu .show").removeClass("show");
        $("#mainMenu li.menu-border").removeClass("menu-border");
        $("#mainMenu a.dropdown-toggle").attr("aria-expanded", "false");
        }
});

//Hover Options disabled
//$("#mainMenu .dropdown-menu").hover(function(){
//  $(this).prev().attr("aria-expanded", "true");
//  $(this).prev().parent().addClass("menu-border");
//
//  },
//  function(){
//  $(this).prev().parent().removeClass("menu-border");
//}
//);

//$("#mainMenu a.dropdown-toggle").hover(function(){
//  $(this).addClass("show");
//  $(this).next().addClass("show");
//  $(this).parent().addClass("menu-border");
//  $(this).attr("aria-expanded", "true");

//  },
//  function(){
//    $(this).removeClass("show");
//    $(this).next().removeClass("show");
//   $(this).parent().removeClass("menu-border");
//    $(this).attr("aria-expanded", "false");
//}
//);