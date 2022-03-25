document.getElementById("student_reg_list").style.display = "none";


let student_reg_form = document.getElementById("student-registration-form");
console.log(12);
const letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н' ,'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', ' ЦЧШЩЪЫЪЭЮЯ]
student_reg_form.addEventListener("change", function(){
    if (student_reg_form.checked){
        let grade_letter = document.getElementById("grade-letter");
        let end_year = document.getElementById("end-year");
        document.getElementById("student_reg_list").style.display = "block";
        document.getElementById("end-year").addEventListener(
        "change", function(){
            $("#id_grade_letter").empty();
            $.getJSON("/get_grades",
            {
                'year': $("#end-year").val()
            }, function(data){
                $.each(data, function(i, val) {
                    console.log(i);
                    $("#id_grade_letter").append("<option>" + i + " : " + val + "</option>");
                  });
                  $("#id_grade_letter").append("<option>other</option>");

            });
        });
    }
    else{
        document.getElementById("student_reg_list").style.display = "none";
    }
});