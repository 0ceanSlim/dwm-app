function updateMonsterFamily() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;
  
    // Make an API request to get the stats for the selected monster
    fetch(`/api/monster/stats?monster=${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Function to capitalize the first letter
        function capitalizeFirstLetter(string) {
          return string.charAt(0).toUpperCase() + string.slice(1);
        }
  
        // Update the HTML content with the capitalized monster family
        var familyContainer = document.getElementById("monsterFamilyContainer");
        familyContainer.innerHTML = `<h2>Family: ${capitalizeFirstLetter(data.Family)}</h2>`;
      })
      .catch(error => {
        console.error("Error fetching monster family:", error);
      });
  }
  