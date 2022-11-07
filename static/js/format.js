
let save = document.getElementById("save_poem");

save.addEventListener("click", () => {
    let send_to_server_poem = {};
    let lines = document.getElementsByClassName("edit_line");
    for (let i = 0; i < lines.length; i++) {
        send_to_server_poem[lines.item(i).id] = lines.item(i).innerText;
    }
    fetch(window.origin + "/Format", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request": "save poem"
        }),
        cache: "no-cache",
        body: JSON.stringify(send_to_server_poem)
    })
        .then((respone) => {
            if (respone.status !== 200) {
                console.log("request status for poems is" + respone.status);
                return;
            }
            respone.json().then((data) => {
                window.location="/Account/Poems";
            });
        });

})


