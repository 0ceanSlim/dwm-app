// static/js/app.js

document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");
    const iframe = document.getElementById("monsterIframe");

    // Initialize dropdowns and iframe
    updateMonstersDropdown();
    updateIframe();

    // Fetch families data from the server
    fetch("/get_families")
        .then(response => response.json())
        .then(data => {
            populateDropdown(familyDropdown, data);
            updateMonstersDropdown();
            updateIframe();
        })
        .catch(error => console.error("Error fetching families:", error));

    familyDropdown.addEventListener("change", function () {
        updateMonstersDropdown();
        updateIframe();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframe();
    });

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

    function updateMonstersDropdown() {
        const selectedFamily = familyDropdown.value;

        // Fetch monsters data from the server based on the selected family
        fetch(`/get_monsters?family=${selectedFamily}`)
            .then(response => response.json())
            .then(data => populateDropdown(monsterDropdown, data))
            .catch(error => console.error("Error fetching monsters:", error));
    }

    function updateIframe() {
        const selectedFamily = familyDropdown.value;
        const selectedMonster = monsterDropdown.value;

        // Update iframe src based on selected family and monster
        const iframeSrc = selectedMonster
            ? `/monster/${selectedMonster}`
            : selectedFamily
            ? `/monster/${selectedFamily}`
            : "about:blank";

        iframe.src = iframeSrc;
    }
});
