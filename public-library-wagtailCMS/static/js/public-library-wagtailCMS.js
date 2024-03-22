//back to top button code

//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

//Digital Resources JS

var input_checkboxes = $('input');
for (var i=0; i<input_checkboxes.length; i++)  {
  if (input_checkboxes[i].type == 'checkbox')   {
    input_checkboxes[i].checked = false;
  }
}
function defaultHideIfChecked() {
if($('.db-checkbox:checked').length >0) {
$('#contentAreaDefault').css("display", "none");
$('#contentAreaDefault').removeAttr("aria-live");
$('#contentArea').css("display", "block");
$('#contentArea').attr("aria-live", "polite");
}
}

function toggle(className, obj) {
  $(className).toggle( obj.checked );
}

function defaultShow(){
  if($('#contentArea .db-checkbox:checked').length ==0) {
    $('#contentAreaDefault').css("display", "block");
    $('#contentAreaDefault').attr("aria-live", "polite");
    $('#contentArea').css("display", "none");
    $('#contentArea').removeAttr("aria-live");
  }
}

// set alt text to an empty string per accessibility guidelines for decorative images. TODO: use the wagtail template, rather than JavaScript. 
$("#features img").attr("alt", "");

//add aria-hidden to honeypot field
$('#whf_name').attr('aria-hidden', 'true');
