document.addEventListener("DOMContentLoaded", function () {
    const familyDropdown = document.getElementById("familyDropdown");
    const monsterDropdown = document.getElementById("monsterDropdown");
    const monsterIframe = document.getElementById("monsterIframe");
    const breedingIframe = document.getElementById("breedingIframe");

    // Initialize dropdowns and iframes
    updateMonstersDropdown();
    updateIframes();

    // Fetch families data from the server
    fetch("/get_families")
        .then(response => response.json())
        .then(data => {
            populateDropdown(familyDropdown, data);
            updateMonstersDropdown();
            updateIframes();
        })
        .catch(error => console.error("Error fetching families:", error));

    familyDropdown.addEventListener("change", function () {
        updateMonstersDropdown();
        updateIframes();
    });

    monsterDropdown.addEventListener("change", function () {
        updateIframes();
    });

    function populateDropdown(dropdown, data) {
        // Clear existing options
        dropdown.innerHTML = '<option value="">All</option>';

        // Populate dropdown options
        data.forEach(item => {
            const option = document.createElement("option");
            option.value = item;
            option.text = item;
            dropdown.appendChild(option);
        });
    }

    function updateMonstersDropdown() {
        const selectedFamily = familyDropdown.value;

        // Fetch monsters data from the server based on the selected family
        fetch(`/get_monsters?family=${selectedFamily}`)
            .then(response => response.json())
            .then(data => populateDropdown(monsterDropdown, data))
            .catch(error => console.error("Error fetching monsters:", error));
    }

    function updateIframes() {
        const selectedFamily = familyDropdown.value;
        const selectedMonster = monsterDropdown.value;

        // Update monsterIframe src based on selected family and monster
        const monsterIframeSrc = selectedMonster
            ? `/monster/${selectedMonster}`
            : selectedFamily
            ? `/monster/${selectedFamily}`
            : "about:blank";

        monsterIframe.src = monsterIframeSrc;

        // Update breedingIframe src based on the selected monster
        const breedingIframeSrc = selectedMonster
            ? `/get_breeding_combinations?monster=${selectedMonster}`
            : "about:blank";

        breedingIframe.src = breedingIframeSrc;
    }

//I was trying to get rid of the scroll bars but h-auto/fit wasn't working
// This works to resize but still leaves some scrollbar
//to-do:fix

    // Function to resize iframe
    //function resizeIframe(iframe) {
    //    const body = iframe.contentDocument.body;
    //    const html = iframe.contentDocument.documentElement;
    //
    //    const height = Math.max(
    //        body.scrollHeight,
    //        body.offsetHeight,
    //        html.clientHeight,
    //        html.scrollHeight,
    //        html.offsetHeight
    //    );
    //
    //    iframe.style.height = height + "px";
    //}
    

    // Add event listeners for iframe load
    monsterIframe.addEventListener("load", function () {
        resizeIframe(monsterIframe);
    });

    breedingIframe.addEventListener("load", function () {
        resizeIframe(breedingIframe);
    });
});
