# Keamogetswe Moagi — Chef Portfolio

A responsive portfolio website for South African chef Keamogetswe Moagi. It presents his culinary profile, skills, qualifications, work history, food photography, and contact information.

**Live site:** [Keamo Chef Portfolio](https://siyabonga-makhubu.github.io/Keamo_Chef_Portfolio/)

## Pages

- `index.html` — Home page and portfolio overview
- `About.html` — Chef profile
- `Skills.html` — Culinary skills
- `Artisinal_Creations.html` — Food and event gallery
- `education.html` — Education and qualifications
- `experience.html` — Work experience
- `contact.html` — Contact details and enquiry form
- `register.html`, `admin.html`, and `dashboard.html` — Registration and admin interface pages

## Tech stack

- HTML, CSS, and vanilla JavaScript; no build step is required
- Tailwind CSS and Lucide icons loaded from CDNs
- Python `http.server` for local preview
- GitHub Actions and GitHub Pages for deployment
- Git LFS for selected large media files

## Run locally

From the project root, start a local web server:

```powershell
python -m http.server 8000
```

Open [http://localhost:8000/](http://localhost:8000/) in your browser. Serving over HTTP is recommended instead of opening HTML files directly. The site loads some styling and icons from external CDNs, so an internet connection is needed for those resources.

## Contact form

The portfolio enquiry form validates the visitor's details and opens WhatsApp with a prefilled message. The visitor reviews and sends the message in WhatsApp; enquiries are not submitted to a portfolio backend.

The destination number is set in `contact-config.js` as `window.CHEF_WHATSAPP_NUMBER`. Use the international number as digits only, without a plus sign, spaces, or punctuation. This value is public contact information, not a secret.

## Registration and admin pages

The registration and admin interface pages call an API at `http://localhost:5055/api` for registration, login, profile, and admin message operations. That backend is not included in this static-site repository, so those features require a separately running compatible API and are not available on the GitHub Pages deployment by default.

## Tests

The browser automation suite uses pytest with Playwright and Selenium. Install its dependencies and Playwright's Chromium browser with:

```powershell
python -m pip install -r requirements-test.txt
python -m playwright install chromium
```

Run the suite:

```powershell
python -m pytest
```

See [TESTING.md](TESTING.md) for browser-specific commands, Selenium setup, and manual contact-form checks.

## Deploy

The workflow in `.github/workflows/deploy-pages.yml` deploys the static site to GitHub Pages when changes are pushed to `main`. It can also be run manually from the repository's **Actions** tab. In repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**.

The workflow fetches the portfolio videos from Git LFS and publishes the site's HTML, JavaScript, CSS, and image assets. To work with the full media locally after cloning, install Git LFS and fetch the assets:

```powershell
git lfs install
git lfs pull
```
