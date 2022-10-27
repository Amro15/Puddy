
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

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
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

// show and hide div
function show_div(str, display_mode){
   div = document.querySelector(str);
   div.style.display=display_mode;
   div.scrollIntoView({ behavior: 'smooth'});
}
function hide_div(str){
   div = document.querySelector(str);
   div.style.display="none";
}
