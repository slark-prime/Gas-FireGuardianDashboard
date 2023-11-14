// Initialize a Chart.js chart for each sensor field
// Initialize a Chart.js chart for Sensor Field 1
const sensorField1Chart = new Chart(document.getElementById('sensorField1Chart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [], // Will hold our timestamps
        datasets: [
            {
                label: 'Sensor Readings',
                data: [], // Will hold our sensor readings
                borderColor: 'orange',
                borderWidth: 2,
                fill: false,
                pointRadius: 3, // Adjust point size
                pointBackgroundColor: 'orange',
                pointBorderColor: 'orange'
            },
            {
                label: 'Average Value',
                data: [], // Will hold our average values
                borderColor: 'blue',
                borderWidth: 2,
                fill: false,
                pointRadius: 0, // No points for average line
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                    stepSize: 1,
                    displayFormats: {
                        second: 'h:mm:ss a' // Adjust as needed
                    },
                    tooltipFormat: 'll HH:mm:ss' // Format tooltip time
                },
                title: {
                    display: true,
                    text: 'Timestamp'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y;
                        }
                        return label;
                    }
                }
            }
        }
    }
});

// Initialize a Chart.js chart for Sensor Field 2
const sensorField2Chart = new Chart(document.getElementById('sensorField2Chart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [], // Will hold our timestamps
        datasets: [
            {
                label: 'Sensor Readings',
                data: [], // Will hold our sensor readings
                borderColor: 'orange',
                borderWidth: 2,
                fill: false,
                pointRadius: 3, // Adjust point size
                pointBackgroundColor: 'orange',
                pointBorderColor: 'orange'
            },
            {
                label: 'Average Value',
                data: [], // Will hold our average values
                borderColor: 'blue',
                borderWidth: 2,
                fill: false,
                pointRadius: 0, // No points for average line
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                    stepSize: 1,
                    displayFormats: {
                        second: 'h:mm:ss a' // Adjust as needed
                    },
                    tooltipFormat: 'll HH:mm:ss' // Format tooltip time
                },
                title: {
                    display: true,
                    text: 'Timestamp'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y;
                        }
                        return label;
                    }
                }
            }
        }
    }
});


// Initialize a Chart.js chart for Sensor Field 3
const sensorField3Chart = new Chart(document.getElementById('sensorField3Chart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [], // Will hold our timestamps
        datasets: [
            {
                label: 'Sensor Readings',
                data: [], // Will hold our sensor readings
                borderColor: 'orange',
                borderWidth: 2,
                fill: false,
                pointRadius: 3, // Adjust point size
                pointBackgroundColor: 'orange',
                pointBorderColor: 'orange'
            },
            {
                label: 'Average Value',
                data: [], // Will hold our average values
                borderColor: 'blue',
                borderWidth: 2,
                fill: false,
                pointRadius: 0, // No points for average line
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                    stepSize: 1,
                    displayFormats: {
                        second: 'h:mm:ss a' // Adjust as needed
                    },
                    tooltipFormat: 'll HH:mm:ss' // Format tooltip time
                },
                title: {
                    display: true,
                    text: 'Timestamp'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y;
                        }
                        return label;
                    }
                }
            }
        }
    }
});

// Function to check sensor readings and display a warning if necessary
// Function to check sensor readings and display a warning if necessary
// Function to check sensor readings and display a warning if necessary
function checkForDangerousReadings(fieldData, fieldNumber) {
  let message = "";
  let latestReadingTime = null;

  fieldData.readings.forEach((reading, index) => {
    console.log(`Original timestamp [index ${index}]:`, fieldData.timestamps[index]);

    try {
      // Parse the timestamp directly without appending 'Z'
      let date = new Date(fieldData.timestamps[index]);
      console.log(`Parsed Date Object [index ${index}]:`, date);

      // Since the timestamp is already in UTC (indicated by +00:00), we only need to add 8 hours for UTC+8
      date.setTime(date.getTime() + (8 * 60 * 60 * 1000)); // 8 hours in milliseconds
      console.log(`Adjusted Date Object for UTC+8 [index ${index}]:`, date);

      // Convert to ISO string and remove milliseconds and timezone information
      const timestamp = date.toISOString().replace(/\.\d{3}Z$/, 'Z');
      console.log(`Formatted Timestamp for message [index ${index}]:`, timestamp);

    // Conditions for Field 1
    if (fieldNumber === 1) {
      if (reading > 50) {
        message = `On fire at ${timestamp}!`;
        latestReadingTime = timestamp;
      } else if (reading > 40) {
        message = `Warning: High reading detected at ${timestamp}!`;
        latestReadingTime = timestamp;
      }
    }

    // Conditions for Field 2
    else if (fieldNumber === 2) {
      if (reading >= 40 && reading <= 100) {
        message = `Smoke of fire detected at ${timestamp}!`;
        latestReadingTime = timestamp;
      } else if (reading >= 10 && reading <= 40) {
        message = `Alcohol level warning at ${timestamp}.`;
        latestReadingTime = timestamp;
      }
    }

    // Add more conditions for other fields if needed
    // else if (fieldNumber === 3) {
    //   // Similar checks for field3
    // }
    } catch (error) {
      console.error(`Error parsing timestamp [index ${index}]:`, fieldData.timestamps[index], error);
    }
  });

  const warningIndicator = document.getElementById(`warning-indicator-${fieldNumber}`);

  // If a message was set, display it
  if (message) {
    warningIndicator.innerHTML = message;
    warningIndicator.style.display = 'block';
  } else {
    warningIndicator.style.display = 'none';
  }
}


// Function to fetch new data and update the chart
function fetchAndUpdateChart(chart, fieldNumber) {
    fetch(`/data?field=${fieldNumber}`)
        .then(response => response.json())
        .then(data => {
            const fieldKey = `field${fieldNumber}`;
            const fieldData = data[fieldKey];
            // Update the chart with the new data
            updateSensorFieldChart(chart, fieldData);
            // Check for dangerous readings and update warning display
            checkForDangerousReadings(fieldData, fieldNumber);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Function to update the chart with new data
// Function to update the chart with new data
function updateSensorFieldChart(chart, fieldData) {
    // Replace the current data with the new data
    chart.data.labels = fieldData.timestamps; // Assuming fieldData.timestamps is an array of 36 timestamps
    chart.data.datasets[0].data = fieldData.readings; // Assuming fieldData.readings is an array of 36 readings
    chart.data.datasets[1].data = fieldData.average_values; // Assuming fieldData.average_values is an array of 36 average values

    // Update the chart to reflect the new data
    chart.update();
}


// Function to update all charts
function updateAllCharts() {
    fetchAndUpdateChart(sensorField1Chart, 1);
    fetchAndUpdateChart(sensorField2Chart, 2);
    fetchAndUpdateChart(sensorField3Chart, 3);
}

// Update all charts every 15 seconds
setInterval(updateAllCharts, 5000);
