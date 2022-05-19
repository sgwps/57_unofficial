const main_input = document.getElementById("main_input")
const text = document.getElementById("user_list")

function checkData(){
    main_input_data = main_input.value
    request = 'get_users?main=' + main_input_data
    $.ajax({
        type: 'GET',
        url: request,
        success: function(response){
            const data = response.response
            for (var key in data){
                user = data[key]
                var inp = document.createElement("text");
                inp.innerHTML = JSON.stringify(user)
                text.appendChild(inp);
            }
            setTimeout(()=>{
                console.log("done");
            }, 500)
        },
        error: function(error){
            console.log(error);
        }
    });
}

main_input.addEventListener("change", checkData)