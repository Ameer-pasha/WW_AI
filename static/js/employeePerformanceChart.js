// Employee Performance Trend Chart - Current Month vs Previous Month
// For Employee Detail View page

function initEmployeePerformanceChart() {
    console.log('=== EMPLOYEE PERFORMANCE CHART INITIALIZATION ===');

    // Get employee ID from multiple possible sources
    let employeeId = null;

    // Method 1: From URL path (e.g., /employee/123 or /employee_detail/123)
    const pathParts = window.location.pathname.split('/');
    const lastPart = pathParts[pathParts.length - 1];
    if (!isNaN(lastPart) && lastPart !== '') {
        employeeId = lastPart;
        console.log('Employee ID from URL:', employeeId);
    }

    // Method 2: From data attribute on body or main element
    if (!employeeId) {
        const mainElement = document.querySelector('main');
        if (mainElement && mainElement.dataset.employeeId) {
            employeeId = mainElement.dataset.employeeId;
            console.log('Employee ID from data attribute:', employeeId);
        }
    }

    // Method 3: From a hidden input or element
    if (!employeeId) {
        const hiddenInput = document.getElementById('employee-id');
        if (hiddenInput) {
            employeeId = hiddenInput.value;
            console.log('Employee ID from hidden input:', employeeId);
        }
    }

    if (!employeeId) {
        console.error('❌ Could not determine employee ID!');
        console.log('Current URL:', window.location.pathname);
        showError('Unable to determine employee ID');
        return;
    }

    console.log('✅ Using employee ID:', employeeId);

    // Look for chart container
    let container = document.querySelector('.chart-placeholder');

    if (!container) {
        console.error('❌ Chart container (.chart-placeholder) not found!');
        return;
    }

    console.log('✅ Chart container found');

    // Create canvas element if it doesn't exist
    let canvas = container.querySelector('canvas');
    if (!canvas) {
        console.log('Creating new canvas element...');
        canvas = document.createElement('canvas');
        canvas.id = 'employeePerformanceChart';
        canvas.style.maxHeight = '350px';
        // Clear placeholder content and add canvas
        container.innerHTML = '';
        container.appendChild(canvas);
        container.style.background = 'transparent';
        container.style.padding = '0';
    }

    console.log('✅ Canvas ready');

    // Show loading message
    const loadingMsg = document.createElement('p');
    loadingMsg.textContent = 'Loading chart...';
    loadingMsg.style.textAlign = 'center';
    loadingMsg.style.color = '#666';
    loadingMsg.style.padding = '20px';
    container.appendChild(loadingMsg);

    const apiUrl = `/employee_performance_data/${employeeId}`;
    console.log('Fetching data from:', apiUrl);

    // Fetch employee performance data from the API
    fetch(apiUrl)
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response OK:', response.ok);

            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP ${response.status}`);
                }).catch(() => {
                    throw new Error(`HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('✅ Data received:', data);

            // Remove loading message
            if (loadingMsg.parentElement) {
                loadingMsg.remove();
            }

            // Validate data structure
            if (!data.labels || !Array.isArray(data.labels) || data.labels.length === 0) {
                throw new Error('Invalid data: missing or empty labels');
            }

            if (!data.current_month) {
                throw new Error('Invalid data: missing current_month');
            }

            if (!data.previous_month) {
                throw new Error('Invalid data: missing previous_month');
            }

            console.log('✅ Data validation passed');

            const ctx = canvas.getContext('2d');

            // Destroy existing chart if it exists
            if (window.employeePerformanceChartInstance) {
                console.log('Destroying existing chart...');
                window.employeePerformanceChartInstance.destroy();
            }

            // Create new chart
            console.log('Creating chart...');
            window.employeePerformanceChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Current Month',
                            data: data.current_month,
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
                            label: 'Previous Month',
                            data: data.previous_month,
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
                    aspectRatio: 2.5,
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
                                }
                            },
                            title: {
                                display: true,
                                text: 'Week',
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

            console.log('✅ Employee performance chart created successfully!');
        })
        .catch(error => {
            console.error('❌ Error loading chart:', error);
            console.error('Error details:', error.message);
            showError(error.message);
        });
}

function showError(message) {
    const container = document.querySelector('.chart-placeholder');
    if (container) {
        container.innerHTML = `
            <div style="text-align: center; color: #dc3545; padding: 40px; background: #fff3cd; border-radius: 8px; border: 1px solid #ffc107;">
                <span class="material-icons" style="font-size: 48px; margin-bottom: 10px;">error_outline</span>
                <p style="margin: 0; font-weight: 600;">Unable to load performance chart</p>
                <p style="margin: 5px 0 0 0; font-size: 0.9em;">${message}</p>
                <p style="margin: 10px 0 0 0; font-size: 0.85em; color: #666;">Check browser console (F12) for details</p>
            </div>
        `;
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmployeePerformanceChart);
} else {
    // DOM already loaded
    initEmployeePerformanceChart();
}