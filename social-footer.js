(() => {
  const footer =
    document.querySelector("footer") || document.body.appendChild(
      document.createElement("footer"),
    );
  footer.classList.add("site-footer");

  if (!footer.querySelector("[data-template-id='footer-text']")) {
    const copyright = document.createElement("p");
    copyright.dataset.templateId = "footer-text";
    copyright.className = "canva-text text-sm";
    copyright.textContent =
      "© 2026 Chef Keamogetswe Moagi. All rights reserved.";
    footer.appendChild(copyright);
  }

  const socialLinks = document.createElement("nav");

  socialLinks.className = "footer-social-links";
  socialLinks.setAttribute("aria-label", "Social media");
  socialLinks.innerHTML = `
    <a href="https://wa.me/27834806216" target="_blank"
       rel="noopener noreferrer" aria-label="Chat on WhatsApp">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.7 6L.2 24l6.4-1.7a11.8 11.8 0 0 0 5.5 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.5-8.4ZM12.1 21.7c-1.7 0-3.4-.5-4.8-1.3l-.3-.2-3.8 1 1-3.7-.2-.4a9.8 9.8 0 1 1 8.1 4.6Zm5.4-7.4c-.3-.2-1.7-.9-2-.9-.3-.1-.5-.2-.7.2-.2.3-.8.9-1 1.1-.2.2-.4.2-.7.1-.3-.2-1.2-.4-2.3-1.4-.9-.8-1.5-1.7-1.7-2-.2-.3 0-.5.1-.7l.5-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5-.1-.2-.7-1.6-1-2.2-.2-.5-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1.1 1.1-1.1 2.5s1.1 2.9 1.2 3.1c.2.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.3.2-.6.2-1.2.2-1.3-.1-.2-.3-.3-.6-.4Z"/>
      </svg>
    </a>
    <a href="https://www.instagram.com/" target="_blank"
       rel="noopener noreferrer" aria-label="Open Instagram">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2.2A2.8 2.8 0 0 0 4.2 7v10A2.8 2.8 0 0 0 7 19.8h10a2.8 2.8 0 0 0 2.8-2.8V7A2.8 2.8 0 0 0 17 4.2H7Zm5 2.1a5.7 5.7 0 1 1 0 11.4 5.7 5.7 0 0 1 0-11.4Zm0 2.2a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Zm5.9-3.1a1.3 1.3 0 1 1 0 2.6 1.3 1.3 0 0 1 0-2.6Z"/>
      </svg>
    </a>
  `;
  footer.appendChild(socialLinks);

  const style = document.createElement("style");
  style.textContent = `
    .site-footer {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
      align-items: center;
      gap: 24px;
      text-align: center;
    }

    .site-footer > [data-template-id="footer-text"] {
      grid-column: 2;
      margin: 0;
    }

    .footer-social-links {
      display: flex;
      grid-column: 3;
      justify-self: end;
      align-items: center;
      gap: 18px;
      flex-shrink: 0;
      margin: 0;
    }

    .footer-social-links a {
      display: inline-flex;
      width: 44px;
      height: 44px;
      align-items: center;
      justify-content: center;
      color: #9ca3af;
      border: 1px solid #374151;
      border-radius: 50%;
      transition: color 180ms ease, border-color 180ms ease,
        transform 180ms ease;
    }

    .footer-social-links a:hover,
    .footer-social-links a:focus-visible {
      color: #38bdf8;
      border-color: #38bdf8;
      transform: translateY(-2px);
    }

    .footer-social-links svg {
      width: 22px;
      height: 22px;
      fill: currentColor;
    }

    @media (max-width: 480px) {
      .site-footer {
        gap: 12px;
      }

      .site-footer > [data-template-id="footer-text"] {
        font-size: 12px;
        overflow-wrap: anywhere;
      }

      .footer-social-links {
        gap: 8px;
      }

      .footer-social-links a {
        width: 38px;
        height: 38px;
      }
    }
  `;
  document.head.appendChild(style);
})();
