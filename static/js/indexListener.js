document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");
    // Implementing Family Icon Grid in place of family dropdown
    //const familyGrid = document.getElementById("familyGrid")

    // Initialize dropdowns
    updateMonstersDropdown();
    // Initialize Family Grid();
    // populateFamilyGrid();

    // Fetch families data from the server and populate families dropdown
    fetch("/get_families")
        .then(response => response.json())
        .then(data => {
            populateDropdown(familyDropdown, data);
        })
        .catch(error => console.error("Error fetching families:", error));

    // Listeners for Dropdown Changes
    familyDropdown.addEventListener("change", function () {
        updateMonstersDropdown();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframes();
    });

    // Listener for a click on the one of the family icons
    //familyGrid.addEventListener("on click", function() {
    //    updateMonsterGrid(); // Need a function for this too...
    //});

});
