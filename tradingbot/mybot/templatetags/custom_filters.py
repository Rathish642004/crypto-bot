# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_asset_price')
def get_asset_price(asset_prices_dict, asset_name):
    """
    Custom template filter to retrieve the price of an asset based on its name.

    Parameters:
    - asset_prices_dict: A dictionary containing asset prices, where keys are asset names and values are prices.
    - asset_name: The name of the asset whose price needs to be retrieved.

    Returns:
    - The price of the asset, or an empty string if the asset name is not found in the dictionary.
    """
    return asset_prices_dict.get(asset_name, '')
