document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");

    // Initialize dropdowns and iframes
    updateMonstersDropdown();

    // Fetch families data from the server
    fetch("/get_families")
        .then(response => response.json())
        .then(data => {
            populateDropdown(familyDropdown, data);
        })
        .catch(error => console.error("Error fetching families:", error));

    familyDropdown.addEventListener("change", function () {
        updateMonstersDropdown();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframes();
    });


});
