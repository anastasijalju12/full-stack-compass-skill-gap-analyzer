const selectedSkills = {};

const LEVEL_LABELS = {
    1: 'Beginner',
    2: 'Basic',
    3: 'Intermediate',
    4: 'Advanced',
    5: 'Expert'
};

function toggleSkill(skillElement) {
    const id   = skillElement.dataset.id;
    const name = skillElement.dataset.name;

    if (skillElement.classList.contains('selected')) {
        skillElement.classList.remove('selected');
        delete selectedSkills[id];
    } else {
        skillElement.classList.add('selected');
        selectedSkills[id] = { name: name, level: 1 };
    }

    rebuildSliders();
    

    const anySelected = Object.keys(selectedSkills).length > 0;
    
    if(anySelected){
        document.getElementById('skill-levels-div').style.display='flex'
    }
    else{
        document.getElementById('skill-levels-div').style.display='none'
    }
    
    //document.getElementById('preview-div').style.display = 'none';
}

function rebuildSliders() {
    const container = document.getElementById('sliders-container');
    container.innerHTML = '';

    for (const [id, data] of Object.entries(selectedSkills)) {
        const div = document.createElement('div');
        div.className = 'd-flex align-items-center gap-4 mb-3';
        div.innerHTML = `
            <div class="slider-skill-name">${data.name}</div>
            <div class="flex-grow-1">
                <input 
                    type="range" 
                    class="form-range" 
                    min="1" max="5" 
                    value="${data.level}" 
                    oninput="updateLevel(this, '${id}')">
            </div>
            <div id="selected-id-${id}" class="slider-value">
                ${data.level}
            </div>
            <div id="selected-level-labels-${id}" class="slider-level-label">
                ${LEVEL_LABELS[data.level]}
            </div>
            <input type="hidden" name="skill-${id}" id="hidden-skill-${id}" value="${data.level}">
        `;
        container.appendChild(div);
    }
}

function updateLevel(input, id) {
    const val = parseInt(input.value);
    selectedSkills[id].level = val;

    document.getElementById('selected-id-' + id).textContent = val;
    document.getElementById('selected-level-labels-' + id).textContent = LEVEL_LABELS[val];
    document.getElementById('hidden-skill-' + id).value = val;
    
}

function toggleLearnSkills(elementId) {
    const section = document.getElementById('learn-skills-' + elementId);
    if (!section) return;

    section.style.display = section.style.display === 'none' ? 'block' : 'none';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function toggleFavourite(type, id, isFavorited) {
    const csrftoken = getCookie('csrftoken');

    fetch('/toggle-favourite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `type=${type}&id=${id}`
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.log('Failed to update favorite status.');
        }
    });
}

