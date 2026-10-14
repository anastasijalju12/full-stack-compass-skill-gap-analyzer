document.addEventListener("DOMContentLoaded", function () {
    const careerSearchInput = document.getElementById("careerSearchInput");
    const careerSearchButton = document.getElementById("careerSearchButton");
    const careerSortSelect = document.getElementById("careerSortSelect");
    const careersRow = document.getElementById("careersRow");

    if (!careerSearchInput || !careerSearchButton || !careerSortSelect || !careersRow) {
        return;
    }

    const originalCareerCards = Array.from(document.querySelectorAll(".career-item"));

    function filterCareers() {
        const searchValue = careerSearchInput.value.toLowerCase().trim();

        originalCareerCards.forEach(function (card) {
            const cardText = card.textContent.toLowerCase();

            if (cardText.includes(searchValue)) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        });
    }

    function sortCareers() {
        const sortValue = careerSortSelect.value;

        let cards = Array.from(document.querySelectorAll(".career-item"));

        cards.sort(function (a, b) {
            const titleA = a.dataset.title.toLowerCase();
            const titleB = b.dataset.title.toLowerCase();

            if (sortValue === "titleAsc") {
                return titleA.localeCompare(titleB);
            }

            if (sortValue === "titleDesc") {
                return titleB.localeCompare(titleA);
            }

            return 0;
        });

        if (sortValue === "default") {
            cards = originalCareerCards;
        }

        cards.forEach(function (card) {
            careersRow.appendChild(card);
        });
    }

    function loadFavoriteCareers() {
        const favoriteCheckboxes = document.querySelectorAll(".favoriteCheckbox");

        favoriteCheckboxes.forEach(function (checkbox) {
            const careerId = checkbox.dataset.careerId;
            const storageKey = "favoriteCareer_" + careerId;

            if (localStorage.getItem(storageKey) === "true") {
                checkbox.checked = true;
            }

            checkbox.addEventListener("change", function () {
                localStorage.setItem(storageKey, checkbox.checked);
            });
        });
    }

    careerSearchButton.addEventListener("click", filterCareers);

    careerSearchInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            filterCareers();
        }
    });

    careerSearchInput.addEventListener("input", filterCareers);

    careerSortSelect.addEventListener("change", function () {
        sortCareers();
        filterCareers();
    });

    loadFavoriteCareers();
});