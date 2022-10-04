let show_poem = document.getElementsByClassName("show_poem");
   for(let i=0; i<show_poem.length; i++){
         show_poem.item(i).addEventListener("click",()=>{
            let poem= document.getElementById("container"+show_poem.item(i).id);
            let flex_container = document.getElementById(show_poem.item(i).id);
         if (poem.style.visibility!=="visible" && poem.style.position!=="relative"){
            poem.style.cssText = "position: relative; visibility:visible;";
            show_poem.item(i).innerText = "Hide"
            flex_container.style.height = `${poem.offsetHeight+335}px`;
         }
         else {
            poem.style.cssText = "position: absolute; visibility:hidden;";
            show_poem.item(i).innerText = "Show"
            flex_container.style.height = "335px";
         }
      })
      }

let delete_poem = document.getElementsByClassName("delete_poem")
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
      fetch(window.origin+"/Account/Poem",{
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
                  if (selectobject.options[i].value == `#${data["poem_title"]}/${data["poem_num"]}`)
                     selectobject.remove(i);
               }
               document.getElementById(data["poem_title"]+"/"+data["poem_num"]).style.cssText = "position: absolute; visibility: hidden";
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
   fetch(window.origin+"/Account/Poem",{
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
               if (selectobject.options[i].value == `#${data["poem_title"]}/${data["poem_num"]}`)
                  selectobject.remove(i);
            }
            document.getElementById(data["poem_title"]+"/"+data["poem_num"]).style.cssText = "position: absolute; visibility: hidden";
            if(selectobject.length==1){
               window.location.reload();
            }
         }
      });
   });
}
})
}


