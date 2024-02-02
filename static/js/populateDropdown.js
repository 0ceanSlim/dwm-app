function populateDropdown(dropdown, data) {
    dropdown.innerHTML = '<option value="">All</option>';
    
    data.forEach(item => {
        const option = document.createElement("option");
        option.value = item;
        option.text = item;
        dropdown.appendChild(option);
    });
}
