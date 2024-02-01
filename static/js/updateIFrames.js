function updateIframes(familyDropdown, monsterDropdown) {
    const selectedFamily = familyDropdown.value;
    const selectedMonster = monsterDropdown.value;

    const monsterIframeSrc = selectedMonster
        ? `/monster/${selectedMonster}`
        : selectedFamily
            ? `/monster/${selectedFamily}`
            : "about:blank";

    const breedingIframeSrc = selectedMonster
        ? `/get_breeding_combinations?monster=${selectedMonster}`
        : "about:blank";

    updateIframeSrc("monsterIframe", monsterIframeSrc);
    updateIframeSrc("breedingIframe", breedingIframeSrc);
}

function updateIframeSrc(iframeId, src) {
    const iframe = document.getElementById(iframeId);
    iframe.src = src;
}

// Usage example:
updateIframes(familyDropdown, monsterDropdown);
