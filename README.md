# TripPlanner421

TripPlanner421 is a web application that helps users plan trips by managing their budget, itinerary, and providing a chat feature for trip participants. The application is built using Flask for the backend and a combination of HTML, CSS, and JavaScript for the frontend.

## Features

- User authentication and authorization
- Budget management for trips
- Itinerary management
- Real-time chat for trip participants
- Interactive map with hotel, restaurant, and attraction information

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/TripPlanner421.git
   cd TripPlanner421
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following environment variables:

   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=your_mongo_uri
   GOOGLEMAPS_API_KEY=your_googlemaps_api_key
   RAPIDAPI_KEY=your_rapidapi_key
   ```
    [Google Maps JavaScript API + Places API key](https://developers.google.com/maps/documentation/javascript/get-api-key)

    [RapidAPI key for Travel Advisor API](https://rapidapi.com/apidojo/api/travel-advisor/playground/apiendpoint_29754943-5eb1-4dff-9153-fa9c67a72d9b)

5. **Run the application:**

   In the root of the application, initiate a MongoDB instance:
   ```bash
   mongod --dbpath ./backend/data/db
   ```

   In a separate terminal:
   ```bash
   flask run
   ```

6. **Access the application:**

   Open your web browser and go to `http://127.0.0.1:5000`

## File Structure

```
TripPlanner421/
├── backend/
│   ├── auth.py
│   ├── budget.py
│   ├── chat.py
│   ├── itinerary.py
│   └── models.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── map.js
├── templates/
│   ├── admit.html
│   ├── base0.html
│   ├── base1.html
│   ├── budget.html
│   ├── itinerary.html
│   ├── mainpage.html
│   ├── signup.html
│   ├── trip_chat.html
│   ├── trip.html
│   └── welcome.html
├── LICENSE
├── package.json
├── README.md
└── requirements.txt
```

### Backend

- auth.py: Handles user authentication and authorization.
- budget.py: Manages trip budget operations.
- chat.py: Manages chat functionality for trip participants.
- itinerary.py: Handles itinerary management.
- models.py: Defines the MongoDB connection and models.

### Frontend

- styles.css: Contains the CSS styles for the application.
- map.js: Contains JavaScript for map functionality using the Google Maps API.

### Templates

- admit.html: Login page template.
- base0.html: Base template without user-specific navigation.
- base1.html: Base template with user-specific navigation.
- budget.html: Template for managing trip budgets.
- itinerary.html: Template for managing itineraries.
- mainpage.html: Main page template after login.
- signup.html: Signup page template.
- trip_chat.html: Template for trip chat functionality.
- trip.html: Template for viewing a trip's details.
- welcome.html: Welcome page template.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Creators

- Christian Collins
- Rizwan Khan
- Naomi Fokkens
- Xavier Golden

## Citations

- Flask: [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/)
- HTML: [MDN Web Docs - HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- CSS: [MDN Web Docs - CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- JavaScript: [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- Google Maps API: [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- MongoDB: [MongoDB Documentation](https://docs.mongodb.com/)
- Python: [Python Documentation](https://docs.python.org/3/)
