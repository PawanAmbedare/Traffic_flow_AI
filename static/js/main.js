var socket = io();

let chartCtx = document.getElementById('trafficChart').getContext('2d');
let trafficChart = new Chart(chartCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'North Traffic',
            data: [],
            borderWidth: 2
        }]
    }
});

socket.on("update", function(data) {

    document.getElementById("north").innerText = data.north;
    document.getElementById("south").innerText = data.south;
    document.getElementById("east").innerText = data.east;
    document.getElementById("west").innerText = data.west;

    document.getElementById("activeLane").innerText =
        "Active Lane: " + data.active_lane.toUpperCase();

    document.getElementById("timer").innerText = data.timer;

    // Reset signals
    ["north","south","east","west"].forEach(lane => {
        document.getElementById(lane+"Signal").className = "signal red";
    });

    document.getElementById(data.active_lane+"Signal").className = "signal green";

    // Emergency effect
    if(data.emergency){
        document.body.style.boxShadow = "0 0 40px red";
    } else {
        document.body.style.boxShadow = "none";
    }

    // Logs
    let logsDiv = document.getElementById("logs");
    logsDiv.innerHTML = data.logs.map(l => "<div>"+l+"</div>").join("");

    // Graph update
    trafficChart.data.labels.push("");
    trafficChart.data.datasets[0].data.push(data.north);
    if (trafficChart.data.labels.length > 15){
        trafficChart.data.labels.shift();
        trafficChart.data.datasets[0].data.shift();
    }
    trafficChart.update();
});