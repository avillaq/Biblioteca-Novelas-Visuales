const customSelects = document.querySelectorAll(".custom-select");

customSelects.forEach(function(select) {
    const classes = select.getAttribute("class");
    let template = `<div class="${classes}">
                                        <span class="custom-select-trigger">${select.selectedOptions[0].text}</span>
                                        <div class="custom-options">`;

    const options = select.querySelectorAll("option");
    options.forEach(function(option) {
        template += `<span class="custom-option" data-value="${option.getAttribute("value")}">${option.innerHTML}</span>`;
    });

    template += `</div></div>`;

    

    select.insertAdjacentHTML("afterend", template);
});


// Open/close select
const triggers = document.querySelectorAll(".custom-select-trigger");
triggers.forEach(function(trigger) {
    trigger.addEventListener("click", function(e) {
        const currentSelect = this.closest(".custom-select");

        /* Close all other select boxes */
        document.querySelectorAll(".custom-select").forEach(function (select) {
            if (select !== currentSelect) {
                select.classList.remove("opened");
            }
        });

        currentSelect.classList.toggle("opened");
    });
});


const customOptions = document.querySelectorAll(".custom-option");
customOptions.forEach(function(option) {
    option.addEventListener("click", function(e) {
        
        // Set the value of the original select element
        const select = this.closest(".custom-select").previousElementSibling;
        select.value = this.getAttribute("data-value");
        console.log(select.value);

        const options = this.closest(".custom-options").querySelectorAll(".custom-option");
        options.forEach(function(option) {
            option.classList.remove("selection");
        });

        this.classList.add("selection");
        this.closest(".custom-select").classList.remove("opened");
        this.closest(".custom-select").querySelector(".custom-select-trigger").textContent = this.textContent;
    });
});
