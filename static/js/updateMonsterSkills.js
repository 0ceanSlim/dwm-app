function updateMonsterSkills() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Make an API request to get the stats for the selected monster
    fetch(`/api/monster/stats?monster=${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Update the HTML content with the monster skills
        var skillsContainer = document.getElementById("monsterSkillsContainer");
        skillsContainer.innerHTML = `<h2>Skills: ${data.Skills}</h2>`;
      })
      .catch(error => {
        console.error("Error fetching monster skills:", error);
      });
  }