function updateMonsterLocation() {
  // Get the selected monster from the dropdown
  var selectedMonster = document.getElementById("monsterDropdown").value;

  // Make an API request to get the stats for the selected monster
  fetch(`/api/monster/stats?monster=${selectedMonster}`)
    .then(response => response.json())
    .then(data => {
      // Check if location is not null before updating HTML content
      if (data.Location !== null) {
        // Update the HTML content with the monster location
        var locationContainer = document.getElementById("monsterLocationContainer");
        locationContainer.innerHTML = `<h2>Known Locations:<br>${data.Location}</h2>`;
      } else {
        // Handle the case when location is null (optional)
        var locationContainer = document.getElementById("monsterLocationContainer");
        locationContainer.innerHTML = "";  // Clear the content or provide a default message
      }
    })
    .catch(error => {
      console.error("Error fetching monster location:", error);
    });
}
