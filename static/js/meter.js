let foot_type = {
    "trochaic": "STRESSED-unstressed | ", "iambic": "unstressed-STRESSED | ",
    "spondaic": "STRESSED-STRESSED | ", "dactylic": "STRESSED-unstressed-unstressed | ",
    "anapestic": "unstressed-unstressed-STRESSED | "
}

let select_foot_type = document.getElementById("meter_foot_type");
let select_foot_amount = document.getElementById("meter_foot_amount");
let meter_example = document.getElementById("meter_example");

select_foot_type.addEventListener("change", (event) => {
    let meter_example_content = document.createElement("p");
    console.log(foot_type[event.target.value])
    meter_example.innerHTML = "";
    meter_example_content.innerHTML = (foot_type[event.target.value]).repeat(parseInt(select_foot_amount.value));
    meter_example.appendChild(meter_example_content);
})

select_foot_amount.addEventListener("change", (event) => {
    let meter_example_content = document.createElement("p");
    meter_example.innerHTML = "";
    meter_example_content.innerHTML = (foot_type[select_foot_type.value]).repeat(parseInt(event.target.value));
    meter_example.appendChild(meter_example_content);
})