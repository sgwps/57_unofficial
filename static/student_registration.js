document.getElementById("student_reg_list").style.display = "none";

function check_end_year(){
    let end_year = document.getElementById("end-year");
    if (end_year.min <= $("#end-year").val() && end_year.max >= $("#end-year").val()){
        return true;
    }
    else return false;
}


let student_reg_form = document.getElementById("student-registration-checkbox");
student_reg_form.addEventListener("change", function(){
    if (student_reg_form.checked){
        document.getElementById("student_reg_list").style.display = "block";
        document.getElementById("custom_grade_li").style.display = "none";
    }
    else{
        document.getElementById("student_reg_list").style.display = "none";
    }
});

function EndYearProcesing(data){
    $.each(data["grades"], function(i, val) {
        $("#id_grade_letter").append("<option value='" + i + "'>" + val[0] + " : " + val[1] + "</option>");
    });
    for (const i of data["letters"])
    {
    $("#id_grade_letter_other").append("<option value='" + i + "'>" + i + "</option>");
    }
    if (document.getElementById("id_grade_letter_other").options.length != 0) {
    $("#id_grade_letter").append("<option id='other_letter' value='0'>other</option>");
    }
    if (document.getElementById("id_grade_letter").options.length == 1) {
        console.log("test44")
        document.getElementById("id_grade_letter").style.display = "none";
        document.getElementById("custom_grade_li").style.display = "block";

    }
    $('#id_grade_letter').change(function(){
    var selected = $('option:selected', this).attr('id')
    if (selected == 'other_letter'){
        document.getElementById("custom_grade_li").style.display = "block";
    }
    else{
        document.getElementById("custom_grade_li").style.display = "none";
    }
    });
}


let end_year = document.getElementById("end-year");
end_year.addEventListener(
    "change", function(){
        if (check_end_year()){
        $("#id_grade_letter").empty();
        $.getJSON("/get_grades",
        {
            'year': $(end_year).val()
        })
        .done(function(data){
            EndYearProcesing(data);
        });
    }
    else{
        alert("Enter a valid graduation year")  //делать красную подстветку
    }

});