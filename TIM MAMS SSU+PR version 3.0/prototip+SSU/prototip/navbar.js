// Linkovi za ulogovanog korisnika
const loggedInLinks = `
    <li class="nav-item"><a href="HomeUser.html" class="nav-link">Početna</a></li>
    <li class="nav-item"><a href="careers.html" class="nav-link">Zanimanja</a></li>
    <li class="nav-item"><a href="jobAds.html" class="nav-link">Oglasi</a></li>
    <li class="nav-item"><a href="skillMatch.html" class="nav-link">Analiza</a></li>
    <li class="nav-item"><a href="favourites.html" class="nav-link">Omiljeno</a></li>
    <li class="nav-item"><a href="companies.html" class="nav-link">Kompanije</a></li>
    <li class="nav-item"><a href="aboutUs.html" class="nav-link">O nama</a></li>
    <li class="nav-item dropdown">
        <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Avatar</a>
        <ul class="dropdown-menu dropdown-menu-end">
            <li><a href="psiIndex.html" class="dropdown-item">Moj profil</a></li>
            <li><a href="index.html" class="dropdown-item" id="logoutBtn">Odjava</a></li>
        </ul>
    </li>
`;

// Linkovi za gosta
const guestLinks = `
    <li class="nav-item"><a href="index.html" class="nav-link">Početna</a></li>
    <li class="nav-item"><a href="careers.html" class="nav-link">Zanimanja</a></li>
    <li class="nav-item"><a href="jobAds.html" class="nav-link">Oglasi</a></li>
    <li class="nav-item"><a href="Login.html" class="nav-link">Analiza</a></li>
    <li class="nav-item"><a href="Login.html" class="nav-link">Omiljeno</a></li>
    <li class="nav-item"><a href="companies.html" class="nav-link">Kompanije</a></li>
    <li class="nav-item"><a href="aboutUs.html" class="nav-link">O nama</a></li>
    <li class="nav-item"><a href="Login.html" class="nav-link">Prijava</a></li>
`;

// Učitaj navbar HTML, pa popuni linkove
fetch('navbar.html')
    .then(res => res.text())
    .then(html => {
        // Ubaci navbar na vrh stranice
        document.body.insertAdjacentHTML('afterbegin', html);

        // Provjeri da li je korisnik ulogovan
        const isLoggedIn = localStorage.getItem('loggedIn') === 'true';

        document.getElementById('navLinks').innerHTML = 
            isLoggedIn ? loggedInLinks : guestLinks;

        // Logout dugme
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('loggedIn');
                window.location.href = 'index.html';
            });
        }
    });