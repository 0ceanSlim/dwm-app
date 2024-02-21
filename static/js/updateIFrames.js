function updateIframes() {
    const selectedMonster = monsterDropdown.value;

    // Update breedingIframe src based on the selected monster
    const breedingIframeSrc = selectedMonster
        ? `/breed?monster=${selectedMonster}`
        : "about:blank";

    breedingIframe.src = breedingIframeSrc;
}