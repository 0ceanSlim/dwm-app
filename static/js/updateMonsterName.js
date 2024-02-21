function updateMonsterName() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Make an API request to get the stats for the selected monster
    fetch(`/api/monster/stats?monster=${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Update the HTML content with the monster name
        var nameContainer = document.getElementById("monsterNameContainer");
        nameContainer.innerHTML = `<h2 class="text-3xl font-bold">${data.name}</h2>`;
      })
      .catch(error => {
        console.error("Error fetching monster name:", error);
      });
  }