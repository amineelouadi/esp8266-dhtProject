const apiEndpoint = '/api/sensor-data/';

// DOM Elements
const elements = {
    temperature: document.getElementById('temperature'),
    temperatureF: document.getElementById('temperature-f'),
    humidity: document.getElementById('humidity'),
    deviceId: document.getElementById('device-id'),
    lastUpdate: document.getElementById('last-update')
};

async function fetchSensorData() {
    try {
        const response = await fetch(apiEndpoint);
        const data = await response.json();
        console.log('Données reçues:', data);

        // Vérifier si nous avons les données du capteur
        if (data.temperature && data.humidity) {  // Données directes maintenant
            elements.temperature.textContent = data.temperature;
            elements.temperatureF.textContent = 
                ((data.temperature * 9/5) + 32).toFixed(1);
            elements.humidity.textContent = data.humidity;
            elements.deviceId.textContent = data.device;
            elements.lastUpdate.textContent = new Date().toLocaleString();
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}

// Actualiser les données toutes les 5 secondes
fetchSensorData();
setInterval(fetchSensorData, 5000);