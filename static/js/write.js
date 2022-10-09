//hide nav btn
let navbar = document.getElementById("nav_div");
toggle_nav.addEventListener("click", () => {
    if ((navbar.style.visibility !== "hidden") && (navbar.style.position !== "absolute")) {
        navbar.style.cssText = "visibility :hidden; position: absolute";
    }
    else {
        navbar.style.cssText = "visibility :visible; position: relative";
    }
})

// toggle notepad
let notepad = document.getElementById("notepad");
toggle_note.addEventListener("click", () => {
    if ((notepad.style.visibility !== "visible") && (notepad.style.position !== "relative")) {
        notepad.style.cssText = "visibility: visible; position:relative";
    }
    else {
        notepad.style.cssText = "visibility: hidden; position:absolute"
    }
})


// toggle btn div
let detatch_util = document.getElementById("detatch_util")
let arrow = document.getElementById("arrow");
let arrow_symbol = document.getElementById("arrow_symbol")
let btn_div = document.getElementById("btn_div")

// pin btn div
detatch_util.addEventListener("click", () => {
    if (!detatch_util.checked) {
        btn_div.style.cssText = "position: relative;"
        arrow.style.cssText = "position: relative;"
    }
    else {
        btn_div.style.cssText = "position: fixed; right:0px"
        arrow.style.cssText = "position: fixed; right:245px"
    }
})

// hide and show div with arrow
arrow.addEventListener("click", () => {
    if (btn_div.style.visibility !== "hidden" && btn_div.style.position !== "absoliute") {
        btn_div.style.cssText = "position: absolute; visibility:hidden";
        arrow_symbol.classList.remove("right");
        arrow_symbol.classList.add("left");
        if (!detatch_util.checked) {
            arrow.style.cssText = "position:relative;"
        }
        else {
            arrow.style.cssText = "position:fixed; right:0px"
        }
    }
    else {
        arrow_symbol.classList.remove("left");
        arrow_symbol.classList.add("right");
        if (!detatch_util.checked) {
            btn_div.style.cssText = "position: relative; visibility:visible"
            arrow.style.cssText = "position: relative; right:0px"
        }
        else {
            btn_div.style.cssText = "position: fixed; visibility:visible"
            arrow.style.cssText = "position: fixed; right:245px"
        }
    }
})

// extra rhyme info
let rhyme_info_btn = document.getElementById("rhyme_check_info");
let rhyme_info_div = document.getElementById("rhyme_info_div");
let ctr=0
if (rhyme_info_btn){
rhyme_info_btn.addEventListener("click", ()=>{
        rhyme_info_div.style.cssText="visibility:visible; position:relative";
})
let hide_rhyme_info = document.getElementById("hide_rhyme_info");
if(hide_rhyme_info){
    hide_rhyme_info.addEventListener("click", ()=>{
        console.log("click")
    rhyme_info_div.style.cssText="visibility:hidden; position:absolute";
    })
}
}

//Check Rhymes
let check_rhyme_btn = document.getElementById("check_rhymes");
if (check_rhyme_btn){
check_rhyme_btn.addEventListener("click", () => {
    if (check_rhyme_btn.checked) {
        let send_to_server_rhymes = {};
        let input = document.getElementsByClassName("line");
        console.log(input.length)
        for (let i = 0; i < input.length; i++) {
            console.log(input.item(i).innerText);
            console.log(i);
            if (send_to_server_rhymes.hasOwnProperty(input.item(i).getAttribute("name"))) {
                send_to_server_rhymes[input.item(i).getAttribute("name")].push(input.item(i).innerText);
            }
            else {
                send_to_server_rhymes[input.item(i).getAttribute("name")] = [input.item(i).innerText];
            }
        }
        console.log(send_to_server_rhymes)

        //send data to server if btn is checked

        fetch(window.origin + "/Write", {
            method: "POST",
            headers: new Headers({
                "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                "Content-Type": "application/json",
                "Request": "get rhyme"
            }),
            cache: "no-cache",
            body: JSON.stringify(send_to_server_rhymes)
        })
            .then((respone) => {
                if (respone.status !== 200) {
                    console.log("request status for rhyme is " + respone.status, respone.statusText, "response.json " + respone.json());
                    return;
                }
                respone.json().then((data) => {

                    console.log("this is the workable with data", data)
                    // check if user is trying to detect rhymes of empty lines
                    let no_data_rhymes = document.getElementById("no_data_rhymes");
                    let obj_len = 0;
                    for (let i in data) {
                        obj_len += data[i].length;
                    }
                    if (obj_len === 0) {
                        no_data_rhymes.innerHTML = "There must at least two words of the same rhyme in your poem!";
                    }
                    // change element color corresponding to the returned object's key
                    if (data["red"]) {
                        for (let i in data["red"]) {
                            console.log("data is red")
                            let rhyme_symbol = document.getElementById("symbol" + data["red"][i]);
                            if (check_rhyme_btn.checked) {
                                rhyme_symbol.style.backgroundColor = "red";
                            }
                        };
                    };
                    if (data["green"]) {
                        for (let i in data["green"]) {
                            console.log("data is green")
                            console.log("symbol" + data["green"][i])
                            let rhyme_symbol = document.getElementById("symbol" + data["green"][i]);
                            console.log(rhyme_symbol)
                            rhyme_symbol.style.backgroundColor = "green";
                        };
                    };
                    if (data["yellow"]) {
                        for (let i in data["yellow"]) {
                            console.log("data is yellow")
                            let rhyme_symbol = document.getElementById("symbol" + data["yellow"][i]);
                            rhyme_symbol.style.backgroundColor = "yellow";
                        };
                    };
                    if (data["blue"]) {
                        for (let i in data["blue"]) {
                            console.log("data is blue")
                            let rhyme_symbol = document.getElementById("symbol" + data["blue"][i]);
                            rhyme_symbol.style.backgroundColor = "blue";
                        };
                    };
                });
            });
    }
    //if btn is not checked all background colors go back to normal 
    else {
        // remove error msg
        no_data_rhymes.innerHTML = "";
        // rever all elements to their original color
        let input = document.getElementsByClassName("line");
        for (let i = 0; i < input.length; i++) {
            let symbol_id = "symbol" + input.item(i).id;
            document.getElementById(symbol_id).style.backgroundColor = "rgb(105, 113, 132)";
        }
    }
});
}

// Check syllables

let check_syllables_btn = document.getElementById("display_syllable_count");
let input = document.getElementsByClassName("line");
let syllables = document.getElementsByClassName("syllables");
let syllables_text = document.getElementsByClassName("syllables_text");
check_syllables_btn.addEventListener("click", () => {
    if (check_syllables_btn.checked) {
        let send_to_server_syllables = {};
        let input = document.getElementsByClassName("line");
        for (let i = 0; i < input.length; i++) {
            send_to_server_syllables[input.item(i).id] = input.item(i).innerText;
        }
        console.log(send_to_server_syllables);
        fetch(window.origin + "/Write", {
            method: "POST",
            headers: new Headers({
                "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                "Content-Type": "application/json",
                "Request": "get syllables"
            }),
            cache: "no-cache",
            body: JSON.stringify(send_to_server_syllables)
        })

            .then((respone) => {
                if (respone.status !== 200) {
                    console.log("request status for syllables is" + respone.status);
                    return;
                }
                respone.json().then((data) => {
                    console.log("this is the workable with data", data)
                    for (let j = 0; j < input.length; j++) {
                        console.log(syllables[j])
                        if (data[input.item(j).id]) {
                            for (k in data[input.item(j).id]) {
                                if (data[input.item(j).id][k] === 0) {
                                    console.log("entry", data[input.item(j).id][k])
                                    let no_data_syllables = document.getElementById("no_data_syllables");
                                    if (no_data_syllables.style.position !== "relative" && no_data_syllables.style.visibility !== "visible") {
                                        no_data_syllables.style.cssText = "position: relative; visibility: visible";
                                    }
                                }
                            }
                            let total_rhymes = data[input.item(j).id].reduce((a, b) => a + b, 0);
                            console.log(syllables[j])
                            if (syllables[j].style.visibility !== "visible" && syllables[j].style.position !== "relative") {
                                syllables[j].style.cssText = "display:flex";
                                syllables_text[j].innerText = data[input.item(j).id].join(" / ").concat(" = " + total_rhymes);
                            }
                        }
                    }
                });
            });
    }
    // if btn isin t checked hide all paragrapahs 
    else {
        let no_data_syllables = document.getElementById("no_data_syllables");
        if (no_data_syllables.style.position !== "hidden" && no_data_syllables.style.visibility !== "absolute") {
            no_data_syllables.style.cssText = "visibility: hidden; position: absolute";
        }
        // hide all syllable divs
        for (let j = 0; j < syllables.length; j++) {
            syllables[j].style.cssText = "display:none";
            syllables_text[j].innerText="";
        }
    }
})


// check meter
let check_meter_btn = document.getElementById("check_meter");
let meter_divs = document.getElementsByClassName("meter");
let meter_text = document.getElementsByClassName("meter_text");
let no_data_meter = document.getElementById("no_data_meter");
check_meter_btn.addEventListener("click", () => {
    if(check_meter_btn.checked){
    let send_to_server_meter = {};
    let input = document.getElementsByClassName("line");
    for (let i = 0; i < input.length; i++) {
        send_to_server_meter[input.item(i).id] = input.item(i).innerText;
    }
    fetch(window.origin + "/Write", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request": "check meter"
        }),
        cache: "no-cache",
        body: JSON.stringify(send_to_server_meter)
    })
        .then((respone) => {
            if (respone.status !== 200) {
                console.log("request status for is" + respone.status);
                return;
            }
            respone.json().then((data) => {
                console.log(data)
                let lines = document.getElementsByClassName("line");
                for(let i =0; i<lines.length; i++){
                    console.log(i)
                    meter_divs[i].style.cssText="display:flex";
                    meter_text[i].innerHTML= data[lines[i].id].slice(1, -1).replace(/([.|])/g, " $1 ");
                    if(data[lines[i].id]==="[None]"){
                        no_data_meter.innerText="Please Check Your Spelling"
                    }
                }
             });
        });
    }
    else{
                for(let i =0; i<meter_divs.length; i++){
                    meter_text[i].innerHTML= "";
                    meter_divs[i].style.cssText="display:none";
                }
                no_data_meter.innerText="";
    }


})


let save_draft = document.getElementById("save_draft");
let success_msg = document.getElementById("confirmation_msg_write");
let success_msg_div = document.getElementById("msg_container");
let close_success_msg = document.getElementById("hide");
let save_draft_modal = document.getElementById("save_draft_modal");
let update_draft_btn = document.getElementById("update_draft");

// try saving user poem as draft to db
const write_modal = new bootstrap.Modal(document.getElementById('write_modal'), { keyboard: false, backdrop: "static" });
if(save_draft){
save_draft.addEventListener("click", () => {
    console.log("click")
    let title = document.getElementById("title").innerText;
    let notepad = document.getElementById("notepad").innerText;
    let send_to_server_draft = { "title": title, "notes": notepad };
    let input = document.getElementsByClassName("line");
    for (let i = 0; i < input.length; i++) {
        send_to_server_draft[input.item(i).id] = input.item(i).innerText;
    }
    console.log(send_to_server_draft);
    fetch(window.origin + "/Write", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request": "save draft"
        }),
        cache: "no-cache",
        body: JSON.stringify(send_to_server_draft)
    })
        .then((respone) => {
            // if request fails
            if (respone.status !== 200) {
                console.log("request status for draft is" + respone.status);
                return;
            }
            // if request succeeds 
            respone.json().then((data) => {
                console.log("data we got back is", data);
                // if the poem already has a draft ask user what to do 
                if (data["response"] === "draft already exists") {
                    write_modal.show()
                }
                // else save and notify the user
                else {
                    success_msg.innerText = "Draft succesfully saved";
                    success_msg_div.style.cssText = "display:block";

                }
            });
        });
});
}
if (save_draft_modal) {
    // if user chooses to save from the modal
    save_draft_modal.addEventListener("click", () => {
        console.log("user wants to save");
        fetch(window.origin + "/Write", {
            method: "POST",
            headers: new Headers({
                "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                "Content-Type": "application/json",
                "Request": "save another draft"
            }),
            cache: "no-cache",
            body: JSON.stringify({ "request": "save another draft" })
        })
            .then((respone) => {
                console.log("saved another draft");
                if (respone.status !== 200) {
                    console.log("request status for draft is" + respone.status);
                    return;
                }
                respone.json().then((data) => {
                    write_modal.hide()
                    success_msg_div.style.cssText = "display:block";
                    success_msg.innerHTML = "Draft succesfully saved";

                });
            });
    })
}
if (update_draft_btn) {
    // if user wants to update existing draft
    update_draft_btn.addEventListener("click", () => {
        console.log("user wants to update");
        // tell the server
        fetch(window.origin + "/Write", {
            method: "POST",
            headers: new Headers({
                "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                "Content-Type": "application/json",
                "Request": "update draft"
            }),
            cache: "no-cache",
            body: JSON.stringify({ "request": "update draft" })
        })
            .then((respone) => {
                if (respone.status !== 200) {
                    console.log("request status for draft is" + respone.status);
                    return;
                }
                respone.json().then((data) => {
                    console.log("updated")
                    write_modal.hide()
                    success_msg_div.style.cssText = "display:block";
                    success_msg.innerText = "Draft successfully updated";

                });
            });
    })
}

close_success_msg.addEventListener("click", () => {
    success_msg_div.style.cssText = "visibility: hidden, position:absolute";
    success_msg.innerHTML = "";
})


// /if user wants to save poem
let save_poem_btn = document.getElementById("save_poem");
if (save_poem_btn){
save_poem_btn.addEventListener("click", () => {
    let title = document.getElementById("title").innerText;
    let send_to_server_format = { "title": title };
    let input = document.getElementsByClassName("line");
    for (let i = 0; i < input.length; i++) {
        send_to_server_format[input.item(i).id] = input.item(i).innerText;
    }
    console.log(send_to_server_format);
    fetch(window.origin + "/Write", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request": "format"
        }),
        cache: "no-cache",
        body: JSON.stringify(send_to_server_format)
    })
        .then((respone) => {
            if (respone.status !== 200) {
                console.log("request status for draft is" + respone.status);
                return;
            }
            respone.json().then((data) => {
                console.log("data we got back is", data);
                location.replace(window.origin + "/Format");

            });
        });
});
};

// update poem
let update_poem_btn = document.getElementById("update_poem")
if (update_poem_btn){
    update_poem_btn.addEventListener("click", ()=>{
        let title = document.getElementById("title").innerText;
        const urlParams = new URLSearchParams(window.location.search);
        let send_to_server_update_poem = {"title": title, "poem_id": urlParams.get("poem") };
        let input = document.getElementsByClassName("line");
        for (let i = 0; i < input.length; i++) {
            send_to_server_update_poem[input.item(i).id] = input.item(i).innerText;
        }
        console.log(send_to_server_update_poem);
        fetch(window.origin + "/Write", {
            method: "POST",
            headers: new Headers({
                "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                "Content-Type": "application/json",
                "Request": "update poem"
            }),
            cache: "no-cache",
            body: JSON.stringify(send_to_server_update_poem)
        })
            .then((respone) => {
                if (respone.status !== 200) {
                    console.log("request status for draft is" + respone.status);
                    return;
                }
                respone.json().then((data) => {
                    console.log("data we got back is", data);
                    success_msg_div.style.cssText = "display:block";
                    success_msg.innerHTML="Poem Successfuly Updated";
    
                });
            });
    })
}


window.addEventListener("beforeunload", (e) => {
    e.preventDefault();
    return e.returnValue = "";
});

