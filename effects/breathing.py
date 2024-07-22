def change_brightness(hex_color, reduction_factor):
    """
    Adjusts the brightness of a given hex color.

    Args:
        hex_color (str): The hex color code (e.g., "#ff0000").
        reduction_factor (float): The factor by which to reduce the brightness (e.g., 0.5 for 50% brightness).

    Returns:
        str: The new hex color code after applying the brightness reduction.
    """
    # Remove the '#' from the hex color if present
    hex_color = hex_color.lstrip('#')
    
    # Extract the red, green, and blue components from the hex color
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Apply the brightness reduction factor
    r = int(r * reduction_factor)
    g = int(g * reduction_factor)
    b = int(b * reduction_factor)
    
    # Ensure the RGB values are within the valid range [0, 255]
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    # Format the new color as a hex string
    new_hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return new_hex_color

def breathing(hex_color, n):
    """
    Generates a list of colors representing a breathing effect by adjusting brightness.

    Args:
        hex_color (str): The hex color code (e.g., "#ff0000").
        n (float): The step size for brightness adjustment (e.g., 0.05).

    Yields:
        str: The hex color codes representing different brightness levels.
    """
    brightness = 1  # Start with full brightness

    # Fade out the color by reducing brightness
    while brightness > 0:
        new_hex_color = change_brightness(hex_color, brightness)
        brightness = round(brightness - n, 2)
        yield new_hex_color
    
    # Fade in the color by increasing brightness
    while brightness < 1:
        brightness = round(brightness + n, 2)
        new_hex_color = change_brightness(hex_color, brightness)
        yield new_hex_color
