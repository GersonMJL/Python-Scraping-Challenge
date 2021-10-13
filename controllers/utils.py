def filter_best_seller(list: list):
    """Loops over the list and returns list of best sellers

    Args:
        list (list): List of items

    Returns:
        list: List of best selling items
    """
    best_sellers = []
    for item in list:
        if item["best_seller"]:
            print(item["best_seller"])
            best_sellers.append(item)
    return best_sellers


def filter_rating(list: list, rating: float):
    """Looping over the item details and appending to the new
    list if rating is equal or above given rating

    Args:
        list (list): List of items
        rating (float): Rating to be filtered

    Returns:
        list: List of items with rating above given rating
    """
    ratings = []

    for item in list:
        if item["rating"] >= rating:
            ratings.append(item)
    return ratings


def filter_exact_name(list: list, name: str):
    """Looping over the item details and append to the new
    list if title is equal to given name

    Args:
        list (list): List of items
        name (str): Name to be filtered

    Returns:
        list: List containing item with title equal to given name
    """
    exact_name = []
    for item in list:
        if item["title"] == name:
            exact_name.append(item)
            break
    return exact_name
