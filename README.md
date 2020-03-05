# **TIKI WEB SCRAPING** 

**Tiki Web Scraping** is an assignment to collect and store available product data from TIKI.VN to SQL database, then display the data on a Flask App. 

The project successfully scraped 100,000 products accross all the categories. 

-------

## **PROCESS:**

***Data Scraping***

CODE CAN BE REFERED IN ```main_nb.py```

*1. Scraping Categories:* 
* Create "Categories" database using PostgreSQL.

| Field Name | Type | 
| --------   | -------- |
| ID | INTEGER | 
| Name       | VARCHAR (255)|
| Parent ID | INTEGER |
* Find and scrape the categories data using BeautifulSoup. (Main categories and sub-categories)
* Store into database. 


*2. Scraping Products:* 
* Creat "Products" database using PostgreSQL. 

| Field Name | Type | 
| --------   | -------- | 
| ID | INTEGER |
| Data ID | INTEGER 
| Seller ID | INTEGER
| Name      | VARCHAR (255)|
| Price | INTEGER|
| Image Link | TEXT
| Category ID | INTEGER |

* Create a list of "deepest categories" (ones that have no children).
* Go through the list, find, and scrape the products data using BeautifulSoup. 
* Store into database using PostgreSQL. 

![](https://i.imgur.com/U2ojQq0.jpg)

***Communicate database to users.***

* Connect database to FlaskApp.
* Visualize database using html, CSS.
* Added features: 
1. Main categories link to sub categories 
2. Price Filter: High to Low, Low to High
3. Paginations 
4. Search tool