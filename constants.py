class Constant:
    """
    This class to hold constant values used in the application.
    """
    NYKAA_PRODUCT_PATTERNS = [
            '/buy/',
            '/product/',
            '/p/',
            '/products/',
            '/item/'
        ]
    NYKAA_EXCLUDE_PATTERNS = [
            '/category/',
            '/brand/',
            '/search',
            '/wishlist',
            '/cart',
            '/account',
            '/login',
            '/c/',
            '/lp/'
        ]
    
    VIGIO_PRODUCT_PATTERNS  = [
            '/products/',
            '/product/',
            '/p/',
            '/item/'
        ]
    
    VIGIO_EXCLUDE_PATTERNS = [
            '/collections/',
            '/pages/',
            '/smile-in-style',
            '/know-your-size',
            '/account',
            '/cart',
            '/checkout',
            '/search',
            '/wishlist',
            '/login',
            '/register'
        ]