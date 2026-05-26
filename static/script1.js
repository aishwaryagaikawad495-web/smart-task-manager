document.addEventListener("DOMContentLoaded", () => {

    // Progress bar
    const analyticsFill = document.querySelector(".analytics-fill");

    if (analyticsFill) {

        const width = analyticsFill.dataset.width || 0;

        setTimeout(() => {
            analyticsFill.style.width = width + "%";
        }, 300);
    }

    // Animated bars
    const chartBars = document.querySelectorAll(".chart-bar");

    chartBars.forEach((bar) => {

        const height = bar.dataset.height || 0;

        setTimeout(() => {
            bar.style.height = height + "px";
        }, 300);
    });


    // PIE CHART
    const pieCanvas = document.getElementById("taskPieChart");

    if (pieCanvas) {

        new Chart(pieCanvas, {

            type: "doughnut",

            data: {

                labels: ["Completed", "Pending", "Overdue"],

                datasets: [{
                    data: [
                        completedTasks,
                        pendingTasks,
                        overdueTasks
                    ],

                    backgroundColor: [
                        "#00adb5",
                        "#ffc107",
                        "#dc3545"
                    ]
                }]
            },

            options: {
                responsive: true
            }
        });
    }


    // LINE CHART
    const trendCanvas = document.getElementById("trendChart");

    if (trendCanvas) {

        new Chart(trendCanvas, {

            type: "line",

            data: {

                labels: [
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat",
                    "Sun"
                ],

                datasets: [{

                    label: "Completed Tasks",

                    data: weeklyData,

                    borderColor: "#00adb5",

                    backgroundColor: "rgba(0,173,181,0.2)",

                    tension: 0.4,

                    fill: true
                }]
            },

            options: {
                responsive: true
            }
        });
    }

});