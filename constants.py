class Constant:
    """
    This class to hold constant values used in the application.
    """
    URL_MAPPING = {
        "nykaa": ("https://www.nykaafashion.com/", "nykaafashion.com"),
        "virgio": ("https://www.virgio.com/", "virgio.com"),
        "westside": ("https://www.westside.com/", "westside.com"),
        "tatacliq": ("https://www.tatacliq.com/", "tatacliq.com"),
    }

    COMMON_SEARCH_TERMS = ["dress", "shirt", "jeans", "top", "skirt"]

    COMMON_PRODUCT_PATTERNS = [
        "/product/",
        "/products/",
        "/item/",
        "/p/",
    ]
    NYKAA_PRODUCT_PATTERNS = [
        "/buy/",
    ] + COMMON_PRODUCT_PATTERNS
    VIGIO_PRODUCT_PATTERNS = [] + COMMON_PRODUCT_PATTERNS
    WESTSIDE_PRODUCT_PATTERNS = ["/shop/"] + COMMON_PRODUCT_PATTERNS
    TATACLIQ_PRODUCT_PATTERNS = [
            '/p-',
            '/-p-',
            '/mdp/',
            '/pdp/',
            '/buy/',
            '/shop/'
        ] +  COMMON_PRODUCT_PATTERNS

    COMMON_EXLCUDE_PATTERNS = [
        "/cart",
        "/search",
        "/login",
        "/register",
        "/wishlist",
        "/account",
        "/contact",
        "/help",
        "/faq",
        "/terms",
        "/privacy",
        "/about",
        "/category/",
        "/checkout",
    ]
    NYKAA_EXCLUDE_PATTERNS = [
        "/brand/",
        "/c/",
        "/lp/",
    ] + COMMON_EXLCUDE_PATTERNS

    VIGIO_EXCLUDE_PATTERNS = [
        "/collections/",
        "/pages/",
        "/smile-in-style",
        "/know-your-size",
    ] + COMMON_EXLCUDE_PATTERNS

    WESTSIDE_EXCLUDE_PATTERNS = [
        "/collection/",
        "/collections/",
    ] + COMMON_EXLCUDE_PATTERNS

    TATACLIQ_EXCLUDE_PATTERNS = [
            '/c-',
            '/brand/',
            '/support',
            '/contact',
            '/terms',
            '/shipping',
            '/returns',
            '/payment',
            '/offers',
            '/deals',
            '/sale'
        ] + COMMON_EXLCUDE_PATTERNS
