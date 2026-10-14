-- =============================================
-- SEED DATA — full database (careers + job ads)
-- Project: Kompas, team MAMS
-- Author: Anastasija
-- Tables: skill, career, career_skill, resource,
--         career_project, company, job_ad, job_ad_skill
-- Note: file_path for career_project is just the
--       file name (no folder), since MEDIA_ROOT is
--       already set to the projects_for_careers
--       folder in settings.py
-- =============================================

USE kompas;

-- --- Clear existing data (order matters because of FK constraints) ---
DELETE FROM `application`;
DELETE FROM `administrator`;
DELETE FROM `user`;
DELETE FROM `job_ad_skill`;
DELETE FROM `job_ad`;
DELETE FROM `company`;
DELETE FROM `career_project`;
DELETE FROM `resource`;
DELETE FROM `career_skill`;
DELETE FROM `career`;
DELETE FROM `skill`;
-- =============================================
-- SKILL
-- =============================================
INSERT INTO `skill` (`id`, `name`, `description`) VALUES
(1,  'HTML',         'Markup language for structuring web pages'),
(2,  'CSS',          'Styling and layout for web pages'),
(3,  'JavaScript',   'Programming language for frontend and backend'),
(4,  'TypeScript',   'JavaScript with static typing'),
(5,  'React',        'JavaScript library for building UI components'),
(6,  'Node.js',      'JavaScript runtime for server-side programming'),
(7,  'Python',       'General-purpose language, popular in data science and backend development'),
(8,  'Django',       'Python web framework for rapid application development'),
(9,  'Java',         'Object-oriented programming language'),
(10, 'SQL',          'Language for managing relational databases'),
(11, 'MySQL',        'Relational database management system'),
(12, 'MongoDB',      'NoSQL database'),
(13, 'Git',          'Version control system for code'),
(14, 'Docker',       'Platform for containerizing applications'),
(15, 'Linux',        'Operating system commonly used on servers'),
(16, 'Figma',        'Tool for designing user interfaces'),
(17, 'Kotlin',       'Programming language for Android development'),
(18, 'React Native', 'Framework for mobile applications (iOS and Android)'),
(19, 'Excel',        'Tool for tabular data analysis'),
(20, 'C++',          'High-performance systems programming language');

-- =============================================
-- CAREER
-- =============================================
INSERT INTO `career` (`id`, `name`, `description`) VALUES
(1, 'Frontend Developer',
    'Builds the user interface of web applications using HTML, CSS and JavaScript.'),
(2, 'Backend Developer',
    'Develops server-side logic, databases and APIs for web and mobile applications.'),
(3, 'Web Developer',
    'Works on both frontend and backend — responsible for the entire web project, from interface to server.'),
(4, 'Web Designer',
    'Designs the visual look and user experience of web pages, from layout to typography.'),
(5, 'Mobile Developer',
    'Builds applications for Android and iOS platforms, either natively or with cross-platform solutions.'),
(6, 'Data Analyst',
    'Analyzes datasets and delivers business insights through visualizations and reports.'),
(7, 'DevOps Engineer',
    'Automates development and deployment processes; manages server infrastructure and CI/CD pipelines.');

-- =============================================
-- CAREER_SKILL
-- =============================================
INSERT INTO `career_skill` (`career_id`, `skill_id`, `required_level`, `weight`) VALUES
(1,  1, 4, 0.20),
(1,  2, 4, 0.20),
(1,  3, 4, 0.25),
(1,  5, 3, 0.20),
(1, 13, 2, 0.10),
(1, 16, 2, 0.05),
(2,  7, 4, 0.20),
(2,  8, 3, 0.20),
(2, 10, 4, 0.20),
(2, 11, 3, 0.15),
(2, 13, 3, 0.10),
(2, 14, 2, 0.10),
(2,  9, 2, 0.05),
(3,  1, 3, 0.15),
(3,  2, 3, 0.10),
(3,  3, 4, 0.25),
(3,  5, 3, 0.15),
(3,  6, 3, 0.15),
(3, 10, 2, 0.10),
(3, 13, 3, 0.10),
(4, 16, 5, 0.40),
(4,  2, 4, 0.30),
(4,  1, 3, 0.20),
(4,  3, 2, 0.10),
(5, 17, 4, 0.35),
(5,  9, 3, 0.20),
(5, 18, 3, 0.30),
(5, 13, 2, 0.15),
(6,  7, 3, 0.30),
(6, 10, 4, 0.35),
(6, 19, 4, 0.20),
(6, 12, 2, 0.15),
(7, 14, 4, 0.30),
(7, 15, 4, 0.30),
(7, 13, 4, 0.20),
(7,  7, 3, 0.15),
(7, 11, 2, 0.05);

-- =============================================
-- RESOURCE
-- =============================================
INSERT INTO `resource` (`skill_id`, `name`, `url`, `level`) VALUES
(1,  'MDN Web Docs – HTML basics',
     'https://developer.mozilla.org/en-US/docs/Web/HTML',                      'beginner'),
(1,  'freeCodeCamp – Responsive Web Design',
     'https://www.freecodecamp.org/learn/responsive-web-design/',              'beginner'),
(2,  'CSS-Tricks – complete guide to Grid and Flexbox',
     'https://css-tricks.com/snippets/css/complete-guide-grid/',               'intermediate'),
(2,  'Flexbox Froggy – learn through a game',
     'https://flexboxfroggy.com',                                              'beginner'),
(3,  'javascript.info – modern JS from the basics',
     'https://javascript.info',                                                'beginner'),
(3,  'The Odin Project – JavaScript course',
     'https://www.theodinproject.com/paths/full-stack-javascript',             'intermediate'),
(4,  'TypeScript official documentation',
     'https://www.typescriptlang.org/docs/',                                   'intermediate'),
(4,  'Total TypeScript – free course',
     'https://www.totaltypescript.com/tutorials',                              'beginner'),
(5,  'React official documentation',
     'https://react.dev',                                                      'intermediate'),
(5,  'Scrimba – Learn React for free',
     'https://scrimba.com/learn/learnreact',                                   'beginner'),
(7,  'Python.org – official documentation',
     'https://docs.python.org/3/',                                             'beginner'),
(7,  'Real Python – practical tutorials',
     'https://realpython.com',                                                 'intermediate'),
(8,  'Official Django documentation',
     'https://docs.djangoproject.com',                                         'intermediate'),
(8,  'Django Girls Tutorial',
     'https://tutorial.djangogirls.org',                                       'beginner'),
(10, 'SQLZoo – interactive SQL exercises',
     'https://sqlzoo.net',                                                     'beginner'),
(10, 'Mode SQL Tutorial',
     'https://mode.com/sql-tutorial/',                                         'intermediate'),
(11, 'MySQL official documentation',
     'https://dev.mysql.com/doc/',                                             'intermediate'),
(13, 'Pro Git book (free)',
     'https://git-scm.com/book/en/v2',                                        'beginner'),
(13, 'Learn Git Branching – visual',
     'https://learngitbranching.js.org',                                       'beginner'),
(14, 'Docker Getting Started',
     'https://docs.docker.com/get-started/',                                   'beginner'),
(14, 'Play with Docker – online sandbox',
     'https://labs.play-with-docker.com',                                      'intermediate'),
(15, 'The Linux Command Line (free book)',
     'https://linuxcommand.org/tlcl.php',                                      'beginner'),
(15, 'OverTheWire – Bandit (wargame for learning)',
     'https://overthewire.org/wargames/bandit/',                               'intermediate'),
(16, 'Figma Learn – official course',
     'https://help.figma.com/hc/en-us/articles/360038510773',                  'beginner'),
(16, 'Designcode.io – UI/UX with Figma',
     'https://designcode.io',                                                  'intermediate'),
(17, 'Kotlin Koans – interactive exercises',
     'https://kotlinlang.org/docs/koans.html',                                 'beginner'),
(17, 'Android Developers – Kotlin course',
     'https://developer.android.com/kotlin',                                   'intermediate'),
(18, 'React Native official documentation',
     'https://reactnative.dev/docs/getting-started',                           'beginner'),
(19, 'ExcelJet – formulas and tips',
     'https://exceljet.net',                                                   'intermediate'),
(19, 'Microsoft Excel – official support',
     'https://support.microsoft.com/en-us/excel',                             'beginner');

-- =============================================
-- CAREER_PROJECT
-- file_path is just the file name (no folder),
-- since MEDIA_ROOT is already set to the
-- projects_for_careers folder in settings.py
-- =============================================
INSERT INTO `career_project` (`career_id`, `name`, `description`, `level`, `file_path`) VALUES
(1, 'Portfolio website',
    'Build a personal portfolio with sections: About Me, Projects, Contact. Responsive design, CSS animations, no framework.',
    'beginner', 'portfolio_website_beginner.zip'),
(1, 'Todo app with React',
    'Todo app with adding, deleting and marking tasks as done. Uses useState and useEffect, data is stored in localStorage.',
    'intermediate', 'todo_app_react_intermediate.zip'),
(2, 'REST API for a blog',
    'Django REST API with CRUD operations for posts and comments. Token authentication, pagination, filtering by category.',
    'intermediate', 'blog_rest_api_intermediate.zip'),
(2, 'Authentication system',
    'Registration, login, logout and password reset in Django. Django auth system, email confirmation, session management.',
    'beginner', 'auth_system_django_beginner.zip'),
(3, 'Polls application',
    'Full-stack app: a user creates a poll, others vote, results are displayed graphically. Django backend + JavaScript frontend.',
    'intermediate', 'polls_app_fullstack_intermediate.zip'),
(3, 'E-commerce prototype',
    'Store with a product list, search, cart and simulated checkout. Django + React or plain JS.',
    'advanced', 'ecommerce_prototype_advanced.zip'),
(4, 'Redesign of a well-known website in Figma',
    'Pick a site with poor UX, analyze the issues and do a complete redesign in Figma with mobile and desktop versions.',
    'beginner', 'figma_redesign_beginner.zip'),
(4, 'Design system with components',
    'Build a consistent design system in Figma: typography, colors, iconography and a set of UI components.',
    'intermediate', 'design_system_figma_intermediate.zip'),
(5, 'Android calculator',
    'Calculator app in Kotlin with basic operations. Error handling (division by zero), landscape and portrait mode.',
    'beginner', 'android_calculator_beginner.zip'),
(5, 'Habit tracking app',
    'Mobile app for creating habits, daily check-ins and streak display. Room database, RecyclerView.',
    'intermediate', 'habit_tracker_app_intermediate.zip'),
(6, 'Sales data analysis',
    'Download a public sales CSV dataset, clean the data in pandas and build visualizations: trends, top products.',
    'beginner', 'sales_data_analysis_beginner.zip'),
(6, 'COVID-19 trend analysis',
    'Use public COVID data (Our World in Data), analyze trends by country and build an interactive dashboard.',
    'intermediate', 'covid_trend_dashboard_intermediate.zip'),
(7, 'Dockerizing a Django application',
    'Take a Django project and create a Dockerfile + docker-compose.yml with nginx and MySQL. Run everything with a single command.',
    'beginner', 'django_dockerization_beginner.zip'),
(7, 'CI/CD pipeline with GitHub Actions',
    'Set up a GitHub Actions workflow that automatically runs tests on every push and deploys to the server on merge.',
    'advanced', 'cicd_github_actions_advanced.zip');

-- =============================================
-- COMPANY
-- =============================================
INSERT INTO `company` (`id`, `name`, `username`, `email`, `password`, `industry`, `contact`, `description`, `logo_path`, `status`) VALUES
(1, 'Nimbus Software',      'nimbus_software',      'hr@nimbussoftware.rs',      'placeholder_hash', 'Web development',      '+381 11 111 1111', 'A boutique agency building web and mobile applications, focused on startup clients.',                  'Nimbus Software.png', 'active'),
(2, 'DataForge Analytics',  'dataforge_analytics',  'jobs@dataforge.rs',         'placeholder_hash', 'Data & Analytics',     '+381 11 222 2222', 'A company specialized in data analysis and business intelligence solutions.',                        'DataForge Analytics.png', 'active'),
(3, 'PixelCraft Studio',    'pixelcraft_studio',    'careers@pixelcraft.rs',     'placeholder_hash', 'Design',               '+381 21 333 3333', 'A design studio focused on UI/UX and the visual identity of digital products.',                            NULL, 'active'),
(4, 'CloudNine Systems',    'cloudnine_systems',    'hr@cloudnine.rs',           'placeholder_hash', 'DevOps & Infrastructure', '+381 11 444 4444', 'Provides DevOps and cloud infrastructure for mid-size and large companies in the region.',                       'CloudNine Systems.png', 'active'),
(5, 'Mobicore Apps',        'mobicore_apps',        'jobs@mobicore.rs',          'placeholder_hash', 'Mobile development',   '+381 21 555 5555', 'Builds mobile applications for Android and iOS, both natively and cross-platform.',                                'Mobicore Apps.png', 'active'),
(6, 'Vertex Solutions',     'vertex_solutions',     'hr@vertexsolutions.rs',     'placeholder_hash', 'IT Consulting',        '+381 11 666 6666', 'An IT consulting company covering the full spectrum of software development, from backend to frontend solutions.',       'Vertex Solutions.png', 'pending');

-- =============================================
-- JOB_AD
-- =============================================
INSERT INTO `job_ad` (`id`, `company_id`, `name`, `description`, `type`, `location`, `application_deadline`, `status`) VALUES
(1, 1, 'Junior Frontend Developer',
    'We are looking for a Junior Frontend Developer who will work on building the user interfaces of our web applications using React and modern CSS tools.',
    'junior', 'Belgrade', '2026-08-15', 'active'),
(2, 1, 'Frontend Development Intern',
    'An internship for students who want to learn the basics of frontend development by working on real projects with mentorship from the senior team.',
    'internship', 'Belgrade (hybrid)', '2026-07-31', 'active'),
(3, 2, 'Junior Data Analyst',
    'You will analyze sales and user data, and build reports and dashboards for internal and external clients.',
    'junior', 'Novi Sad', '2026-08-01', 'active'),
(4, 2, 'Data Analytics Intern',
    'An internship on the analytics team — working with SQL queries, Excel reports and basic data visualizations.',
    'internship', 'Novi Sad (remote)', '2026-07-20', 'active'),
(5, 3, 'Junior UI/UX Designer',
    'You will design user interfaces for web and mobile applications, working closely with the development team on implementation.',
    'junior', 'Novi Sad', '2026-08-10', 'active'),
(6, 3, 'UI/UX Design Intern',
    'An internship at the design studio — working on wireframes, prototypes in Figma and the basics of visual identity.',
    'internship', 'Novi Sad (hybrid)', '2026-07-25', 'active'),
(7, 4, 'Junior DevOps Engineer',
    'You will help maintain CI/CD pipelines, containerize applications and work with Linux servers.',
    'junior', 'Belgrade', '2026-08-20', 'active'),
(8, 5, 'Junior Mobile Developer (Android)',
    'You will build and maintain Android applications in Kotlin, with the possibility of also working on React Native projects.',
    'junior', 'Novi Sad', '2026-08-05', 'active'),
(9, 5, 'Mobile Development Intern',
    'An internship for students interested in mobile development — working on smaller features with mentor support.',
    'internship', 'Novi Sad (remote)', '2026-07-18', 'active'),
(10, 6, 'Junior Backend Developer',
    'You will develop server-side logic and APIs using Python/Django, working with MySQL databases.',
    'junior', 'Belgrade', '2026-08-12', 'inactive'),
(11, 6, 'Junior Full-Stack Developer',
    'We are looking for a Junior Full-Stack Developer to work on complete web solutions — from the database to the user interface.',
    'junior', 'Belgrade (hybrid)', '2026-09-01', 'pending');

-- =============================================
-- JOB_AD_SKILL
-- =============================================

-- job_ad 1: Junior Frontend Developer (Nimbus Software)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(1, 1, 3),   -- HTML
(1, 2, 3),   -- CSS
(1, 3, 3),   -- JavaScript
(1, 5, 3),   -- React
(1, 13, 2);  -- Git

-- job_ad 2: Frontend Development Intern (Nimbus Software)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(2, 1, 2),   -- HTML
(2, 2, 2),   -- CSS
(2, 3, 1);   -- JavaScript

-- job_ad 3: Junior Data Analyst (DataForge Analytics)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(3, 10, 3),  -- SQL
(3, 11, 2),  -- MySQL
(3, 19, 3),  -- Excel
(3, 7, 2);   -- Python

-- job_ad 4: Data Analytics Intern (DataForge Analytics)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(4, 10, 1),  -- SQL
(4, 19, 2);  -- Excel

-- job_ad 5: Junior UI/UX Designer (PixelCraft Studio)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(5, 16, 4),  -- Figma
(5, 2, 2),   -- CSS
(5, 1, 2);   -- HTML

-- job_ad 6: UI/UX Design Intern (PixelCraft Studio)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(6, 16, 2);  -- Figma

-- job_ad 7: Junior DevOps Engineer (CloudNine Systems)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(7, 14, 3),  -- Docker
(7, 15, 3),  -- Linux
(7, 13, 3),  -- Git
(7, 7, 2);   -- Python

-- job_ad 8: Junior Mobile Developer - Android (Mobicore Apps)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(8, 17, 3),  -- Kotlin
(8, 18, 2),  -- React Native
(8, 13, 2);  -- Git

-- job_ad 9: Mobile Development Intern (Mobicore Apps)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(9, 17, 1),  -- Kotlin
(9, 18, 1);  -- React Native

-- job_ad 10: Junior Backend Developer (Vertex Solutions)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(10, 7, 3),  -- Python
(10, 8, 3),  -- Django
(10, 11, 2), -- MySQL
(10, 10, 3); -- SQL

-- job_ad 11: Junior Full-Stack Developer (Vertex Solutions)
INSERT INTO `job_ad_skill` (`job_ad_id`, `skill_id`, `required_level`) VALUES
(11, 1, 2),  -- HTML
(11, 2, 2),  -- CSS
(11, 3, 3),  -- JavaScript
(11, 7, 3),  -- Python
(11, 8, 2),  -- Django
(11, 10, 2); -- SQL



-- =============================================
-- USER
-- =============================================
INSERT INTO `user`
(`id`, `first_name`, `last_name`, `username`, `email`, `password`, `contact`, `status`, `role`, `registered_at`, `rejection_reason`)
VALUES
(1, 'Anastasija', 'Ljubicic', 'anastasija', 'anastasija@example.com',
 'placeholder_hash', '+381 64 111 1111', 'active', 'user',
 '2026-06-01 10:00:00', NULL),

(2, 'Marko', 'Petrovic', 'marko_petrovic', 'marko@example.com',
 'placeholder_hash', '+381 64 222 2222', 'active', 'user',
 '2026-06-05 12:30:00', NULL),

(3, 'Jovana', 'Nikolic', 'jovana_nikolic', 'jovana@example.com',
 'placeholder_hash', '+381 64 333 3333', 'active', 'user',
 '2026-06-10 09:15:00', NULL),

(4, 'Admin', 'Kompas', 'admin', 'admin@kompas.rs',
 'placeholder_hash', '+381 11 999 9999', 'active', 'admin',
 '2026-05-01 08:00:00', NULL),
 
 (5, 'Ana', 'Admin', 'ana_admin', 'ana_admin@example.com',
 'pbkdf2_sha256$1200000$FMaKiV11QzN4P75OiYAMzO$5eMt5DjXHxD53Rm43M/nu05J57X/m0XYJC/nz4xJUK8=',
 NULL, 'active', 'admin', '2026-07-13 00:00:00', NULL);
-- =============================================
-- APPLICATION

-- =============================================
INSERT INTO application (applied_at, status, user_id, job_ad_id, cv_path, skills, education, cover_message) VALUES
('2026-07-10 00:04:00.000000', 'active', 1, 1, NULL, 'Python, Django, SQL', 'ETF Beograd', 'Veoma sam zainteresovan za ovu poziciju.'),
('2026-07-01 11:30:00.000000', 'active', 2, 2, NULL, 'HTML, CSS, JavaScript', 'FTN Novi Sad', 'Nadam se uspešnoj saradnji.'),
('2026-07-02 09:45:00.000000', 'withdrawn', 3, 3, NULL, 'Project Management, Scrum', 'Ekonomski fakultet', NULL),
('2026-07-02 14:20:00.000000', 'accepted', 1, 4, NULL, 'Python, Docker, AWS', 'ETF Beograd', 'Radujem se tehničkom intervjuu.'),
('2026-07-03 08:10:00.000000', 'active', 2, 5, NULL, 'React, Node.js', 'Visoka ICT', 'Zanimljiv projekat, želim da doprinesem timu.'),
('2026-07-03 16:35:00.000000', 'active', 3, 6, NULL, 'QA Testing, Selenium', 'PMF Kragujevac', NULL),
('2026-07-04 12:00:00.000000', 'denied', 1, 7, NULL, 'Java, Spring Boot', 'ETF Beograd', 'Prijava za backend inženjera.'),
('2026-07-04 13:25:00.000000', 'accepted', 2, 8, NULL, 'UI/UX Design, Figma', 'FPU Beograd', 'Portfolio šaljem u prilogu.'),
('2026-07-05 09:00:00.000000', 'active', 3, 9, NULL, 'C#, .NET Core', 'Singidunum', 'Motivisan sam za učenje novih tehnologija.'),
('2026-07-05 17:40:00.000000', 'denied', 1, 10, NULL, 'PHP, Laravel', 'Samouk', 'Dugogodišnje iskustvo u frilensu.');


-- =============================================
-- ADMINISTRATOR (test admin account for functional testing)
-- =============================================
INSERT INTO `administrator` (`user_id`, `access_level`, `assigned_date`)
VALUES (5, 'standard', CURDATE());