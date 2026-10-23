(() => {
    const form = document.getElementById("contact-form");
    const status = document.getElementById("whatsapp-status");

    if (!form || !status) return;

    const fields = {
        name: document.getElementById("name"),
        phone: document.getElementById("phone"),
        enquiryType: document.getElementById("enquiry-type"),
        message: document.getElementById("message")
    };
    const submitButton = form.querySelector('button[type="submit"]');
    let isSubmitting = false;

    const fieldErrors = {
        name: document.getElementById("name-error"),
        phone: document.getElementById("phone-error"),
        enquiryType: document.getElementById("enquiry-type-error"),
        message: document.getElementById("message-error")
    };

    function setFieldError(fieldName, message) {
        const field = fields[fieldName];
        const error = fieldErrors[fieldName];
        field.setAttribute("aria-invalid", message ? "true" : "false");
        error.textContent = message;
    }

    function showStatus(message, isError) {
        status.textContent = message;
        status.setAttribute("role", isError ? "alert" : "status");
        status.classList.remove("hidden");
        status.classList.toggle("form-error", isError);
        status.classList.toggle("form-success", !isError);
    }

    Object.keys(fields).forEach((fieldName) => {
        const eventName = fieldName === "enquiryType" ? "change" : "input";
        fields[fieldName].addEventListener(eventName, () => {
            setFieldError(fieldName, "");
        });
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (isSubmitting) return;

        const name = fields.name.value.trim();
        const rawPhone = fields.phone.value.trim();
        const enquiryType = fields.enquiryType.value;
        const message = fields.message.value.trim();
        const phoneDigits = rawPhone.replace(/\D/g, "");
        const phoneIsValid =
            /^\+?[\d\s().-]+$/.test(rawPhone) &&
            phoneDigits.length >= 7 &&
            phoneDigits.length <= 15;

        const values = {
            name: name ? "" : "Enter your full name.",
            phone: !rawPhone
                ? "Enter your phone number."
                : phoneIsValid
                    ? ""
                    : "Enter a valid phone number with 7 to 15 digits.",
            enquiryType: enquiryType ? "" : "Select a type of enquiry.",
            message: message ? "" : "Enter a message."
        };

        Object.keys(values).forEach((fieldName) => {
            setFieldError(fieldName, values[fieldName]);
        });

        const firstInvalidField = Object.keys(values).find(
            (fieldName) => values[fieldName]
        );
        if (firstInvalidField) {
            fields[firstInvalidField].focus();
            return;
        }

        const chefNumber = window.CHEF_WHATSAPP_NUMBER;
        if (typeof chefNumber !== "string" || !/^\d{7,15}$/.test(chefNumber)) {
            showStatus(
                "The WhatsApp contact is not configured yet. Please use the contact details shown on this page.",
                true
            );
            return;
        }

        const normalizedPhone =
            `${rawPhone.startsWith("+") ? "+" : ""}${phoneDigits}`;
        const whatsappMessage = [
            "Hello Chef,",
            "",
            "I would like to enquire about your services.",
            "",
            `Customer Name: ${name}`,
            `Customer Phone: ${normalizedPhone}`,
            `Enquiry Type: ${enquiryType}`,
            "",
            "Message:",
            message,
            "",
            "Thank you."
        ].join("\n");
        const whatsappUrl =
            `https://wa.me/${chefNumber}?text=${encodeURIComponent(whatsappMessage)}`;

        isSubmitting = true;
        if (submitButton) submitButton.disabled = true;
        window.open(whatsappUrl, "_blank", "noopener,noreferrer");
        showStatus(
            "WhatsApp should open in a new tab or app. Review your message and press Send to send your enquiry.",
            false
        );
    });
})();
