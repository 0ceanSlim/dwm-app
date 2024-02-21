function updateMonsterStats() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Make an API request to get the stats for the selected monster
    fetch(`/api/monster/stats?monster=${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Update the HTML content with the monster stats
        var statsContainer = document.getElementById("monsterStatsContainer");
        statsContainer.innerHTML = `<p>Max Level: ${data["Max Level"]}</p>
                                    <p>Experience: ${data.Experience}</p>
                                    <p>Health Points: ${data["Health Points"]}</p>
                                    <p>Attack: ${data.Attack}</p>
                                    <p>Defense: ${data.Defense}</p>
                                    <p>Agility: ${data.Agility}</p>
                                   <p>Intelligence: ${data.Intelligence}</p>
                                   `;
      })
      .catch(error => {
        console.error("Error fetching monster stats:", error);
      });
  }