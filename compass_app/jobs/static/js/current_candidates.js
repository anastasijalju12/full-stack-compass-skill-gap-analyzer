function showCandidatesModal() {
    const overlay = document.getElementById('modalOverlayCC');
    overlay.style.display = 'flex';
}

function closeCandidatesModal() {
    const overlay = document.getElementById('modalOverlayCC');
    overlay.style.display = 'none';
}

function toggleDropdown(element) {
    const dropdown = element.closest('.dropdown-container');
    dropdown.classList.toggle('active');
}
