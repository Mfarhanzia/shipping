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
        // $('.navbar-toggler').on('click', function() {
        //     $('#overlay').slideToggle();
        //     $('.color_15').css({"color":"black"});
        // });

        //remove blank options
        $("ul[id=id_1-letter_of_credit] > li:first").remove();
        $("ul[id=id_1-line_of_credit] > li:first").remove();
        $("ul[id=id_2-learn_about_electric_drive] > li:first").remove();
        $("ul[id=id_1-septic_infrastructure] > li:first").remove();
        $("ul[id=id_1-installation_septic_infrastructure] > li:first").remove();


        // add dashes to phone number
        $('#id_1-phone_number').keyup(function() {
            $(this).val($(this).val().replace(/(\d{3})\-?(\d{3})\-?(\d{3})/, '$1-$2-$3'))
        });

        $('#id_phone_number_8').keyup(function() {
            $(this).val($(this).val().replace(/(\d{3})\-?(\d{3})\-?(\d{4})/, '$1-$2-$3'))
        });

        
        // letter_of_credit show/hide
        letter_of_credit_input()
        $("#id_radio_field_7").on("click",function() {
            letter_of_credit_input()
        });

        // line_of_credit show/hide
        line_of_credit_input()
        $("#id_radio_field_9").on("click",function() {
            line_of_credit_input()
        });


        //When are u looking to order
        $("#id_1-when_to_order_0").click(function() {
            $('#id_1-other_when_to_order').removeAttr('required');
            $('#id_1-other_when_to_order').val('');
            $("#id_12").hide();
        });
        if ($("#id_1-when_to_order_1").is(":checked")){
            $("#id_12").show();
            $('#id_1-other_when_to_order').attr('required', 'required');
        }

        $("#id_1-when_to_order_1").click(function() {
            $("#id_12").show();
            $('#id_1-other_when_to_order').attr('required', 'required');
        });
        show_hide_fields()
        // other1_in registration_step_3
        $("#id_2-type_of_development_10").click(function() {
            show_hide_fields()
        });

        // other2_climate_area
        $("#id_1-type_of_climate_area_6").click(function() {
            if ($('#id_1-type_of_climate_area_6').is(":checked")) {
                $('#id_1-other_type_of_climate_area').attr('required', 'required');
                $('#id_14').show();
            } else {
                $('#id_1-other_type_of_climate_area').removeAttr('required');
                $('#id_1-other_type_of_climate_area').val('');
                $("#id_14").hide();
            }
        });

        //admin-check Time access show/hide
        $("input[name=selector]").click(function() {
            access_time_admin()
        });
        access_time_admin()

        //register.html
        $("#id_1-user_type").click(function() {
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
        $("#id_2-type_of_development_0").click(function() {
            $("#id_2-type_of_development_1").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_2").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_3").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_4").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_5").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_6").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_7").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_8").prop('checked', $(this).prop('checked'));
            $("#id_2-type_of_development_9").prop('checked', $(this).prop('checked'));
        });

        //select all
        $("#id_1-type_of_climate_area_0").click(function() {
            $("#id_1-type_of_climate_area_1").prop('checked', $(this).prop('checked'));
            $("#id_1-type_of_climate_area_2").prop('checked', $(this).prop('checked'));
            $("#id_1-type_of_climate_area_3").prop('checked', $(this).prop('checked'));
            $("#id_1-type_of_climate_area_4").prop('checked', $(this).prop('checked'));
            $("#id_1-type_of_climate_area_5").prop('checked', $(this).prop('checked'));
        });

        $('#id_1-how_much_letter_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$'})

        $('#id_1-how_much_line_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })

        $("input[name=price]").inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$', 'align': 'left' })

        var path = window.location.pathname;
        if (path == '/order-form/') {
            $('[href="/order-form/"]').addClass('active1');
        }
        else if (path == '/login/') {
            $('[href*="/login"]').addClass('active1');
        } else if (path == '/buyer/applications') {
            $('[href="/buyer/applications"]').addClass('active1');
        } 
        else if (path == '/floor-plan') {
            $('.about').addClass('active1');
            $('[href*="/floor-plan"]').addClass('active1');
        }
         else if (path == '/assembling/') {
            $('.about').addClass('active1');
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
        else if (path.indexOf('/view/structural-drawings') != -1) {
            $('[href="/view/structural-drawings"]').addClass('active1');
            $('.about').addClass('active1');
        }
        else if (path.indexOf('/view/architectural-drawings') != -1) {
            $('[href="/view/architectural-drawings"]').addClass('active1');
            $('.about').addClass('active1');
        }
        else if (path == '/concept') {
            $('[href*="/concept"]').addClass('active1');
            $('.about').addClass('active1');
        }
        else if (path == '/amenities') {
            $('[href*="/amenities"]').addClass('active1');
            $('.about').addClass('active1');
        }
        else if (path.indexOf('/view/reportsap') != -1) {
            $('[href="/view/reportsap"]').addClass('active1');
            $('.about').addClass('active1');
        }
        else if (path.indexOf('/contactus') != -1) {
            $('[href="/contactus"]').addClass('active1');
            
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

    /// signup/register.html validation
    function register_Validation() {
        if ($('#id_1-user_type').val() == "homeowner") {
            $("#div_id_dealer_no").show();
            $("#div_id_company_name").hide();
            $("#id_1-company_name").val('');
            $("#div_id_title").hide();
            $("#id_1-title").val('');

        } else if ($('#id_1-user_type').val() == "dealer") {
            $("#div_id_company_name").hide();
            $("#id_1-company_name").val('');
            $("#div_id_title").hide();
            $("#id_1-title").val('');
            $("#div_id_dealer_no").hide();
            $("#id_1-dealer_no").val('');

        } else if ($('#id_1-user_type').val() == "Municipality/Government Official") {
            $("#div_id_company_name").hide();
            $("#id_1-company_name").val('');
            $("#div_id_title").hide();
            $("#id_1-title").val('');
            $("#div_id_dealer_no").hide();
            $("#id_1-dealer_no").val('');
        } else if ($('#id_1-user_type').val() == "developer" || $('#id_1-user_type').val() == "lender" || $('#id_1-user_type').val() == "dealer" ) {
            $("#div_id_company_name").show();
            $("#div_id_title").show();
            $("#div_id_dealer_no").hide();
            $("#id_1-dealer_no").val('');
        } else if ($('#id_1-user_type').val() == "vendor") {
            $("#div_id_company_name").show();
            $("#div_id_title").hide();
            $("#id_1-title").val('');
            $("#div_id_dealer_no").hide();
            $("#id_1-dealer_no").val('');
        }
    }

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
            // $("#buyer_name").text($("#print_name").val()) 
            var d = new Date();
            var month = d.getMonth()+1;
            var day = d.getDate();
            var output = d.getFullYear() + '/' +
                ((''+month).length<2 ? '0' : '') + month + '/' +
                ((''+day).length<2 ? '0' : '') + day;
            $(".date_today").text(output) 
            
        });
    // on form submission
    $("#id_2-accept_1").click(function()
        {
            Webcam.snap( function(image) {
                $("#image-input_id").val(image);
            });
        });
    
    $("#multi-step-continue").click(function()
        {
            if($("#image-input_id").val() == ""){
                Webcam.snap( function(image) {
                    $("#image-input_id").val(image);
                });
            }
    });


    checkbox_checked()
    $(":checkbox").on("change",function(){
        checkbox_checked()
    });

    radio_checked()
    $(":radio").on("change",function(){
        radio_checked()
    });

    $("#form_submission").click(function() {
        form_submissions()
    });

})(jQuery); // end jQuery

function radio_checked(){
    $(":radio").each(function(){
        if($(this).is(":checked")){
            $(this).parent().addClass("checkbox_checked"); 
        }else{
            $(this).parent().removeClass("checkbox_checked");  
        }
    });
}

function checkbox_checked(){
    $(":checkbox").each(function(){
        if($(this).is(":checked")){
            $(this).parent().addClass("checkbox_checked"); 
        }else{
            $(this).parent().removeClass("checkbox_checked");  
        }
    });
}

function format(){
    $('#id_1-how_much_letter_of_credit').inputmask({ 'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': true, 'prefix': '$' })
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
                // console.log("error",data)
                // $("#MESSAGE-DIV").html("Something went wrong!");
            }
        });
        return false;
}

function show_hide_fields(){
    if ($('#id_2-type_of_development_10').is(":checked")) {
        $("#div_id_2-other_type_of_development").show();
        $('#id_2-other_type_of_development').attr('required', 'required');
    } else {
        $('#id_2-other_type_of_development').removeAttr('required');
        $('#id_2-other_type_of_development').val('');
        $("#div_id_2-other_type_of_development").hide();
    }
}
function myFunction(){
    $('#b-color').css("color","black");
}   
function letter_of_credit_input(){
    if ($("#id_1-letter_of_credit_1").is(":checked")){
        $("#id_8").show();
        $('#id_1-how_much_letter_of_credit').attr('required', 'required');
    }
    else{
        $('#id_1-how_much_letter_of_credit').removeAttr('required');
        $('#id_1-how_much_letter_of_credit').val('');
        $("#id_8").hide();
    }
}
function line_of_credit_input(){
    if ($('#id_1-line_of_credit_1').is(":checked")) {
        $("#id_10").show();
        $('#id_1-how_much_line_of_credit').attr('required', 'required');
    }
    else{
        $('#id_1-how_much_line_of_credit').removeAttr('required');
        $('#id_1-how_much_line_of_credit').val('');
        $("#id_10").hide();
    }
}

