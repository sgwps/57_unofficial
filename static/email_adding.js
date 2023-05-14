var flag_add_another_email = true;
var len_emails = 0;

function AddAnotherEmail(){
    if(flag_add_another_email){
        
        var email_list = document.getElementById("add_email")
        var li = document.createElement("li");
        var inp = document.createElement("input");
        inp.setAttribute("type", "email");
        inp.setAttribute("name", "another_email" + len_emails);
        inp.setAttribute("id", "another_subject" + len_emails);
        inp.addEventListener("change", function(){
            let str = $(inp).val();
            if (!str.trim().length){
                flag_add_another_email = false;
            }
            else{
                flag_add_another_email = true;
            }
        })
        li.appendChild(inp);
        var br = document.createElement("br");
        email_list.appendChild(br);

        email_list.appendChild(inp);
        len_emails += 1;
        flag_add_another_email = false;
    }
}
