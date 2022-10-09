// object that contains what descriptive paragraph to show when user chooses a rhyme scheme
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


//change description based on rhyme scheme chosen
let rhyme_scheme = document.getElementById("rhyme_schemes");
let description = document.getElementById("description"); 
let rhyme_repetition = document.getElementById("rhyme_repetition_div");
let br_frequency = document.getElementById("line_break_frequency_div")
rhyme_scheme.addEventListener("change", (event)=>{
    if(!(FIXED_RHYME_SCHEMES.includes(event.target.value))){
        rhyme_repetition.style.cssText = "display:flex";
    }
    else{
        rhyme_repetition.style.cssText = "display:none";

    }
    if(!(CUSTOM_BR.includes(event.target.value))){
        br_frequency.style.cssText = "display:none";
    }
    else{
        br_frequency.style.cssText = "display:flex";
    }
    
    let rhyme_div = document.getElementById("user-custom-rhymes-div")
    let line_div = document.getElementById("line-div")
    if ((event.target.value === "Free Verse")){
        line_div.style.cssText = "display:flex;";
    }
    else{
        line_div.style.cssText = "display:none;";
    }
    if (event.target.value === "Custom"){
        rhyme_div.style.cssText = "display:flex;";
    }
    else{
        rhyme_div.style.cssText = "display:none;";
    }
    // display description 
    let singular_desc_container = document.getElementById("singular_desc_container");
    singular_desc_container.innerHTML=""
    let description_div = document.createElement("div");
        description_div.innerHTML = RHYME_DESCRIPTION[event.target.value];
        description_div.classList.add("rhyme_description");
        description_div.style.cssText="display:block";
        singular_desc_container.appendChild(description_div);
});

// show all rhyme descriptions if btn is pressed
let btn_show_all = document.getElementById("show_all_res_desc");
let rhyme_desc_container = document.getElementById("rhyme_desc_container");
let ctr = 0
btn_show_all.addEventListener("click", ()=>{
    // ctr is used to detect if it's the user's first button press or not
    if(ctr==0){
    for(let key in RHYME_DESCRIPTION){
        let description_div = document.createElement("div");
        description_div.classList.add("rhyme_description");
        description_div.innerHTML = RHYME_DESCRIPTION[key];
       rhyme_desc_container.appendChild(description_div);
       btn_show_all.innerHTML="Hide all";
    }
}
       else{
        if(rhyme_desc_container.style.display!="block"){
            rhyme_desc_container.style.display="block";
            btn_show_all.innerHTML="Hide all";
        }
        else{
            rhyme_desc_container.style.display="none";
            btn_show_all.innerHTML="Show All Rhyme Schemes Descriptions";
        }
    }
        ctr++;
});

// random rhyme scheme btn
let random_pick_btn = document.getElementById("random_create_poem");
random_pick_btn.addEventListener("click", ()=>{
    random_val = Math.floor(Math.random()*Object.keys(RHYME_DESCRIPTION).length);
    rhyme_scheme.value=Object.keys(RHYME_DESCRIPTION)[random_val];
    let change_event = new Event("change");
    rhyme_scheme.dispatchEvent(change_event);
})
