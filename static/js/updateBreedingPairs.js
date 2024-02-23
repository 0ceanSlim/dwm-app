function updateBreedingPairs() {
    // Get the selected monster from the dropdown
    var selectedMonster = document.getElementById("monsterDropdown").value;

    // Fetch data from the API based on the selected monster
    fetch(`/api/breeding/pairs/${selectedMonster}`)
        .then(response => response.json())
        .then(data => {
            // Update the HTML element with breeding pairs
            var breedingPairsContainer = document.getElementById("breedingPairsContainer");
            breedingPairsContainer.innerHTML = `
            <div class='text-center '>
            <h3 class='text-xl font-bold mb-0.5'>Breeding Pairs:</h3>
                <div class='text-xs mb-2 flex justify-center'>
                    (<p class='text-red-300'>base</p> &nbsp;+&nbsp; <p class='text-blue-300'>mate</p>)
                </div>
            </div>
            `;

            if (data.breeding_pairs.length > 0) {
                var pairsList = document.createElement("ul");
                pairsList.classList.add('list-disc', 'ml-4');

                data.breeding_pairs.forEach(pair => {
                    var listItem = document.createElement("li");

                    // Style "base" text
                    var baseText = document.createElement("span");
                    baseText.textContent = pair.base;
                    baseText.classList.add('font-bold', 'text-red-300');

                    // Style "mate" text
                    var mateText = document.createElement("span");
                    mateText.textContent = pair.mate;
                    mateText.classList.add('font-bold', 'text-blue-300');

                    // Combine "base" and "mate" texts in the list item
                    listItem.appendChild(baseText);
                    listItem.appendChild(document.createTextNode(" + "));
                    listItem.appendChild(mateText);

                    pairsList.appendChild(listItem);
                });

                breedingPairsContainer.appendChild(pairsList);
            } else {
                breedingPairsContainer.innerHTML += "<p class='text-red-500'>No breeding pairs found for " + selectedMonster + ".</p>";
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}