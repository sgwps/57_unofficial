var flag_add_another = true;

$.getJSON(
    '/get_subjects', 
    function(data){
      console.log(data)
      $.each(data, function(i, val){
        $("#checkboxes_teacher_id").append("<div class='multiselect'> <label class=selectBox for=subject_" + i + 
        "><input type='checkbox' name=subject_" + i + " />" + val + "</label> </div>"
        );
      })
  
    }
  );
  
let teacher_reg_form = document.getElementById("teacher-registration-form");
document.getElementById("teacher_reg_list").style.display = "none";

teacher_reg_form.addEventListener("change", function(){
    if (teacher_reg_form.checked){
        document.getElementById("teacher_reg_list").style.display = "block";

    }
    else{
        document.getElementById("teacher_reg_list").style.display = "none";

    }

})
  
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
  if (flag_add_another){

    var reg_list = document.getElementById("other_subjects")
    var li = document.createElement("li");
    var inp = document.createElement("input");
    inp.setAttribute("type", "text")
    inp.setAttribute("name", "another_subject" + len_subkects)
    inp.setAttribute("id", "another_subject" + len_subkects)
    inp.addEventListener("change", function(){
      let str = $(inp).val();
      if (!str.trim().length) {
        flag_add_another = false;
      } 
      else{
        flag_add_another = true;
      }
    })
    li.appendChild(inp)
    var br = document.createElement("br")
    reg_list.appendChild(br)
  
    reg_list.appendChild(inp);
    len_subkects += 1
    flag_add_another = false;
  }
  }