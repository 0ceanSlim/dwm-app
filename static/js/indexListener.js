document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");
    //const parent = document.getElementById("parent")

    // Implementing Family Icon Grid in place of family dropdown
    //const familyGrid = document.getElementById("familyGrid")

    // Initialize dropdowns
    updateMonstersDropdownByFamily();
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
        updateMonstersDropdownByFamily();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframes();
    });

    // Listener for a click on the one of the family icons
    //familyGrid.addEventListener("click", function() {
    //    updateMonsterGrid(); // Need a function for this too...
    //});

    // Listener for a click on a breeding parent
    //parent.addEventListener("click", function() {
    //    updateMonstersDropdownBySelected();
    //    updateIFrames();  
    //});

});
