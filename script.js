// =========================
// CONFIG
// =========================
const API_BASE = "http://localhost:5055/api";

const PASSPHRASE = "chef2026";

let dashboardUnlocked = false;
let currentTab = "registrations";

const handler = {
  onDataChanged(data) {
    const regs = data.filter(d => !d.type || d.type === "registration");
    const msgs = data.filter(d => d.type === "message");

    window.allRegistrations = regs;
    window.allMessages = msgs;

    if (dashboardUnlocked) {
      currentTab === "registrations"
        ? renderRegistrations()
        : renderMessages();
    }
  }
};

window.dataSdk?.init?.(handler);


/* ================= ADMIN ================= */

document.getElementById("admin-btn")?.addEventListener("click", () => {
  document.getElementById("passphrase-modal").classList.remove("hidden");
});

document.getElementById("passphrase-cancel-btn")?.addEventListener("click", () => {
  document.getElementById("passphrase-modal").classList.add("hidden");
});

document.getElementById("passphrase-submit-btn")?.addEventListener("click", () => {
  const val = document.getElementById("passphrase-input").value;

  if (val === PASSPHRASE) {
    openDashboard();
  } else {
    document.getElementById("passphrase-error").innerText =
      "Wrong passphrase";
  }
});

function openDashboard() {
  dashboardUnlocked = true;

  document.getElementById("register-view").classList.add("hidden");
  document.getElementById("navbar").classList.add("hidden");
  document.getElementById("dashboard-view").classList.remove("hidden");

  updateTableHeaders();  // Add this line
  renderRegistrations();
}

/* ================= LOGOUT ================= */

document.getElementById("logout-btn")?.addEventListener("click", () => {
  dashboardUnlocked = false;

  document.getElementById("dashboard-view").classList.add("hidden");
  document.getElementById("register-view").classList.remove("hidden");
  document.getElementById("navbar").classList.remove("hidden");
});

/* ================= TABLES ================= */

function renderRegistrations() {
  const body = document.getElementById("registration-table-body");
  body.innerHTML = "";

  (window.allRegistrations || []).forEach(r => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${r.name}</td>
      <td>${r.email}</td>
      <td>${r.contact}</td>
    `;
    body.appendChild(row);
  });
}

function renderMessages() {
  const body = document.getElementById("messages-table-body");
  body.innerHTML = "";

  (window.allMessages || []).forEach(m => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${m.name}</td>
      <td>${m.email}</td>
      <td>${m.message}</td>
    `;
    body.appendChild(row);
  });
}

/* ================= TABS ================= */

function updateTableHeaders() {
  const regHeader = document.getElementById("registrations-header");
  const msgHeader = document.getElementById("messages-header");

  if (currentTab === "registrations") {
    regHeader.classList.remove("hidden");
    msgHeader.classList.add("hidden");
  } else {
    regHeader.classList.add("hidden");
    msgHeader.classList.remove("hidden");
  }
}

document.getElementById("registrations-link")?.addEventListener("click", () => {
  currentTab = "registrations";
  updateTableHeaders();
  renderRegistrations();
});

document.getElementById("messages-link")?.addEventListener("click", () => {
  currentTab = "messages";
  updateTableHeaders();
  renderMessages();
});

// =========================
// INIT APP
// =========================
document.addEventListener("DOMContentLoaded", () => {
    initLucide();
    initMobileMenu();
    initTypingAnimation();
    initReadMore();
    initLightbox();
    initSlider();
    initContactForm();
    initNotifications();
    initProfile();
    initRegisterForm();
});

// =========================
// LUCIDE ICONS
// =========================
function initLucide() {
    window.lucide?.createIcons?.();
}

// =========================
// MOBILE MENU
// =========================
function initMobileMenu() {
    const mobileBtn = document.getElementById("mobile-menu-btn");

    if (!mobileBtn) return;

    mobileBtn.addEventListener("click", () => {
        const menu = document.getElementById("mobile-menu");
        if (menu) menu.classList.toggle("hidden");
    });
}

// =========================
// TYPING ANIMATION
// =========================
function initTypingAnimation() {
    const el = document.getElementById("typing");
    if (!el) return;

    const roles = ["Private Chef", "Culinary Artist", "Food Stylist", "Menu Creator"];

    let i = 0, j = 0, deleting = false;

    function type() {
        const word = roles[i];

        el.textContent = deleting
            ? word.substring(0, j--)
            : word.substring(0, j++);

        if (!deleting && j > word.length) {
            deleting = true;
            setTimeout(type, 1200);
            return;
        }

        if (deleting && j < 0) {
            deleting = false;
            i = (i + 1) % roles.length;
        }

        setTimeout(type, deleting ? 50 : 100);
    }

    type();
}

// =========================
// READ MORE (FIXED - ONE HANDLER ONLY)
// =========================
function initReadMore() {
    document.querySelectorAll(".read-more").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();

            const card =
                btn.closest(".canva-card") ||
                btn.closest(".dish-card");

            if (!card) return;

            const moreText = card.querySelector(".more-text");
            if (!moreText) return;

            const isHidden = moreText.classList.contains("hidden");

            moreText.classList.toggle("hidden");

            btn.textContent = isHidden ? "Show less" : "Read more";
        });
    });
}

// =========================
// LIGHTBOX
// =========================
function initLightbox() {
    const lightbox = document.getElementById("lightbox");
    const img = document.getElementById("lightbox-img");

    if (!lightbox || !img) return;

    window.openLightbox = (src) => {
        img.src = src;
        lightbox.classList.remove("hidden");
        lightbox.classList.add("flex");
    };

    window.closeLightbox = () => {
        lightbox.classList.add("hidden");
        lightbox.classList.remove("flex");
    };

    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) window.closeLightbox();
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") window.closeLightbox();
    });
}

// =========================
// TESTIMONIAL SLIDER
// =========================
function initSlider() {
    const track = document.getElementById("testimonial-slider");
    const dots = document.querySelectorAll(".dot");

    if (!track) return;

    let index = 0;
    const total = track.children.length;

    function show(i) {
        track.style.transform = `translateX(-${i * 100}%)`;

        dots.forEach((d, idx) => {
            d.classList.toggle("bg-cyan-400", idx === i);
            d.classList.toggle("bg-gray-600", idx !== i);
        });
    }

    setInterval(() => {
        index = (index + 1) % total;
        show(index);
    }, 4000);

    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            index = i;
            show(index);
        });
    });
}

// =========================
// CONTACT FORM (SINGLE CLEAN VERSION)
// =========================
function initContactForm() {
    const form = document.getElementById("contact-form");
    const success = document.getElementById("success-message");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            name: document.getElementById("name")?.value,
            email: document.getElementById("email")?.value,
            subject: document.getElementById("subject")?.value,
            message: document.getElementById("message")?.value
        };

        try {
            const res = await fetch(`${API_BASE}/contact`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) throw new Error();

            if (success) success.classList.remove("hidden");

            form.reset();

            let count =
                parseInt(localStorage.getItem("messageNotification")) || 0;

            localStorage.setItem("messageNotification", count + 1);

            initNotifications();

        } catch (err) {
            console.error(err);
            alert("Failed to send message");
        }
    });
}

// =========================
// NOTIFICATIONS
// =========================
function initNotifications() {
    const bell = document.getElementById("notification-bell");
    const countEl = document.getElementById("notification-count");

    if (!bell || !countEl) return;

    const messages =
        parseInt(localStorage.getItem("messageNotification")) || 0;

    const registrations =
        parseInt(localStorage.getItem("registrationNotification")) || 0;

    const total = messages + registrations;

    if (total > 0) {
        bell.classList.remove("hidden");
        countEl.textContent = total;
    } else {
        bell.classList.add("hidden");
    }
}

// =========================
// PROFILE
// =========================
function initProfile() {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch(`${API_BASE}/profile`, {
        headers: { Authorization: `Bearer ${token}` }
    })
        .then(r => r.json())
        .then(data => {
            const section = document.getElementById("profile-section");
            const username = document.getElementById("username-display");

            if (section && username) {
                section.classList.remove("hidden");
                username.textContent = data.username;
            }
        })
        .catch(console.error);
}

// =========================
// REGISTER FORM (FIXED - NO DUPLICATES)
// =========================
function initRegisterForm() {
    const form = document.getElementById("register-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const error = document.getElementById("error-msg");
        if (error) error.classList.add("hidden");

        const user = {
            name: document.getElementById("reg-name")?.value.trim(),
            email: document.getElementById("reg-email")?.value.trim(),
            contact: document.getElementById("reg-contact")?.value.trim()
        };

        if (!user.name || !user.email || !user.contact) {
            if (error) {
                error.textContent = "Please fill in all fields.";
                error.classList.remove("hidden");
            }
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/users/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(user)
            });

            if (!res.ok) throw new Error();

            const data = await res.json();

            localStorage.setItem("user", JSON.stringify(data.user));

            document.getElementById("register-section")?.classList.add("hidden");
            document.getElementById("success-section")?.classList.remove("hidden");

            window.lucide?.createIcons?.();

            setTimeout(() => {
                window.location.href = "index.html";
            }, 2000);

        } catch (err) {
            if (error) {
                error.textContent = "Registration failed.";
                error.classList.remove("hidden");
            }
        }
    });
}
