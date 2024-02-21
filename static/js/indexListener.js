document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");

    // Initialize dropdowns
    updateMonsterDropdownByFamily();

    // Fetch families data from the server and populate families dropdown
    fetch("/api/families")
        .then(response => response.json())
        .then(data => {
            populateDropdown(familyDropdown, data);
        })
        .catch(error => console.error("Error fetching families:", error));

    // Listeners for Dropdown Changes
    familyDropdown.addEventListener("change", function () {
        updateMonsterDropdownByFamily();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframes();
    });

    monsterDropdown.addEventListener("change", function () {
        updateMonsterStats();
    });
});
