// Initialize the grid with initial data
const grid = new gridjs.Grid({
    columns: ["WalletID", "Status", "Wallet Name", "Unclaimed Rewards"],
    data: [
        ["1855", "Online", "Io Glacier 6", "4.0788"],
        ["1855", "Online", "Io Glacier 6", "4.0788"],
        ["1855", "Online", "Io Glacier 6", "4.0788"],
        ["1855", "Online", "Io Glacier 6", "4.0788"],      
    ]
}).render(document.getElementById("wrapper"));

// Async function to fetch data and update the grid
async function update(newData) {
    console.log(newData);
    grid.updateConfig({
        data: newData
    }).forceRender();
}

// Function to fetch data and update the grid
function fetchDataAndUpdate() {
    paling.get_wallet_data()(update);
}

// Function to update the countdown timer
function updateCountdown(seconds) {
    const countdownElement = document.getElementById("countdown");
    countdownElement.textContent = `Next refresh in: ${seconds} seconds`;
}

// Call the update function at startup to initialize the grid with the latest data
fetchDataAndUpdate();

// Set an interval to call the update function every 60 seconds and update the countdown timer
let secondsRemaining = 60;
const countdownInterval = setInterval(() => {
    if (secondsRemaining > 0) {
        updateCountdown(secondsRemaining);
        secondsRemaining--;
    } else {
        fetchDataAndUpdate();
        secondsRemaining = 60;
    }
}, 1000); // 1000 milliseconds = 1 second
