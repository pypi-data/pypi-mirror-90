from typing import Tuple


def HTML_to_RGB(html: str) -> Tuple[int, int, int]:
    """Convert HTML color to RGB

    Parameters
    ----------
    html : str
        color in HEX format (ex: #FFFFFF)
    """
    h = html.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def RGB_to_HTML(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB color to HTML

    Parameters
    ----------
    html : str
        color in HEX format (ex: #FFFFFF)
    """
    return '#{:s}'.format(
        ''.join(
            hex(c).lstrip('0x').ljust(
                2, '0') for c in rgb))
