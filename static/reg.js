let teacher_reg = new Vue({
    el: "#teacher-registration",
    data: {
        checked: false
    }
});


document.getElementById("student_reg_list").style.display = "none";
let student_reg_form = document.getElementById("student-registration-form");
student_reg_form.addEventListener("change", function(){
    console.log(student_reg_form.checked)
    let grade_letter = document.getElementById("grade-letter");
    let end_year = document.getElementById("end-year");
    if (student_reg_form.checked){
        document.getElementById("student_reg_list").style.display = "block";
        document.getElementById("end-year").addEventListener(
        "change", function(){
            console.log($("#end-year").val());
            $("#id_grade_letter").empty();
            $.getJSON("/get_grades",
            {
                'year': $("#end-year").val()
            }, function(data){
                console.log(data)
            })
        }
        )
    }
    else{
        document.getElementById("student_reg_list").style.display = "none";
    }
});