//Digital Resources JS

var input_checkboxes = $('input');
for (var i=0; i<input_checkboxes.length; i++)  {
  if (input_checkboxes[i].type == 'checkbox')   {
    input_checkboxes[i].checked = false;
    var numberOfH2Elements = $("#contentAreaDefault h2").length;
    var ariaPolite = $('#politeAlertDefaultContainer').attr({'aria-live': 'polite'});
    $('#politeAlertDefault').text(numberOfH2Elements + ' results available');
  }
}
function defaultHideIfChecked() {
if($('.db-checkbox:checked').length >0) {
  $('#contentAreaDefault').css("display", "none");
  $('#contentArea').css("display", "block");
  var numberOfH2Elements = $('#contentArea div.category[style=""] h2').length;
  var ariaPolite = $('#politeAlertContainer').attr({'aria-live': 'polite'});
  var rmAriaPolite = $('#politeAlertDefaultContainer').removeAttr('aria-live', 'polite');
  $('#politeAlert').text(numberOfH2Elements + ' results available');
}
else if($('.db-checkbox:checked').length ==0) { 
  var ariaPolite = $('#politeAlertDefaultContainer').attr({'aria-live': 'polite'});
  var rmAriaPolite = $('#politeAlertContainer').removeAttr('aria-live', 'polite');
}}

function toggle(className, obj) {
  $(className).toggle( obj.checked );
}

function defaultShow(){
  if($('#contentArea .db-checkbox:checked').length ==0) {
    $('#contentAreaDefault').css("display", "block");
    $('#contentArea').css("display", "none");
  }
}



// set alt text to an empty string per accessibility guidelines for decorative images. TODO: use the wagtail template, rather than JavaScript. 
$("#features img").attr("alt", "");

//add aria-hidden to honeypot field
$('#whf_name').attr('aria-hidden', 'true');

// back to top button code
let top_button = document.getElementById("returnToTopBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    top_button.style.display = "block";
  } else {
    top_button.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}