function showCandidatesModalOAC(adId) {
    const overlay = document.getElementById('modalOverlayOAC-' + adId);

    if (!overlay) {
        console.log('Modal not found:', adId);
        return;
    }

    overlay.style.display = 'flex';
}

function closeCandidatesModalOAC(adId) {
    const overlay = document.getElementById('modalOverlayOAC-'+ adId);
     const pair = document.getElementById('modalPair-' + adId);
    if (!overlay) {
        return;
    }
    overlay.style.display = 'none';

    if (pair) {
        pair.classList.remove('details-open');
    }

     document.querySelectorAll('#candidateDetailsPanel-' + adId + ' .candidate-details-content')
        .forEach(item => {
            item.classList.remove('active');
        });
}

function toggleDropdownOAC(element) {
    const dropdown = element.closest('.dropdown-container');
    dropdown.classList.toggle('active');
}

function showCandidateDetails(adId, candId) {
    const pair = document.getElementById('modalPair-' + adId);
    const panel = document.getElementById('candidateDetailsPanel-' + adId);

    if (!pair || !panel) {
        console.log('Details panel not found.');
        return;
    }

    panel.querySelectorAll('.candidate-details-content').forEach(item => {
        item.classList.remove('active');
    });

    const selectedDetails = document.getElementById('candidateDetails-' + adId + '-' + candId);

    if (!selectedDetails) {
        console.log('Candidate details not found.', candId);
        return;
    }

    selectedDetails.classList.add('active');
    pair.classList.add('details-open');
}

function closeCandidateDetails(adId) {
    const pair = document.getElementById('modalPair-' + adId);
    const panel = document.getElementById('candidateDetailsPanel-' + adId);

    if (pair) {
        pair.classList.remove('details-open');
    }

    if (panel) {
        panel.querySelectorAll('.candidate-details-content').forEach(item => {
            item.classList.remove('active');
        });
    }
}


function initCompanyAdsSearchAndSort() {
    const companyAdSearchInput = document.getElementById("companyAdSearchInput");
    const companyAdSearchButton = document.getElementById("companyAdSearchButton");
    const companyAdSortSelect = document.getElementById("companyAdSortSelect");
    const companyAdsRow = document.getElementById("companyAdsRow");

    if (!companyAdSearchInput || !companyAdSearchButton || !companyAdSortSelect || !companyAdsRow) {
        console.log("Search/sort not initialized - an element was not found.");
        console.log("input:", companyAdSearchInput);
        console.log("button:", companyAdSearchButton);
        console.log("select:", companyAdSortSelect);
        console.log("row:", companyAdsRow);
        return;
    }

    const originalCompanyAdCards = Array.from(
        companyAdsRow.querySelectorAll(".company-ad-item")
    );

    function filterCompanyAds() {
    const searchValue = companyAdSearchInput.value.toLowerCase().trim();

    const cards = Array.from(companyAdsRow.querySelectorAll(".company-ad-item"));

    cards.forEach(function (card) {
        const title = card.dataset.title.toLowerCase();
        const status = card.dataset.status.toLowerCase();

        const cardText = card.innerText.toLowerCase();

        if (
            title.includes(searchValue) ||
            status.includes(searchValue) ||
            cardText.includes(searchValue)
        ) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

    function sortCompanyAds() {
        const sortValue = companyAdSortSelect.value;

        let cards = Array.from(
            companyAdsRow.querySelectorAll(".company-ad-item")
        );

        cards.sort(function (a, b) {
            const titleA = (a.dataset.title || "").toLowerCase();
            const titleB = (b.dataset.title || "").toLowerCase();

            const statusA = (a.dataset.status || "").toLowerCase();
            const statusB = (b.dataset.status || "").toLowerCase();

            const deadlineA = a.dataset.deadline || "";
            const deadlineB = b.dataset.deadline || "";

            if (sortValue === "titleAsc") {
                return titleA.localeCompare(titleB);
            }

            if (sortValue === "titleDesc") {
                return titleB.localeCompare(titleA);
            }

            if (sortValue === "deadlineAsc") {
                return deadlineA.localeCompare(deadlineB);
            }

            if (sortValue === "deadlineDesc") {
                return deadlineB.localeCompare(deadlineA);
            }

            if (sortValue === "statusAsc") {
                return statusA.localeCompare(statusB);
            }

            if (sortValue === "statusDesc") {
                return statusB.localeCompare(statusA);
            }

            return 0;
        });

        if (sortValue === "default") {
            cards = originalCompanyAdCards;
        }

        cards.forEach(function (card) {
            companyAdsRow.appendChild(card);
        });
    }

    companyAdSearchButton.addEventListener("click", filterCompanyAds);

    companyAdSearchInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            filterCompanyAds();
        }
    });

    companyAdSearchInput.addEventListener("input", filterCompanyAds);

    companyAdSortSelect.addEventListener("change", function () {
        sortCompanyAds();
        filterCompanyAds();
    });

    console.log("Company ads search/sort initialized.");
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCompanyAdsSearchAndSort);
} else {
    initCompanyAdsSearchAndSort();
}

function openDeleteJobAdDialog(button) {
    const deleteUrl = button.dataset.deleteUrl;
    const adName = button.dataset.adName;

    const dialog = document.getElementById("DeleteJobAdDialog");
    const form = document.getElementById("deleteJobAdForm");
    const nameSpan = document.getElementById("deleteJobAdName");

    form.action = deleteUrl;
    nameSpan.innerText = adName;

    dialog.style.display = "flex";
}

function closeDeleteJobAdDialog() {
    document.getElementById("DeleteJobAdDialog").style.display = "none";
}

function openEditJobAdForm(button) {
    const formModal = document.getElementById("JobAdForm");
    const form = document.getElementById("jobAdForm");

    const title = document.getElementById("jobAdFormTitle");
    const submitButton = document.getElementById("jobAdFormSubmitButton");

    form.action = button.dataset.updateUrl;

    title.innerText = "Edit job ad";
    submitButton.innerText = "Save changes";

    setFormFieldValue("id_name", button.dataset.name);
    setFormFieldValue("id_type", button.dataset.type);
    setFormFieldValue("id_location", button.dataset.location);
    setFormFieldValue("id_application_deadline", button.dataset.deadline);
    setFormFieldValue("id_status", button.dataset.status);
    setFormFieldValue("id_description", button.dataset.description);

    formModal.style.display = "flex";
}

function openAddJobAdForm() {
    const formModal = document.getElementById("JobAdForm");
    const form = document.getElementById("jobAdForm");

    const title = document.getElementById("jobAdFormTitle");
    const submitButton = document.getElementById("jobAdFormSubmitButton");

    form.action = form.dataset.addUrl;
    form.reset();

    title.innerText = "New job ad";
    submitButton.innerText = "Post job ad";

    formModal.style.display = "flex";
}

function closeAddJobAdForm() {
    document.getElementById("JobAdForm").style.display = "none";
}

function setFormFieldValue(fieldId, value) {
    const field = document.getElementById(fieldId);

    if (!field) {
        console.log("Field not found:", fieldId);
        return;
    }

    field.value = value || "";
}