from .json_handler import FORMATTED_LAYERS

def format_name(layer_name):
    """
    Checks "formatted_layers.json" data for formatted layer name.
    
    Parameters: layer_name(str): Unformatted layer name.

    Returns: str: Formatted layer name from .json file.
    """
    if layer_name[-9:] in FORMATTED_LAYERS:
        formatted_name = FORMATTED_LAYERS[layer_name[-9:]]
    elif layer_name[-10:-1] in FORMATTED_LAYERS:
        formatted_name = FORMATTED_LAYERS[layer_name[-10:-1]]
    elif layer_name[-7:] in FORMATTED_LAYERS:
        formatted_name = FORMATTED_LAYERS[layer_name[-7:]]
    else:
        formatted_name = layer_name
    return formatted_name