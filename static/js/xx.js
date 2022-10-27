let x = document.getElementById("");

x.addEventListener("click", ()=>{
    if(x.checked){
        setCookie()
    }
    else{
        // google for func
        delCookie()
    }
})