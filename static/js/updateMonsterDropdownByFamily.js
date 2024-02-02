function updateMonsterDropdownByFamily() {
    const selectedFamily = familyDropdown.value;

    // Fetch monsters data from the server based on the selected family
    fetch(`/get_monsters?family=${selectedFamily}`)
        .then(response => response.json())
        .then(data => populateDropdown(monsterDropdown, data))
        .catch(error => console.error("Error fetching monsters:", error));
}
