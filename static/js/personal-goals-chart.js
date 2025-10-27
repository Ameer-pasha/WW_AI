// Personal Goals Chart - Planned vs Actual
document.addEventListener('DOMContentLoaded', function() {
    console.log('Personal goals chart script loaded');

    const canvas = document.getElementById('personalGoalsChart');

    if (!canvas) {
        console.error('personalGoalsChart canvas not found!');
        return;
    }

    console.log('Canvas found, fetching personal goals data...');

    // Fetch personal performance data from the API
    fetch('/personal_performance_data')
        .then(response => {
            console.log('Response received:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            const ctx = canvas.getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Actual Goals',
                            data: data.actual,
                            backgroundColor: 'rgba(40, 167, 69, 0.2)',
                            borderColor: 'rgba(40, 167, 69, 1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 6,
                            pointBackgroundColor: 'rgba(40, 167, 69, 1)',
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointHoverRadius: 8
                        },
                        {
                            label: 'Planned Goals',
                            data: data.planned,
                            backgroundColor: 'rgba(0, 123, 255, 0.2)',
                            borderColor: 'rgba(0, 123, 255, 1)',
                            borderWidth: 3,
                            fill: true,
                            tension: 0.4,
                            pointRadius: 6,
                            pointBackgroundColor: 'rgba(0, 123, 255, 1)',
                            pointBorderColor: '#fff',
                            pointBorderWidth: 2,
                            pointHoverRadius: 8
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                font: {
                                    size: 12,
                                    family: 'Inter, sans-serif'
                                },
                                padding: 15,
                                usePointStyle: true,
                                boxWidth: 12,
                                boxHeight: 12
                            }
                        },
                        title: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            padding: 12,
                            titleFont: {
                                size: 13,
                                family: 'Inter, sans-serif'
                            },
                            bodyFont: {
                                size: 12,
                                family: 'Inter, sans-serif'
                            },
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': ' + context.parsed.y + ' goals';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return value + ' goals';
                                },
                                font: {
                                    size: 11,
                                    family: 'Inter, sans-serif'
                                },
                                stepSize: 5
                            },
                            title: {
                                display: true,
                                text: 'Number of Goals',
                                font: {
                                    size: 12,
                                    family: 'Inter, sans-serif',
                                    weight: '600'
                                }
                            },
                            grid: {
                                color: 'rgba(0, 0, 0, 0.05)'
                            }
                        },
                        x: {
                            ticks: {
                                font: {
                                    size: 11,
                                    family: 'Inter, sans-serif'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Weekly Progress',
                                font: {
                                    size: 12,
                                    family: 'Inter, sans-serif',
                                    weight: '600'
                                }
                            },
                            grid: {
                                display: false
                            }
                        }
                    }
                }
            });

            console.log('Personal goals chart created successfully');
        })
        .catch(error => {
            console.error('Error fetching or rendering chart:', error);
            canvas.parentElement.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">Unable to load goals chart. Please try again later.</p>';
        });
});