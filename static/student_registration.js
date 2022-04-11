var student_reg_list = document.getElementById("student_reg_list")
var custom_profile = document.getElementById("id_custom_profile");
var end_year = document.getElementById("end-year");
var student_reg_form = document.getElementById("student-registration-checkbox");
var custom_grade_letter = document.getElementById("id_grade_letter_other");
var grade_letter = document.getElementById("id_grade_letter")
var custom_grade = document.getElementById("custom_grade_li")



student_reg_list.style.display = "none";

$.getJSON("/get_specializations").done(
    function(data){
        $(custom_profile).append(
            "<option value=''></option>"
        );
        $.each(data, function(i, val){
            $(custom_profile).append(
                "<option value='" + i + "'>" + val + "</option>"
            );
          })
    }
)
custom_grade.style.display = "none";
grade_letter.style.display = "none"

function check_end_year(){
    if (end_year.min <= $(end_year).val() && end_year.max >= $(end_year).val()){
        return true;
    }
    else return false;
}


student_reg_form.addEventListener("change", function(){
    if (student_reg_form.checked){
        student_reg_list.style.display = "block";
    }
    else{
        student_reg_list.style.display = "none";
        custom_grade_letter.attributes.required = false;
        custom_profile.attributes.required = false;
    }
});

function EndYearProcesing(data){
    $(grade_letter).empty()
    $(grade_letter).append("<option value=''></option>");
    $.each(data["grades"], function(i, val) {
        $(grade_letter).append("<option value='" + i + "'>" + val[0] + " : " + val[1] + "</option>");
    });
    $(custom_grade_letter).append("<option value=''></option>");
    for (const i of data["letters"]) {
    $(custom_grade_letter).append("<option value='" + i + "'>" + i + "</option>");
    }
    if (document.getElementById("id_grade_letter_other").options.length != 0) {
    $("#id_grade_letter").append("<option id='other_letter' value='other'>other</option>");
    }
    if (document.getElementById("id_grade_letter").options.length == 2) {
        grade_letter.style.display = "none";
        custom_grade.style.display = "block";
    }
    $(grade_letter).change(function(){
    var selected = $('option:selected', this).attr('id')
    if (selected == 'other_letter'){
        document.getElementById("custom_grade_li").style.display = "block";
    }
    else{
        document.getElementById("custom_grade_li").style.display = "none";
        submit_button.disabled = false;
    }
    });
}


end_year.addEventListener(
    "change", function(){
    if ($(end_year).val() == ""){
        custom_grade.style.display = "none";
        grade_letter.style.display = "none"
    }
    else if (check_end_year()){
        $("#id_grade_letter").empty();
        $.getJSON("/get_grades",
        {
            'year': $(end_year).val()
        })
        .done(function(data){
            EndYearProcesing(data);
        });
        grade_letter.style.display = "block"

    }
    else{
        alert("Enter a valid graduation year")  //делать красную подстветку
    }

});



custom_grade_letter.addEventListener(
    "change", function(){
        console.log($(custom_grade_letter).val)
        if ($(custom_grade_letter).val() != "" && $(custom_profile).val() == "") {
            submit_button.disabled = true;
            console.log("test831")

        }
        else if ($(custom_grade_letter).val() == "" && $(custom_profile).val() != ""){
            submit_button.disabled = true;
            console.log("test832")


        }
        else{
            submit_button.disabled = false;
            console.log("test833")

        }
    }
);

custom_profile.addEventListener(
    "change", function(){
        if ($(custom_grade_letter).val() != "" && $(custom_profile).val() == "") {
            submit_button.disabled = true;
            console.log("test834")


        }
        else if ($(custom_grade_letter).val() == "" && $(custom_profile).val() != ""){
            submit_button.disabled = true;
            console.log("test835")


        }
        else{
            submit_button.disabled = false;
            console.log("test836")

        }
    }
)