(function($) { // Begin jQuery
    $(function() { // DOM ready
      // If a link has a dropdown, add sub menu toggle.
      $('nav ul li a:not(:only-child)').click(function(e) {
        $(this).siblings('.nav-dropdown').toggle();
        // Close one dropdown when selecting another
        $('.nav-dropdown').not($(this).siblings()).hide();
        e.stopPropagation();
      });
      // Clicking away from dropdown will remove the dropdown class
      $('html').click(function() {
        $('.nav-dropdown').hide();
      });
      // Toggle open and close nav styles on click
      $('#nav-toggle').click(function() {
        $('nav ul').slideToggle();
      });
      // Hamburger to X toggle
      $('#nav-toggle').on('click', function() {
        this.classList.toggle('active');
      }); 

      //remove blank options
      $("ul[id=id_letter_of_credit] > li:first").remove();
      $("ul[id=id_line_of_credit] > li:first").remove();
      $("ul[id=id_learn_about_electric_drive] > li:first").remove();
      $("ul[id=id_septic_infrastructure] > li:first").remove();
      $("ul[id=id_installation_septic_infrastructure] > li:first").remove();

      
      // add dashes to phone number
      $('#id_phone_number').keyup(function(){
        $(this).val($(this).val().replace(/(\d{3})\-?(\d{3})\-?(\d{4})/,'$1-$2-$3'))
      });

    // $("#id_letter_of_credit").attr('autocomplete', False);
    
    // id_letter_of_credit
    $("#id_letter_of_credit_1").click(function()
    {
      $("#id_8").show();
      $('#id_how_much_letter_of_credit').attr('required', 'required');
    });

    // letter_credit2_hides
    $("#id_letter_of_credit_2").click(function()
    {
      $('#id_how_much_letter_of_credit').removeAttr('required');
      $('#id_how_much_letter_of_credit').val('');
      $("#id_8").hide();
    });

    // line_of_credit show
    $("#id_line_of_credit_1").click(function()
    {
        $("#id_10").show();
        $('#id_how_much_line_of_credit').attr('required', 'required');
    });

    // linecredit2 hide
    $("#id_line_of_credit_2").click(function()
    {
        $('#id_how_much_line_of_credit').removeAttr('required');
        $('#id_how_much_line_of_credit').val('');
        $("#id_10").hide();
    });


    //When are u looking to order
    $("#id_when_to_order_0").click(function()
    { 
        $('#id_other_when_to_order').removeAttr('required');
        $('#id_other_when_to_order').val('');
        $("#id_12").hide();
    });

    $("#id_when_to_order_1").click(function()
    { 

        $("#id_12").show();
        $('#id_other_when_to_order').attr('required', 'required');
    });

    // other1
    $("#id_type_of_development_10").click(function()
    {
        if($('#id_type_of_development_10').is(":checked"))
        {
            $("#id_14").show();
            $('#id_other_type_of_development').attr('required', 'required');
        }
        else
        {
            $('#id_other_type_of_development').removeAttr('required');
            $('#id_other_type_of_development').val('');
            $("#id_14").hide();
        }
    });

    // other2
    $("#id_type_of_climate_area_6").click(function()
    {
        if($('#id_type_of_climate_area_6').is(":checked"))
        {
            $("#id_16").show();
            $('#id_other_type_of_climate_area').attr('required', 'required');
        }
        else
        {
            $('#id_other_type_of_climate_area').removeAttr('required');
            $('#id_other_type_of_climate_area').val('');
            $("#id_16").hide();
        }
    });



    //register.html
    $("#id_user_type").click(function(){
      register_Validation()
    });
    register_Validation()

    var $on = 'section';
    $($on).css({
      'background':'none',
      'border':'none',
      'box-shadow':'none'
    });

    //select all
    $("#id_type_of_development_0").click(function()
    {  
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
    $("#id_type_of_climate_area_0").click(function()
    {  
      $("#id_type_of_climate_area_1").prop('checked', $(this).prop('checked'));
      $("#id_type_of_climate_area_2").prop('checked', $(this).prop('checked'));
      $("#id_type_of_climate_area_3").prop('checked', $(this).prop('checked'));
      $("#id_type_of_climate_area_4").prop('checked', $(this).prop('checked'));
      $("#id_type_of_climate_area_5").prop('checked', $(this).prop('checked'));  
    });
    
    $('#id_how_much_letter_of_credit').inputmask({'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': false, 'prefix': '$'})

    $('#id_how_much_line_of_credit').inputmask({'alias': 'numeric', 'groupSeparator': ',', 'digits': 2, 'digitsOptional': false, 'prefix': '$'})
    
    var path = window.location.pathname;
 
   if (path == '/order'){
      $('[href*="/order"]').addClass('active1');
    }
    else if (path == '/login/'){
      
      $('[href*="/login"]').addClass('active1');
    }

    else if (path == '/view-order'){
      $('[href*="/view-order"]').addClass('active1');
      
    }
    else if (path == '/floor-plan'){
      $('[href*="/floor-plan"]').addClass('active1');
    }
    else if (path == '/register/'){  
      $('[href*="/register"]').addClass('active1');
    }
    else {
      $('[href="/"]').addClass('active1');   
    }
  }); // end DOM ready
  
/// register.html validation
  function register_Validation(){
    $('#dealer_pass_id').remove();    
    if($('#id_user_type_4').is(":checked"))
    {  
      $("#id_register_7").show();
      $("#id_register_4").hide();
      $("#id_company_name").val('');
      $("#id_register_5").hide();
      $("#id_title").val('');
      
    }
    else if($('#id_user_type_3').is(":checked"))
    {
      
      $('<div/>', {
        id: 'dealer_pass_id',
        "class": 'md-form',
        title: 'now this div has a title!'
      }).insertAfter('#id_register_8');

      $('<i>').attr({
        class: 'prefix',
      }).appendTo('#dealer_pass_id');
      
      $('<label>').text('Password').attr({
        for: 'dealer_pass',
        class: 'label',
        title: 'Password',
        placeholder: 'password',
        error: 'wrong',
        success: 'right',
      }).appendTo('#dealer_pass_id');

      $('<br>').appendTo('#dealer_pass_id');

      $('<input>').attr({
        type: 'password',
        id: 'dealer_pass',
        name: 'password',
        required: true
      }).appendTo('#dealer_pass_id');

      $("#id_register_4").hide();
      $("#id_company_name").val('');
      $("#id_register_5").hide();
      $("#id_title").val('');
      $("#id_register_7").hide();
      $("#id_dealer_no").val('');

    }

    else if($('#id_user_type_5').is(":checked"))
    {
      $("#id_register_4").hide();
      $("#id_company_name").val('');
      $("#id_register_5").hide();
      $("#id_title").val('');
      $("#id_register_7").hide();
      $("#id_dealer_no").val('');
    }
    else if($('#id_user_type_0').is(":checked") || $('#id_user_type_1').is(":checked") ||
    $('#id_user_type_2').is(":checked"))
    {
      $("#id_register_4").show();
      $("#id_register_5").show();
      $("#id_register_7").hide();
      $("#id_dealer_no").val('');
    }
}
  
})(jQuery); // end jQuery