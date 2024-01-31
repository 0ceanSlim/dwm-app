// breeding.js

document.addEventListener("DOMContentLoaded", function () {
    const monsterNames = document.querySelectorAll(".monster-name");
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");

    // Add click event listener to each monster name
    monsterNames.forEach(name => {
        name.addEventListener("click", function () {
            const selectedMonster = this.dataset.name;

            // Update the monsterDropdown and trigger iframes update
            updateDropdownAndIframes(selectedMonster, familyDropdown, monsterDropdown);
        });
    });
});

function updateDropdownAndIframes(selectedMonster, familyDropdown, monsterDropdown) {
    // Update the monsterDropdown value
    monsterDropdown.value = selectedMonster;

    // Update families dropdown (if needed)
    updateMonstersDropdown(familyDropdown);

    // Trigger updateIframes function
    updateIframes(familyDropdown, monsterDropdown);
}

function updateMonstersDropdown(familyDropdown) {
    const selectedFamily = familyDropdown.value;

    // Fetch monsters data from the server based on the selected family
    fetch(`/get_monsters?family=${selectedFamily}`)
        .then(response => response.json())
        .then(data => populateDropdown(monsterDropdown, data))
        .catch(error => console.error("Error fetching monsters:", error));
}

function updateIframes(familyDropdown, monsterDropdown) {
    const selectedFamily = familyDropdown.value;
    const selectedMonster = monsterDropdown.value;

    // Update monsterIframe src based on selected family and monster
    const monsterIframeSrc = selectedMonster
        ? `/monster/${selectedMonster}`
        : selectedFamily
        ? `/monster/${selectedFamily}`
        : "about:blank";

    // Assuming you have these iframe elements defined somewhere
    const monsterIframe = document.getElementById("monsterIframe");
    const breedingIframe = document.getElementById("breedingIframe");

    monsterIframe.src = monsterIframeSrc;

    // Update breedingIframe src based on the selected monster
    const breedingIframeSrc = selectedMonster
        ? `/get_breeding_combinations?monster=${selectedMonster}`
        : "about:blank";

    breedingIframe.src = breedingIframeSrc;
}

function populateDropdown(dropdown, data) {
    // Clear existing options
    dropdown.innerHTML = '<option value="">All</option>';

    // Populate dropdown options
    data.forEach(item => {
        const option = document.createElement("option");
        option.value = item;
        option.text = item;
        dropdown.appendChild(option);
    });
}
