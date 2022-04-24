var student_reg_checkbox = document.getElementById("student-registration-checkbox");
var student_reg_list = document.getElementById("student-registration")
var custom_grade = document.getElementById("custom-grade");
var end_year = document.getElementById("id_end_year");
var grade = document.getElementById("id_grade")
var custom_grade_letter = document.getElementById("id_custom_grade_letter");
var custom_specialization = document.getElementById("id_custom_specialization")


student_reg_list.style.display = "none";
custom_grade.style.display = "none";

student_reg_checkbox.addEventListener("change", function(){
    if (student_reg_checkbox.checked){
        student_reg_list.style.display = "block";
    }
    else{
        student_reg_list.style.display = "none";
        custom_grade_letter.attributes.required = false;
        custom_specialization.attributes.required = false;
    }
});

function check_end_year(){
    try{
    if (end_year.min <= $(end_year).val() && end_year.max >= $(end_year).val()){
        return true;
    }
    else{
        return false;
    }
    }
    catch{
    return false;
    }
}


function EndYearProcesing(data){
    $(grade).empty()
    $(grade).append("<option value=''></option>");
    $.each(data["grades"], function(i, val) {
        $(grade).append("<option value='" + i + "'>" + val[0] + " : " + val[1] + "</option>");
    });
    $(custom_grade_letter).append("<option value=''></option>");
    for (const i of data["letters"]) {
    $(custom_grade_letter).append("<option value='" + i + "'>" + i + "</option>");
    }
    if (custom_grade_letter.options.length != 0) {
    $(grade).append("<option id='other_letter' value='other'>other</option>");
    }
    if (grade.options.length == 2) {
        grade.style.display = "none";
        custom_grade.style.display = "block";
    }
    $(grade).change(function(){
    var selected = $('option:selected', this).attr('id')
    if (selected == 'other_letter'){
        custom_grade.style.display = "block";
        $(custom_specialization).attr('required', 'required');            
        $(custom_grade_letter).attr('required', 'required');            
    }
    else{
        custom_grade.style.display = "none";
        $(custom_profile).removeAttr('required');
        $(custom_grade_letter).removeAttr('required');  
    }
    });
}



end_year.addEventListener(
    "change", function(){
    if ($(end_year).val() == ""){
        custom_grade.style.display = "none";
        grade.style.display = "none"
    }
    else if (check_end_year()){
        $(grade).empty();
        $.getJSON("/grades_api",
        {
            'year': $(end_year).val()
        })
        .done(function(data){
            EndYearProcesing(data);
        });
        grade.style.display = "block"

    }
    else{
        alert("Enter a valid graduation year")  //делать красную подстветку
    }

});

function check_grade_form(){
    if ($(custom_grade_letter).val() != "" && $(custom_profile).val() == "") {
    
    }

    else if ($(custom_grade_letter).val() == "" && $(custom_profile).val() != ""){

    }

    else{
        
    }
    
}


custom_grade_letter.addEventListener(
    "change", check_grade_form()
);

custom_profile.addEventListener(
    "change", check_grade_form()
);
