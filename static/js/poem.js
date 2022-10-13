let show_poem = document.getElementsByClassName("show_poem");
let poem_div = document.getElementsByClassName("poem_container");
let arrow_btn = document.getElementsByClassName("arrow_icon");
let ctr = 0;
for(let i =0; i<show_poem.length; i++){
   show_poem[i].addEventListener("click", ()=>{
      if(ctr==0){
         console.log("poem_div", poem_div[i])
         poem_div[i].style.display = "block";
         arrow_btn[i].setAttribute("src", "/static/icons/up-arrow.png");
      }
      else{
         if(poem_div[i].style.display=="block"){
            poem_div[i].style.display="none";
            arrow_btn[i].setAttribute("src", "/static/icons/down-arrow.png");
         }
         else{
            poem_div[i].style.display="block";
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

let copy_btn = document.getElementById("copy");
copy_btn.addEventListener("click", ()=>{
   let poem = document.createElement("div");
   poem.innerHTML = document.getElementById("poem_title").innerText;
   let poem_lines = document.getElementsByClassName("poem_lines");
   for(let i =0; i<poem_lines.length; i++){
      poem.innerHTML+=poem_lines[i].innerText;
   }
   document.body.appendChild(poem);
   poem.select();
   poem.setSelectionRange(0, 99999); 
   navigator.clipboard.writeText(poem.innerHTML);
   document.body.removeChild(poem);
})


