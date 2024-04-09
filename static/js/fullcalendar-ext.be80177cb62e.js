$(document).ready(function(){
  // Select the td element with specific class values
  var tdElement = $('td.fc-day.fc-daygrid-day[aria-labelledby]');
  
  // Get the value of the data-date attribute
  var dataDateValue = tdElement.attr('data-date');
  
  // Convert the dataDateValue to a human-readable format
  var dateObj = new Date(dataDateValue);
  var options = { year: 'numeric', month: 'long', day: 'numeric' };
  var formattedDate = dateObj.toLocaleDateString('en-US', options);
  
  // Set the value of the new aria-label attribute
  tdElement.attr('aria-label', formattedDate);
  $('.fc-daygrid-day-top a').removeAttr('aria-label');

});

$(document).ready(function(){
    // Select the button by its class
    $('.fc-prevYear-button').attr('aria-label', 'Previous year');
    $('.fc-nextYear-button').attr('aria-label', 'Next year');
    $('.fc-prev-button').attr('aria-label', 'Previous month');
    $('.fc-next-button').attr('aria-label', 'Next month');
});

//update previous buttons with aria-labels based on the view selected
$(document).ready(function(){
// Function to update aria-label
function updateAriaLabel() {
// Find the button element
var button = $('.fc-prev-button');

// Get the title attribute
var title = button.attr('title');

// Set the aria-label attribute to the same value as the title
button.attr('aria-label', title);
}

// Initial update
updateAriaLabel();

// Click event handler for first update button
$('.fc-dayGridMonth-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-timeGridWeek-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-timeGridDay-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-listMonth-button').click(function(){
// Call the update function
updateAriaLabel();
});
});

//update next buttons with aria-labels based on the view selected
$(document).ready(function(){
// Function to update aria-label
function updateAriaLabel() {
// Find the button element
var button = $('.fc-next-button');

// Get the title attribute
var title = button.attr('title');

// Set the aria-label attribute to the same value as the title
button.attr('aria-label', title);
}

// Initial update
updateAriaLabel();

// Click event handler for first update button
$('.fc-dayGridMonth-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-timeGridWeek-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-timeGridDay-button').click(function(){
// Call the update function
updateAriaLabel();
});

// Click event handler for second update button
$('.fc-listMonth-button').click(function(){
// Call the update function
updateAriaLabel();
});
});

//show today aria-label
$(document).ready(function(){
// Add aria-label attribute to the button
$('.fc-today-button').attr('aria-label', 'show today');
});


$(document).ready(function() {
    // Function to remove aria-hidden attribute for elements with class fc-list-day-side-text
    function removeAriaHidden() {
        $('.fc-list-day-side-text').attr('aria-hidden', 'false');
    }

    // Trigger the function when a button with class fc-listMonth-button is clicked
    $('.fc-listMonth-button').click(function() {
        removeAriaHidden();
    });
});