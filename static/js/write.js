// remind user to save after 20 mins 
let warning_div = document.getElementById("warning");
if (warning_div) {
    let warning = setTimeout(() => {
        warning_div.style.display = "inline-block";
        warning_div.scrollIntoView();
        let close_warning_btn = document.getElementById("warning_close");
        close_warning_btn.addEventListener("click", () => {
            warning_div.style.display = "none";
        })

    }, (20 * 60000))
}

let tip_div = document.getElementById("tip_div");
if (!getCookie("first_visit")) {
    setCookie("first_visit", "false", 365);
    tip_div.style.cssText = "display:flex!important;";
}

// if user wants to save as draft
let save_draft = document.getElementById("save_draft");
let success_msg = document.getElementById("confirmation_msg_write");
let success_msg_div = document.getElementById("msg_container");
let save_draft_modal = document.getElementById("save_draft_modal");
let update_draft_btn = document.getElementById("update_draft");
let error_msg = document.getElementById("err_msg");
let save_error_msg = document.getElementById("save_err_msg");

// try saving user poem as draft to db
const urlParams = new URLSearchParams(window.location.search);
const write_modal = new bootstrap.Modal(document.getElementById('write_modal'), { keyboard: false, backdrop: "static" });
if (save_draft) {
    save_draft.addEventListener("click", () => {
        error_msg.style.display = "none";
        save_error_msg.style.display = "none";
        let input = document.getElementsByClassName("line");
        let is_empty;
        for (let i = 0; i < input.length; i++) {
            if (input[i].innerText !== "") {
                is_empty = false
                break
            }
            else {
                is_empty = true
            }
        }
        if (is_empty) {
            error_msg.style.display = "block";
            error_msg.scrollIntoView();
        }
        else {
            let title = document.getElementById("title").innerText;
            let notepad = document.getElementById("notepad").innerText;
            // if session is draft pass the required parameters
            let send_to_server_draft;
            if (urlParams.has("draft")) {
                let draft_id = urlParams.get("draft");
                let draft_num = urlParams.get("dnum");
                let poem_num = urlParams.get("pnum");
                send_to_server_draft = { "title": title, "notes": notepad, "draft_id": draft_id, "draft_num": draft_num, "poem_num": poem_num };
                console.log(send_to_server_draft)
            }
            else {
                send_to_server_draft = { "title": title, "notes": notepad };
            }
            for (let i = 0; i < input.length; i++) {
                console.log(input.item(i).id)
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
                    if (respone.status !== 200) {
                        console.log("request status for draft is" + respone.status);
                        return;
                    }
                    respone.json().then((data) => {
                        console.log("data we got back is", data);
                        if (data["response"] == "input was altered cannot save") {
                            save_error_msg.style.display = "block";
                            save_error_msg.scrollIntoView();
                        }
                        // if the poem already has a draft ask user what to do 
                        else if (data["response"] === "draft already exists") {
                            write_modal.show()
                        }
                        // if draft saved
                        else if (data["response"] == "successful") {
                            success_msg.innerText = "Draft succesfully saved";
                            success_msg_div.style.cssText = "display:block";
                            if (!urlParams.has("draft_id")) {
                                window.location = `/Write?draft=${data["draft_id"]}&dnum=${data["draft_num"]}&pnum=${data["poem_num"]}`
                            }
                        }
                    });
                });
        }
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
                    if (data["response"] === "successful") {
                        success_msg_div.style.display = "block";
                    }
                    else if (data["response"] === "input was altered cannot save") {
                        save_error_msg.style.display = "block";
                        save_error_msg.scrollIntoView();
                    }
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
                    write_modal.hide()
                    if (data["response"] == "successful") {
                        success_msg_div.style.display = "block";
                        success_msg_div.scrollIntoView();
                    }
                    else if (data["response"] === "input was altered cannot save") {
                        save_error_msg.style.display = "block";
                        save_error_msg.scrollIntoView();
                    }
                });
            });
    })
}


// /if user wants to save  as poem
let save_poem_btn = document.getElementById("save_poem");
if (save_poem_btn) {
    save_poem_btn.addEventListener("click", () => {
        error_msg.style.display = "none";
        save_error_msg.style.display = "none";
        let is_empty;
        for (let i = 0; i < input.length; i++) {
            if (input[i].innerText !== "") {
                is_empty = false
                break
            }
            else {
                is_empty = true
            }
        }
        if (is_empty) {
            error_msg.style.display = "block";
        }
        else {
            let title = document.getElementById("title").innerText;
            let send_to_server_format = { "draft_id": urlParams.get("draft"), "title": title };
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
                    "Request": "save poem"
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
                        if (data["response"] === "input was altered cannot save") {
                            save_error_msg.style.display = "block";
                            save_error_msg.scrollIntoView();
                        }
                        else if (data["response"] === "successful") {
                                window.location = "/Account/Poems";
                        }

                    });
                });
        }
    });
};

// update poem
let update_poem_btn = document.getElementById("update_poem")
if (update_poem_btn) {
    update_poem_btn.addEventListener("click", () => {
        error_msg.style.display = "none";
        let is_empty;
        for (let i = 0; i < input.length; i++) {
            if (input[i].innerText !== "") {
                is_empty = false
                break
            }
            else {
                is_empty = true
            }
        }
        if (is_empty) {
            error_msg.style.display = "block";
        }
        else {
            let title = document.getElementById("title").innerText;
            const urlParams = new URLSearchParams(window.location.search);
            let send_to_server_update_poem = { "title": title, "poem_id": urlParams.get("poem") };
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
                        if (data["response"] == "successful") {
                            success_msg_div.style.display = "block";
                            success_msg_div.scrollIntoView();
                        }
                        else if (data["response"] === "input was altered cannot save") {
                            error_msg.style.display = "block";
                            error_msg.scrollIntoView();
                        }

                    });
                });
        }
    })
}

let toggle_edit_btn = document.getElementById("toggle_edit_btn");

if (toggle_edit_btn) {
    let edit_btn_div = document.getElementById("edit_btn_div");
    let edit_btns_div = document.getElementById("edit_btns_div");
    let edit_mode_errors = document.getElementById("edit_mode_errors");
    let toggle_br_btn = document.getElementById("toggle_br_btn");
    let toggle_undo_btn = document.getElementById("toggle_undo_btn");

    let func_buttons_div = document.getElementById("func_btns");
    let save_btn_div = document.getElementById("save_btn_div");

    let add_btn_container = document.getElementsByClassName("add_btn_container");
    let add_line_btn = document.getElementById("add_line_btn");

    let add_bulk_container = document.getElementsByClassName("add_bulk_container");
    let add_lines_bulk_btn = document.getElementById("add_lines_bulk_btn");
    let add_lines_bulk_input_div = document.getElementById("edit_add_lines_bulk_div");
    let add_br_bulk_btn = document.getElementById("add_brs_bulk_btn");
    let add_br_bulk_btn_div = document.getElementById("edit_add_line_breaks_bulk_div");
    let clear_brs_btn = document.getElementById("clear_brs");

    let poem_body = document.getElementById("poem_body");
    let extra_line = document.getElementById("extra_line");

    let undo_btn_container = document.getElementsByClassName("undo_btn_container");
    let undo_btn = document.getElementsByClassName("undo_btn");

    let delete_btn_container = document.getElementsByClassName("delete_btn_container");
    let delete_line_btn = document.getElementsByClassName("delete_line_btn");

    let br_btn = document.getElementsByClassName("br_btn");
    let br_icon = document.getElementsByClassName("br_icon");
    let br_div = document.getElementsByClassName("br_div");

    let verse = document.getElementsByClassName("verse");
    let line = document.getElementsByClassName("line");
    let rhyme_symbol = document.getElementsByClassName("rhyme_symbols");
    // show all edit elements and hide save btns and check rhyme meter and syllables btns
    toggle_edit_btn.addEventListener("click", () => {
        if (toggle_edit_btn.checked) {
            edit_btns_div.style.display = "block";
            func_buttons_div.style.display = "none";
            save_btn_div.style.display = "none";
            for (let i = 0; i < delete_line_btn.length; i++) {
                delete_btn_container[i].style.display = "inline-block";
                let rhyme_symbol_editable = document.createElement("input");
                // edit fv means the user's rhyme scheme is free verse thus we do not want them to edit the line symbol text since it is autoincremented
                if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                    rhyme_symbol_editable.setAttribute("type", "text");
                    rhyme_symbol[i].setAttribute("contenteditable", "true");
                    rhyme_symbol[i].setAttribute("role", "textbox");
                    rhyme_symbol[i].style.backgroundColor = "rgb(37, 37, 37)";
                }
                if (toggle_br_btn.checked) {
                    br_btn[i].style.display = "inline-block";
                }
            }
            add_btn_container[0].style.display = "inline-block";
            add_bulk_container[0].style.display = "inline-block";
        }
        // hide and unhide respective elements
        else {
            func_buttons_div.style.display = "block";
            edit_btns_div.style.display = "none";
            save_btn_div.style.display = "block";
            for (let i = 0; i < delete_line_btn.length; i++) {
                delete_btn_container[i].style.display = "none";
                undo_btn_container[i].style.display = "none";
                br_btn[i].style.display = "none";
                if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                    rhyme_symbol[i].removeAttribute("contenteditable");
                    rhyme_symbol[i].removeAttribute("role");
                    rhyme_symbol[i].style.backgroundColor = "rgb(105, 113, 132)";
                }
            }
            add_btn_container[0].style.display = "none";
            add_bulk_container[0].style.display = "none";
            add_lines_bulk_input_div.style.display = "none";
            add_br_bulk_btn_div.style.display = "none";
            edit_mode_errors.style.display = "none";
        }
    })
    // show and hide line break buttons
    toggle_br_btn.addEventListener("click", () => {
        for (let i = 0; i < br_btn.length; i++) {
            if (toggle_br_btn.checked && toggle_edit_btn.checked) {
                br_btn[i].style.display = "inline-block";
            }
            else {
                br_btn[i].style.display = "none";
            }
        }
    })
    // show and hide undo btns
    toggle_undo_btn.addEventListener("click", () => {
        for (let i = 0; i < undo_btn.length; i++) {
            if (toggle_edit_btn.checked && toggle_undo_btn.checked) {
                if (undo_btn_container[i].style.display == "inline-block") {
                    undo_btn_container[i].style.display = "none";
                    verse[i].style.display = "none";
                }
            }
            else {
                if (line[i].style.display == "none") {
                    undo_btn_container[i].style.display = "inline-block";
                    verse[i].style.display = "flex";
                }
            }
        }
    })

    for (let i = 0; i < delete_line_btn.length; i++) {
        // hide whole line and surrounding elements and display undo btn instead
        delete_line_btn[i].addEventListener("click", () => {
            if (toggle_edit_btn.checked) {
                delete_btn_container[i].style.display = "none";
                line[i].style.display = "none";
                rhyme_symbol[i].style.cssText = "display:none!important";
                br_btn[i].style.display = "none";
                if (toggle_undo_btn.checked) {
                    undo_btn_container[i].style.display = "none";
                }
                else {
                    undo_btn_container[i].style.display = "inline-block";
                }
            }
        })

        // show hidden elements and hide undo btn
        undo_btn[i].addEventListener("click", () => {
            if (toggle_edit_btn.checked) {
                delete_btn_container[i].style.display = "inline-block";
                line[i].style.display = "block";
                if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                    rhyme_symbol[i].style.cssText = "display:inline-block; background-color:rgb(37, 37, 37)";
                }
                else {
                    rhyme_symbol[i].style.cssText = "display:inline-block;"
                }
                if (toggle_br_btn.checked) {
                    br_btn[i].style.display = "inline-block";
                }
                undo_btn_container[i].style.display = "none";
            }
        })

        // add and remove line breaks aswell as changing buttons respectively
        br_btn[i].addEventListener("click", () => {
            if (toggle_edit_btn.checked) {
                if (br_btn[i].id === "remove_br") {
                    br_btn[i].id = "add_br";
                    br_div[i].innerText = "";
                    if (br_icon[i]) {
                        br_icon[i].setAttribute("src", "/static/icons/add-br.png");
                    }
                }
                else {
                    br_btn[i].id = "remove_br";
                    br_div[i].appendChild(document.createElement("br"));
                    if (br_icon[i]) {
                        br_icon[i].setAttribute("src", "/static/icons/remove-br.png");
                    }
                }
            }
        })
    }



    // to add line we need to assign event listeners to all new buttons which are created along with the line
    // we only need to loop over newly created element so we ignore elements that were already there
    // let initial_len_stored = false
    let initial_len;
    let br_frequency = [];
    let add_line_err = document.getElementById("add_line_err");
    add_line_btn.addEventListener("click", () => {
        if (toggle_edit_btn.checked) {
            add_line_err.style.display = "none";
            if (line.length + 2 > 101) {
                add_line_err.style.display = "block";
            }
            else {
                // look for line break frequency to know when to add a line break when adding lines
                for (let i = 0; i < delete_line_btn.length; i++) {
                    if (br_btn[i].id == "remove_br" && br_frequency.length == 0) {
                        br_frequency.push(i + 1);
                    }
                }
                initial_len = delete_line_btn.length;
                if (edit_btn_div.getAttribute("name") === "edit_fv") {
                    extra_line.content.querySelector(".rhyme_symbols").innerText = line.length + 1;
                    extra_line.content.querySelector(".rhyme_symbols").removeAttribute("contenteditable");
                    extra_line.content.querySelector(".rhyme_symbols").removeAttribute("role");
                }
                else {
                    extra_line.content.querySelector(".rhyme_symbols").innerText = "";
                    extra_line.content.querySelector(".rhyme_symbols").style.cssText = "background-color:rgb(37, 37, 37)";
                }
                poem_body.appendChild(extra_line.content.cloneNode(true));
                if ((delete_line_btn.length) % br_frequency[0] == 0) {
                    document.getElementsByClassName("br_div")[delete_line_btn.length - 1].appendChild(document.createElement("br"));
                    document.getElementsByClassName("br_btn")[delete_line_btn.length - 1].id = "remove_br";
                    document.getElementsByClassName("br_icon")[delete_line_btn.length - 1].setAttribute("src", "static/icons/remove-br.png");
                }
                else {
                    document.getElementsByClassName("br_div")[delete_line_btn.length - 1].innerHtml = "";
                    document.getElementsByClassName("br_btn")[delete_line_btn.length - 1].id = "add_br";
                    document.getElementsByClassName("br_icon")[delete_line_btn.length - 1].setAttribute("src", "static/icons/add-br.png");
                }
                for (let i = initial_len; i < delete_line_btn.length; i++) {
                    if (toggle_br_btn.checked) {
                        br_btn[i].style.display = "inline-block";
                    }
                    else {
                        br_btn[i].style.display = "none";
                    }


                    delete_line_btn[i].addEventListener("click", () => {
                        delete_btn_container[i].style.display = "none";
                        line[i].style.display = "none";
                        rhyme_symbol[i].style.cssText = "display:none!important";
                        br_btn[i].style.display = "none";
                        if (toggle_undo_btn.checked) {
                            undo_btn_container[i].style.display = "none";
                        }
                        else {
                            undo_btn_container[i].style.display = "inline-block";
                        }
                    })
                    undo_btn[i].addEventListener("click", () => {
                        delete_btn_container[i].style.display = "inline-block";
                        line[i].style.display = "block";
                        if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                            rhyme_symbol[i].style.cssText = "display:inline-block; background-color:rgb(37, 37, 37)";
                        }
                        else {
                            rhyme_symbol[i].style.cssText = "display:inline-block;"
                        }
                        if (toggle_br_btn.checked) {
                            br_btn[i].style.display = "inline-block";
                        }
                        undo_btn_container[i].style.display = "none";
                    })
                    br_btn[i].addEventListener("click", () => {
                        if (br_btn[i].id === "remove_br") {
                            br_btn[i].id = "add_br";
                            br_div[i].innerText = "";
                            br_icon[i].setAttribute("src", "/static/icons/add-br.png");
                        }
                        else {
                            br_btn[i].id = "remove_br";
                            br_div[i].appendChild(document.createElement("br"));
                            br_icon[i].setAttribute("src", "/static/icons/remove-br.png");
                        }
                    })
                }
            }
        }
    })


    let add_lines_input = document.getElementById("add_lines_input");
    let add_lines_bulk_len_error = document.getElementById("add_lines_bulk_length_error");
    let add_lines_bulk_error = document.getElementById("add_lines_bulk_error");
    add_lines_input.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            add_lines_bulk_btn.click();
        }
    })
    add_lines_bulk_btn.addEventListener("click", () => {
        if (toggle_edit_btn.checked) {
            let lines_to_add = add_lines_input.value.replace(/\s/g, '');
            add_lines_bulk_error.style.display = "none";
            add_lines_bulk_len_error.style.display = "none";
            let pattern;
            if (edit_btn_div.getAttribute("name") == "edit_fv") {
                pattern = /^[0-9]{0,3}$/g
            }
            else {
                pattern = /^[a-zA-Z\-]{1,100}$/;
            }
            if ((pattern.test(lines_to_add)) === false) {
                add_lines_bulk_error.style.display = "block";
            }
            else {
                initial_len = delete_line_btn.length;
                add_lines_input.value = "";
                for (let i = 0; i < delete_line_btn.length; i++) {
                    if (br_btn[i].id == "remove_br" && br_frequency.length == 0) {
                        br_frequency.push(i + 1);
                    }
                }
                // same as add lines but in a loop 
                let iterable;
                if (edit_btn_div.getAttribute("name") == "edit_fv") {
                    if ((parseInt(lines_to_add) + line.length + 1) > 101) {
                        add_lines_bulk_len_error.style.display = "block";
                    }
                    else {
                        iterable = lines_to_add;
                    }
                }
                else {
                    lines_arr = lines_to_add.split("");
                    if ((lines_arr.length + line.length + 1) > 101) {
                        add_lines_bulk_len_error.style.display = "block";
                    }
                    else {
                        console.log("lines_Arr", lines_arr)
                        iterable = lines_arr.length;
                    }
                }
                for (let j = 0; j < iterable; j++) {
                    console.log(j)
                    if (edit_btn_div.getAttribute("name") == "edit_fv") {
                        extra_line.content.querySelector(".rhyme_symbols").innerText = line.length + 1;
                        extra_line.content.querySelector(".rhyme_symbols").removeAttribute("contenteditable");
                        extra_line.content.querySelector(".rhyme_symbols").removeAttribute("role");
                    }
                    else {
                        extra_line.content.querySelector(".rhyme_symbols").innerText = lines_arr[j].toUpperCase();
                        extra_line.content.querySelector(".rhyme_symbols").style.cssText = "background-color:rgb(37, 37, 37)";
                    }
                    poem_body.appendChild(extra_line.content.cloneNode(true));
                    if ((delete_line_btn.length) % br_frequency[0] == 0) {
                        document.getElementsByClassName("br_div")[delete_line_btn.length - 1].appendChild(document.createElement("br"));
                        document.getElementsByClassName("br_btn")[delete_line_btn.length - 1].id = "remove_br";
                        document.getElementsByClassName("br_icon")[delete_line_btn.length - 1].setAttribute("src", "static/icons/remove-br.png");
                    }
                    else {
                        document.getElementsByClassName("br_div")[delete_line_btn.length - 1].innerHtml = "";
                        document.getElementsByClassName("br_btn")[delete_line_btn.length - 1].id = "add_br";
                        document.getElementsByClassName("br_icon")[delete_line_btn.length - 1].setAttribute("src", "static/icons/add-br.png");
                    }
                }
            }
            for (let i = initial_len; i < delete_line_btn.length; i++) {
                if (toggle_br_btn.checked) {
                    br_btn[i].style.display = "inline-block";
                }
                else {
                    br_btn[i].style.display = "none";
                }

                delete_line_btn[i].addEventListener("click", () => {
                    console.log("delete inside add")
                    delete_btn_container[i].style.display = "none";
                    line[i].style.display = "none";
                    rhyme_symbol[i].style.cssText = "display:none!important";
                    br_btn[i].style.display = "none";
                    if (toggle_undo_btn.checked) {
                        undo_btn_container[i].style.display = "none";
                    }
                    else {
                        undo_btn_container[i].style.display = "inline-block";
                    }
                })
                undo_btn[i].addEventListener("click", () => {
                    delete_btn_container[i].style.display = "inline-block";
                    line[i].style.display = "block";
                    if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                        rhyme_symbol[i].style.cssText = "display:inline-block; background-color:rgb(37, 37, 37)";
                    }
                    else {
                        rhyme_symbol[i].style.cssText = "display:inline-block;"
                    }
                    if (toggle_br_btn.checked) {
                        br_btn[i].style.display = "inline-block";
                    }
                    undo_btn_container[i].style.display = "none";
                })
                br_btn[i].addEventListener("click", () => {
                    if (br_btn[i].id === "remove_br") {
                        br_btn[i].id = "add_br";
                        br_div[i].innerText = "";
                        br_icon[i].setAttribute("src", "/static/icons/add-br.png");
                    }
                    else {
                        br_btn[i].id = "remove_br";
                        br_div[i].appendChild(document.createElement("br"));
                        br_icon[i].setAttribute("src", "/static/icons/remove-br.png");
                    }
                })
            }
        }
    })

    let add_brs_input = document.getElementById("add_brs_input");
    let add_brs_bulk_error = document.getElementById("add_brs_bulk_error");
    add_brs_input.addEventListener("keydown", (event) => {
        if (event.key == "Enter") {
            add_br_bulk_btn.click();
        }
    })
    add_br_bulk_btn.addEventListener("click", () => {
        if (Number.isNaN(add_brs_input.value) || add_brs_input.value % 1 != 0) {
            add_brs_bulk_error.style.display = "block";
        }
        else {
            // clear line break and change the frequency by clearing it so it s calculated again next time
            br_frequency = [];
            add_brs_bulk_error.style.display = "none";
            for (let i = 0; i < br_btn.length; i++) {
                br_btn[i].id = "add_br";
                br_icon[i].setAttribute("src", "/static/icons/add-br.png");
                br_div[i].innerText = "";
                if ((i !== 0) && (((i + 1) % parseInt(add_brs_input.value)) == 0)) {
                    br_btn[i].id = "remove_br";
                    br_div[i].appendChild(document.createElement("br"));
                    br_icon[i].setAttribute("src", "/static/icons/remove-br.png");
                }
            }
        }
    })

    clear_brs_btn.addEventListener("click", () => {
        for (let i = 0; i < br_btn.length; i++) {
            br_btn[i].id = "add_br";
            br_icon[i].setAttribute("src", "/static/icons/add-br.png");
            br_div[i].innerText = "";
        }
    })

    let undo_edits = document.getElementById("undo_edits");
    let save_edits = document.getElementById("save_edits");
    let send_to_server_edits = {};
    undo_edits.addEventListener("click", () => {
        let temp = {};
        if (toggle_edit_btn.checked) {
            edit_mode_errors.style.display = "none";
            send_to_server_edits = { "title": document.getElementById("title").innerText, "line_breaks": [], "notes":document.getElementById("notepad").innerText };
            for (let i = 0; i < line.length; i++) {
                if (edit_btn_div.getAttribute("name") === "edit_fv") {
                    send_to_server_edits[i] = line[i].innerText;
                }
                else {
                    if (temp.hasOwnProperty(rhyme_symbol[i].innerText)) {
                        temp[rhyme_symbol[i].innerText] += 1;
                        send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = line[i].innerText;
                    }
                    else {
                        temp[rhyme_symbol[i].innerText] = 0;
                        send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = line[i].innerText;
                    }
                }
                if (br_btn[i].id == "remove_br") {
                    send_to_server_edits["line_breaks"].push(i);
                }
            }
            fetch(window.origin + "/Write", {
                method: "POST",
                headers: new Headers({
                    "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                    "Content-Type": "application/json",
                    "Request": "undo edits"
                }),
                cache: "no-cache",
                body: JSON.stringify(send_to_server_edits)
            })
                // this is executed right after the fetch request
                .then((respone) => {
                    // if request fails
                    if (respone.status !== 200) {
                        console.log("request status for is" + respone.status);
                        return;
                    }
                    // if request succeeds 
                    respone.json().then((data) => {
                        if (data["response"] == "bad input") {
                            edit_mode_errors.style.display = "block";
                        }
                        else if (data["response"] == "success") {
                            window.location = "/Write?resume=resume";
                        }
                    });
                });
        }
    })
    save_edits.addEventListener("click", () => {
        let temp = {}
        if (toggle_edit_btn.checked) {
            edit_mode_errors.style.display = "none";
            send_to_server_edits = { "title": document.getElementById("title").innerText, "line_breaks": [], "notes":document.getElementById("notepad").innerText };
            for (let i = 0; i < line.length; i++) {
                if (edit_btn_div.getAttribute("name") !== "edit_fv") {
                    if (line[i].style.display === "none") {
                        if (temp.hasOwnProperty(rhyme_symbol[i].innerText)) {
                            temp[rhyme_symbol[i].innerText] += 1;
                            send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = false;
                        }
                        else {
                            temp[rhyme_symbol[i].innerText] = 0;
                            send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = false;
                        }
                    }
                    else {
                        if (temp.hasOwnProperty(rhyme_symbol[i].innerText)) {
                            temp[rhyme_symbol[i].innerText] += 1;
                            send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = line[i].innerText;
                        }
                        else {
                            temp[rhyme_symbol[i].innerText] = 0;
                            send_to_server_edits[rhyme_symbol[i].innerText.concat(temp[rhyme_symbol[i].innerText])] = line[i].innerText;
                        }
                    }
                }
                else {
                    if (line[i].style.display === "none") {
                        send_to_server_edits[i] = false;
                    }
                    else {
                        send_to_server_edits[i] = line[i].innerText;
                    }
                }
                if (br_btn[i].id == "remove_br") {
                    send_to_server_edits["line_breaks"].push(i);
                }
            }
            send_to_server_edits["line_breaks"] = send_to_server_edits["line_breaks"].join(",").toString();
            console.log(send_to_server_edits);
            fetch(window.origin + "/Write", {
                method: "POST",
                headers: new Headers({
                    "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
                    "Content-Type": "application/json",
                    "Request": "save edits"
                }),
                cache: "no-cache",
                body: JSON.stringify(send_to_server_edits)
            })
                // this is executed right after the fetch request
                .then((respone) => {
                    // if request fails
                    if (respone.status !== 200) {
                        console.log("request status for save edits is " + respone.status);
                        return;
                    }
                    // if request succeeds 
                    respone.json().then((data) => {
                        if (data["response"] === "bad input") {
                            edit_mode_errors.style.display = "block";
                        }
                        else if (data["response"] === "successful") {
                            window.location = "/Write?resume=resume"
                        }
                    });
                });

        }
    })

}

