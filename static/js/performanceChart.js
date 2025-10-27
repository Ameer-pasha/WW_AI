// Team Performance Chart - Current Week vs Previous Week
// For AI Insights page

function initTeamPerformanceChart() {
    console.log('Initializing team performance chart...');
    
    const canvas = document.getElementById('teamPerformanceChart');
    
    if (!canvas) {
        console.error('teamPerformanceChart canvas not found in DOM!');
        return;
    }
    
    console.log('Canvas found, fetching data from /performance_data...');
    
    // Fetch team performance data from the API
    fetch('/performance_data')
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            
            // Validate data structure
            if (!data.labels || !Array.isArray(data.labels) || data.labels.length === 0) {
                throw new Error('Invalid data structure: missing or empty labels');
            }
            
            if (!data.current_week) {
                throw new Error('Invalid data structure: missing current_week data');
            }
            
            const ctx = canvas.getContext('2d');
            
            // Destroy existing chart if it exists (prevents duplicates)
            if (window.teamPerformanceChartInstance) {
                window.teamPerformanceChartInstance.destroy();
            }
            
            // Prepare datasets based on user role
            const datasets = [
                {
                    label: 'Current Week',
                    data: data.current_week,
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
            ];
            
            // Add previous week data if available (for manager view)
            if (data.previous_week && data.previous_week.length > 0) {
                datasets.push({
                    label: 'Previous Week',
                    data: data.previous_week,
                    backgroundColor: 'rgba(108, 117, 125, 0.2)',
                    borderColor: 'rgba(108, 117, 125, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 6,
                    pointBackgroundColor: 'rgba(108, 117, 125, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointHoverRadius: 8
                });
                
                // Show legend if we have both weeks
                const legendElement = document.querySelector('.chart-legend');
                if (legendElement) {
                    legendElement.style.display = 'block';
                }
            }
            
            // Create new chart instance
            window.teamPerformanceChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: datasets
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
                                    return context.dataset.label + ': ' + context.parsed.y + ' pts';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + ' pts';
                                },
                                font: {
                                    size: 11,
                                    family: 'Inter, sans-serif'
                                },
                                stepSize: 20
                            },
                            title: {
                                display: true,
                                text: 'Performance Score',
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
                                },
                                maxRotation: 45,
                                minRotation: 0
                            },
                            title: {
                                display: true,
                                text: data.previous_week && data.previous_week.length > 0 ? 'Team Members' : 'Weekly Progress',
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
            
            console.log('Team performance chart created successfully');
        })
        .catch(error => {
            console.error('Error loading team performance chart:', error);
            const container = canvas.parentElement;
            if (container) {
                container.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">Unable to load performance chart. Please try again later.</p>';
            }
        });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTeamPerformanceChart);
} else {
    // DOM already loaded
    initTeamPerformanceChart();
}