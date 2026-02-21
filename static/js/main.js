var socket = io();

const ctx = document.getElementById('trafficChart').getContext('2d');

let trafficChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'North Traffic',
            data: [],
            borderWidth: 2
        }]
    },
    options: {
        responsive: true
    }
});

socket.on("traffic_update", function(data) {

    document.getElementById("north").innerText = data.north;
    document.getElementById("south").innerText = data.south;
    document.getElementById("east").innerText = data.east;
    document.getElementById("west").innerText = data.west;

    document.getElementById("signalBox").innerText = "Signal: " + data.signal;

    if (data.emergency) {
        document.getElementById("emergencyAlert").classList.remove("hidden");
    } else {
        document.getElementById("emergencyAlert").classList.add("hidden");
    }

    // Update graph
    trafficChart.data.labels.push("");
    trafficChart.data.datasets[0].data.push(data.north);

    if (trafficChart.data.labels.length > 10) {
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }

    trafficChart.update();
});