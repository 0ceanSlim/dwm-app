function updateBreedingUsage() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Fetch data from the API
    fetch(`/api/breeding/usage/${selectedMonster}`)
      .then(response => response.json())
      .then(data => {
        // Update the HTML with the list of offspring monsters
        renderOffspringList(data.used_in);
      })
      .catch(error => console.error('Error fetching data:', error));
  }

  function renderOffspringList(usageData) {
    var offspringContainer = document.getElementById("offspringContainer");

    // Clear previous HTML content
    offspringContainer.innerHTML = "<h2 class='text-xl font-bold'>Used to Breed: </h2><ul class='list-disc'>";

    // Create and append HTML for each offspring
    usageData.forEach(item => {
      var offspringHTML = `<li class='font-bold marker:text-slate-400 text-purple-300'>
                            ${item.offspring}   
                            </li>
                            `;
      offspringContainer.innerHTML += offspringHTML;
    });

    // Close the unordered list
    offspringContainer.innerHTML += "</ul>";
}