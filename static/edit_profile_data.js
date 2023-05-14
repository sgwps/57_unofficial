
var student_reg_checkbox = document.getElementById("id_is_student");
var student_reg_list = document.getElementById("student-registration")
var custom_grade = document.getElementById("custom-grade");
var end_year = document.getElementById("id_end_year");
var grade = document.getElementById("id_grade")
var custom_grade_letter = document.getElementById("id_custom_grade_letter");
var custom_specialization = document.getElementById("id_custom_specialization")
var submiit_button = document.getElementById("id_submit")
var grade_block = document.getElementById("grade_block")


function EndYearProcesing(data){
    $(grade).empty()
    $(custom_grade_letter).empty()
    submiit_button.disabled = false;
    $(grade).append("<option value=''></option>");


    $.each(data["grades"], function(i, val) {
        let valueOption = document.createElement("option")
        valueOption.innerHTML = val[1][0] + " : " + val[1][1]
        valueOption.value = val[0]
        console.log(val[0], grade_val)
        if (val[0] == grade_val) {
            valueOption.selected=true;
        }
        grade.appendChild(valueOption)
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

custom_grade.style.display = "none";

if (student_reg_checkbox.checked){
    end_year.value = end_year_val
    student_reg_list.style.display = "block";
    checkEndYear();

}
else{
    student_reg_list.style.display = "none";
}


