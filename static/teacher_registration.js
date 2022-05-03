var teacher_reg_checkbox = document.getElementById("id_is_teacher");
var teacher_reg_list = document.getElementById("teacher-registration")
var another_subject_button = document.getElementById("id_another_subject_button")
var other_subjects = document.getElementById("other_subjects")
var len_subjects = 0


if (!teacher_reg_checkbox.checked){
  teacher_reg_list.style.display = "none";
}

teacher_reg_checkbox.addEventListener("change", function(){
    if (teacher_reg_checkbox.checked){
        teacher_reg_list.style.display = "block";
    }
    else{
        teacher_reg_list.style.display = "none";
    }
})
  
another_subject_button.addEventListener("click", function(){
    var inp = document.createElement("input");
    inp.setAttribute("type", "text")
    inp.setAttribute("name", "another_subject" + len_subjects)
    var li = document.createElement("li");
    li.appendChild(inp)
    other_subjects.appendChild(li);
})  
