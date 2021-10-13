import bs4
import re

from controllers import utils


def list_products(best_seller=False, rating=0.0, exact_name="", **kwargs):
    """Returns a list of products matching the given criteria.

    Args:
        best_seller (bool, optional): If it is True, returns only best sellers. Defaults to False.
        rating (float, optional): Will return all items that is equal or above given rating. Defaults to 0.0.
        exact_name (str, optional): It will return one item with the exact string, if it exists. Defaults to "".

    Returns:
        list: Returns a list with dictionaries. Each dictionary contains the following keys:
            - name (str): The name of the product.
            - price (float): The price of the product.
            - rating (float): The rating of the product.
            - best_seller (bool): If the product is a best seller.
    """

    # Read html
    e_commerce_html = open("pages/content.html", "r")

    # Parse html
    item_details = []
    soup = bs4.BeautifulSoup(e_commerce_html.read(), "html.parser")
    # Results from the search
    itens_results = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Looping over the results
    for item in itens_results:

        # Removing white spaces from title
        title = re.sub(
            r"\s+",
            r" ",
            item.h2.a.text,
            flags=re.M,
        )
        # Removing white space in end of title
        title = re.sub(r"\s+$", r"", title)

        # Finding the price span tag
        item_price = item.find("span", {"class": "a-price"})
        # Finding the price
        price = item_price.find("span", {"class": "a-offscreen"}).text
        # Filtering unwanted characters from price tag and splitting whole
        # number from decimal
        price = re.findall(r"(?<![a-zA-Z:])[-+]?\d*\.?\d+", price)
        # Removing dots from price and converting to float
        price_whole = float(re.sub(r"\.", "", price[0]))
        # Converting to float and transforming in decimal
        price_decimal = float(price[1]) * 0.1

        # Since not all of the items have badge, we need to check if it exists
        try:
            # Finding the badge tag
            item_best_seller = item.find("span", {"class": "a-badge"})
            item_is_best_seller = item_best_seller.find(
                "span", {"class": "a-badge-text"}
            ).text.strip()
            # Removing white spaces from badge text
            item_is_best_seller = re.sub(
                r"\s+",
                r" ",
                item_is_best_seller,
                flags=re.M,
            )
            # Checking if badge is "Mais Vendido"
            if item_is_best_seller == "Mais vendido":
                item_is_best_seller = True
            else:
                item_is_best_seller = False
        except AttributeError:
            item_is_best_seller = False

        # Finding the rating
        item_rating = item.find("span", {"class": "a-icon-alt"}).text.strip()
        # Getting the rating from the text
        item_rating = item_rating[: item_rating.find(" ")]
        # If there is comma in the string, replace with dot
        item_rating = re.sub(r",", ".", item_rating)

        # Creating temporary dictionary to append to the list
        dict = {}
        dict["title"] = title
        dict["price"] = price_whole + price_decimal
        dict["best_seller"] = item_is_best_seller
        dict["rating"] = float(item_rating)
        # Appending temporary dictionary to the list
        item_details.append(dict)

    # If the best seller is True, we need to filter the list
    if best_seller:
        return utils.filter_best_seller(item_details)

    # If the rating is not 0.0, we need to filter the list
    if rating > 0.0:
        return utils.filter_rating(item_details, rating)

    # If the exact name is not empty, we need to filter the list
    if exact_name != "":
        return utils.filter_exact_name(item_details, exact_name)

    return item_details
