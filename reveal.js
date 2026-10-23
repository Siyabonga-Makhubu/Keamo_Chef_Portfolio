(() => {
  const style = document.createElement("style");
  style.textContent = `
    @keyframes page-fade-in {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    body.page-fade-in {
      animation: page-fade-in 1500ms ease-out both;
    }

    .fade-in-section {
      opacity: 0;
      transform: translateY(24px);
      transition: opacity 1400ms ease-in-out, transform 1400ms ease-in-out;
    }

    .fade-in-section.is-visible {
      opacity: 1;
      transform: translateY(0);
    }

    @media (prefers-reduced-motion: reduce) {
      body.page-fade-in {
        animation: none;
      }

      .fade-in-section {
        opacity: 1;
        transform: none;
        transition: none;
      }
    }
  `;
  document.head.append(style);
  document.body.classList.add("page-fade-in");

  const sections = [
    ...document.querySelectorAll("section:not(.hidden), footer"),
  ];

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    sections.forEach((section) => section.classList.add("is-visible"));
    return;
  }

  if (!("IntersectionObserver" in window)) {
    sections.forEach((section) => section.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries, currentObserver) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        entry.target.classList.add("is-visible");
        currentObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" },
  );

  sections.forEach((section) => {
    section.classList.add("fade-in-section");
    observer.observe(section);
  });
})();
