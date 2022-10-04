
window.onload=function(){
   // Dropdown list btn
  let nav_dropdown_btn = document.getElementById("dropdown-btn");
  let dropdown_elements = document.getElementById("list-items");
   //variables used in other func but declared here to hide them when dropwdown elements shown
let toggle_nav = document.getElementById("toggle_nav");
let toggle_note = document.getElementById("toggle_note");
  if(nav_dropdown_btn){
   nav_dropdown_btn.addEventListener("click", ()=>{
     if(dropdown_elements.style.display !=="block") {  
        dropdown_elements.style.display ="block";  
     } else {  
        dropdown_elements.style.display ="none";  
     }   
})}

// Show pass btn
// /Signin /Register
let checkBox = document.getElementById("showPassBtn");
let pass = document.getElementById("password");
let cpass = document.getElementById("cpassword");
if(checkBox){
checkBox.addEventListener("click", ()=>{
   if(checkBox.checked){
   if (pass && pass.type === "password") {
      pass.type = "text";
    } 
   if (cpass && cpass.type === "password") {
      cpass.type = "text";
      }
   }
   else{
      if (pass){
         pass.type = "password";
      }
      if (cpass){
         cpass.type = "password";
      }
   }
})}

// Logout user
let logout_btn = document.getElementById("logout")
let confirm_logout_btn = document.getElementById("confirm_logout");

if (logout_btn){
   logout_btn.addEventListener("click",()=>{
      const logout_modal = new bootstrap.Modal(document.getElementById('logout_modal'), {backdrop:"static" });
            logout_modal.show();
            confirm_logout_btn.addEventListener("click", ()=>{
               window.location.replace(window.origin+"/Signout")
            })
            
   })
}



// /Get Inspired
let search_btn = document.getElementById("search_poem")
if (search_btn){
   let send = true
   search_btn.addEventListener("click", ()=>{
      search_btn.setAttribute("disabled","disabled");
      let send_to_server_poem_search;
      let poem_search = document.getElementById("poem_search");
      let search_by = document.getElementsByClassName("search_by");
      for(let i =0; i<search_by.length; i++){
         if (search_by.item(i).checked && poem_search.value){
            send_to_server_poem_search = {"request":"search poem", "search by": search_by.item(i).id, "query":poem_search.value};
            send = true;
         }
      }
      if (!send_to_server_poem_search){
         send = false;
      }
         console.log(send)
      if(send){
         let loading_div = document.getElementById("loading_poems");
         loading_div.style.cssText="visibility:visible; position:relative";
         fetch(window.origin+"/GetInspired",{
            method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_poem_search)
         })

         .then((respone)=>{
            // if request fails
            if (respone.status !== 200){
               console.log("request status for search poem is"+respone.status);
               return;
            }
            // if request succeeds 
         respone.json().then((data)=>{
            if(data["response"]!=="empty"){
               window.location.reload();
               // let poem_select = document.getElementById("poem_search_select");
               // let poem_result = document.getElementById("poem_result");
               // console.log("Data recieved")
               // poem_result.innerHTML = "";
               // poem_select.options.length = 0;
               // loading_div.style.cssText="visibility:hidden; position:absolute";
               // for(let i in data["response"]){
               //    if(i == 10){
               //       poem_result.innerHTML +='<button class="button">Load More</button>';
               //       break;
               //    }
               //       // poem_obj = JSON.parse(data["response"][i]);
               //       poem_obj = data["response"][i];
               //       poem_select.options[poem_select.options.length]= new Option(`${poem_obj["title"]} / ${poem_obj["author"]}`, `#${i}`)
               //       poem_result.innerHTML += `<div id="${i}"><h3>${poem_obj["title"]} By ${poem_obj["author"]}</h3><br>`;
               //       for(let i in poem_obj["lines"]){
               //          console.log("making lines")
               //          poem_result.innerHTML +=`<pre>${poem_obj["lines"][i]}`;
               //       }        
               //       poem_result.innerHTML +="</pre></div><br><hr><br></br>";
               //    }
               search_btn.removeAttribute("disabled");
            }
            
         });
   });
}
else{
   poem_result.innerHTML = "<p class='error_msg'>No Matches</p>"
}
   })
   
}
let random_poem = document.getElementById("poem_rand");
if (random_poem){
   random_poem.addEventListener("click",()=>{
      let loading_div = document.getElementById("loading_poems");
      loading_div.style.cssText="visibility:visible; position:relative";

      random_poem.setAttribute("disabled", "disabled")
      fetch(window.origin+"/GetInspired",{
         method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify({"request":"random"})
         })

         .then((respone)=>{
            // if request fails
            if (respone.status !== 200){
               console.log("request status for is"+respone.status);
               return;
            }
            // if request succeeds 
         respone.json().then((data)=>{ 
            let poem_select = document.getElementById("poem_search_select");
            let poem_result = document.getElementById("poem_result");
               console.log("Data recieved")
               console.log(data)
               poem_result.innerHTML = "";
               poem_select.options.length = 0;
               loading_div.style.cssText="visibility:hidden; position:absolute";
               for(let i in data["response"]){
                  poem_obj = JSON.parse(data["response"][i]);
                  poem_select.options[poem_select.options.length]= new Option(`${poem_obj["Title"]} / ${poem_obj["Poet"]}`, `#${i}`)
                  poem_result.innerHTML += `<div id="${i}"><h3>${poem_obj["Title"]} By ${poem_obj["Poet"]}</h3><pre>${poem_obj["Poem"]}</pre></div><br><hr><br>`        
                  
                  }
               random_poem.removeAttribute("disabled");
         });
   });
   })
}
}

// cookie functions
function setCookie(name,value,days) {
   var expires = "";
   if (days) {
       var date = new Date();
       date.setTime(date.getTime() + (days*24*60*60*1000));
       expires = "; expires=" + date.toUTCString();
   }
   document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
   var nameEQ = name + "=";
   var ca = document.cookie.split(';');
   for(var i=0;i < ca.length;i++) {
       var c = ca[i];
       while (c.charAt(0)==' ') c = c.substring(1,c.length);
       if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
   }
   return null;
}
