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
    // Check if both familyDropdown and monsterDropdown exist
    if (familyDropdown && monsterDropdown) {
        // Update the monsterDropdown value
        monsterDropdown.value = selectedMonster;

        // Update families dropdown
        updateMonstersDropdown(familyDropdown);

        // Trigger updateIframes function
        updateIframes(familyDropdown, monsterDropdown);
    }
}

function updateMonstersDropdown(familyDropdown) {
    // Check if familyDropdown exists
    if (familyDropdown) {
        const selectedFamily = familyDropdown.value;

        // Fetch monsters data from the server based on the selected family
        fetch(`/get_monsters?family=${selectedFamily}`)
            .then(response => response.json())
            .then(data => populateDropdown(monsterDropdown, data))
            .catch(error => console.error("Error fetching monsters:", error));
    }
}


function populateDropdown(dropdown, data) {
    // Check if dropdown exists
    if (dropdown) {
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
}
