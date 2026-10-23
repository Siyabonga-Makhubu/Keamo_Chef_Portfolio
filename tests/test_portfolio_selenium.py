from selenium.webdriver.common.by import By


def test_navigation_opens_about_page(selenium_driver: object, base_url: str) -> None:
    selenium_driver.get(f"{base_url}/index.html")

    selenium_driver.find_element(
        By.XPATH, "//nav//a[normalize-space()='About']"
    ).click()

    assert selenium_driver.current_url.endswith("/About.html")
    assert selenium_driver.find_element(
        By.XPATH, "//h2[normalize-space()='About Me']"
    ).is_displayed()


def test_book_me_links_directly_to_whatsapp(
    selenium_driver: object, base_url: str
) -> None:
    selenium_driver.get(f"{base_url}/index.html")
    book_link = selenium_driver.find_element(
        By.XPATH, "//a[normalize-space()='Book Me']"
    )

    assert book_link.get_attribute("href") == "https://wa.me/27834806216"
    assert book_link.get_attribute("onclick") is None


def test_registration_requires_email(selenium_driver: object, base_url: str) -> None:
    selenium_driver.get(f"{base_url}/register.html")
    email = selenium_driver.find_element(By.ID, "reg-email")

    email.send_keys("not-an-email")

    assert not email.get_property("validity")["valid"]
