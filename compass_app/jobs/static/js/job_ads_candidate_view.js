function closeApplyForJobForm() {
    document.getElementById("ApplyForJobForm").style.display = "none";
}

function openApplyForJobForm(button) {
    const adId = button.dataset.adId;
    const adName = button.dataset.adName;
    const companyName = button.dataset.companyName;

    document.getElementById("applicationAdId").value = adId;
    document.getElementById("selectedJobTitle").innerText = adName;
    document.getElementById("selectedCompany").innerText = companyName;

    document.getElementById("ApplyForJobForm").style.display = "flex";
}

document.addEventListener("DOMContentLoaded", function () {
    const jobSearchInput = document.getElementById("jobSearchInput");
    const jobSearchButton = document.getElementById("jobSearchButton");
    const jobSortSelect = document.getElementById("jobSortSelect");
    const jobsRow = document.getElementById("jobsRow");

    if (!jobSearchInput || !jobSearchButton || !jobSortSelect || !jobsRow) {
        return;
    }

    const originalJobCards = Array.from(document.querySelectorAll(".job-item"));

    function filterJobs() {
        const searchValue = jobSearchInput.value.toLowerCase().trim();

        originalJobCards.forEach(function (card) {
            const cardText = card.textContent.toLowerCase();

            if (cardText.includes(searchValue)) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        });
    }

    function sortJobs() {
        const sortValue = jobSortSelect.value;

        let cards = Array.from(document.querySelectorAll(".job-item"));

        cards.sort(function (a, b) {
            const titleA = a.dataset.title.toLowerCase();
            const titleB = b.dataset.title.toLowerCase();

            const deadlineA = new Date(a.dataset.deadline);
            const deadlineB = new Date(b.dataset.deadline);

            if (sortValue === "titleAsc") {
                return titleA.localeCompare(titleB);
            }

            if (sortValue === "titleDesc") {
                return titleB.localeCompare(titleA);
            }

            if (sortValue === "deadlineAsc") {
                return deadlineA - deadlineB;
            }

            if (sortValue === "deadlineDesc") {
                return deadlineB - deadlineA;
            }

            return 0;
        });

        if (sortValue === "default") {
            cards = originalJobCards;
        }

        cards.forEach(function (card) {
            jobsRow.appendChild(card);
        });
    }

    jobSearchButton.addEventListener("click", filterJobs);

    jobSearchInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            filterJobs();
        }
    });

    jobSearchInput.addEventListener("input", filterJobs);

    jobSortSelect.addEventListener("change", function () {
        sortJobs();
        filterJobs();
    });
});