const btn = document.getElementById("darkToggle");

// APPLY saved theme on page load
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}

// toggle button click
if (btn) {
    btn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        // save preference
        if (document.body.classList.contains("dark")) {
            localStorage.setItem("theme", "dark");
            btn.innerText = "☀️";
        } else {
            localStorage.setItem("theme", "light");
            btn.innerText = "🌙";
        }
    });
}
if (btn) {
    if (localStorage.getItem("theme") === "dark") {
        btn.innerText = "☀️";
    } else {
        btn.innerText = "🌙";
    }
}