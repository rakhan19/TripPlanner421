async function fetchRestaurants(bl_latitude, tr_latitude, bl_longitude, tr_longitude) {
    const options = {
      method: 'GET',
      url: 'https://travel-advisor.p.rapidapi.com/restaurants/list-in-boundary',
      params: {
        bl_latitude: bl_latitude,
        tr_latitude: tr_latitude,
        bl_longitude: bl_longitude,
        tr_longitude: tr_longitude,
      },
      headers: {
        'x-rapidapi-key': '97189cc006mshcc41988e5682cc9p1049bejsn943f1811da0f',
        'x-rapidapi-host': 'travel-advisor.p.rapidapi.com'
      }
    };
  
    try {
      const response = await axios.request(options);
      console.log("API Response (Restaurants):", response.data); // Debugging
      return response.data.data;
    } catch (error) {
      console.error("API Error (Restaurants):", error); // Debugging
      return [];
    }
  }
  
  async function fetchAttractions(bl_latitude, tr_latitude, bl_longitude, tr_longitude) {
    const options = {
      method: 'GET',
      url: 'https://travel-advisor.p.rapidapi.com/attractions/list-in-boundary',
      params: {
        bl_latitude: bl_latitude,
        tr_latitude: tr_latitude,
        bl_longitude: bl_longitude,
        tr_longitude: tr_longitude,
      },
      headers: {
        'x-rapidapi-key': '97189cc006mshcc41988e5682cc9p1049bejsn943f1811da0f',
        'x-rapidapi-host': 'travel-advisor.p.rapidapi.com'
      }
    };
  
    try {
      const response = await axios.request(options);
      console.log("API Response (Attractions):", response.data); // Debugging
      return response.data.data;
    } catch (error) {
      console.error("API Error (Attractions):", error); // Debugging
      return [];
    }
  }
  
  function displayRestaurants(restaurants) {
    const tableBody = document.getElementById('restaurants-table-body');
    tableBody.innerHTML = '';
  
    if (restaurants.length === 0) {
      console.log("No restaurants found"); // Debugging
      return;
    }
  
    restaurants.forEach(restaurant => {
      const row = document.createElement('tr');
  
      const nameCell = document.createElement('td');
      nameCell.textContent = restaurant.name;
      row.appendChild(nameCell);
  
      const websiteCell = document.createElement('td');
      const websiteLink = document.createElement('a');
      websiteLink.href = restaurant.web_url;
      websiteLink.textContent = 'Website';
      websiteLink.target = '_blank';
      websiteCell.appendChild(websiteLink);
      row.appendChild(websiteCell);
  
      const priceLevelCell = document.createElement('td');
      priceLevelCell.textContent = restaurant.price_level || 'N/A';
      row.appendChild(priceLevelCell);
  
      const ratingCell = document.createElement('td');
      ratingCell.textContent = restaurant.rating || 'N/A';
      row.appendChild(ratingCell);
  
      tableBody.appendChild(row);
    });
  }
  
  function displayAttractions(attractions) {
    const tableBody = document.getElementById('restaurants-table-body');
    tableBody.innerHTML = '';
  
    if (attractions.length === 0) {
      console.log("No attractions found"); // Debugging
      return;
    }
  
    attractions.forEach(attraction => {
      const row = document.createElement('tr');
  
      const nameCell = document.createElement('td');
      nameCell.textContent = attraction.name;
      row.appendChild(nameCell);
  
      const websiteCell = document.createElement('td');
      const websiteLink = document.createElement('a');
      websiteLink.href = attraction.web_url;
      websiteLink.textContent = 'Website';
      websiteLink.target = '_blank';
      websiteCell.appendChild(websiteLink);
      row.appendChild(websiteCell);
  
      const priceLevelCell = document.createElement('td');
      priceLevelCell.textContent = 'N/A'; // Price level may not be available for attractions
      row.appendChild(priceLevelCell);
  
      const ratingCell = document.createElement('td');
      ratingCell.textContent = attraction.rating || 'N/A';
      row.appendChild(ratingCell);
  
      tableBody.appendChild(row);
    });
  }
  
  function addMarkers(map, items) {
    items.forEach(item => {
      const marker = new google.maps.Marker({
        position: { lat: parseFloat(item.latitude), lng: parseFloat(item.longitude) },
        map: map,
        title: item.name,
        icon: {
          url: item.photo ? item.photo.images.small.url : 'https://maps.google.com/mapfiles/ms/icons/restaurant.png', // Use a default icon if no photo available
          scaledSize: new google.maps.Size(50, 50) // Scale size as needed
        }
      });
  
      google.maps.event.addListener(marker, 'click', function() {
        window.open(item.web_url, '_blank');
      });
    });
  }
  
  function initMap() {
    // Initialize the map centered on a default location
    var defaultLocation = { lat: 37.7749, lng: -122.4194 }; // San Francisco
    var map = new google.maps.Map(document.getElementById('map'), {
      center: defaultLocation,
      zoom: 10
    });
  
    // Initialize the autocomplete input
    var input = document.getElementById('autocomplete');
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(['geometry']);
  
    // Bias the search results to the map's viewport
    autocomplete.bindTo('bounds', map);
  
    // Listen for the event fired when the user selects a prediction
    autocomplete.addListener('place_changed', function() {
      var place = autocomplete.getPlace();
      if (!place.geometry) {
        // User entered the name of a place that was not suggested
        console.log("No details available for input: '" + place.name + "'");
        return;
      }
  
      // If the place has a geometry, present it on the map
      if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
      } else {
        map.setCenter(place.geometry.location);
        map.setZoom(10); // Adjust zoom level as needed
      }
  
      // Get the bounds of the map
      var bounds = map.getBounds();
      var bl = bounds.getSouthWest();
      var tr = bounds.getNorthEast();
  
      console.log("Map Bounds:", {
        bl_latitude: bl.lat(),
        bl_longitude: bl.lng(),
        tr_latitude: tr.lat(),
        tr_longitude: tr.lng()
      }); // Debugging
  
      // Determine if attractions or restaurants should be displayed
      const showAttractions = document.getElementById('toggleAttractions').checked;
  
      if (showAttractions) {
        fetchAttractions(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(attractions => {
          displayAttractions(attractions);
          addMarkers(map, attractions);
        });
      } else {
        fetchRestaurants(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(restaurants => {
          displayRestaurants(restaurants);
          addMarkers(map, restaurants);
        });
      }
    });
  
    // Trigger place_changed event on toggle switch change
    document.getElementById('toggleAttractions').addEventListener('change', function() {
      google.maps.event.trigger(input, 'place_changed');
    });
  }
  
  // Load the map when the window loads
  window.addEventListener('load', initMap);