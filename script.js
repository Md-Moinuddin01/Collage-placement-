document.addEventListener("DOMContentLoaded", function () {
    setupMenu();
    setupDarkMode();
    setupScrollTop();
    setupCompanySearch();
    setupStudentSearch();
    setupApplyButtons();
    setupLoginForm();
    setupResumeUpload();
    setupInterviewButtons();
    setupCodingTest();
    setupContactForm();
    setupFaq();
});

function setupMenu() {
    var menuBtn = document.getElementById("menuBtn");
    var navLinks = document.getElementById("navLinks");

    if (!menuBtn || !navLinks) {
        return;
    }

    menuBtn.addEventListener("click", function () {
        navLinks.classList.toggle("show");
    });
}

function setupDarkMode() {
    var darkToggle = document.getElementById("darkToggle");
    var savedMode = localStorage.getItem("ggitsDarkMode");

    if (savedMode === "yes") {
        document.body.classList.add("dark-mode");
    }

    if (!darkToggle) {
        return;
    }

    updateDarkButton(darkToggle);

    darkToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("ggitsDarkMode", "yes");
        } else {
            localStorage.setItem("ggitsDarkMode", "no");
        }

        updateDarkButton(darkToggle);
    });
}

function updateDarkButton(button) {
    if (document.body.classList.contains("dark-mode")) {
        button.textContent = "Light";
    } else {
        button.textContent = "Dark";
    }
}

function setupScrollTop() {
    var scrollTop = document.getElementById("scrollTop");

    if (!scrollTop) {
        return;
    }

    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            scrollTop.classList.add("show");
        } else {
            scrollTop.classList.remove("show");
        }
    });

    scrollTop.addEventListener("click", function () {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });
}

function setupCompanySearch() {
    var input = document.getElementById("companySearch");
    var cards = document.querySelectorAll(".company-card");

    if (!input || cards.length === 0) {
        return;
    }

    input.addEventListener("input", function () {
        var searchText = input.value.toLowerCase();

        cards.forEach(function (card) {
            var companyName = card.getAttribute("data-name").toLowerCase();

            if (companyName.indexOf(searchText) !== -1) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
}

function setupStudentSearch() {
    var input = document.getElementById("studentSearch");
    var table = document.getElementById("studentTable");

    if (!input || !table) {
        return;
    }

    input.addEventListener("input", function () {
        var searchText = input.value.toLowerCase();
        var rows = table.querySelectorAll("tbody tr");

        rows.forEach(function (row) {
            var rowText = row.textContent.toLowerCase();

            if (rowText.indexOf(searchText) !== -1) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
}

function setupApplyButtons() {
    var buttons = document.querySelectorAll(".apply-btn");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            var card = button.closest(".company-card");
            var name = card.querySelector("h3").textContent;

            button.textContent = "Applied";
            button.disabled = true;
            button.style.opacity = "0.8";

            showSmallMessage("Application submitted for " + name + ".");
        });
    });
}

function setupLoginForm() {
    var form = document.getElementById("loginForm");
    var message = document.getElementById("loginMessage");

    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        message.textContent = "Demo login successful. Redirecting to dashboard...";

        setTimeout(function () {
            window.location.href = "dashboard.html";
        }, 800);
    });
}

function setupResumeUpload() {
    var button = document.getElementById("resumeBtn");
    var fileInput = document.getElementById("resumeFile");
    var message = document.getElementById("resumeMessage");

    if (!button || !fileInput || !message) {
        return;
    }

    button.addEventListener("click", function () {
        if (fileInput.files.length === 0) {
            message.textContent = "Please choose a resume file first.";
            message.style.color = "#b91c1c";
            return;
        }

        message.textContent = "Resume uploaded. Dummy ATS score generated below.";
        message.style.color = "#15803d";
    });
}

function setupInterviewButtons() {
    var startBtn = document.getElementById("startInterview");
    var endBtn = document.getElementById("endInterview");
    var message = document.getElementById("interviewMessage");

    if (!startBtn || !endBtn || !message) {
        return;
    }

    startBtn.addEventListener("click", function () {
        message.textContent = "Interview started. Answer the questions one by one.";
        message.style.color = "#2563EB";
    });

    endBtn.addEventListener("click", function () {
        message.textContent = "Interview ended. Feedback updated with sample scores.";
        message.style.color = "#15803d";
    });
}

function setupCodingTest() {
    var timer = document.getElementById("timer");
    var submitBtn = document.getElementById("submitCode");
    var score = document.getElementById("codingScore");
    var result = document.getElementById("codingResult");

    if (timer) {
        startDemoTimer(timer);
    }

    if (!submitBtn || !score || !result) {
        return;
    }

    submitBtn.addEventListener("click", function () {
        score.textContent = "78%";
        result.textContent = "Good attempt. Improve edge case handling and code comments.";
        submitBtn.textContent = "Submitted";
        submitBtn.disabled = true;
    });
}

function startDemoTimer(timerElement) {
    var secondsLeft = 20 * 60;

    setInterval(function () {
        if (secondsLeft <= 0) {
            timerElement.textContent = "00:00";
            return;
        }

        secondsLeft--;
        var minutes = Math.floor(secondsLeft / 60);
        var seconds = secondsLeft % 60;
        timerElement.textContent = padNumber(minutes) + ":" + padNumber(seconds);
    }, 1000);
}

function padNumber(number) {
    if (number < 10) {
        return "0" + number;
    }
    return number;
}

function setupContactForm() {
    var form = document.getElementById("contactForm");
    var message = document.getElementById("contactMessage");

    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        message.textContent = "Thanks, your feedback has been saved for demo.";
        form.reset();
    });
}

function setupFaq() {
    var items = document.querySelectorAll(".faq-item");

    items.forEach(function (item) {
        var button = item.querySelector("button");

        button.addEventListener("click", function () {
            item.classList.toggle("open");
        });
    });
}

function showSmallMessage(text) {
    var box = document.createElement("div");
    box.textContent = text;
    box.style.position = "fixed";
    box.style.left = "50%";
    box.style.bottom = "28px";
    box.style.transform = "translateX(-50%)";
    box.style.background = "#1E3A8A";
    box.style.color = "#ffffff";
    box.style.padding = "12px 18px";
    box.style.borderRadius = "8px";
    box.style.boxShadow = "0 10px 24px rgba(0,0,0,0.18)";
    box.style.zIndex = "50";

    document.body.appendChild(box);

    setTimeout(function () {
        box.remove();
    }, 2200);
}

function loadDemoStats() {
    fetch("/api/stats")
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log("Demo stats loaded", data);
        })
        .catch(function () {
            console.log("Flask API not running. Static page still works.");
        });
}

loadDemoStats();
