// static/js/breeding.js

function breed() {
    var parent1 = document.getElementById("parent1").value;
    var parent2 = document.getElementById("parent2").value;

    // Make an AJAX request to your Flask route for breeding logic
    // You can use fetch or another library for AJAX requests

    // For demonstration purposes, we'll assume you have a Flask route named /breed
    fetch(`/breed?parent1=${parent1}&parent2=${parent2}`)
        .then(response => response.json())
        .then(data => {
            // Display the breeding result in the breedingResult div
            var breedingResultDiv = document.getElementById("breedingResult");
            breedingResultDiv.innerHTML = `<p>Breeding Result: ${data.result}</p>`;
        })
        .catch(error => console.error('Error:', error));
}
