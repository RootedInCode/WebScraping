import requests
from bs4 import BeautifulSoup
import pandas as pd  # Install using: pip install pandas

# Base URL of the book website
url = "http://books.toscrape.com/"
r = requests.get(url)  # Sending a request to fetch the page content

# Parsing the HTML response using BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')

# Finding all books (Each book is inside an <article> tag with class="product_pod")
books = soup.find_all("article", class_="product_pod")
book_data = []  # List to store book details

for index, book in enumerate(books, 1):
    # Extract book title from the <h3> tag inside <article>
    # Stored like <a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>
    title_book = book.h3.a["title"]

    # Extract price from the <p> tag with class="price_color"
    # Stored like <p class="price_color">£51.77</p>
    price_tag = book.find("p", class_="price_color")
    price = price_tag.text.strip() if price_tag else "No Price Found"

    # Extract rating from <p> tag with class like <p class="star-rating Three"> </p>
    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag["class"][1] if rating_tag else "No Rating"  # Second class is the rating (e.g., "Four")

    # Extract product link from <a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a> 
    product_link = book.h3.a["href"]
    full_product_link = url + product_link.replace("../../../", "catalogue/")  # Fixing relative URL to full URL

    # Send request to the book's detail page
    r_prod = requests.get(full_product_link)
    soup_prod = BeautifulSoup(r_prod.content, 'html.parser')

    # Extract description from the first <p> tag WITHOUT a class
    # Example: <p>This is the book's description.</p> (This <p> has no class)
    description_div = soup_prod.find("p", class_=False)
    description = description_div.text.strip() if description_div else "No Description Found"

    # Append all extracted details as a row in book_data list
    book_data.append([index, title_book, price, rating, description])

# Convert book data to a pandas DataFrame
df = pd.DataFrame(book_data, columns=["#", "Title", "Price", "Rating", "Description"])

# Export to Excel (.xlsx format)
df.to_excel("books_data.xlsx", index=False)
print("Data exported successfully: books_data.xlsx")
 
