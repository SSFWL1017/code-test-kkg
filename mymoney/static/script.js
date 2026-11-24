
// 월별 수입·지출 그래프
const monthlyCanvas = document.getElementById("monthlyChart");

if (monthlyCanvas) {
    new Chart(monthlyCanvas, {
        type: "line",
        data: {
            labels: chartLabels,
            datasets: [
                {
                    label: "수입",
                    data: chartIncome,
                    borderColor: "#18a879",
                    backgroundColor: "rgba(24, 168, 121, 0.10)",
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4
                },
                {
                    label: "지출",
                    data: chartExpense,
                    borderColor: "#e66b78",
                    backgroundColor: "rgba(230, 107, 120, 0.08)",
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: "#f0f2f7"
                    },
                    ticks: {
                        callback: value => value.toLocaleString() + "원"
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 전체 수입·지출 비율 도넛 그래프
const flowCanvas = document.getElementById("flowChart");

if (flowCanvas) {
    new Chart(flowCanvas, {
        type: "doughnut",
        data: {
            labels: ["수입", "지출"],
            datasets: [{
                data: [totalIncome, totalExpense],
                backgroundColor: ["#18a879", "#e66b78"],
                borderWidth: 0,
                hoverOffset: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "72%",
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
