document.getElementById("student_reg_list").style.display = "none";
document.getElementById("teacher_reg_list").style.display = "none";



function check_end_year(){
    let end_year = document.getElementById("end-year");

    if (end_year.min <= $("#end-year").val() && end_year.max >= $("#end-year").val()){
        return true;
    }
    else return false;
}


let student_reg_form = document.getElementById("student-registration-form");
console.log(12);
const letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К', 'Л', 'М', 'Н' ,'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
student_reg_form.addEventListener("change", function(){
    if (student_reg_form.checked){
        let grade_letter = document.getElementById("grade-letter");
        let end_year = document.getElementById("end-year");
        document.getElementById("student_reg_list").style.display = "block";
        document.getElementById("custom_profile_li").style.display = "none";

        document.getElementById("end-year").addEventListener(
        "change", function(){
            if (check_end_year()){
            $("#id_grade_letter").empty();
            console.log($("#end-year").val());
            $.getJSON("/get_grades",
            {
                'year': $("#end-year").val()
            }, function(data){
                var letters_list = [];
                $.each(data, function(i, val) {
                    console.log(i);
                    $("#id_grade_letter").append("<option>" + i + " : " + val + "</option>");
                    letters_list.push(i);
                  });
                  console.log(letters_list);
                  $("#id_grade_letter").append("<option id='other_letter'>other</option>");
                  for (const i of letters){
                    if (!letters_list.includes(i)) $("#id_grade_letter_other").append("<option>" + i + "</option>");
                  }

                  $('#id_grade_letter').change(function(){
                    var selected = $('option:selected', this).attr('id')
                    if (selected == 'other_letter'){
                        document.getElementById("custom_profile_li").style.display = "block";

                    }
                    else{
                        document.getElementById("custom_profile_li").style.display = "none";

                    }
                    });
            });
        }
        else{
            alert("Enter a valid graduation year")  //делать красную подстветку
        }

        });
    }
    else{
        document.getElementById("student_reg_list").style.display = "none";
    }
});


let teacher_reg_form = document.getElementById("teacher-registration-form");
teacher_reg_form.addEventListener("change", function(){
    if (teacher_reg_form.checked){
        document.getElementById("teacher_reg_list").style.display = "block";

    }
    else{
        document.getElementById("teacher_reg_list").style.display = "none";

    }

})


