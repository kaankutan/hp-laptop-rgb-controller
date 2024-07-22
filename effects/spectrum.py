import colorsys

def spectrum(n):
    """
    Generates a list of colors representing a smooth spectrum.

    Args:
    n (int): Number of colors in the spectrum.

    Returns:
    List[str]: List of hex color strings.
    """
    spectrum = []
    for i in range(n):
        h = i / n
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        color = '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
        spectrum.append(color)
    return spectrum
