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