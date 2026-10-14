document.addEventListener("DOMContentLoaded", function () {
    const companySearchInput = document.getElementById("companySearchInput");
    const companySearchButton = document.getElementById("companySearchButton");
    const companySortSelect = document.getElementById("companySortSelect");
    const companiesRow = document.getElementById("companiesRow");

    if (!companySearchInput || !companySearchButton || !companySortSelect || !companiesRow) {
        return;
    }

    const originalCompanyCards = Array.from(
        companiesRow.querySelectorAll(".company-item")
    );

    function filterCompanies() {
        const searchValue = companySearchInput.value.toLowerCase().trim();

        const cards = Array.from(
            companiesRow.querySelectorAll(".company-item")
        );

        cards.forEach(function (card) {
            const cardText = card.innerText.toLowerCase();

            if (cardText.includes(searchValue)) {
                card.classList.remove("company-item--hidden");
            } else {
                card.classList.add("company-item--hidden");
            }
        });
    }

    function sortCompanies() {
        const sortValue = companySortSelect.value;

        let cards = Array.from(
            companiesRow.querySelectorAll(".company-item")
        );

        cards.sort(function (a, b) {
            const nameA = (a.dataset.name || "").toLowerCase();
            const nameB = (b.dataset.name || "").toLowerCase();

            const industryA = (a.dataset.industry || "").toLowerCase();
            const industryB = (b.dataset.industry || "").toLowerCase();

            if (sortValue === "nameAsc") {
                return nameA.localeCompare(nameB);
            }

            if (sortValue === "nameDesc") {
                return nameB.localeCompare(nameA);
            }

            if (sortValue === "industryAsc") {
                return industryA.localeCompare(industryB);
            }

            if (sortValue === "industryDesc") {
                return industryB.localeCompare(industryA);
            }

            return 0;
        });

        if (sortValue === "default") {
            cards = originalCompanyCards;
        }

        cards.forEach(function (card) {
            companiesRow.appendChild(card);
        });
    }

    companySearchButton.addEventListener("click", filterCompanies);

    companySearchInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            filterCompanies();
        }
    });

    companySearchInput.addEventListener("input", filterCompanies);

    companySortSelect.addEventListener("change", function () {
        sortCompanies();
        filterCompanies();
    });
});

function toggleCompanyDescription(button) {
    const descriptionBox = button.closest(".company-card__description");

    if (!descriptionBox) {
        return;
    }

    descriptionBox.classList.toggle("company-card__description--expanded");

    if (descriptionBox.classList.contains("company-card__description--expanded")) {
        button.innerText = "View less";
    } else {
        button.innerText = "View more";
    }
}