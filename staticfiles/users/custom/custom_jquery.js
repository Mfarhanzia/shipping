(function($) { // Begin jQuery
    $(function() { // DOM ready
        // // If a link has a dropdown, add sub menu toggle.
        // $('nav ul li a:not(:only-child)').click(function(e) {
        //     $(this).siblings('.nav-dropdown').toggle();
        //     // Close one dropdown when selecting another
        //     $('.nav-dropdown').not($(this).siblings()).hide();
        //     e.stopPropagation();
        // });
        // // Clicking away from dropdown will remove the dropdown class
        // $('html').click(function() {
        //     $('.nav-dropdown').hide();
        // });
        // // Toggle open and close nav styles on click
        // $('#nav-toggle').click(function() {
        //     $('nav ul').slideToggle();
        // });
        // // Hamburger to X toggle
        // $('#nav-toggle').on('click', function() {
        //     this.classList.toggle('active');
        // });

        //remove blank options
        $("ul[id=id_letter_of_credit] > li:first").remove();
        $("ul[id=id_line_of_credit] > li:first").remove();
        $("ul[id=id_learn_about_electric_drive] > li:first").remove();
        $("ul[id=id_septic_infrastructure] > li:first").remove();
        $("ul[id=id_installation_septic_infrastructure] > li:first").remove();


        // add dashes to phone number
        $('#id_phone_number').keyup(function() {
            $(this).val($(this).val().replace(/(\d{3})\-?(\d{3})\-?(\d{4})/, '$1-$2-$3'))
        });

        $('#id_phone_number_8').keyup(function() {
            $(this).val($(this).val().replace(/(\d{3})\-?(\d{3})\-?(\d{4})/, '$1-$2-$3'))
        });


        // id_letter_of_credit
        $("#id_letter_of_credit_1").click(function() {
            $("#id_8").show();
            $('#id_how_much_letter_of_credit').attr('required', 'required');
        });

        // letter_credit2_hides
        $("#id_letter_of_credit_2").click(function() {
            $('#id_how_much_letter_of_credit').removeAttr('required');
            $('#id_how_much_letter_of_credit').val('');
            $("#id_8").hide();
        });

        // line_of_credit show
        $("#id_line_of_credit_1").click(function() {
            $("#id_10").show();
            $('#id_how_much_line_of_credit').attr('required', 'required');
        });

        // linecredit2 hide
        $("#id_line_of_credit_2").click(function() {
            $('#id_how_much_line_of_credit').removeAttr('required');
            $('#id_how_much_line_of_credit').val('');
            $("#id_10").hide();
        });


        //When are u looking to order
        $("#id_when_to_order_0").click(function() {
            $('#id_other_when_to_order').removeAttr('required');
            $('#id_other_when_to_order').val('');
            $("#id_12").hide();
        });

        $("#id_when_to_order_1").click(function() {

            $("#id_12").show();
            $('#id_other_when_to_order').attr('required', 'required');
        });

        // other1
        $("#id_type_of_development_10").click(function() {
            if ($('#id_type_of_development_10').is(":checked")) {
                $("#id_14").show();
                $('#id_other_type_of_development').attr('required', 'required');
            } else {
                $('#id_other_type_of_development').removeAttr('required');
                $('#id_other_type_of_development').val('');
                $("#id_14").hide();
            }
        });

        // other2
        $("#id_type_of_climate_area_6").click(function() {
            if ($('#id_type_of_climate_area_6').is(":checked")) {

                $('#id_other_type_of_climate_area').attr('required', 'required');
            } else {
                $('#id_other_type_of_climate_area').removeAttr('required');
                $('#id_other_type_of_climate_area').val('');
                $("#id_16").hide();
            }
        });

        //admin-check Time access show/hide
        $("input[name=selector]").click(function() {
            access_time_admin()
        });
        access_time_admin()

        //register.html
        $("#id_user_type").click(function() {
            register_Validation()
        });
        register_Validation()

        var $on = 'section';
        $($on).css({
            'background': 'none',
            'border': 'none',
            'box-shadow': 'none'
        });

        //select all
        $("#id_type_of_development_0").click(function() {
            $("#id_type_of_development_1").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_2").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_3").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_4").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_5").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_6").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_7").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_8").prop('checked', $(this).prop('checked'));
            $("#id_type_of_development_9").prop('checked', $(this).prop('checked'));
        });

        //select all
        $("#id_type_of_climate_area_0").click(function() {
            $("#id_type_of_climate_area_1").prop('checked', $(this).prop('checked'));
            $("#id_type_of_climate_area_2").prop('checked', $(this).prop('checked'));
            $("#id_type_of_climate_area_3").prop('checked', $(this).prop('checked'));
            $("#id_type_of_climate_area_4").prop('checked', $(this).prop('checked'));
            $("#id_type_of_climate_area_5").prop('checked', $(this).prop('checked'));
        });

        $('#id_how_much_letter_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })

        $('#id_how_much_line_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })

        $("input[name=price]").inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$', 'align': 'left' })

        var path = window.location.pathname;
        if (path == '/create/buyer/application') {
            $('[href="/create/buyer/application"]').addClass('active1');
        }else if (path == '/order-form/') {
            $('[href="/order-form/"]').addClass('active1');
        }
         
        else if (path == '/login/') {
            $('[href*="/login"]').addClass('active1');
        } else if (path == '/buyer/applications') {
            $('[href="/buyer/applications"]').addClass('active1');
        } 
        else if (path == '/floor-plan') {
            $('.plans').addClass('active1');
            $('[href*="/floor-plan"]').addClass('active1');
        }
         else if (path == '/assembling/') {
            $('[href*="/assembling/"]').addClass('active1');
        }
         else if (path == '/quotation/') {
            $('[href*="/quotation/"]').addClass('active1');
        }
         else if (path == '/view/quotation/') {
            $('[href*="/view/quotation/"]').addClass('active1');
        }
         else if (path == '/register/') {
            $('[href*="/register"]').addClass('active1');
        }
         else if (path == '/dealer/') {
            $('[href*="/dealer/"]').addClass('active1');
        }
         else if (path == '/models') {
            $('.models').addClass('active1');
            $('[href*="/models"]').addClass('active1');
        }
        else if (path == '/electric-cars/') {
            $('[href="/electric-cars/"]').addClass('active1');
            $('.electric_car').addClass('active1');
        }
        else if (path == '/electric-cars/interior') {
            $('.electric_car').addClass('active1');
            $('[href*="/electric-cars/interior"]').addClass('active1');
        }
        else if (path == '/electric-cars/exterior') {
            $('.electric_car').addClass('active1');
            $('[href*="/electric-cars/exterior"]').addClass('active1');
        }
        // else if (path == '/view-content'){  
        else if (path.indexOf('/view/structural-drawings') != -1) {
            $('[href="/view/structural-drawings"]').addClass('active1');
            $('.designs').addClass('active1');
        }
        else if (path.indexOf('/view/architectural-drawings') != -1) {
            $('[href="/view/architectural-drawings"]').addClass('active1');
            $('.designs').addClass('active1');
        }
        else if (path.indexOf('/view/reportsap') != -1) {
            $('[href="/view/reportsap"]').addClass('active1');
            $('.designs').addClass('active1');
        }
         else {
            $('[href="/"]').addClass('active1');
        }



    }); // end DOM ready

    /// show/hide access time 
    function access_time_admin() {
        if ($('#f-option').is(":checked")) {
            $('#time_access_input').attr('required', 'required');
            $("#access_time_div").show();
        } else {
            $('#time_access_input').removeAttr('required');
            $("#access_time_div").hide();
        }
    }

    /// register.html validation
    function register_Validation() {

        if ($('#id_user_type_4').is(":checked")) {
            $("#id_register_9").show();
            $("#id_register_7").hide();
            $("#id_company_name").val('');
            $("#id_register_8").hide();
            $("#id_title").val('');

        } else if ($('#id_user_type_3').is(":checked")) {
            $("#id_register_7").hide();
            $("#id_company_name").val('');
            $("#id_register_8").hide();
            $("#id_title").val('');
            $("#id_register_9").hide();
            $("#id_dealer_no").val('');

        } else if ($('#id_user_type_5').is(":checked")) {
            $("#id_register_7").hide();
            $("#id_company_name").val('');
            $("#id_register_8").hide();
            $("#id_title").val('');
            $("#id_register_9").hide();
            $("#id_dealer_no").val('');
        } else if ($('#id_user_type_0').is(":checked") || $('#id_user_type_1').is(":checked") ||
            $('#id_user_type_2').is(":checked")) {
            $("#id_register_7").show();
            $("#id_register_8").show();
            $("#id_register_9").hide();
            $("#id_dealer_no").val('');
        } else if ($('#id_user_type_6').is(":checked")) {
            $("#id_register_7").show();
            $("#id_register_8").hide();
            $("#id_title").val('');
            $("#id_register_9").hide();
            $("#id_dealer_no").val('');
        }
    }
    // 
    $("select").on('change',function() {
        form_submissions()
    });
    $("select").click(function() {
        form_submissions()
    });

    // form submissions
    $("#print_name").on("focusout",function() {
        $("#buyer_name").text($("#print_name").val()) 
        var d = new Date();
        var month = d.getMonth()+1;
        var day = d.getDate();
        var output = d.getFullYear() + '/' +
            ((''+month).length<2 ? '0' : '') + month + '/' +
            ((''+day).length<2 ? '0' : '') + day;
        $(".date_today").text(output) 
       
    });
    // on form submission
    $("#order_form").submit(function (e) {
            $("#buyer_name").text($("#print_name").val()) 
            var d = new Date();
            var month = d.getMonth()+1;
            var day = d.getDate();
            var output = d.getFullYear() + '/' +
                ((''+month).length<2 ? '0' : '') + month + '/' +
                ((''+day).length<2 ? '0' : '') + day;
            $(".date_today").text(output) 
            Webcam.snap( function(image) {
                $("#image-input_id").val(image);
            });
            // while (true){
            //     if ($("#image-input_id").val()!=""){
            //         console.log("==",$("#image-input_id").val())
            //         break;
            //     }
            //     console.log("==",$("#image-input_id").val())
            // }
        });

    $("#form_submission").click(function() {
        form_submissions()
    });

})(jQuery); // end jQuery
function format(){
    $('#id_how_much_letter_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })
}
function total(){
    $('#total').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })
}

function ajax() {
    document.getElementById("price_span").innerHTML= "$ " + $('#myselect option:selected').val().toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,"); 
}

function form_submissions(){
    var frm = $("#order_form");
        $.ajax({
            type: "GET",
            url: "/add-order/",
            data: frm.serialize(),
            dataType: "json",
            success: function (data) {
                var parts = data.toString().split(".");
                parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                parts.join(".")
                $("#total").html("$ " + parts.join("."));
              
            },
            error: function(data) {
                // console.log("success",data)
                // $("#MESSAGE-DIV").html("Something went wrong!");
            }
        });
        return false;
}

// function form_save(){
//     var frm = $("#order_form");
//     console.log("data",frm)
//     frm.submit(function () {
//         $.ajax({
//             type: frm.attr('method'),
//             url: "/add-order/",
//             data: frm.serialize(),
//             // data:json,
//             dataType: "json",
//             success: function (data) {
//                 $("#total").html("$ " + data.total);
//                 console.log("abc",data.total)
//             },
//             error: function(data) {
//                 console.log("success",data)
//                 // $("#MESSAGE-DIV").html("Something went wrong!");
//             }
//         });
//         return false;
//     });
// }