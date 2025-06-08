# Apricot — Game Deals Tracker  
#### Video Demo: https://www.youtube.com/watch?v=XmEhqlK_jZs  
#### App link: https://apricotxs-c956d8f16aaf.herokuapp.com/
#### Description:

**Apricot** is a web application designed to help users track the best deals on video games from multiple digital storefronts. Built as my final project for **CS50x**, Apricot offers a streamlined and user-friendly experience that allows gamers to search for their favorite titles, compare prices across different stores, and manage a personal wishlist. It utilizes real-time data from the [CheapShark API](https://apidocs.cheapshark.com/) and stores user preferences in a PostgreSQL database hosted on Heroku.

### Features

- **User Authentication**: Users can register and securely log into their own account. Session management ensures each user’s data remains private and persistent.
- **Game Search**: Users can search for any game, and Apricot will fetch the latest deals from various stores including Steam, Green Man Gaming, and Humble Bundle.
- **Wishlist Functionality**: Logged-in users can save any game to their personal wishlist to track prices over time.
- **Live Price Comparison**: Game listings display real-time pricing data, including the original and sale prices, so users can instantly identify the best deals available.
- **Responsive Design**: The front end is styled using HTML, CSS, and Bootstrap for a clean and responsive interface.

### Tech Stack

- **Frontend**: HTML, CSS, JS, Bootstrap
- **Backend**: Python, Flask
- **Database**: PostgreSQL on Heroku
- **API Integration**: CheapShark API for real-time game deals
- **Deployment**: Hosted on Heroku

---

### File Structure

- `app.py` — The main Flask application. Contains route logic, user session management, and integration with the CheapShark API and PostgreSQL database.
- `templates/` — Contains HTML templates using Jinja2 syntax. Includes:
  - `index.html` — Homepage and search form
  - `login.html` — User login interface
  - `register.html` — Registration form
  - `wishlist.html` — Displays the user’s saved games
- `static/` — Contains static assets like custom CSS and images
- `requirements.txt` — Lists all Python dependencies for easy deployment or installation
- `Procfile` — Required by Heroku for app deployment
- `README.md` — This file; documents and explains the project
- `.env` or `config.py` — (Not committed for security) Handles secret keys and environment variables for Heroku and database access

---

### Design Choices

Initially, the project used SQLite for local development. However, since the app needed to be deployed and used across sessions and users, I transitioned to **PostgreSQL** using **Heroku's cloud database**. This decision improved scalability and robustness.

Another major decision was using **CheapShark’s public API** rather than scraping data directly from stores. This made the app more reliable and ethical while drastically simplifying the development process.

For the front end, I used **Bootstrap** to achieve a responsive and professional look without spending too much time on styling from scratch. The site is designed to be clean, minimalist, and intuitive.

---

### Challenges and Lessons Learned

Deploying a full-stack app with user authentication, database integration, and real-time API usage required solving many small but critical problems, especially around handling HTTP requests, session management, and debugging deployment issues on Heroku.

I also learned a lot about environment management, securely storing credentials, and configuring production environments using `.env` files and Heroku’s config vars.

---

### Future Improvements

- **Email notifications** when a wishlist game goes on sale
- **Sorting and filtering** options for search results
- **User profile pages**
- **Integration with more APIs** for expanded functionality (e.g., user reviews, screenshots)
- **Dark mode** toggle for better UI experience

---

**Apricot** represents my growth as a developer through CS50x, and I'm proud of the functionality and polish it delivers. This project is just a starting point, and I’m excited to expand it further in the future.
