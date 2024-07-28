//API snippet grabbed from RapidApi's Travel Advisor API

async function fetchRestaurants(bl_latitude, tr_latitude, bl_longitude, tr_longitude) {
  const options = {
    method: 'GET',
    url: 'https://travel-advisor.p.rapidapi.com/restaurants/list-in-boundary',
    params: { bl_latitude, tr_latitude, bl_longitude, tr_longitude },
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

//API snippet grabbed from RapidApi's Travel Advisor API

//API snippet grabbed from RapidApi's Travel Advisor API

async function fetchAttractions(
  bl_latitude, tr_latitude, bl_longitude, tr_longitude
) {
  const options = {
    method: 'GET',
    url: 'https://travel-advisor.p.rapidapi.com/attractions/list-in-boundary',
    params: { bl_latitude, tr_latitude, bl_longitude, tr_longitude },
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

//API snippet grabbed from RapidApi's Travel Advisor API

async function fetchHotels(bl_latitude, tr_latitude, bl_longitude, tr_longitude) {
  const options = {
    method: 'GET',
    url: 'https://travel-advisor.p.rapidapi.com/hotels/list-in-boundary',
    params: { bl_latitude, tr_latitude, bl_longitude, tr_longitude },
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

//Display base function for restaurants, attractions, and hotels. Adds them to the table

function displayPlaces(places, type) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  tableBody.innerHTML = '';

  if (places.length === 0) {
    console.log(`No ${type} found`);
    return;
  }

  places.forEach(place => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${place.name || 'N/A'}</td>
      <td><a href="${place.web_url || '#'}" target="_blank">Website</a></td>
      <td>${place.price_level || 'N/A'}</td>
      <td>${place.rating || 'N/A'}</td>
      <td><button>Send to Itinerary</button></td>
    `;
    row.querySelector('button').onclick = () => {
      document.querySelector('input[name="activity"]').value = place.name || '';
      document.querySelector('input[name="location"]').value = place.location_string || 'Unknown City';
      document.querySelector('textarea[name="notes"]').value = place.web_url || 'No website available';
    };
    tableBody.appendChild(row);
  });
}

function displayRestaurants(restaurants) {
  displayPlaces(restaurants, 'restaurants');
}

function displayAttractions(attractions) {
  displayPlaces(attractions, 'attractions');
}

function displayHotels(hotels) {
  displayPlaces(hotels, 'hotels');
}

//Add places on the map

function addMarkers(map, items) {
  items.forEach((item) => {
    const marker = new google.maps.Marker({
      position: {
        lat: parseFloat(item.latitude),
        lng: parseFloat(item.longitude),
      },
      map: map,
      title: item.name,
      icon: {
        url: item.photo ? item.photo.images.small.url : 'https://maps.google.com/mapfiles/ms/icons/restaurant.png',
        scaledSize: new google.maps.Size(50, 50)
      }
    });

    google.maps.event.addListener(marker, "click", function () {
      window.open(item.web_url, "_blank");
      highlightTableRow(item.web_url);
    });
  });
}

//When clicking a marker on the map, Bolden the name in the table and its website

function highlightTableRow(url) {
  const tableBody = document.getElementById('places-table').getElementsByTagName('tbody')[0];
  const rows = tableBody.getElementsByTagName('tr');
  for (let row of rows) {
    const nameCell = row.getElementsByTagName('td')[0];
    const websiteLink = row.getElementsByTagName('a')[0];
    if (websiteLink && websiteLink.href === url) {
      nameCell.style.fontWeight = 'bold';
      websiteLink.style.fontWeight = 'bold';
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      websiteLink.style.fontWeight = 'normal';
      nameCell.style.fontWeight
    }
  }
}

//Initialize map

function initMap() {
  const defaultLocation = { lat: 37.7749, lng: -122.4194 }; 
  const map = new google.maps.Map(document.getElementById('map'), {
    center: defaultLocation,
    zoom: 12
  });

  const input = document.getElementById('autocomplete');
  const autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.setFields(['geometry']);
  autocomplete.bindTo('bounds', map);

  autocomplete.addListener('place_changed', () => {
    const place = autocomplete.getPlace();
    if (!place.geometry) {
      console.log(`No details available for input: '${place.name}'`);
      return;
    }
    map.fitBounds(place.geometry.viewport || place.geometry.location);
    map.setZoom(12);

    const bounds = map.getBounds();
    const bl = bounds.getSouthWest();
    const tr = bounds.getNorthEast();

    console.log("Map Bounds:", { bl_latitude: bl.lat(), bl_longitude: bl.lng(), tr_latitude: tr.lat(), tr_longitude: tr.lng() });

    const showAttractions = document.getElementById('toggleAttractions').checked;
    const showHotels = document.getElementById('toggleHotels').checked;

    const fetchAndDisplay = (fetchFn, displayFn) => {
      fetchFn(bl.lat(), tr.lat(), bl.lng(), tr.lng()).then(places => {
        displayFn(places);
        addMarkers(map, places);
      });
    };

    if (showAttractions) {
      fetchAndDisplay(fetchAttractions, displayAttractions);
    } else if (showHotels) {
      fetchAndDisplay(fetchHotels, displayHotels);
    } else {
      fetchAndDisplay(fetchRestaurants, displayRestaurants);
    }
  });

  document.getElementById('toggleAttractions').addEventListener('change', () => google.maps.event.trigger(input, 'place_changed'));
  document.getElementById('toggleHotels').addEventListener('change', () => google.maps.event.trigger(input, 'place_changed'));
}

window.addEventListener("load", initMap);

function copyInviteCode() {
  var copyText = document.getElementById("inviteCode");
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices
  document.execCommand("copy");
  alert("Invite code copied: " + copyText.value);
}
