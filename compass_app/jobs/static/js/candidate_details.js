console.log("Loaded candidate_details.js");

document.addEventListener("submit", function (event) {
    const form = event.target.closest(".status-change-form");

    if (!form) {
        return;
    }

    event.preventDefault();

    const clickedButton = event.submitter;

    if (!clickedButton) {
        return;
    }

    clickedButton.disabled = true;
    clickedButton.classList.add("is-loading");

    const formData = new FormData(form);
    formData.append(clickedButton.name, clickedButton.value);

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "same-origin"
    })
        .then(response => response.json())
        .then(data => {
            console.log("Server response:", data);

            if (!data.ok) {
                return;
            }

            const adId = form.dataset.adId;
            const applicationId = form.dataset.applicationId;

            console.log("adId:", adId);
            console.log("applicationId:", applicationId);
            console.log("new_status:", data.new_status);
            console.log("new_status_display:", data.new_status_display);

            const statusSpan = document.getElementById(
                "applicationStatus-" + adId + "-" + applicationId
            );

            console.log("statusSpan:", statusSpan);

            if (statusSpan) {
                statusSpan.innerText = data.new_status_display || data.new_status;
            }

            const message = document.getElementById(
                "statusMessage-" + adId + "-" + applicationId
            );

            console.log("message:", message);

            if (message) {
                message.innerText = data.message;
                message.classList.add("visible");

                setTimeout(function () {
                    message.classList.remove("visible");
                }, 2500);
            }

            form.querySelectorAll(".status-button-group").forEach(group => {
                group.classList.remove("active");
            });

            const newButtonGroup = form.querySelector(
                '[data-status-group="' + data.new_status + '"]'
            );

            console.log("newButtonGroup:", newButtonGroup);

            if (newButtonGroup) {
                newButtonGroup.classList.add("active");
            }

            const applicationItem = document.getElementById(
                "applicationItem-" + adId + "-" + applicationId
            );

            const targetList = document.querySelector(
                '#modalOverlayOAC-' + adId + ' [data-status-list="' + data.new_status + '"]'
            );

            console.log("applicationItem:", applicationItem);
            console.log("targetList:", targetList);

            if (applicationItem && targetList) {
                const oldList = applicationItem.closest(".dropdown-list");

                const emptyItemInTarget = targetList.querySelector(".empty-candidates");

                if (emptyItemInTarget) {
                    emptyItemInTarget.remove();
                }

                targetList.appendChild(applicationItem);

                const targetDropdown = targetList.closest(".dropdown-container");

                if (targetDropdown) {
                    targetDropdown.classList.add("active");
                }

                if (oldList && oldList !== targetList) {
                    const hasRealCandidates = oldList.querySelector("li:not(.empty-candidates)");

                    if (!hasRealCandidates) {
                        const emptyLi = document.createElement("li");
                        emptyLi.classList.add("empty-candidates");

                        const oldStatus = oldList.dataset.statusList;

                        if (oldStatus === "accepted") {
                            emptyLi.innerText = "There are currently no accepted candidates.";
                        } else if (oldStatus === "active") {
                            emptyLi.innerText = "There are currently no candidates under review.";
                        } else if (oldStatus === "denied") {
                            emptyLi.innerText = "There are currently no rejected candidates.";
                        } else {
                            emptyLi.innerText = "There are currently no candidates.";
                        }

                        oldList.appendChild(emptyLi);
                    }
                }
            }
        })
        .catch(error => {
            console.log("Error:", error);
        })
        .finally(() => {
            clickedButton.disabled = false;
            clickedButton.classList.remove("is-loading");
        });
});

function getCsrfToken() {
    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");

    if (csrfInput) {
        return csrfInput.value;
    }

    return "";
}

function toggleFavoriteCandidate(button) {
    const userId = button.dataset.userId;
    const jobAdId = button.dataset.jobAdId;
    const toggleUrl = button.dataset.toggleUrl;

    console.log("Star clicked:", userId, jobAdId, toggleUrl);
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("job_ad_id", jobAdId);

    fetch(toggleUrl, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCsrfToken(),
            "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "same-origin"
    })
    .then(function (response) {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(function (data) {
        console.log("Django view response:", data);

        if (!data.ok) {
            console.log("Request failed:", data.error);
            return;
        }

        if (data.is_favorite) {
            button.classList.add("favorite-candidate-btn--active");
        } else {
            button.classList.remove("favorite-candidate-btn--active");
        }

        updateFavoriteIndicators(data.user_id, data.job_ad_id, data.is_favorite);
    })
    .catch(function (error) {
        console.log("Fetch error:", error);
    });
}
function updateFavoriteIndicators(userId, jobAdId, isFavorite) {
    const indicators = document.querySelectorAll(
        '[data-favorite-user-id="' + userId + '"][data-favorite-job-ad-id="' + jobAdId + '"]'
    );

    indicators.forEach(function (indicator) {
        if (isFavorite) {
            indicator.classList.remove("candidate-favorite-indicator--hidden");
        } else {
            indicator.classList.add("candidate-favorite-indicator--hidden");
        }
    });
}