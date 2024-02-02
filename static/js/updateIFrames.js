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