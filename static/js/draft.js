let draft_delete = document.getElementsByClassName("delete");

for (let i = 0; i < draft_delete.length; i++) {
    let selectobject = document.getElementById("draft_select")
    draft_delete[i].addEventListener("click", () => {
        send_to_server_draft_delete = {};
        send_to_server_draft_delete["draft_delete"] = draft_delete.item(i).getAttribute("name");
        console.log(send_to_server_draft_delete)
        poem_draft_num = draft_delete.item(i).getAttribute("name");
        console.log(poem_draft_num)
        // determine if to show modal or not
        const draft_modal = new bootstrap.Modal(document.getElementById('draft_modal'), { keyboard: false, backdrop: "static" });
        if (!getCookie("hide_draft_modal")) {
            console.log(document.cookie)
            draft_modal.show();
            let delete_btn = document.getElementById("delete_btn");
            let stop_showing_modal = document.getElementById("dont_show_draft_modal")
            delete_btn.addEventListener("click", () => {
                if (stop_showing_modal.checked) {
                    setCookie("hide_draft_modal", true, 365)
                }
                draft_modal.hide();
                fetch(window.origin + "/Account/Draft", {
                    method: "POST",
                    headers: new Headers({
                        "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                        "Content-Type": "application/json"
                    }),
                    cache: "no-cache",
                    body: JSON.stringify(send_to_server_draft_delete)
                })

                    .then((respone) => {
                        // if request fails
                        if (respone.status !== 200) {
                            console.log("request status for delete draft is" + respone.status);
                            return;
                        }
                        // if request succeeds 
                        respone.json().then((data) => {
                            for (let j = 0; j < selectobject.length; j++) {
                                if (selectobject.options[j].value == `#${data["draft_title"]}/${data["poem_num"]}/${data["draft_num"]}`)
                                    selectobject.remove(j);
                            }
                            document.getElementsByName(draft_delete.item(i).getAttribute("name"))[0].style.visibility = "hidden";
                            document.getElementsByName(draft_delete.item(i).getAttribute("name"))[0].style.position = "absolute";
                            if (selectobject.length == 1) {
                                window.location.reload();
                            }
                        });
                    });
            })
        }
        else {
            fetch(window.origin + "/Account/Draft", {
                method: "POST",
                headers: new Headers({
                    "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                    "Content-Type": "application/json"
                }),
                cache: "no-cache",
                body: JSON.stringify(send_to_server_draft_delete)
            })

                .then((respone) => {
                    // if request fails
                    if (respone.status !== 200) {
                        console.log("request status for delete draft is" + respone.status);
                        return;
                    }
                    // if request succeeds 
                    respone.json().then((data) => {
                        for (let j = 0; j < selectobject.length; j++) {
                            if (selectobject.options[j].value == `#${data["draft_title"]}/${data["poem_num"]}/${data["draft_num"]}`)
                                selectobject.remove(j);
                        }
                        document.getElementsByName(draft_delete.item(i).getAttribute("name"))[0].style.visibility = "hidden";
                        document.getElementsByName(draft_delete.item(i).getAttribute("name"))[0].style.position = "absolute";
                        if (selectobject.length == 1) {
                            window.location.reload();
                        }
                    });
                });
        }
    })
}

// display draft
let show_draft = document.getElementsByClassName("show_draft");
let poem_div = document.getElementsByClassName("poem_container");
let arrow_btn = document.getElementsByClassName("arrow_icon");
let ctr = 0;
for(let i =0; i<show_draft.length; i++){
   show_draft[i].addEventListener("click", ()=>{
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
