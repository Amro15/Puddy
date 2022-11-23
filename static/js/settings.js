let change_username_btn = document.getElementById("change_username_btn");
let input = document.getElementById("settings_username");
let username_error = document.getElementById("username_error");

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        change_username_btn.click();
    }
});

change_username_btn.addEventListener("click", () => {
    username_error.style.display = "none";
    fetch(window.origin + "/Account/Settings", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request": "change username"
        }),
        cache: "no-cache",
        body: JSON.stringify({ "request": input.value })
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
                if (data["response"] === "successful") {
                    window.location.reload();
                }
                else {
                    username_error.style.display = "block";
                }
            });
        });
})