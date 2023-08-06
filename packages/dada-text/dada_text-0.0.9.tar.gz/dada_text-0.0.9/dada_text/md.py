import markdown


def md_to_html(md: str):
    """
    Convert a markdown string into html.
    :param md: A string containing mardown
    :return str
    """
    return markdown(md)
