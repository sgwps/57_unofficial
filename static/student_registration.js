var student_reg_checkbox = document.getElementById("student-registration-checkbox");
var student_reg_list = document.getElementById("student-registration")
var custom_grade = document.getElementById("custom-grade");
var end_year = document.getElementById("id_end_year");
var grade = document.getElementById("id_grade")
var custom_grade_letter = document.getElementById("id_custom_grade_letter");
var custom_specialization = document.getElementById("id_custom_specialization")
var submiit_button = document.getElementById("id_submit")


student_reg_list.style.display = "none";
custom_grade.style.display = "none";


student_reg_checkbox.addEventListener("change", function(){
    if (student_reg_checkbox.checked){
        student_reg_list.style.display = "block";
    }
    else{
        student_reg_list.style.display = "none";
        submiit_button.disabled = false;
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
    submiit_button.disabled = false;
    $(grade).append("<option></option>");


    $.each(data["grades"], function(i, val) {
        $(grade).append("<option value='" + val[0] + "'>" + val[1][0] + " : " + val[1][1] + "</option>");
    });

    $(custom_grade_letter).append("<option value=''></option>");
    for (const i of data["letters"]) {
    $(custom_grade_letter).append("<option value='" + i + "'>" + i + "</option>");
    }
    if (custom_grade_letter.options.length > 1) {
    $(grade).append("<option id='other_letter' value='other'>other</option>");
    }


    if (grade.options.length == 2) {
        grade.style.display = "none";
        custom_grade.style.display = "block";
        $(grade).val('other');
    }

    $(grade).change(function(){
    var selected = $('option:selected', this).attr('id')
    if (selected == 'other_letter'){
        custom_grade.style.display = "block";          
    }
    else{
        custom_grade.style.display = "none";
        submiit_button.disabled = false;  
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

    if ($(custom_grade_letter).val() != "" && $(custom_specialization).val() == 0) {
        submiit_button.disabled = true;
    }

    else if ($(custom_grade_letter).val() == "" && $(custom_specialization).val() != 0){
        submiit_button.disabled = true;
    }
    else{
        submiit_button.disabled = false;
    }
    
}


custom_grade_letter.addEventListener(
    "change", check_grade_form
);

custom_specialization.addEventListener(
    "change", check_grade_form
);
