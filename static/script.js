// object that contains what descriptive paragraph to show when user chooses a rhyme scheme
// /Create
let RHYME_DESCRIPTION = {
   "Monorhyme" :"<h3>Monorhyme</h3><h4>Rhyme Scheme: AAAA ...</h4><p><u>Rhyme repetiton (each letter represents a line):</u><br>0(Default): A<br>1: AA<br>2: AAA<br>....<br><u>Description:</u> Monorhyme <b>(mono meaning 1)</b> describes a part of or an entire poem where all the lines end with the same rhyme.<br><br>(This is how a <b>rhyme repetition: 11 line break every:3</b> would look like)<br><u>Example:</u> William Blake, Silent Silent Night.<br><br>Silent Silent Night (A)<br>Quench the holy light (A)<br>Of thy torches bright (A)<br><br>For possessd of day (A)<br>Thousand spirits stray (A)<br>That sweet joys betray (A)<br><br>Why should joys be sweet (A)<br>Used with deceit (A)<br>Nor with sorrows meet (A)<br><br>But an honest joy (A)<br>Does itself destroy (A)<br>For a harlot coy (A)</p>",
   "Coupled Rhyme":"<h3>Coupled Rhyme</h3><h4>Rhyme Scheme: AA BB CC ...</h4><p><u>Rhyme repetiton (each letter represents a line):</u><br>0(Default): AA<br>1: AA BB<br>2: AA BB CC<br>....<br><u>Description:</u> Coupled Rhymes describes part of or an entire poem where every 2 lines <b>(a couple)</b> end with the same rhyme.<br><br>(This is how a <b>rhyme repetition: 1</b> would look like)<br><u>Example:</u>  Dr. Seuss, Green Eggs and Ham.<br><br>I would not like them here or there. (A)<br>I would not like them anywhere. (A)<br>I do not like green eggs and ham. (B)<br>I do not like them, Sam-I-Am. (B)",
   "Triplet":"<h3>Triplet</h3><h4>Rhyme Scheme: AAA ...</h4><p><u>Rhyme repetiton (each letter represents a line):</u><br>0(Default): AAA<br>1: AAA BBB<br>2: AAA BBB CCC<br>....<br><u>Description:</u> Triplet <b>(meaning 3)</b> describes part of or an entire poem where every 3 lines end with the same rhyme.<br><br>(This is how a <b>rhyme repetition: 1</b> would look like)<br><u>Example:</u> Robert Herrick, Upon Julia's Clothes.<br><br>Whenas in silks my Julia goes, (A)<br>Then, then (methinks) how sweetly flows (A)<br>That liquefaction of her clothes. (A)<br><br>Next, when I cast mine eyes, and see (B)<br>That brave vibration each way free, (B)<br>O how that glittering taketh me! (B)",
   "Alternating Rhyme":"<h3>Alternating Rhyme</h3><h4>Rhyme Scheme: ABAB ...</h4><p><u>Rhyme repetiton (each letter represents a line):</u><br>0(Default): ABAB<br>1: ABAB CDCD<br>2: ABAB CDCD EFEF<br>....<br><u>Description:</u> Alternating Rhyme describe a quatrain(4 lines) or an entire poem where lines 1 and 3 rhyme and lines 2 and 4 rhyme thus the rhymes <b>alternate</b>.<br><br>(This is how a <b>rhyme repetition: 1</b> would look like)<br><u>Example:</u> Robert Frost, Neither Out Far Nor In Deep.<br><br>The people along the sand (A)<br>All turn and look one way. (B)<br>They turn their back on the land. (A)<br>They look at the sea all day. (B)<br><br>As long as it takes to pass (C)<br>A ship keeps raising its hull; (D)<br>The wetter ground like glass (C)<br>Reflects a standing gull (D)",
   "Encolsed Rhyme" :"<h3>Enclosed Rhyme</h3><h4>Rhyme Scheme: ABBA ...</h4><p><u>Rhyme repetiton (each letter represents a line):</u><br>0(Default): ABBA<br>1: ABBA CDDC<br>2: ABBA CDDC EFFE<br>....<br><u>Description:</u> Enclosed Rhyme describe a quatrain(4 lines) or an entire poem where lines 1 and 4 rhyme and <b>enclose</b> line 2s and 3 which also rhyme<br><br>(This is how a <b>rhyme repetition: 1</b> would look like)<br><u>Example: </u> Wilfred Owen, Exposure.<br><br>Our brains ache, in the merciless iced east winds that knive us... (A)<br>Wearied we keep awake because the night is silent... (B)<br>Low drooping flares confuse our memory of the salient... (B)<br>Worried by silence, sentries whisper, curious, nervous, (A)<br>&emsp;But nothing happens.<br><br>Watching, we hear the mad gusts tugging on the wire, (C)<br>Like twitching agonies of men among its brambles. (D)<br>Northward, incessantly, the flickering gunnery rumbles, (D)<br>Far off, like a dull rumour of some other war. (C)<br>&emsp; What are we doing here?",
   "Free Verse":"<h3>Free Verse</h3><br><u>Description:</u> Free Verse describes a poem that follows no specific rhyme scheme or rythm.<br><br><u>Example:</u> Walt Whitman, When I Heard the Learn'd Astronomer.<br><br>When I heard the lear'd astronomer,<br>When the proofs, the figures, were ranged in columns before me,<br>When I was shown the charts and diagrams, to add, divide, and measure them,<br><br>When I sitting heard the astronomer where he lectured with much applause in the lecture-room,<br>How soon unaccountable I became tired and sick,<br>Till rising and gliding out I wander'd off by myself,<br>In the mystical moist night-air, and from time to time,<br>Look'd up in perfect silence at the stars.",
   "Custom": "<h3>Custom</h3><br><u>Description:</u> Feeling adventurous? Create your own rhyme scheme!",
   "Shakespearean Sonnet":"<h3>Shakespearean Sonnet</h3><h4>Rhyme Scheme: ABAB CDCD EFEF GG</h4><p><br><u>Description:</u> Shakespearean Sonnet describes a poem of 14 lines with 10 syllables each.<br><br><u>Example:</u> William Shakespeare, My Mistress' Eyes Are Nothing Like the Sun.<br><br>My mistress' eyes are nothing like the sun; (A)<br>Coral is far more red than her lips' red; (B)<br>If snow be white, why then her breasts are dun; (A)<br>If hairs be wires, black wires grow on her head. (B)<br>I have seen roses damasked, red and white, (C)<br>But no such roses see I in her cheeks; (D)<br>And in some perfumes is there more delight (C)<br>Than in the breath that from my mistress reeks. (D)<br>I love to hear her speak, yet well I know (E)<br>That music hath a far more pleasing sound; (F)<br>I grant I never saw a goddess go; (E)<br>My mistress, when she walks, treads on the ground. (F)<br>  And yet, by heaven, I think my love as rare (G)<br>  As any she belied with false compare. (G)</p>",
   "Terza Rima":"<h3>Terza Rima</h3><h4>Rhyme Scheme: ABA BCB CDC DED EE</h4><br><p><u>Description:</u> Terza Rima describes an arrangement of triplets(lines of 3) usually in iambic pentameter(a line of verse with five metrical feet, each consisting of one short (or unstressed) syllable followed by one long (or stressed) syllable, for example Two households, both alike in dignity.)<br><br><u>Example: </u>Shelley, Ode To The West Wind<br><br>O wild West Wind, thou breath of Autumn's being, (A)<br> Thou, from whose unseen presence the leaves dead	(B)<br>Are driven, like ghosts from an enchanter fleeing, (A)<br>Yellow, and black, and pale, and hectic red, (B)<br>Pestilence-stricken multitudes: O thou, (C)<br>Who chariotest to their dark wintry bed (B)<br>The winged seeds, where they lie cold and low, (C)<br>Each like a corpse within its grave, until (D)<br>Thine azure sister of the Spring shall blow (C)<br>Her clarion o'er the dreaming earth, and fill (D)<br>Driving sweet buds like flocks to feed in air (E)<br>With living hues and odours plain and hill: (D)<br>Wild Spirit, which art moving everywhere; (E)<br>Destroyer and preserver; hear, oh, hear! (E)</p>",
   "Limerick":"<h3>Limerick</h3><h4>Rhyme Scheme: AABBA</h4><br><p><u>Description:</u> Limeric describes a humorous five live poem.<br><br><u>Example:</u> Edward Lear, There was an Old Man with a Beard<br>There was an Old Man with a Beard (A)<br>Who said, 'It is just as I feared!— (A)<br>Two Owls and a Hen, (B)<br> four Larks and a Wren, (B)<br>Have all built their nests in my beard. (A)",
   "Haiku":"<h3>Haiku</h3><br><p><u>Description: </u>Haiku describes a japanese poem of 3 lines and 17 syllables total usually talking about nature.<br><br><u>Example: </u> Matsuo Bashō, The Old Pond<br>An old silent pond<br>A frog jumps into the pond—<br>Splash! Silence again.</p>"
};
RHYME_DESCRIPTION = Object.freeze(RHYME_DESCRIPTION);

const SPECIAL_RHYME_SCHEME = []
   
const FIXED_RHYME_SCHEMES = ["Limerick","Shakespearean Sonnet","Haiku","Free Verse","Custom","Terza Rima", "Vilanelle"]
const CUSTOM_BR = ["Monorhyme", "Free Verse", "Custom"]
// let RHYME_SCHEMES = {"Alternate Rhyme" : ["A", "B", "A", "B"],
//                 "Ballade" : ["A", "B", "A", "B", "B", "C", "B", "C", "B","C","B","C"],
//             "Coupled Rhymes (AABBCC)" :["A", "A"],
//             "Monorhyme (AAA...)" : ["A"],
//             "Encolsed Rhyme (ABBA)" : ["A", "B"],
//             "Shakespearean Sonnet (ABAB CDCD EFEF GG)" :["A", "B", "C", "D", "E", "F", "G"],
//             "Triplet (AAA)": ["A", "A", "A"],
//             "Terza Rima (ABA BCB CDC DED EE)":["A", "B", "C", "D", "E"],
//             "Limerick (AABBA)": ["A", "B"],
//             "Vilanelle (ABA ABA ABA ABBA)" :["A", "B"],
//             "HaikuNo Rhyme Scheme)" : [],
//             "Free Verse(No Rhyme Scheme)" : [],
//             "Custom" : []};
// RHYME_SCHEMES = Object.freeze(RHYME_SCHEMES);


window.onload=function(){
   // Dropdown list btn
  let nav_dropdown_btn = document.getElementById("dropdown-btn");
  let dropdown_elements = document.getElementById("list-items");
   //variables used in other func but declared here to hide them when dropwdown elements shown
let toggle_nav = document.getElementById("toggle_nav");
let toggle_note = document.getElementById("toggle_note");
  if(nav_dropdown_btn){
   nav_dropdown_btn.addEventListener("click", ()=>{
     if(dropdown_elements.style.display !=="block") {  
        dropdown_elements.style.display ="block";  
     } else {  
        dropdown_elements.style.display ="none";  
     }   
})}

// Show pass btn
// /Signin /Register
let checkBox = document.getElementById("showPassBtn");
let pass = document.getElementById("password");
let cpass = document.getElementById("cpassword");
if(checkBox){
checkBox.addEventListener("click", ()=>{
   if(checkBox.checked){
   if (pass && pass.type === "password") {
      pass.type = "text";
    } 
   if (cpass && cpass.type === "password") {
      cpass.type = "text";
      }
   }
   else{
      if (pass){
         pass.type = "password";
      }
      if (cpass){
         cpass.type = "password";
      }
   }
})}

let logout_btn = document.getElementById("logout")
let confirm_logout_btn = document.getElementById("confirm_logout");

if (logout_btn){
   logout_btn.addEventListener("click",()=>{
      const logout_modal = new bootstrap.Modal(document.getElementById('logout_modal'), {backdrop:"static" });
            logout_modal.show();
            confirm_logout_btn.addEventListener("click", ()=>{
               window.location.replace(window.origin+"/signout")
            })
            
   })
}



//hide nav btn
// /Write
let navbar = document.getElementById("nav_div");
if(toggle_nav){
toggle_nav.addEventListener("click", ()=>{
   if((navbar.style.visibility !== "hidden")&&(navbar.style.position !== "absolute")){
      navbar.style.cssText = "visibility :hidden; position: absolute";
   }
   else{
      navbar.style.cssText = "visibility :visible; position: relative";
   }
})}

// toggle notepad
// /Write
let notepad = document.getElementById("notepad");
if(toggle_note){
   toggle_note.addEventListener("click", ()=>{
      if((notepad.style.visibility !== "visible")&&(notepad.style.position !== "relative")){
         notepad.style.cssText="visibility: visible; position:relative";
      }
      else{
         notepad.style.cssText="visibility: hidden; position:absolute"
      }
   })
}

// toggle btn div
// /Write
let detatch_util = document.getElementById("detatch_util")
let arrow = document.getElementById("arrow");
let arrow_symbol = document.getElementById("arrow_symbol")
let btn_div = document.getElementById("btn_div")
// pin btn div
if(detatch_util){

   detatch_util.addEventListener("click",()=>{
      if(!detatch_util.checked){
         btn_div.style.cssText = "position: relative;"
         arrow.style.cssText = "position: relative;"
      }
   else{
      btn_div.style.cssText = "position: fixed; right:0px"
      arrow.style.cssText = "position: fixed; right:245px"
   }
})
// hide and show div with arrow
if(arrow){
   arrow.addEventListener("click",()=>{
      if(btn_div.style.visibility!=="hidden" && btn_div.style.position !=="absoliute"){
         btn_div.style.cssText = "position: absolute; visibility:hidden";
         arrow_symbol.classList.remove("right");
         arrow_symbol.classList.add("left");
         if (!detatch_util.checked){
            arrow.style.cssText = "position:relative;"
         }
         else{
            arrow.style.cssText = "position:fixed; right:0px"
         }
   }
   else{
      arrow_symbol.classList.remove("left");
      arrow_symbol.classList.add("right");
      if (!detatch_util.checked){
         btn_div.style.cssText = "position: relative; visibility:visible"
         arrow.style.cssText = "position: relative; right:0px"
      }
      else{
         btn_div.style.cssText = "position: fixed; visibility:visible"
         arrow.style.cssText = "position: fixed; right:245px"
      }
   }
})
}
}


// popus
let popup = document.getElementById("popup");
let x = document.getElementById("myPopup");
if (popup){
   x.classList.toggle("show");
}

//change description based on rhyme scheme chosen
// /Create
let rhyme_scheme = document.getElementById("rhyme_schemes");
let description = document.getElementById("description"); 
let rhyme_repetition = document.getElementById("rhyme_repetition_div");
let br_frequency = document.getElementById("line_break_frequency_div")
if(rhyme_scheme){
   rhyme_scheme.addEventListener("change", (event)=>{
      if(!(FIXED_RHYME_SCHEMES.includes(event.target.value))){
         rhyme_repetition.style.cssText = "visibility: visible; position: relative";
      }
      else{
         rhyme_repetition.style.cssText = "visibility: hidden; position: absolute";

      }
      if(!(CUSTOM_BR.includes(event.target.value))){
         br_frequency.style.cssText = "visibility: hidden; position: absolute";
      }
      else{
         br_frequency.style.cssText = "visibility: visible; position: relative";
      }
      if(description.style.visibility !== "visible" && description.style.position !== "relative"){
         description.style.cssText = "visibility: visible; position: relative"
      }
         description.innerHTML = RHYME_DESCRIPTION[event.target.value];
      let rhyme_div = document.getElementById("user-custom-rhymes-div")
      let line_div = document.getElementById("line-div")
      if ((event.target.value === "Free Verse")){
         line_div.style.cssText = "position: relative; visibility:visible;";
      }
      else{
         line_div.style.cssText = "position: absolute; visibility:hidden;";
      }
      if (event.target.value === "Custom"){
         rhyme_div.style.cssText = "position: relative; visibility:visible;";
      }
      else{
         rhyme_div.style.cssText = "position: absolute; visibility:hidden;";
      };
});
// /Create
// show all rhyme descriptions if btn is pressed
let btn_show_all = document.getElementById("show_all_res_desc");
btn_show_all.addEventListener("click", ()=>{
   let ctr = 0;
   for(let key in RHYME_DESCRIPTION){
      console.log("desc_par"+key)
      let description_paragraph = document.getElementById("desc_par"+key);
      if (description_paragraph.style.visibility!=="visible" && description_paragraph.style.position!=="relative"){
         if( btn_show_all.innerText !== "Hide all"){
            btn_show_all.innerText = "Hide all";
         }
         if(description_paragraph.style.visibility !== "hidden" && description_paragraph.style.position !== "absolute"){
            description_paragraph.style.cssText = "position: absolute; visibility:hidden;";
         }
         
         description_paragraph.innerHTML = RHYME_DESCRIPTION[key];
         description_paragraph.style.cssText = "position: relative; visibility:visible";
      }
      else{
         if(btn_show_all.innerText !== "Show all rhyme schemes description"){
            btn_show_all.innerText = "Show all rhyme schemes description";
         }
         console.log(description_paragraph)
         description_paragraph.style.cssText = "position: absolute; visibility:hidden;";
         
      };
   };
});
};

// fetch(window.origin+'/Rhyme')
//       .then((response) => {
//           return response.json();
//       }).then((text)=> {
//           console.log('GET response:');
//           console.log(text); 
//       });


// MAIN FUNCTION---------------------------------------------------------------------Check Rhymes
// let create_poem = document.getElementById("create_poem")
// // /Write
// if (create_poem){
//    create_poem.addEventListener("click", ()=>{
//       console.log("click detected")
//       fetch(window.origin+"/Write",{
//          method:"POST",
//             headers: new Headers({
//                "Content-Type":"application/json"
//             }),
//             cache:"no-cache",
//             body: JSON.stringify({"request":"get rhyme scheme"})
//          })
//          // this is executed right after the fetch request
//          .then((respone)=>{
//             // if request fails
//             if (respone.status !== 200){
//                console.log("request status for syllables is"+respone.status);
//                return;
//             }
//             // if request succeeds 
//          respone.json().then((data)=>{ 
//             console.log("rhyme scheme is",data);
//             user_rhyme_scheme = data["rhyme scheme"];
//             user_rhymes_for_custom = data["custom rhyme scheme"]
//          })
//       });
//    })
// }

let check_rhyme_btn = document.getElementById("check_rhymes");
if(check_rhyme_btn){
   check_rhyme_btn.addEventListener("click", ()=>{
      if(check_rhyme_btn.checked){
         let send_to_server_rhymes = {"request":"get rhyme"};
         let input = document.getElementsByClassName("line");
      console.log(input.length)
      for (let i=0; i<input.length; i++){
         console.log(input.item(i).innerText);
         console.log(i);
         if (send_to_server_rhymes.hasOwnProperty(input.item(i).getAttribute("name"))){
            send_to_server_rhymes[input.item(i).getAttribute("name")].push(input.item(i).innerText);
         }
         else{
            send_to_server_rhymes[input.item(i).getAttribute("name")]=[input.item(i).innerText];
         }
      }
      console.log(send_to_server_rhymes)
      
      //send data to server if btn is checked

         fetch(window.origin+"/Write",{
            method:"POST",
               headers: new Headers({
                  "Content-Type":"application/json"
               }),
               cache:"no-cache",
               body: JSON.stringify(send_to_server_rhymes)
            })
            // this is executed right after the fetch request
            .then((respone)=>{
               // if request fails
               if (respone.status !== 200){
                  console.log("request status for rhyme is"+respone.status);
                  return;
               }
               // if request succeeds 
            respone.json().then((data)=>{
               
               console.log("this is the workable with data", data)
               // check if user is trying to detect rhymes of empty lines
               let no_data_rhymes = document.getElementById("no_data_rhymes");
               let obj_len = 0;
               for (let i in data){
                  obj_len += data[i].length;
               }
               console.log(obj_len)
               if(obj_len===0){
                  no_data_rhymes.innerHTML = "There must at least two words of the same rhyme in your poem!";
               }
               // change element color corresponding to the returned object's key
               if (data["red"]){
                  for (let i in data["red"]){
                     console.log("data is red")
                     let rhyme_symbol = document.getElementById("symbol"+data["red"][i]);
                     if (check_rhyme_btn.checked){
                        rhyme_symbol.style.backgroundColor = "red";
                     }
                  };
               };
               if (data["green"]){
                  for (let i in data["green"]){
                     console.log("data is green")
                     console.log("symbol"+data["green"][i])
                     let rhyme_symbol = document.getElementById("symbol"+data["green"][i]);
                        console.log(rhyme_symbol)
                        rhyme_symbol.style.backgroundColor = "green";
                     };
                  };
                  if (data["yellow"]){
                     for (let i in data["yellow"]){
                        console.log("data is yellow")
                        let rhyme_symbol = document.getElementById("symbol"+data["yellow"][i]);
                        rhyme_symbol.style.backgroundColor = "yellow";
                     };
               };
               if (data["blue"]){
                  for (let i in data["blue"]){
                     console.log("data is blue")
                     let rhyme_symbol = document.getElementById("symbol"+data["blue"][i]);
                     rhyme_symbol.style.backgroundColor = "blue";
                  };
               };
            });
         });
      }
   //if btn is not checked all background colors go back to normal 
   else{
      // remove error msg
      no_data_rhymes.innerHTML = "";
      // rever all elements to their original color
      let input = document.getElementsByClassName("line");
      for (let i=0; i<input.length; i++){
         let symbol_id = "symbol"+input.item(i).id;
         document.getElementById(symbol_id).style.backgroundColor = "rgb(105, 113, 132)";
      }
   }
   });
   }


// CHECK SYLLABLES==============================================================================================================

let check_syllables_btn= document.getElementById("display_syllable_count");
const RHYME_AMOUNT = 10; //how many rhymes of each letter there can be A0 A1 A2 B0 B1 ...
const LINE_AMOUNT = 101; //max is 100 lines
if(check_syllables_btn){
   check_syllables_btn.addEventListener("click", ()=>{
   if(check_syllables_btn.checked){
      let send_to_server_syllables = {"request":"get syllables"};
      let input = document.getElementsByClassName("line");
      for(let i =0; i<input.length; i++){
         send_to_server_syllables[input.item(i).id] = input.item(i).innerText;
      }
      console.log(send_to_server_syllables);
         fetch(window.origin+"/Write",{
            method:"POST",
               headers: new Headers({
                  "Content-Type":"application/json"
               }),
               cache:"no-cache",
               body: JSON.stringify(send_to_server_syllables)
            })
            // this is executed right after the fetch request
            .then((respone)=>{
               // if request fails
               if (respone.status !== 200){
                  console.log("request status for syllables is"+respone.status);
                  return;
               }
               // if request succeeds 
            respone.json().then((data)=>{
               console.log("this is the workable with data", data)
                  let input = document.getElementsByClassName("line");
                  for(let j=0; j<input.length; j++){
                     console.log(input.item(j).id)
                     console.log(data[input.item(j).id])
                     if(data[input.item(j).id]){
                        let syllables = document.getElementById("syllables"+input.item(j).id)
                        console.log(data[input.item(j).id] == 0)
                        for(k in data[input.item(j).id]){
                        // console.log("data",data[input.item(j).id][j])
                        if(data[input.item(j).id][j]==0){
                           let no_data_syllables = document.getElementById("no_data_syllables");
                           if(no_data_syllables.style.position!=="relative" && no_data_syllables.style.visibility!=="visible"){
                              no_data_syllables.style.cssText = "position: relative; visibility: visible";
                           }
                        }
                     }
                        let total_rhymes = data[input.item(j).id].reduce((a,b)=> a+b,0);
                        if(syllables.style.visibility !== "visible" && syllables.style.position !== "relative"){
                           syllables.style.cssText = "visibility: visible; position: relative";
                              syllables.innerText = data[input.item(j).id].join(" / ").concat(" = "+total_rhymes);
                        }
                     }
                  }
            });
         });
      }
      // if btn isin t checked hide all paragrapahs 
      else{
         let no_data_syllables = document.getElementById("no_data_syllables");
         if(no_data_syllables.style.position!=="hidden" && no_data_syllables.style.visibility!=="absolute"){
         no_data_syllables.style.cssText = "visibility: hidden; position: absolute";
         }
         // hide all syllable divs
         let input = document.getElementsByClassName("line");
                  for(let j=0; j<input.length; j++){
                     let syllables = document.getElementById("syllables"+input.item(j).id);
                     syllables.style.cssText = "visibility: hidden; position: absolute";
                     }
}
   })
}
let save_draft = document.getElementById("save_draft");
let success_msg = document.getElementById("confirmation_msg_write");
let success_msg_div = document.getElementById("msg_container");
let close_success_msg = document.getElementById("hide");
// const write_modal = new bootstrap.Modal(document.getElementById('write_modal'), {keyboard:false, backdrop:"static" });
let save_btn = document.getElementById("save");
let update_btn = document.getElementById("update");

// try saving user poem as draft to db
if (save_draft){
   const write_modal = new bootstrap.Modal(document.getElementById('write_modal'), {keyboard:false, backdrop:"static" });
   save_draft.addEventListener("click",()=>{
      let title = document.getElementById("title").innerText;
      let notepad = document.getElementById("notepad").innerText;
      let send_to_server_draft = {"request":"save draft", "title":title, "notes":notepad};
      let input = document.getElementsByClassName("line");
      for(let i =0; i<input.length; i++){
         send_to_server_draft[input.item(i).id] = input.item(i).innerText;
      }
      console.log(send_to_server_draft);
   fetch(window.origin+"/Write",{
         method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify(send_to_server_draft)
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         // if request fails
         if (respone.status !== 200){
            console.log("request status for draft is"+respone.status);
            return;
         }
         // if request succeeds 
      respone.json().then((data)=>{
         console.log("data we got back is", data);
         // if the poem already has a draft ask user what to do 
         if (data["response"] === "draft already exists"){
            write_modal.show()
            }
         // else save and notify the user
         else{
               success_msg.innerText="Draft succesfully saved";
               success_msg_div.style.cssText="position: relative; visibility: visible";

         }
      });
      });
});
if(save_btn){
   // if user chooses to save from our modal
   save_btn.addEventListener("click", ()=>{
      console.log("user wants to save");
      // tell the server to do so
   fetch(window.origin+"/Write",{
      method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify({"request":"save another draft"})
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         console.log("saved another draft");
         // if request fails
         if (respone.status !== 200){
            console.log("request status for draft is"+respone.status);
            return;
         }
         // if request succeeds 
         respone.json().then((data)=>{
            write_modal.hide()
            success_msg_div.style.cssText = "position: relative; visibility: visible";
            success_msg.innerHTML = "Draft succesfully saved";

         });
      });
   })
}
if(update_btn){
   // if user wants to update existing draft
   update_btn.addEventListener("click", ()=>{
      console.log("user wants to update");
   // tell the server
   fetch(window.origin+"/Write",{
      method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify({"request":"update draft"})
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         // if request fails
         if (respone.status !== 200){
            console.log("request status for draft is"+respone.status);
            return;
         }
         // if request succeeds 
         respone.json().then((data)=>{ 
            console.log("updated")
            write_modal.hide()
            success_msg_div.style.cssText="position: relative; visibility: visible";
            success_msg.innerText="Draft successfully updated";

         });
      });
   })
}
}
if (close_success_msg){
   close_success_msg.addEventListener("click", ()=>{
      success_msg_div.style.cssText = "visibility: hidden, position:absolute";
      success_msg.innerHTML = "";
   })
}

let draft_resume = document.getElementsByClassName("resume");
let draft_delete = document.getElementsByClassName("delete");

if (draft_resume){
   for(let i =0; i<draft_resume.length; i++){
   draft_resume[i].addEventListener("click", ()=>{
      poem_draft_num = String(draft_resume.item(i).getAttribute("name"));
      send_to_server_draft_resume = {};
      send_to_server_draft_resume["draft_resume"] = draft_resume.item(i).getAttribute("name");
      console.log(send_to_server_draft_resume)
      fetch(window.origin+"/Account/Draft",{
         method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_draft_resume)
         })
         // this is executed right after the fetch request
         .then((respone)=>{
            // if request fails
            if (respone.status !== 200){
               console.log("request status for resume draft is"+respone.status);
               return;
            }
            // if request succeeds 
         respone.json().then((data)=>{
            // redirect user to write
            window.location.replace(window.origin+("/Write"));
          });
   });

   })
}
}
if (draft_delete){
   for(let i =0; i<draft_delete.length; i++){
      draft_delete[i].addEventListener("click", ()=>{
      send_to_server_draft_delete = {};
      send_to_server_draft_delete["draft_delete"] = draft_delete.item(i).getAttribute("name");
      console.log(send_to_server_draft_delete)
      poem_draft_num = draft_delete.item(i).getAttribute("name");
      console.log(poem_draft_num)
         if (document.cookie !== "draft_hide=true"){
            console.log(document.cookie)
            const draft_modal = new bootstrap.Modal(document.getElementById('draft_modal'), {keyboard:false, backdrop:"static" });
            draft_modal.show();
            let delete_btn = document.getElementById("delete_btn");
            let stop_showing_modal = document.getElementById("dont_show_again")
            delete_btn.addEventListener("click", ()=>{
               if(stop_showing_modal.checked){
                  document.cookie = "draft_hide = true"
               }
               draft_modal.hide();
               fetch(window.origin+"/Account/Draft",{
                  method:"POST",
                     headers: new Headers({
                        "Content-Type":"application/json"
                     }),
                     cache:"no-cache",
                     body: JSON.stringify(send_to_server_draft_delete)
                  })
                  // this is executed right after the fetch request
                  .then((respone)=>{
                     // if request fails
                     if (respone.status !== 200){
                        console.log("request status for delete draft is"+respone.status);
                        return;
                     }
                     // if request succeeds 
                  respone.json().then((data)=>{
                     document.getElementsByName( draft_delete.item(i).getAttribute("name"))[0].style.visibility = "hidden";
                     document.getElementsByName( draft_delete.item(i).getAttribute("name"))[0].style.position = "absolute";
                   });
            });
            })
         }
         else{
      fetch(window.origin+"/Account/Draft",{
         method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_draft_delete)
         })
         // this is executed right after the fetch request
         .then((respone)=>{
            // if request fails
            if (respone.status !== 200){
               console.log("request status for delete draft is"+respone.status);
               return;
            }
            // if request succeeds 
         respone.json().then((data)=>{
            document.getElementsByName( draft_delete.item(i).getAttribute("name"))[0].style.visibility = "hidden";
            document.getElementsByName( draft_delete.item(i).getAttribute("name"))[0].style.position = "absolute";
          });
         });
         
}
   })
}
}
let next = document.getElementById("next");
if(next){
   next.addEventListener("click",()=>{
      let title = document.getElementById("title").innerText;
      let send_to_server_format = {"request":"format", "title":title};
      let input = document.getElementsByClassName("line");
      for(let i =0; i<input.length; i++){
         send_to_server_format[input.item(i).id] = input.item(i).innerText;
      }
      console.log(send_to_server_format);
   fetch(window.origin+"/Write",{
         method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify(send_to_server_format)
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         // if request fails
         if (respone.status !== 200){
            console.log("request status for draft is"+respone.status);
            return;
         }
         // if request succeeds 
      respone.json().then((data)=>{
         console.log("data we got back is", data);
         location.replace(window.origin+"/Format");
         
      });
      });
});
}

if (window.location == window.origin+"/Format"){
   fetch(window.origin+"/Format",{
      method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify({"request":"get rhyme scheme"})
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         // if request fails
         if (respone.status !== 200){
            console.log("request status for format is"+respone.status);
            return;
         }
         // if request succeeds 
      respone.json().then((data)=>{
         data["response"] = rhyme_scheme
         if (rhyme_scheme == "Alternate Rhyme (ABAB)"){
            let hshs = document.getElementById("B0");
            let lb = document.createElement("br");
            insertAfter(lb, hshs)
         }
      });
});
}

// /Format
if(window.location == window.origin+"/Format"){

let save = document.getElementById("save_poem");
let poem_div = document.getElementById("poem");

save.addEventListener("click",()=>{
   let send_to_server_poem = {"request":"save poem"};
   let lines = document.getElementsByClassName("edit_line");
   send_to_server_poem["title"]= document.getElementById("poem_title").innerText;
   console.log(document.getElementById("poem_title").innerText)
   for (let i =0;i<lines.length;i++){
      send_to_server_poem[lines.item(i).id]= lines.item(i).innerText;
   }
   fetch(window.origin+"/Format",{
      method:"POST",
         headers: new Headers({
            "Content-Type":"application/json"
         }),
         cache:"no-cache",
         body: JSON.stringify(send_to_server_poem)
      })
      // this is executed right after the fetch request
      .then((respone)=>{
         // if request fails
         if (respone.status !== 200){
            console.log("request status for poems is"+respone.status);
            return;
         }
         // if request succeeds 
      respone.json().then((data)=>{
         console.log(data)
         window.location.replace(window.origin+("/Account/Poem"))
       });
});

})
}

let show_poem = document.getElementsByClassName("show_poem");
if (show_poem){
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
}
let delete_poem = document.getElementsByClassName("delete_poem")
if (delete_poem){
   for(let i=0; i<delete_poem.length; i++){
      delete_poem.item(i).addEventListener("click", ()=>{
         let send_to_server_poem_delete = {"request":"delete_poem", "poem_id":delete_poem.item(i).getAttribute("name")}
      fetch(window.origin+"/Account/Poem",{
         method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_poem_delete)
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
            if (data["response"] === "successful"){
               document.getElementById("container"+data["poem_title"]+"/"+data["poem_num"]).style.cssText = "position: absolute; visibility:hidden;";
               document.getElementById(data["poem_title"]+"/"+data["poem_num"]).style.cssText = "position: absolute; visibility: hidden";
            }
         });
      });
   })
}
}

// /Get Inspired
let search_btn = document.getElementById("search_poem")
if (search_btn){
   let send = true
   search_btn.addEventListener("click", ()=>{
      search_btn.setAttribute("disabled","disabled");
      let send_to_server_poem_search;
      let poem_search = document.getElementById("poem_search");
      let search_by = document.getElementsByClassName("search_by");
      for(let i =0; i<search_by.length; i++){
         if (search_by.item(i).checked && poem_search.value){
            send_to_server_poem_search = {"request":"search poem", "search by": search_by.item(i).id, "query":poem_search.value};
            send = true;
         }
      }
      if (!send_to_server_poem_search){
         send = false;
      }
         console.log(send)
      if(send){
         let loading_div = document.getElementById("loading_poems");
         loading_div.style.cssText="visibility:visible; position:relative";
         fetch(window.origin+"/GetInspired",{
            method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify(send_to_server_poem_search)
         })
         // this is executed right after the fetch request
         .then((respone)=>{
            // if request fails
            if (respone.status !== 200){
               console.log("request status for search poem is"+respone.status);
               return;
            }
            // if request succeeds 
         respone.json().then((data)=>{
            if(data["response"]!=="empty"){
               window.location.reload();
               // let poem_select = document.getElementById("poem_search_select");
               // let poem_result = document.getElementById("poem_result");
               // console.log("Data recieved")
               // poem_result.innerHTML = "";
               // poem_select.options.length = 0;
               // loading_div.style.cssText="visibility:hidden; position:absolute";
               // for(let i in data["response"]){
               //    if(i == 10){
               //       poem_result.innerHTML +='<button class="button">Load More</button>';
               //       break;
               //    }
               //       // poem_obj = JSON.parse(data["response"][i]);
               //       poem_obj = data["response"][i];
               //       poem_select.options[poem_select.options.length]= new Option(`${poem_obj["title"]} / ${poem_obj["author"]}`, `#${i}`)
               //       poem_result.innerHTML += `<div id="${i}"><h3>${poem_obj["title"]} By ${poem_obj["author"]}</h3><br>`;
               //       for(let i in poem_obj["lines"]){
               //          console.log("making lines")
               //          poem_result.innerHTML +=`<pre>${poem_obj["lines"][i]}`;
               //       }        
               //       poem_result.innerHTML +="</pre></div><br><hr><br></br>";
               //    }
               search_btn.removeAttribute("disabled");
            }
            
         });
   });
}
else{
   poem_result.innerHTML = "<p class='error_msg'>No Matches</p>"
}
   })
   
}
let random_poem = document.getElementById("poem_rand");
if (random_poem){
   random_poem.addEventListener("click",()=>{
      let loading_div = document.getElementById("loading_poems");
      loading_div.style.cssText="visibility:visible; position:relative";

      random_poem.setAttribute("disabled", "disabled")
      fetch(window.origin+"/GetInspired",{
         method:"POST",
            headers: new Headers({
               "Content-Type":"application/json"
            }),
            cache:"no-cache",
            body: JSON.stringify({"request":"random"})
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
            let poem_select = document.getElementById("poem_search_select");
            let poem_result = document.getElementById("poem_result");
               console.log("Data recieved")
               console.log(data)
               poem_result.innerHTML = "";
               poem_select.options.length = 0;
               loading_div.style.cssText="visibility:hidden; position:absolute";
               for(let i in data["response"]){
                  poem_obj = JSON.parse(data["response"][i]);
                  poem_select.options[poem_select.options.length]= new Option(`${poem_obj["Title"]} / ${poem_obj["Poet"]}`, `#${i}`)
                  poem_result.innerHTML += `<div id="${i}"><h3>${poem_obj["Title"]} By ${poem_obj["Poet"]}</h3><pre>${poem_obj["Poem"]}</pre></div><br><hr><br>`        
                  
                  }
               random_poem.removeAttribute("disabled");
         });
   });
   })
}
}

if(window.location == window.origin+"/Write"){
   window.addEventListener("beforeunload", (e)=>{
            e.preventDefault();
            return e.returnValue="";
         });
      }

