function check_year() {
	
}

const graduation_year = document.getElementById("id_end_year")
const letter = document.getElementById("id_grade_letter")


graduation_year.addEventListener('input', check_active)

function check_active(){
	if(parseInt(el.value) < parseInt(el.min) && parseInt(el.value) > parseInt(el.max)){
      el.value = el.min;
    }
    else {
      el.value = el.max;
    }
}