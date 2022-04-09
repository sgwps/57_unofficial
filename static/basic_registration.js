let username_element = document.getElementById('id_username');
let submit_button = document.getElementById('id_submit');
submit_button.blur();

username_element.addEventListener("change", function(){
    $.getJSON(
        "/check_username", 
        {'username' : $(username_element).val()},
        function(data){
            if (data['result'] == false){
                submit_button.disabled = true;
            }
            else{
                submit_button.disabled = false;
            }
        }
    )
});


let email_element = document.getElementById('id_email');
email_element.addEventListener("change", function(){
    $.getJSON(
        "/check_email", 
        {'email' : $(email_element).val()},
        function(data){
            if (data['result'] == false){
                submit_button.disabled = true;
            }
            else{
                submit_button.disabled = false;
            }
        }
    )
});