"""Tests written by Milica Pavlovic for Anastasija's careers functionality."""

from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from accounts.models import Company, User
from careers.models import (
    Career,
    CareerSkill,
    FavoriteCareer,
    FavoriteJobAd,
    JobAd,
    JobAdSkill,
    Resource,
    Skill,
)
from careers.views import level_to_label

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CareersUnitTests(TestCase):
    """Django unit and controller tests for Favorites and Skill Match."""

    def setUp(self):
        self.user = User.objects.create(
            first_name="Milica",
            last_name="Tester",
            username="milica_test",
            email="milica.test@example.com",
            password=make_password("test1234"),
            contact="060111222",
            status="active",
            role="user",
        )
        self.other_user = User.objects.create(
            first_name="Other",
            last_name="User",
            username="other_user",
            email="other.user@example.com",
            password=make_password("test1234"),
            status="active",
            role="user",
        )
        self.company = Company.objects.create(
            name="Test Company",
            username="test_company",
            email="company@example.com",
            password=make_password("test1234"),
            industry="Software",
            status="active",
        )

        self.python = Skill.objects.create(name="Python", description="Python skill")
        self.sql = Skill.objects.create(name="SQL", description="SQL skill")

        self.backend = Career.objects.create(
            name="Backend Engineer",
            description="Develops server-side applications.",
        )
        self.data_analyst = Career.objects.create(
            name="Data Analyst",
            description="Analyzes data.",
        )

        CareerSkill.objects.create(
            career=self.backend,
            skill=self.python,
            required_level=5,
            weight=Decimal("1.00"),
        )
        CareerSkill.objects.create(
            career=self.data_analyst,
            skill=self.python,
            required_level=2,
            weight=Decimal("1.00"),
        )
        CareerSkill.objects.create(
            career=self.data_analyst,
            skill=self.sql,
            required_level=4,
            weight=Decimal("1.00"),
        )

        self.job_ad = JobAd.objects.create(
            company=self.company,
            name="Junior Python Developer",
            description="Python and SQL position.",
            type="junior",
            location="Belgrade",
            status="active",
        )
        JobAdSkill.objects.create(
            job_ad=self.job_ad,
            skill=self.python,
            required_level=4,
        )
        JobAdSkill.objects.create(
            job_ad=self.job_ad,
            skill=self.sql,
            required_level=3,
        )

        self.sql_resource = Resource.objects.create(
            skill=self.sql,
            name="SQL Intermediate Course",
            url="https://example.com/sql-course",
            level="intermediate",
        )

        FavoriteCareer.objects.create(user=self.user, career=self.backend)
        FavoriteJobAd.objects.create(user=self.user, job_ad=self.job_ad)
        FavoriteCareer.objects.create(user=self.other_user, career=self.data_analyst)

    def login_as_user(self, user=None):
        """Stores the custom application login data in the test session."""
        logged_user = user or self.user
        session = self.client.session
        session["role"] = "user"
        session["user_id"] = logged_user.id
        session.save()

    def test_model_helpers_and_resource_string(self):
        """Checks model persistence and the level-label boundary helper."""
        self.assertEqual(str(self.sql_resource), "SQL Intermediate Course")
        self.assertTrue(Career.objects.filter(name="Backend Engineer").exists())
        self.assertEqual(level_to_label(1), "beginner")
        self.assertEqual(level_to_label(2), "beginner")
        self.assertEqual(level_to_label(3), "intermediate")
        self.assertEqual(level_to_label(4), "intermediate")
        self.assertEqual(level_to_label(5), "advanced")

    def test_favourites_page_requires_login(self):
        response = self.client.get(reverse("favourites"))
        self.assertRedirects(response, reverse("login"))

    def test_favourites_page_shows_only_current_users_items(self):
        self.login_as_user()
        response = self.client.get(reverse("favourites"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "careers/favourites.html")
        self.assertContains(response, "Backend Engineer")
        self.assertContains(response, "Junior Python Developer")
        self.assertNotContains(response, "Data Analyst")

    def test_toggle_career_favourite_adds_and_removes_item(self):
        self.login_as_user()

        add_response = self.client.post(
            reverse("toggle_favourite"),
            {"type": "career", "id": self.data_analyst.id},
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertTrue(add_response.json()["success"])
        self.assertTrue(add_response.json()["is_favourite"])
        self.assertTrue(
            FavoriteCareer.objects.filter(
                user=self.user,
                career=self.data_analyst,
            ).exists()
        )

        remove_response = self.client.post(
            reverse("toggle_favourite"),
            {"type": "career", "id": self.data_analyst.id},
        )
        self.assertEqual(remove_response.status_code, 200)
        self.assertFalse(remove_response.json()["is_favourite"])
        self.assertFalse(
            FavoriteCareer.objects.filter(
                user=self.user,
                career=self.data_analyst,
            ).exists()
        )

    def test_toggle_job_favourite_removes_and_restores_item(self):
        self.login_as_user()

        remove_response = self.client.post(
            reverse("toggle_favourite"),
            {"type": "job", "id": self.job_ad.id},
        )
        self.assertEqual(remove_response.status_code, 200)
        self.assertFalse(remove_response.json()["is_favourite"])
        self.assertFalse(
            FavoriteJobAd.objects.filter(
                user=self.user,
                job_ad=self.job_ad,
            ).exists()
        )

        add_response = self.client.post(
            reverse("toggle_favourite"),
            {"type": "job", "id": self.job_ad.id},
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertTrue(add_response.json()["is_favourite"])
        self.assertTrue(
            FavoriteJobAd.objects.filter(
                user=self.user,
                job_ad=self.job_ad,
            ).exists()
        )

    def test_toggle_favourite_rejects_invalid_type(self):
        self.login_as_user()
        response = self.client.post(
            reverse("toggle_favourite"),
            {"type": "invalid", "id": self.backend.id},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["error"], "Invalid type")

    def test_skill_match_page_requires_login(self):
        response = self.client.get(reverse("skill_match"))
        self.assertRedirects(response, reverse("login"))

    def test_skill_match_get_displays_available_skills(self):
        self.login_as_user()
        response = self.client.get(reverse("skill_match"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "careers/skill_match.html")
        self.assertContains(response, "Python")
        self.assertContains(response, "SQL")

    def test_skill_match_calculates_gaps_and_sorts_results(self):
        self.login_as_user()
        response = self.client.post(
            reverse("skill_match"),
            {
                f"skill-{self.python.id}": "5",
                f"skill-{self.sql.id}": "1",
                "show_careers": "on",
                "show_jobs": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        results = response.context["combined_matching"]
        percentages = [result["match_percentage"] for result in results]

        self.assertEqual(percentages, sorted(percentages, reverse=True))
        self.assertEqual(percentages, [100, 67, 62])

        data_result = next(
            result
            for result in results
            if result["type"] == "career"
            and result["career"] == self.data_analyst
        )
        sql_match = next(
            skill
            for skill in data_result["skills_match"]
            if skill["skill_name"] == "SQL"
        )

        self.assertEqual(sql_match["gap"], 3)
        self.assertIn(self.sql_resource, sql_match["missing_skills_resources"])
        self.assertTrue(data_result["has_missing_resources"])

    def test_skill_match_can_show_only_careers(self):
        self.login_as_user()
        response = self.client.post(
            reverse("skill_match"),
            {
                f"skill-{self.python.id}": "5",
                "show_careers": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        results = response.context["combined_matching"]
        self.assertTrue(results)
        self.assertTrue(all(result["type"] == "career" for result in results))
        self.assertTrue(response.context["show_careers"])
        self.assertFalse(response.context["show_jobs"])


class CareersSeleniumTests(StaticLiveServerTestCase):
    """Browser tests for Anastasija's Favorites and Skill Match pages."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.browser = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.browser, 12)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.browser.delete_all_cookies()

        self.user = User.objects.create(
            first_name="Milica",
            last_name="Selenium",
            username="milica_selenium",
            email="milica.selenium@example.com",
            password=make_password("test1234"),
            contact="060333444",
            status="active",
            role="user",
        )
        self.empty_user = User.objects.create(
            first_name="Empty",
            last_name="Favorites",
            username="empty_favorites",
            email="empty.favorites@example.com",
            password=make_password("test1234"),
            status="active",
            role="user",
        )
        self.company = Company.objects.create(
            name="Selenium Company",
            username="selenium_company",
            email="selenium.company@example.com",
            password=make_password("test1234"),
            industry="Software",
            status="active",
        )

        self.python = Skill.objects.create(
            name="Python",
            description="Python skill",
        )
        self.sql = Skill.objects.create(
            name="SQL",
            description="SQL skill",
        )

        self.backend = Career.objects.create(
            name="Backend Engineer",
            description="Develops server-side applications.",
        )
        self.data_analyst = Career.objects.create(
            name="Data Analyst",
            description="Analyzes data.",
        )

        CareerSkill.objects.create(
            career=self.backend,
            skill=self.python,
            required_level=5,
            weight=Decimal("1.00"),
        )
        CareerSkill.objects.create(
            career=self.data_analyst,
            skill=self.python,
            required_level=2,
            weight=Decimal("1.00"),
        )
        CareerSkill.objects.create(
            career=self.data_analyst,
            skill=self.sql,
            required_level=4,
            weight=Decimal("1.00"),
        )

        self.job_ad = JobAd.objects.create(
            company=self.company,
            name="Junior Python Developer",
            description="Python and SQL position.",
            type="junior",
            location="Belgrade",
            status="active",
        )
        JobAdSkill.objects.create(
            job_ad=self.job_ad,
            skill=self.python,
            required_level=4,
        )
        JobAdSkill.objects.create(
            job_ad=self.job_ad,
            skill=self.sql,
            required_level=3,
        )

        self.sql_resource = Resource.objects.create(
            skill=self.sql,
            name="SQL Intermediate Course",
            url="https://example.com/sql-course",
            level="intermediate",
        )

        FavoriteCareer.objects.create(
            user=self.user,
            career=self.backend,
        )
        FavoriteJobAd.objects.create(
            user=self.user,
            job_ad=self.job_ad,
        )

    def app_url(self, route_name):
        """Builds an absolute URL served by Django's temporary test server."""
        return f"{self.live_server_url}{reverse(route_name)}"

    def safe_click(self, element):
        """Scrolls an element to the center and clicks it reliably."""
        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element,
        )
        self.wait.until(
            lambda driver: element.is_displayed() and element.is_enabled()
        )
        self.browser.execute_script("arguments[0].click();", element)

    def login_through_browser(self, user=None):
        """Logs in through the real login form, not by editing the session."""
        login_user = user or self.user

        self.browser.get(self.app_url("login"))

        username = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password = self.browser.find_element(By.NAME, "password")

        username.clear()
        username.send_keys(login_user.username)
        password.clear()
        password.send_keys("test1234")

        self.browser.find_element(
            By.CSS_SELECTOR,
            "input[type='submit']",
        ).click()

        self.wait.until(
            lambda driver: reverse("login") not in driver.current_url
        )

    def select_skill_and_level(self, skill, level):
        """Selects a skill tag and changes the generated slider value."""
        tag = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'.skill-field[data-id="{skill.id}"]')
            )
        )
        tag.click()

        hidden = self.wait.until(
            EC.presence_of_element_located(
                (By.ID, f"hidden-skill-{skill.id}")
            )
        )
        row = hidden.find_element(By.XPATH, "./parent::div")
        slider = row.find_element(By.CSS_SELECTOR, "input[type='range']")

        self.browser.execute_script(
            """
            const slider = arguments[0];
            slider.value = arguments[1];
            slider.dispatchEvent(new Event('input', {bubbles: true}));
            """,
            slider,
            str(level),
        )

        self.wait.until(
            lambda driver: driver.find_element(
                By.ID,
                f"hidden-skill-{skill.id}",
            ).get_attribute("value")
            == str(level)
        )

    def run_skill_analysis(self):
        """Selects representative levels and submits the Skill Match form."""
        self.browser.get(self.app_url("skill_match"))

        self.select_skill_and_level(self.python, 5)
        self.select_skill_and_level(self.sql, 1)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "skill-levels-div"))
        )

        self.browser.find_element(
            By.CSS_SELECTOR,
            "#skill-form button[type='submit']",
        ).click()

        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".career-percentage")
            )
        )

    def test_guest_is_redirected_from_skill_match_to_login(self):
        self.browser.get(self.app_url("skill_match"))

        self.wait.until(
            lambda driver: reverse("login") in driver.current_url
        )
        self.assertIn(reverse("login"), self.browser.current_url)

    def test_user_runs_skill_analysis_and_opens_learning_resources(self):
        self.login_through_browser()
        self.run_skill_analysis()

        percentage_elements = self.browser.find_elements(
            By.CSS_SELECTOR,
            ".career-percentage",
        )
        percentages = [
            int(element.text.strip().replace("%", ""))
            for element in percentage_elements
        ]

        self.assertEqual(percentages, sorted(percentages, reverse=True))
        self.assertEqual(percentages, [100, 67, 62])

        result_names = [
            element.text.strip()
            for element in self.browser.find_elements(
                By.CSS_SELECTOR,
                ".career-name",
            )
        ]
        self.assertIn("Backend Engineer", result_names)
        self.assertIn("Data Analyst", result_names)
        self.assertIn("Junior Python Developer", result_names)

        data_card = self.browser.find_element(
            By.XPATH,
            (
                "//div[contains(@class,'career-name') "
                "and normalize-space()='Data Analyst']"
                "/ancestor::div[contains(@class,'custom-card')][1]"
            ),
        )
        learn_skills_button = data_card.find_element(
            By.XPATH,
            ".//button[contains(@onclick, 'toggleLearnSkills')]",
        )
        self.safe_click(learn_skills_button)

        resource_section = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"learn-skills-career-{self.data_analyst.id}")
            )
        )
        self.assertIn("SQL Intermediate Course", resource_section.text)
        self.assertIn("needs 3 more level", resource_section.text)

    def test_user_adds_career_to_favorites_from_skill_match(self):
        self.login_through_browser()
        self.run_skill_analysis()

        favorite_label = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    f'label[for="career-star-{self.data_analyst.id}"]',
                )
            )
        )
        self.safe_click(favorite_label)

        self.wait.until(
            lambda driver: FavoriteCareer.objects.filter(
                user=self.user,
                career=self.data_analyst,
            ).exists()
        )

        self.browser.get(self.app_url("favourites"))

        self.browser.find_elements(By.CSS_SELECTOR, ".tab-btn")[1].click()
        career_card = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"career-card-{self.data_analyst.id}")
            )
        )
        self.assertIn("Data Analyst", career_card.text)

    def test_favorites_tabs_and_remove_buttons_update_database(self):
        self.login_through_browser()
        self.browser.get(self.app_url("favourites"))

        job_card = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"job-card-{self.job_ad.id}")
            )
        )
        self.assertIn("Junior Python Developer", job_card.text)

        tab_buttons = self.browser.find_elements(By.CSS_SELECTOR, ".tab-btn")
        tab_buttons[1].click()

        career_card = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"career-card-{self.backend.id}")
            )
        )
        self.assertIn("Backend Engineer", career_card.text)

        career_card.find_elements(By.TAG_NAME, "button")[0].click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.ID, f"career-card-{self.backend.id}")
            )
        )
        self.wait.until(
            lambda driver: not FavoriteCareer.objects.filter(
                user=self.user,
                career=self.backend,
            ).exists()
        )

        self.browser.find_elements(By.CSS_SELECTOR, ".tab-btn")[0].click()
        job_card = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"job-card-{self.job_ad.id}")
            )
        )
        job_card.find_elements(By.TAG_NAME, "button")[0].click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (By.ID, f"job-card-{self.job_ad.id}")
            )
        )
        self.wait.until(
            lambda driver: not FavoriteJobAd.objects.filter(
                user=self.user,
                job_ad=self.job_ad,
            ).exists()
        )

    def test_empty_favorites_page_has_no_item_cards(self):
        self.login_through_browser(self.empty_user)
        self.browser.get(self.app_url("favourites"))

        self.assertFalse(
            self.browser.find_elements(By.CSS_SELECTOR, '[id^="job-card-"]')
        )
        self.assertFalse(
            self.browser.find_elements(By.CSS_SELECTOR, '[id^="career-card-"]')
        )
        self.assertIn(
            "You have no favorite job ads yet.",
            self.browser.page_source,
        )
        self.assertIn(
            "You have no favorite careers yet.",
            self.browser.page_source,
        )