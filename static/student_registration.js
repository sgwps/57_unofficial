var student_reg_checkbox = document.getElementById("id_is_student");
var student_reg_list = document.getElementById("student-registration")
var custom_grade = document.getElementById("custom-grade");
var end_year = document.getElementById("id_end_year");
var grade = document.getElementById("id_grade")
var custom_grade_letter = document.getElementById("id_custom_grade_letter");
var custom_specialization = document.getElementById("id_custom_specialization")
var submiit_button = document.getElementById("id_submit")
var grade_block = document.getElementById("grade_block")

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
    $(custom_grade_letter).empty()
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
        grade_block.style.display = "none";
        custom_grade.style.display = "block";
        $(grade).val('other');
    }
    else{
        grade_block.style.display = "block";
        custom_grade.style.display = "none";
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


function checkEndYear(){
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
        submiit_button.disabled = false;  

    }
    else{
        alert("Enter a valid graduation year");  //делать красную подстветку
        submiit_button.disabled = true;  

    }

}

end_year.addEventListener(
    "change", checkEndYear);

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