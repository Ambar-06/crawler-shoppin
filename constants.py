class Constant:
    """
    This class to hold constant values used in the application.
    """

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
        "/privacy" "/about",
    ]
    NYKAA_EXCLUDE_PATTERNS = [
        "/category/",
        "/brand/",
        "/c/",
        "/lp/",
    ] + COMMON_EXLCUDE_PATTERNS

    VIGIO_EXCLUDE_PATTERNS = [
        "/collections/",
        "/pages/",
        "/smile-in-style",
        "/know-your-size",
        "/checkout",
    ] + COMMON_EXLCUDE_PATTERNS

    WESTSIDE_EXCLUDE_PATTERNS = [
        "/category/",
        "/collection/",
        "/collections/",
        "/checkout",
    ] + COMMON_EXLCUDE_PATTERNS
