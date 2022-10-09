// turn text field to number field when option is selected
let select_filter = document.getElementsByName("filters")[0];
let poem_query = document.getElementById("poem_search");
select_filter.addEventListener("change", (event)=>{
    if(event.target.value==="linecount"){
        poem_query.setAttribute("type","number")
    }
    else{
        poem_query.setAttribute("type","text")
    }
})

// toggle advanced rhyme div

let advanced_filters_btn = document.getElementById("advanced_filters_btn");
let advanced_filters_div = document.getElementById("advanced_filters");
advanced_filters_btn.addEventListener("click", ()=>{
    if(advanced_filters_div.style.display!=="block"){
        advanced_filters_div.style.display="block";
    }
    else{
        advanced_filters_div.style.display="none";
    }
})

// advanced rhyme divs toggle

let length_radio = document.getElementById("length_radio");
let lenght_div = document.getElementById("length");
let length_range_radio = document.getElementById("length_range_radio");
let length_range = document.getElementById("length_range");
length_radio.addEventListener("click", ()=>{
        lenght_div.style.display="flex";
        length_range.style.display = "none";
})

length_range_radio.addEventListener("click", ()=>{
    length_range.style.display = "flex";
    lenght_div.style.display="none";
})

// random query

let random_poem_btn = document.getElementById("poem_rand");
let loading_div = document.getElementById("loading_poems");
random_poem_btn.addEventListener("click", () => {
    loading_div.style.display = "block";
    fetch(window.origin + "/GetInspired", {
        method: "POST",
        headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
            "Content-Type": "application/json",
            "Request":"randomise"
        }),
        cache: "no-cache",
        body: JSON.stringify({ "request": "random" })
    })

        .then((respone) => {
            if (respone.status !== 200) {
                console.log("request status for is" + respone.status);
                return;
            }
            respone.json().then((data) => {
                if(data["response"] === "success"){
                    window.location = "/GetInspired?page=1"
                }
            });
        });
})

// toggle rest of poem

let read_more_btn = document.getElementsByClassName("read_more_btn");
let read_more_div = document.getElementsByClassName("read_more_div");
let ctr= 0;
for(let i=0; i<read_more_btn.length; i++){
    read_more_btn[i].addEventListener("click", ()=>{
        if(ctr==0){
            read_more_div[i].style.cssText="display:block;";
            read_more_btn[i].innerText = "Hide";
        }
        else{
            if(read_more_div[i].style.display=="block"){
                read_more_div[i].style.cssText="display:none";
                read_more_btn[i].innerText = "Read More ...";
            }
            else{
                read_more_div[i].style.cssText="display:block";
                read_more_btn[i].innerText = "Hide";
            }

        }
        ctr++;
    })
}

// sort poems

let sort_by = document.getElementById("get_inspired_sort_by");
if(sort_by){
sort_by.addEventListener("change", (event)=>{
    loading_div.style.display = "block";
    console.log("change")
    fetch(window.origin+"/GetInspired",{
        method:"POST",
           headers: new Headers({
            "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
              "Content-Type":"application/json",
              "Request":"sort"
           }),
           cache:"no-cache",
           body: JSON.stringify({"request":event.target.value})
        })
        // this is executed right after the fetch request
        .then((respone)=>{
           // if request fails
           if (respone.status !== 200){
              console.log("request status for sort is"+respone.status);
              return;
           }
           // if request succeeds 
        respone.json().then((data)=>{window.location.reload()});
    });
})
}
