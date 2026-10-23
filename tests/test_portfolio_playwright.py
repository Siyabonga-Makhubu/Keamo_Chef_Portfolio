import json
from urllib.parse import parse_qs, urlsplit

import pytest


@pytest.mark.parametrize(
    "page_name",
    [
        "index.html",
        "About.html",
        "Skills.html",
        "Artisinal_Creations.html",
        "education.html",
        "experience.html",
        "contact.html",
        "register.html",
        "admin.html",
        "dashboard.html",
    ],
)
def test_portfolio_pages_load_in_playwright(
    playwright_page: object, base_url: str, page_name: str
) -> None:
    if page_name == "contact.html":
        playwright_page.add_init_script(
            "localStorage.setItem('user', JSON.stringify({isRegistered: true}));"
        )

    response = playwright_page.goto(
        f"{base_url}/{page_name}", wait_until="domcontentloaded"
    )

    assert response is not None
    assert response.status == 200
    assert playwright_page.title()
    assert playwright_page.locator("body").inner_text().strip()
    assert "page-fade-in" in (
        playwright_page.locator("body").get_attribute("class") or ""
    )
    assert playwright_page.locator("nav a[href='admin.html']").count() == 0
    assert playwright_page.locator("nav a[href='dashboard.html']").count() == 0
    social_links = playwright_page.locator("footer .footer-social-links a")
    assert social_links.count() == 2
    assert social_links.nth(0).get_attribute("href") == (
        "https://wa.me/27834806216"
    )
    assert social_links.nth(1).get_attribute("href") == (
        "https://www.instagram.com/"
    )
    footer_text = playwright_page.locator("footer [data-template-id='footer-text']")
    footer_text_box = footer_text.bounding_box()
    social_links_box = playwright_page.locator(
        "footer .footer-social-links"
    ).bounding_box()
    assert footer_text_box is not None
    assert social_links_box is not None
    assert social_links_box["x"] > footer_text_box["x"]
    footer_box = playwright_page.locator("footer").bounding_box()
    assert footer_box is not None
    footer_text_center = footer_text_box["x"] + footer_text_box["width"] / 2
    footer_center = footer_box["x"] + footer_box["width"] / 2
    assert abs(footer_text_center - footer_center) < 12
    assert abs(
        (social_links_box["y"] + social_links_box["height"] / 2)
        - (footer_text_box["y"] + footer_text_box["height"] / 2)
    ) < 12


def test_portfolio_pages_fit_mobile_and_tablet_viewports(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.add_init_script(
        "localStorage.setItem('user', JSON.stringify({isRegistered: true}));"
    )
    page_names = [
        "index.html",
        "About.html",
        "Skills.html",
        "Artisinal_Creations.html",
        "education.html",
        "experience.html",
        "contact.html",
        "register.html",
        "admin.html",
        "dashboard.html",
    ]
    viewport_sizes = [
        {"width": 320, "height": 640},
        {"width": 390, "height": 844},
        {"width": 768, "height": 1024},
        {"width": 844, "height": 390},
        {"width": 1024, "height": 768},
    ]

    for viewport_size in viewport_sizes:
        playwright_page.set_viewport_size(viewport_size)

        for page_name in page_names:
            response = playwright_page.goto(
                f"{base_url}/{page_name}", wait_until="domcontentloaded"
            )

            assert response is not None
            assert response.status == 200
            dimensions = playwright_page.evaluate(
                """() => {
                  const root = document.documentElement;
                  const offenders = [...document.querySelectorAll("body *")]
                    .filter(element => {
                      const rect = element.getBoundingClientRect();
                      return rect.right > root.clientWidth + 1;
                    })
                    .slice(0, 5)
                    .map(element => ({
                      tag: element.tagName,
                      className: typeof element.className === "string"
                        ? element.className
                        : "",
                      right: Math.round(element.getBoundingClientRect().right),
                    }));
                  return {
                    clientWidth: root.clientWidth,
                    scrollWidth: root.scrollWidth,
                    offenders,
                  };
                }"""
            )
            assert dimensions["scrollWidth"] <= dimensions["clientWidth"], (
                f"{page_name} overflows at {viewport_size['width']}px: "
                f"{dimensions}"
            )

            nav_links = playwright_page.locator("nav .nav-links a")
            for index in range(nav_links.count()):
                link = nav_links.nth(index)
                assert link.is_visible(), (
                    f"{page_name} navigation link is hidden at "
                    f"{viewport_size['width']}px"
                )
                if viewport_size["width"] <= 900:
                    assert link.bounding_box()["height"] >= 44

            if viewport_size["width"] <= 900:
                footer_text = playwright_page.locator(
                    "footer [data-template-id='footer-text']"
                )
                social_links = playwright_page.locator(
                    "footer .footer-social-links"
                )
                if footer_text.count() and social_links.count():
                    text_box = footer_text.bounding_box()
                    social_box = social_links.bounding_box()
                    assert text_box is not None
                    assert social_box is not None
                    assert social_box["y"] >= (
                        text_box["y"] + text_box["height"]
                    )


def test_main_navigation_opens_about_page(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")

    playwright_page.get_by_role("link", name="About", exact=True).click()

    assert playwright_page.url.endswith("/About.html")
    playwright_page.get_by_role("heading", name="About Me").wait_for(
        state="visible"
    )


def test_book_me_links_directly_to_whatsapp(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")

    book_link = playwright_page.get_by_role("link", name="Book Me")

    assert book_link.get_attribute("href") == "https://wa.me/27834806216"
    assert book_link.get_attribute("onclick") is None


def test_registration_success_with_mocked_api(
    playwright_page: object, base_url: str
) -> None:
    def register(route: object) -> None:
        cors_headers = {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Origin": "*",
        }
        if route.request.method == "OPTIONS":
            route.fulfill(status=204, headers=cors_headers)
            return

        route.fulfill(
            status=200,
            content_type="application/json",
            headers={"Access-Control-Allow-Origin": "*"},
            body=json.dumps(
                {
                    "user": {
                        "id": "test-user",
                        "name": "Test Chef",
                        "email": "chef@example.test",
                        "isRegistered": True,
                    }
                }
            ),
        )

    playwright_page.route("http://localhost:5055/api/users/register", register)
    playwright_page.goto(f"{base_url}/register.html", wait_until="domcontentloaded")
    playwright_page.locator("#reg-name").fill("Test Chef")
    playwright_page.locator("#reg-email").fill("chef@example.test")
    playwright_page.locator("#reg-contact").fill("0712345678")
    playwright_page.get_by_role("button", name="Register").click()

    playwright_page.locator("#success-section").wait_for(state="visible")
    assert playwright_page.evaluate("localStorage.getItem('user')") is not None


def _mock_whatsapp_window(page: object) -> None:
    page.add_init_script(
        "window.CHEF_WHATSAPP_NUMBER = '27820000000';"
        "window.__openedUrls = [];"
        "window.open = (url, target, features) => {"
        "window.__openedUrls.push({url, target, features}); return {};"
        "};"
    )


def _fill_contact_form(page: object) -> None:
    page.locator("#name").fill("Zoë & Co")
    page.locator("#phone").fill("+27 (82) 123-4567")
    page.locator("#enquiry-type").select_option(label="Catering enquiry")
    page.locator("#message").fill("Hello, chef!\nCanapé & crème brûlée.")


@pytest.mark.parametrize("page_name", ["index.html", "contact.html"])
def test_contact_form_opens_prefilled_whatsapp_message(
    playwright_page: object, base_url: str, page_name: str
) -> None:
    _mock_whatsapp_window(playwright_page)
    playwright_page.goto(f"{base_url}/{page_name}", wait_until="domcontentloaded")
    _fill_contact_form(playwright_page)

    playwright_page.get_by_role(
        "button", name="Send via WhatsApp"
    ).click()

    opened = playwright_page.evaluate("window.__openedUrls[0]")
    parsed = urlsplit(opened["url"])
    message = parse_qs(parsed.query)["text"][0]

    assert parsed.scheme == "https"
    assert parsed.netloc == "wa.me"
    assert parsed.path == "/27820000000"
    assert message == (
        "Hello Chef,\n\n"
        "I would like to enquire about your services.\n\n"
        "Customer Name: Zoë & Co\n"
        "Customer Phone: +27821234567\n"
        "Enquiry Type: Catering enquiry\n\n"
        "Message:\n"
        "Hello, chef!\nCanapé & crème brûlée.\n\n"
        "Thank you."
    )
    assert "%C3%AB" in opened["url"]
    assert "%26" in opened["url"]
    assert "%0A" in opened["url"]
    assert opened["target"] == "_blank"
    assert "noopener" in opened["features"]
    assert "press Send" in playwright_page.locator("#whatsapp-status").inner_text()
    assert "successfully" not in playwright_page.locator("#whatsapp-status").inner_text()


def test_contact_form_shows_errors_for_missing_required_fields(
    playwright_page: object, base_url: str
) -> None:
    _mock_whatsapp_window(playwright_page)
    playwright_page.goto(f"{base_url}/contact.html", wait_until="domcontentloaded")
    playwright_page.get_by_role("button", name="Send via WhatsApp").click()

    for field_id in ("name", "phone", "enquiry-type", "message"):
        assert playwright_page.locator(f"#{field_id}").get_attribute(
            "aria-invalid"
        ) == "true"
        assert playwright_page.locator(f"#{field_id}-error").inner_text()
    assert playwright_page.evaluate("window.__openedUrls") == []


def test_contact_form_rejects_invalid_phone_number(
    playwright_page: object, base_url: str
) -> None:
    _mock_whatsapp_window(playwright_page)
    playwright_page.goto(f"{base_url}/contact.html", wait_until="domcontentloaded")
    playwright_page.locator("#name").fill("Test Customer")
    playwright_page.locator("#phone").fill("not-a-phone")
    playwright_page.locator("#enquiry-type").select_option(
        label="General enquiry"
    )
    playwright_page.locator("#message").fill("Please get in touch.")
    playwright_page.get_by_role("button", name="Send via WhatsApp").click()

    assert "valid phone number" in playwright_page.locator(
        "#phone-error"
    ).inner_text()
    assert playwright_page.evaluate("window.__openedUrls") == []


def test_contact_form_requires_chef_whatsapp_configuration(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/contact.html", wait_until="domcontentloaded")
    _fill_contact_form(playwright_page)
    playwright_page.get_by_role("button", name="Send via WhatsApp").click()

    assert "not configured" in playwright_page.locator(
        "#whatsapp-status"
    ).inner_text()


def test_contact_form_prevents_duplicate_whatsapp_actions(
    playwright_page: object, base_url: str
) -> None:
    _mock_whatsapp_window(playwright_page)
    playwright_page.goto(f"{base_url}/contact.html", wait_until="domcontentloaded")
    _fill_contact_form(playwright_page)
    button = playwright_page.get_by_role("button", name="Send via WhatsApp")
    button.click()
    playwright_page.locator("#contact-form").dispatch_event("submit")
    playwright_page.locator("#contact-form").dispatch_event("submit")

    assert playwright_page.evaluate("window.__openedUrls.length") == 1
    assert button.is_disabled()


def test_contact_form_fits_mobile_viewport(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.set_viewport_size({"width": 320, "height": 640})
    playwright_page.goto(f"{base_url}/contact.html", wait_until="domcontentloaded")

    dimensions = playwright_page.evaluate(
        """() => {
          const form = document.querySelector("#contact-form");
          const rect = form.getBoundingClientRect();
          return {
            left: rect.left,
            right: rect.right,
            viewportWidth: document.documentElement.clientWidth,
            scrollWidth: document.documentElement.scrollWidth,
          };
        }"""
    )
    assert dimensions["left"] >= 0
    assert dimensions["right"] <= dimensions["viewportWidth"]
    assert dimensions["scrollWidth"] <= dimensions["viewportWidth"]
    assert playwright_page.get_by_role(
        "button", name="Send via WhatsApp"
    ).is_visible()


def test_foodtography_images_open_in_lightbox(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(
        f"{base_url}/Artisinal_Creations.html", wait_until="domcontentloaded"
    )
    dish_images = playwright_page.locator(".dish-card .dish-img")
    gallery = playwright_page.locator(
        "section:has(h2:text('Foodtography Feed')) img"
    )
    gallery.first.scroll_into_view_if_needed()
    playwright_page.wait_for_function(
        "selector => [...document.querySelectorAll(selector)].every("
        "image => image.complete && image.naturalWidth > 0)",
        arg=".dish-card .dish-img",
    )
    playwright_page.wait_for_function(
        "selector => [...document.querySelectorAll(selector)].every("
        "image => image.complete && image.naturalWidth > 0)",
        arg="section:has(h2) .foodtography-img",
    )

    assert dish_images.count() == 9
    dish_image_layouts = dish_images.evaluate_all(
        "images => images.every(image => image.complete && image.naturalWidth > 0 "
        "&& getComputedStyle(image).objectFit === 'cover' "
        "&& getComputedStyle(image).aspectRatio === '4 / 3') && images.map("
        "image => { const {width, height} = image.getBoundingClientRect(); "
        "return [width, height]; })"
    )
    assert all(
        abs(layout[0] - dish_image_layouts[0][0]) < 1
        and abs(layout[1] - dish_image_layouts[0][1]) < 1
        for layout in dish_image_layouts
    )
    assert gallery.count() == 12
    gallery_image_layouts = gallery.evaluate_all(
        "images => images.every(image => image.complete && image.naturalWidth > 0 "
        "&& getComputedStyle(image).objectFit === 'cover' "
        "&& getComputedStyle(image.parentElement).aspectRatio === '4 / 3') "
        "&& images.map(image => { const {width, height} = "
        "image.getBoundingClientRect(); return [width, height]; })"
    )
    assert all(
        abs(layout[0] - gallery_image_layouts[0][0]) < 1
        and abs(layout[1] - gallery_image_layouts[0][1]) < 1
        for layout in gallery_image_layouts
    )

    first_image = gallery.first
    image_url = first_image.evaluate("(image) => image.src")
    first_image.click()

    playwright_page.locator("#lightbox").wait_for(state="visible")
    assert playwright_page.locator("#lightbox-img").get_attribute("src") == image_url
    assert playwright_page.locator("#lightbox-img").evaluate(
        "(image) => image.complete && image.naturalWidth > 0"
    )

    image_bounds = playwright_page.locator("#lightbox-img").bounding_box()
    previous_bounds = playwright_page.get_by_role(
        "button", name="Previous picture"
    ).bounding_box()
    next_bounds = playwright_page.get_by_role(
        "button", name="Next picture"
    ).bounding_box()
    assert image_bounds is not None
    assert previous_bounds is not None
    assert next_bounds is not None
    assert previous_bounds["x"] + previous_bounds["width"] <= image_bounds["x"]
    assert next_bounds["x"] >= image_bounds["x"] + image_bounds["width"]


def test_dish_card_read_more_expands_and_collapses(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(
        f"{base_url}/Artisinal_Creations.html", wait_until="domcontentloaded"
    )
    card = playwright_page.locator(".dish-card").first
    more_text = card.locator(".more-text")
    read_more = card.get_by_role("button", name="Read more")

    assert "hidden" in (more_text.get_attribute("class") or "")
    read_more.click()
    assert "hidden" not in (more_text.get_attribute("class") or "")
    assert card.get_by_role("button", name="Show less").is_visible()

    card.get_by_role("button", name="Show less").click()
    assert "hidden" in (more_text.get_attribute("class") or "")


def test_sections_fade_in_when_scrolled(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")
    sections = playwright_page.locator("section:not(.hidden)")

    assert sections.count() > 1
    first_section = sections.first
    first_section.wait_for()
    assert "fade-in-section" in (first_section.get_attribute("class") or "")
    assert "is-visible" in (first_section.get_attribute("class") or "")

    last_section = sections.last
    last_section.scroll_into_view_if_needed()
    playwright_page.wait_for_function(
        "element => element.classList.contains('is-visible')",
        arg=last_section.element_handle(),
    )


def test_reduced_motion_keeps_sections_visible(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.emulate_media(reduced_motion="reduce")
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")
    section = playwright_page.locator("section:not(.hidden)").first

    assert "is-visible" in (section.get_attribute("class") or "")
    assert playwright_page.locator("body").evaluate(
        "body => getComputedStyle(body).animationName"
    ) == "none"


def test_home_qualification_items_expand_with_description_and_image(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")
    qualifications = playwright_page.locator("#qualification-list")
    items = qualifications.locator("details.qualification-item")

    assert items.count() == 7

    for item in items.all():
        summary = item.locator(":scope > summary")
        summary.scroll_into_view_if_needed()
        summary.click()

        details = item.locator(".qualification-details")
        assert details.is_visible()
        assert details.locator("p").inner_text().strip()
        image = details.locator("img")
        assert image.get_attribute("alt")
        playwright_page.wait_for_function(
            "image => image.complete && image.naturalWidth > 0",
            arg=image.element_handle(),
        )
        assert image.evaluate("image => image.naturalWidth > 0")
        image_box = image.bounding_box()
        description_box = details.locator("p").bounding_box()
        assert image_box is not None
        assert description_box is not None
        assert image_box["x"] >= description_box["x"] + description_box["width"]

        summary.click()
        assert not details.is_visible()


def test_fade_in_uses_slower_timing(
    playwright_page: object, base_url: str
) -> None:
    playwright_page.goto(f"{base_url}/index.html", wait_until="domcontentloaded")

    durations = playwright_page.locator("section:not(.hidden)").first.evaluate(
        """section => ({
            page: getComputedStyle(document.body).animationDuration,
            section: getComputedStyle(section).transitionDuration
        })"""
    )

    assert durations["page"] == "1.5s"
    assert durations["section"] == "1.4s, 1.4s"
