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
    return response.data.data;
  } catch (error) {
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
    return response.data.data;
  } catch (error) {
    return [];
  }
}

async function fetchHotels(bl_latitude, tr_latitude, bl_longitude, tr_longitude) {
  const options = {
    method: 'GET',
    url: 'https://travel-advisor.p.rapidapi.com/hotels/list-in-boundary',
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
    console.log("API Response (Hotels):", response.data);
    return response.data.data;
  } catch (error) {
    console.error("API Error (Hotels):", error);
    return [];
  }
}

function displayRestaurants(restaurants) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  tableBody.innerHTML = '';

  if (restaurants.length === 0) {
    console.log("No restaurants found");
    return;
  }

  restaurants.forEach(restaurant => {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = restaurant.name || 'N/A';
    row.appendChild(nameCell);

    const websiteCell = document.createElement('td');
    const websiteLink = document.createElement('a');
    websiteLink.href = restaurant.web_url || '#';
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

    const sendToItineraryCell = document.createElement('td');
    const button = document.createElement('button');
    button.textContent = 'Send to Itinerary';
    button.onclick = function() {
      document.querySelector('input[name="activity"]').value = restaurant.name || '';
      document.querySelector('input[name="location"]').value = restaurant.location_string || 'Unknown City';
      document.querySelector('textarea[name="notes"]').value = restaurant.web_url || 'No website available';
    };
    sendToItineraryCell.appendChild(button);
    row.appendChild(sendToItineraryCell);

    tableBody.appendChild(row);
  });
}

function displayAttractions(attractions) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  tableBody.innerHTML = '';

  if (attractions.length === 0) {
    console.log("No attractions found");
    return;
  }

  attractions.forEach(attraction => {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = attraction.name || 'N/A';
    row.appendChild(nameCell);

    const websiteCell = document.createElement('td');
    const websiteLink = document.createElement('a');
    websiteLink.href = attraction.web_url || '#';
    websiteLink.textContent = 'Website';
    websiteLink.target = '_blank';
    websiteCell.appendChild(websiteLink);
    row.appendChild(websiteCell);

    const priceLevelCell = document.createElement('td');
    priceLevelCell.textContent = 'N/A';
    row.appendChild(priceLevelCell);

    const ratingCell = document.createElement('td');
    ratingCell.textContent = attraction.rating || 'N/A';
    row.appendChild(ratingCell);

    const sendToItineraryCell = document.createElement('td');
    const button = document.createElement('button');
    button.textContent = 'Send to Itinerary';
    button.onclick = function() {
      document.querySelector('input[name="activity"]').value = attraction.name || '';
      document.querySelector('input[name="location"]').value = attraction.location_string || 'Unknown City';
      document.querySelector('textarea[name="notes"]').value = attraction.web_url || 'No website available';
    };
    sendToItineraryCell.appendChild(button);
    row.appendChild(sendToItineraryCell);

    tableBody.appendChild(row);
  });
}

function displayHotels(hotels) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  tableBody.innerHTML = '';

  if (hotels.length === 0) {
    console.log("No hotels found");
    return;
  }

  hotels.forEach(hotel => {
    const row = document.createElement('tr');

    const nameCell = document.createElement('td');
    nameCell.textContent = hotel.name || 'N/A';
    row.appendChild(nameCell);

    const websiteCell = document.createElement('td');
    const websiteLink = document.createElement('a');
    websiteLink.href = hotel.web_url || '#';
    websiteLink.textContent = 'Website';
    websiteLink.target = '_blank';
    websiteCell.appendChild(websiteLink);
    row.appendChild(websiteCell);

    const priceLevelCell = document.createElement('td');
    priceLevelCell.textContent = hotel.price_level || 'N/A';
    row.appendChild(priceLevelCell);

    const ratingCell = document.createElement('td');
    ratingCell.textContent = hotel.rating || 'N/A';
    row.appendChild(ratingCell);

    const sendToItineraryCell = document.createElement('td');
    const button = document.createElement('button');
    button.textContent = 'Send to Itinerary';
    button.onclick = function() {
      document.querySelector('input[name="activity"]').value = hotel.name || '';
      document.querySelector('input[name="location"]').value = hotel.location_string || 'Unknown City';
      document.querySelector('textarea[name="notes"]').value = hotel.web_url || 'No website available';
    };
    sendToItineraryCell.appendChild(button);
    row.appendChild(sendToItineraryCell);

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
        url: item.photo ? item.photo.images.small.url : 'https://maps.google.com/mapfiles/ms/icons/restaurant.png',
        scaledSize: new google.maps.Size(50, 50)
      }
    });

    google.maps.event.addListener(marker, 'click', function() {
      window.open(item.web_url, '_blank');
      highlightTableRow(item.web_url);
    });
  });
}

function highlightTableRow(url) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  const rows = tableBody.getElementsByTagName('tr');

  for (let row of rows) {
    const websiteLink = row.getElementsByTagName('a')[0];
    if (websiteLink && websiteLink.href === url) {
      row.style.backgroundColor = 'lightgray';
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      row.style.backgroundColor = '';
    }
  }
}

function initMap() {
  var defaultLocation = { lat: 37.7749, lng: -122.4194 }; 
  var map = new google.maps.Map(document.getElementById('map'), {
    center: defaultLocation,
    zoom: 14
  });

  var input = document.getElementById('autocomplete');
  var autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.setFields(['geometry']);

  autocomplete.bindTo('bounds', map);

  autocomplete.addListener('place_changed', function() {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
      console.log("No details available for input: '" + place.name + "'");
      return;
    }

    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(16);
    }

    var bounds = map.getBounds();
    var bl = bounds.getSouthWest();
    var tr = bounds.getNorthEast();

    console.log("Map Bounds:", {
      bl_latitude: bl.lat(),
      bl_longitude: bl.lng(),
      tr_latitude: tr.lat(),
      tr_longitude: tr.lng()
    });

    const showAttractions = document.getElementById('toggleAttractions').checked;
    const showHotels = document.getElementById('toggleHotels').checked;

    if (showAttractions) {
      fetchAttractions(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(attractions => {
        displayAttractions(attractions);
        addMarkers(map, attractions);
      });
    } else if (showHotels) {
      fetchHotels(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(hotels => {
        displayHotels(hotels);
        addMarkers(map, hotels);
      });
    } else {
      fetchRestaurants(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(restaurants => {
        displayRestaurants(restaurants);
        addMarkers(map, restaurants);
      });
    }
  });

  document.getElementById('toggleAttractions').addEventListener('change', function() {
    google.maps.event.trigger(input, 'place_changed');
  });

  document.getElementById('toggleHotels').addEventListener('change', function() {
    google.maps.event.trigger(input, 'place_changed');
  });
}

window.addEventListener('load', initMap);