# Inside Out; Job Seeker’s Best Friend
Inside Out is an web app that provides to job seekers essential company data that are not easily found elsewhere. It uses key APIs including Google Maps API, Bing Web Search API, and News API. It also uses real salary data from U.S Labor Department as well as real time job listings scraped from Glassdoor. By simply typing in a company name, users can get the company overview, employee rating, location, and latest Google search trends visualized through Chart.js. Clicking on specific dates on the trend chart retrieves relevant news. Users can even check and compare company ranking within each industry based on search volume growth.

# Tech Stack
- Python, JavaScript (AJAX, JSON), HTML, CSS, SQL, Flask, jQuery, Bootstrap, Jinja, Chart JS, PostgreSQL, SQLAlchemy, Flask-WTF

# APIs Used
- Google Maps API(Geocode, Maps), Bing Web Search API, News API

# Features
## Homepage
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/1.png?raw=true)

## Main page

### Company Overview
- I used Bing Web Search API for the company's logo and description, and Google Maps API for the company's location.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/2.png?raw=true)

### Search Volume Trend from Google Trends
- I used Chart JS to show company's search volume data from Google Trends.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/3.png?raw=true)

### Related News
- This news card generator responds to user's click. When user clicks a point on the chart, Chart JS method is called, and captures date. I used it to make a request to News API then loops over JSON results, and generates news card from the specific week.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/4.png?raw=true)

### Real Salary Data from U.S Labor Department
- I used Postgre and SQLAlchemy for this.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/5.png?raw=true)

### Job Listing from Glassdoor
- Glass door doesn't have an API. So I wrote my own scraper with the Python request and lxml modules to scrape the company's rating and job listings.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/6.png?raw=true)

## Ranking Page
- Search volume growth ranking within same industries. To improve loading time, I used an eager join on a db relationship between db tables, and created table index to avoid a full table scan.
![alt text](https://github.com/parksunah/Project-Inside-Out/blob/master/static/images/_readme/7.png?raw=true)

