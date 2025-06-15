
document.addEventListener('DOMContentLoaded', function () {
    console.log("De-kadmo Portal JavaScript loaded.");

    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function () {
            alert("Form submitted successfully!");
        });
    });
});
