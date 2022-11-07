let flex_container = document.getElementsByClassName("flex-item");
let show_poem = document.getElementsByClassName("show_poem");
let poem_div = document.getElementsByClassName("poem_container");
let arrow_btn = document.getElementsByClassName("arrow_icon");
let ctr = 0;
for(let i =0; i<show_poem.length; i++){
   show_poem[i].addEventListener("click", ()=>{
      if(ctr==0){
         console.log("poem_div", poem_div[i])
         poem_div[i].style.display = "block";
         flex_container[i].style.cssText = "flex-basis:100%";
         arrow_btn[i].setAttribute("src", "/static/icons/up-arrow.png");
      }
      else{
         if(poem_div[i].style.display=="block"){
            poem_div[i].style.display="none";
            flex_container[i].style.cssText = "flex-basis:";
            arrow_btn[i].setAttribute("src", "/static/icons/down-arrow.png");
         }
         else{
            poem_div[i].style.display="block";
            flex_container[i].style.cssText = "flex-basis:100%";
            arrow_btn[i].setAttribute("src", "/static/icons/up-arrow.png");
         }
      }
      ctr++;
   })
}

let delete_poem = document.getElementsByClassName("delete_poem");
   let selectobject = document.getElementById("poem_select");
   for(let i=0; i<delete_poem.length; i++){
      const poem_modal = new bootstrap.Modal(document.getElementById('poem_modal'), { keyboard: false, backdrop: "static" });
      let stop_showing_modal = document.getElementById("dont_show_poem_modal")
      delete_poem.item(i).addEventListener("click", ()=>{
      if(!getCookie("hide_poem_modal")){
            poem_modal.show();
            document.getElementById("delete_poem_btn").addEventListener("click", ()=>{
               if(stop_showing_modal.checked){
                  setCookie("hide_poem_modal", true, 365);
            }
            poem_modal.hide();
            let send_to_server_poem_delete = {"poem_id":document.getElementsByClassName("poem count")[i].getAttribute("value")}
      fetch(window.origin+"/Account/Poems",{
         method:"POST",
            headers: new Headers({
               "X-CSRFToken":document.getElementsByName("csrf_token")[0].value,
               "Request":"delete poem",
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_poem_delete)
         })

         .then((respone)=>{
            if (respone.status !== 200){
               console.log("request status for is"+respone.status);
               return;
            }
         respone.json().then((data)=>{
            if (data["response"] === "successful"){
               for (let i=0; i<selectobject.length; i++) {
                  if (selectobject.options[i].id == send_to_server_poem_delete["poem_id"])
                     selectobject.remove(i);
               }
               document.getElementsByName(send_to_server_poem_delete["poem_id"])[0].style.display = "none";
               if(selectobject.length==1){
                  window.location.reload();
               }
            }
         });
      });
   })
}
// if cookie hide draft  == true delete poem without warning
else{
   let send_to_server_poem_delete = {"poem_id":document.getElementsByClassName("poem count")[i].getAttribute("value")}
   fetch(window.origin+"/Account/Poems",{
      method:"POST",
         headers: new Headers({
            "X-CSRFToken":document.getElementsByName("csrf_token")[0].value,
            "Request":"delete poem",
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify(send_to_server_poem_delete)
      })

      .then((respone)=>{
         if (respone.status !== 200){
            console.log("request status for is"+respone.status);
            return;
         }
      respone.json().then((data)=>{
         if (data["response"] === "successful"){
            for (let i=0; i<selectobject.length; i++) {
               console.log(selectobject.options[i].id)
               if (selectobject.options[i].id == send_to_server_poem_delete["poem_id"])
                  selectobject.remove(i);
            }
            document.getElementsByName(send_to_server_poem_delete["poem_id"])[0].style.display = "none";
            if(selectobject.length==1){
               window.location.reload();
            }
         }
      });
   });
}
})
}


