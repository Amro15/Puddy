// LINES SHORTCUTS
let lines = document.getElementsByClassName("line");
for (let i = 0; i < lines.length; i++) {
    lines[i].addEventListener("keydown", (event) => {
        if (event.shiftKey && event.key === "Enter") {
            event.preventDefault();
            if (i !== lines.length - 1) {
                lines[i + 1].focus();
            }
        }
        if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            event.preventDefault();
            if (i !== 0) {
                lines[i - 1].focus();
            }
        }
    });
}

// SHORTCUTS
document.addEventListener("keydown", (event) => {
    if (event.altKey && event.key == "n") {
        document.getElementById("toggle_note").click();
    }
    if (event.altKey && event.key == "r") {
        check_rhyme_btn.click();
    }
    if (event.altKey && event.key == "s") {
        check_syllables_btn.click();
    }
    if (event.altKey && event.key == "m") {
        check_meter_btn.click()
    }
})

// quick search for rhymes
let search_btn = document.getElementById("quick_search_rhymes_btn");
let search_query = document.getElementById("quick_search");
let search_results = document.getElementById("search_results");
let search_results_list = document.getElementById("search_results_list");
let loading_search_results = document.getElementById("loading_quick_search");

search_query.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        search_btn.click();
    }
});
search_btn.addEventListener("click", () => {
    loading_search_results.style.display = "block";
    search_results_list.innerHTML = "";
    fetch(`https://api.datamuse.com/words?rel_rhy=${search_query.value}`)
        .then((response) => {
            if (response.status != 200) {
                console.log("Could Not Get Rhymes From Api");
            }
            return response.json();
        })
        .then((data) => {
            loading_search_results.style.display = "none";
            if (data.length == 0) {
                err_msg = document.createElement("p");
                err_msg.innerText = "There Are No Results That Match Your Search";
                err_msg.classList.add("error_msg");
                search_results_list.appendChild(err_msg);
                search_results.style.display = "inline-block";
            }
            else {
                let sorted_results = {}
                for (let i in data) {
                    if (!sorted_results.hasOwnProperty(data[i].numSyllables)) {
                        sorted_results[data[i].numSyllables] = [data[i].word];
                    }
                    else {
                        sorted_results[data[i].numSyllables].push(data[i].word);
                    }
                };
                for (let i in sorted_results) {
                    let list_item = document.createElement("li");
                    let line_break = document.createElement("br");
                    list_item.innerHTML = `<b><u>${i} Syllable(s) rhyme(s):</u></b> `
                    for (let j in sorted_results[i]) {
                        list_item.innerHTML += `${sorted_results[i][j]}, `;
                        if (j == 15) {
                            break;
                        }
                    }
                    search_results_list.appendChild(list_item);
                    search_results_list.appendChild(line_break);
                    search_results.style.display = "inline-block";
                    search_results.scrollIntoView({ behavior: 'smooth' });
                }
            }
        })
})

let advanced_search_btn = document.getElementById("advanced_search");
advanced_search_btn.addEventListener("click", () => {
    window.open(`/Rhymes?query=${search_query.value}&search=Search&filters=rel_rhy`, "_blank");
})

//hide nav btn
let navbar = document.getElementById("nav_div");
toggle_nav.addEventListener("click", () => {
    if (navbar.style.display !== "none") {
        navbar.style.display = "none";
    }
    else {
        navbar.style.display = "block";
    }
})

// toggle notepad
let notepad = document.getElementById("notepad");
toggle_note.addEventListener("click", () => {
    if (notepad.style.display !== "block") {
        notepad.style.display = "block";
    }
    else {
        notepad.style.display = "none"
    }
})


// toggle btn div
let detatch_util = document.getElementById("detatch_util")
let arrow = document.getElementById("arrow");
let arrow_symbol = document.getElementById("arrow_symbol")
let btn_div = document.getElementById("btn_div")

// detatch btn div
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


//Check Rhymes
let loading_rhymes = document.getElementById("loading_rhymes")
let check_rhyme_btn = document.getElementById("check_rhymes");
if (check_rhyme_btn) {
    check_rhyme_btn.addEventListener("click", () => {
        if (check_rhyme_btn.checked) {
            loading_rhymes.style.display = "block";
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
                        loading_rhymes.style.display = "none";
                        console.log("this is the workable with data", data)
                        // check if user is trying to detect rhymes of empty lines
                        let no_data_rhymes = document.getElementById("no_data_rhymes");
                        let obj_len = 0;
                        for (let i in data) {
                            obj_len += data[i].length;
                        }
                        if (obj_len === 0) {
                            no_data_rhymes.style.display = "block";
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
            no_data_rhymes.style.display = "none";
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
let loading_syllables = document.getElementById("loading_syllables");
let check_syllables_btn = document.getElementById("display_syllable_count");
let input = document.getElementsByClassName("line");
let syllables = document.getElementsByClassName("syllables");
let syllables_text = document.getElementsByClassName("syllables_text");
if (check_syllables_btn) {
    check_syllables_btn.addEventListener("click", () => {
        if (check_syllables_btn.checked) {
            loading_syllables.style.display = "block";
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
                        let rs;
                        if ("rs" in data) {
                            rs = data["rs"]
                            delete data["rs"];
                        }
                        loading_syllables.style.display = "none";
                        console.log("this is the workable with data", data)
                        for (let j = 0; j < input.length; j++) {
                            if (data[input.item(j).id]) {
                                for (k in data[input.item(j).id]) {
                                    if (data[input.item(j).id][k] === 0) {
                                        let no_data_syllables = document.getElementById("no_data_syllables");
                                        if (no_data_syllables.style.display !== "block") {
                                            no_data_syllables.style.display = "block";
                                        }
                                    }
                                }
                                let total_rhymes = data[input.item(j).id].reduce((a, b) => a + b, 0);
                                if (syllables[j].style.visibility !== "visible" && syllables[j].style.position !== "relative") {
                                    syllables[j].style.cssText = "display:flex";
                                    syllables_text[j].innerText = data[input.item(j).id].join(" / ").concat(" = " + total_rhymes);
                                    console.log(rs)
                                    if (rs == "Haiku") {
                                        if ((j == 0 || j == 2) && total_rhymes == 5) {
                                            syllables_text[j].style.color = "lime";
                                        }
                                        else if (j == 1 && total_rhymes == 7) {
                                            syllables_text[j].style.color = "lime";
                                        }
                                        else {
                                            syllables_text[j].style.color = "red";
                                        }
                                    }
                                    if (rs == "Shakespearean Sonnet") {
                                        if (total_rhymes == 10) {
                                            syllables[j].style.color = "lime";
                                        }
                                        else {
                                            syllables[j].style.color = "red";
                                        }
                                    }
                                }
                            }
                        }
                    });
                });
        }
        // if btn isin t checked hide all paragrapahs 
        else {
            let no_data_syllables = document.getElementById("no_data_syllables");
            if (no_data_syllables.style.display !== "none") {
                no_data_syllables.style.display = "none";
            }
            // hide all syllable divs
            for (let j = 0; j < syllables.length; j++) {
                syllables[j].style.cssText = "display:none";
                syllables_text[j].innerText = "";
            }
        }
    })
}

// check meter
let loading_meter = document.getElementById("loading_meter");
let check_meter_btn = document.getElementById("check_meter");
let meter_divs = document.getElementsByClassName("meter");
let meter_text = document.getElementsByClassName("meter_text");
let no_data_meter = document.getElementById("no_data_meter");
check_meter_btn.addEventListener("click", () => {
    if (check_meter_btn.checked) {
        loading_meter.style.display = "block";
        let send_to_server_meter = {};
        let input = document.getElementsByClassName("line");
        for (let i = 0; i < input.length; i++) {
            send_to_server_meter[input.item(i).id] = input.item(i).innerText;
        }
        console.log(send_to_server_meter)
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
                    loading_meter.style.display = "none";
                    console.log(data)
                    lines = document.getElementsByClassName("line");
                    for (let i = 0; i < lines.length; i++) {
                        console.log(i)
                        meter_divs[i].style.cssText = "display:flex";
                        meter_text[i].innerHTML = data[lines[i].id].slice(1, -1).replace(/([.|])/g, " $1 ");
                        if (data[lines[i].id] === "[None]") {
                            no_data_meter.innerText = "Please Check Your Spelling"
                        }
                    }
                });
            });
    }
    else {
        for (let i = 0; i < meter_divs.length; i++) {
            meter_text[i].innerHTML = "";
            meter_divs[i].style.cssText = "display:none";
        }
        no_data_meter.innerText = "";
    }

})


