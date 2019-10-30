// $(function(){
$(document).ready(function(){
    $.validator.addMethod(
        "ValidateDateFormat",
        function(value, element) {
            // put your own logic here, this is just a (crappy) example
            // return value.match(/^\d\d\d\d?-\d\d?-\d\d$/);
            return value.match(/^(19|20)\d{2}[-](0?[1-9]|1[0-2])[-](0?[1-9]|[12][0-9]|3[0-1])$/);
        },
        "Please enter a valid date. Ex:2018-01-01"
    );

    // Must ust form id to use the Jquery validation function. class id doesn't work.

    // $(".datepicker").validate({
    //     rules:{
    //         start_date:{
    //             required:true,
    //             ValidateDateFormat:true
    //         },
    //         end_date:{
    //             required:true,
    //             ValidateDateFormat:true
    //         }
    //     },
    //     messages:{
    //         start_date:{
    //             required:"Please enter a date.",
    //             start_date:"please enter a valid date."
    //         },
    //         end_date:{
    //             required:"Please enter a date.",
    //             end_date:"please enter a valid date."
    //         }
    //     }
    // });

    $("#date_search_form").validate({
        rules:{
            start_date:{
                required:true,
                ValidateDateFormat:true
            },
            end_date:{
                required:true,
                ValidateDateFormat:true
            }
        },
        messages:{
            start_date:{
                required:"Please enter a date.",
                start_date:"please enter a valid date."
            },
            end_date:{
                required:"Please enter a date.",
                end_date:"please enter a valid date."
            }
        }
    });

});