const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        const id = urlParams.get('id')
        if (id != null){
        setInterval(function(){
            const xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/article_in_progress?id=" + id , true);
            xhttp.timeout = 3000;
            xhttp.onreadystatechange=function() {
            if (xhttp.readyState === 4){  
                if(xhttp.status != 200){  
                alert("smt went wrong"); 
                }
            } 
            }
            xhttp.send();
        },
        5000)
        }