function updateMonsterStats() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Make an API request to get the stats for the selected monster
    fetch(`/api/monster/stats?monster=${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Update the HTML content with the monster stats
        var statsContainer = document.getElementById("monsterStatsContainer");
        statsContainer.innerHTML = `<div class="font-bold text-center text-xl">Stats</div>
                                    <div class="grid grid-cols-4 mt-1 mb-1 gap-x-2">
                                    <p class="font-bold">Max Level:                                 </p><p class="font-bold text-violet-500">${data["Max Level"]}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EXP:   </p><p class="font-bold text-violet-500">${data.Experience}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;HP:&nbsp;          </p><p class="font-bold text-violet-500">${data["Health Points"]}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ATK:   </p><p class="font-bold text-violet-500">${data.Attack}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;MP:&nbsp;          </p><p class="font-bold text-violet-500">${data["Mana Points"]}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DEF:   </p><p class="font-bold text-violet-500">${data.Defense}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;AGL:               </p><p class="font-bold text-violet-500">${data.Agility}</p>
                                    <p class="font-bold">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;INT:   </p><p class="font-bold text-violet-500">${data.Intelligence}</p>
                                    `;
      })
      .catch(error => {
        console.error("Error fetching monster stats:", error);
      });
  }