let icon_btn = document.getElementsByClassName("icon_btn");
let icon = document.getElementsByClassName("small_icon");
let syllables_div = document.getElementsByClassName("syllable_div");
for(let i = 0; i<icon_btn.length; i++){
    let ctr = 0;
    icon_btn.item(i).addEventListener("click", ()=>{
        if(ctr=0){
            syllables_div[i].style.display = "none";
            icon[i].setAttribute("src","/static/icons/down-arrow.png");
        }
        else{
            if(syllables_div[i].style.display == "none"){
                syllables_div[i].style.display = "block";
                icon[i].setAttribute("src","/static/icons/up-arrow.png");
            }
            else{
                syllables_div[i].style.display = "none";
                icon[i].setAttribute("src","/static/icons/down-arrow.png");
            }
        }
        ctr++;
    })
}

let search_rhymes= document.getElementById("serach_for_rhymes");
let loading = document.getElementById("loading_rhymes");
search_rhymes.addEventListener("submit", ()=>{
    loading.style.display = "block";
})

let check_rhymes_btn = document.getElementById("check_rhymes_btn");
let rhyme_check_results = document.getElementById("rhyme_check_results");
let word1 = document.getElementById("word1");
let word2 = document.getElementById("word2");

word1.addEventListener("keydown", (event)=> {
    if (event.key === "Enter") {
        event.preventDefault();
        word2.focus();
    }
    });
word2.addEventListener("keydown", (event)=> {
    if (event.key === "Enter") {
        event.preventDefault();
        check_rhymes_btn.click();
    }
    });

check_rhymes_btn.addEventListener("click", ()=>{
    rhyme_check_results.style.backgroundColor="#e9ecef";
    fetch(window.origin+"/Rhymes",{
        method:"POST",
           headers: new Headers({
              "Content-Type":"application/json",
              "X-CSRFToken": document.getElementsByName("csrf_token")[0].value,
              "Request":"check if words rhyme"
           }),
           cache:"no-cache",
           body: JSON.stringify({"request" : [word1.value.toLowerCase(), word2.value.toLowerCase()]})
        })
        // this is executed right after the fetch request
        .then((respone)=>{
           // if request fails
           if (respone.status !== 200){
              console.log("request status for is"+respone.status);
              return;
           }
           // if request succeeds 
        respone.json().then((data)=>{
            if(data["response"]){
                rhyme_check_results.style.backgroundColor = "green";
            }
            else{
                rhyme_check_results.style.backgroundColor = "red";
            }
        });
    });

})