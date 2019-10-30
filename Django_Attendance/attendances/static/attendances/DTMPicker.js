// $(function() {
$(document).ready(function () {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1970:2019",
      // You can put more options here.
      dateFormat: "yy-mm-dd"
    });

    $("#myAnotherDate").datepicker();
});
