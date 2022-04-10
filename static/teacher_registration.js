$.getJSON(
    '/get_subjects', 
    function(data){
      $.each(data, function(i, val){
        $("#checkboxes_teacher_id").append("<div class='multiselect'> <label class=selectBox for=subject_" + i + 
        "><input type='checkbox' id=subject_" + i + " />" + val + "</label> </div>"
        );
      })
  
    }
  );
  
  
  var checkboxes = document.getElementById("checkboxes_teacher_id");
  var expanded = false;
  checkboxes.style.display = "none";
  function showCheckboxes() {
    var checkboxes = document.getElementById("checkboxes_teacher_id");
    if (!expanded) {
      checkboxes.style.display = "block";
      expanded = true;
    } else {
      checkboxes.style.display = "none";
      expanded = false;
    }
  }
  
  var len_subkects = 0
  function AddAnotherSubject(){
  if (len_subkects == 0 || document.getElementById("another_subject" + (len_subkects - 1)).val != ""){

    var reg_list = document.getElementById("other_subjects")
    var li = document.createElement("li");
    var inp = document.createElement("input");
    inp.setAttribute("type", "text")
    inp.setAttribute("name", "another_subject" + len_subkects)
    inp.setAttribute("id", "another_subject" + len_subkects)
    li.appendChild(inp)
    var br = document.createElement("br")
    reg_list.appendChild(br)
  
    reg_list.appendChild(inp);
    len_subkects += 1
  }
  }


let teacher_reg_form = document.getElementById("teacher-registration-form");
teacher_reg_form.addEventListener("change", function(){
    if (teacher_reg_form.checked){
        document.getElementById("teacher_reg_list").style.display = "block";

    }
    else{
        document.getElementById("teacher_reg_list").style.display = "none";

    }

})