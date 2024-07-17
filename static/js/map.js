import axios from 'axios';

let map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 37.7749, lng: -122.4194 }, // Default location
        zoom: 13
    });

    const searchButton = document.getElementById('search-button');
    
    searchButton.addEventListener('click', () => {
        const city = document.getElementById('search-box').value;
        geocodeCity(city);
    });
}

function geocodeCity(city) {
    const geocoder = new google.maps.Geocoder();

    geocoder.geocode({ address: city }, (results, status) => {
        if (status === 'OK') {
            if (results[0]) {
                map.setCenter(results[0].geometry.location);
                new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                    title: city
                });
                map.setZoom(12);

                // Fetch restaurants using the new location
                fetchRestaurants(results[0].geometry.location.lat(), results[0].geometry.location.lng());
            } else {
                alert('No results found for ' + city);
            }
        } else {
            alert('Geocoder failed due to: ' + status);
        }
    });
}

function fetchRestaurants(lat, lng) {
    const options = {
        method: 'GET',
        url: 'https://travel-advisor.p.rapidapi.com/restaurants/list-in-boundary',
        params: {
            bl_latitude: lat - 0.1, // Adjust boundaries
            tr_latitude: lat + 0.1,
            bl_longitude: lng - 0.1,
            tr_longitude: lng + 0.1,
        },
        headers: {
            'x-rapidapi-key': '97189cc006mshcc41988e5682cc9p1049bejsn943f1811da0f', // Replace with your actual key
            'x-rapidapi-host': 'travel-advisor.p.rapidapi.com'
        }
    };

    axios.request(options)
        .then(response => {
            console.log(response.data); // Log the data
            displayRestaurants(response.data); // Call a function to display restaurants on the map
        })
        .catch(error => {
            console.error('Error fetching restaurants:', error);
        });
}

function displayRestaurants(data) {
    if (data && data.data) {
        data.data.forEach(restaurant => {
            const { latitude, longitude, name } = restaurant;

            new google.maps.Marker({
                position: { lat: latitude, lng: longitude },
                map: map,
                title: name
            });
        });
    }
}