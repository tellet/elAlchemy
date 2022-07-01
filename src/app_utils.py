from kivy.uix.button import Button


def split_into_pages(cocktails):
    """
    Split list into a list of pages, 10 items per page
    :param cocktails:
    :return: list of lists
    """
    page_size = 10
    all_len = len(cocktails)
    result = []
    if all_len <= page_size:
        return [cocktails]
    pages_count = all_len // page_size + 1
    for p in range(pages_count):
        start = p * page_size
        end = p * page_size + page_size
        result.append(cocktails[start:end])
    return result


def is_base_color(color):
    base_color = [1, 1, 1, 1]
    return all(item == base_color[0] for item in color)


def change_color(button: Button):
    flag = is_base_color(button.background_color)
    if flag:
        button.background_color = [10, 1, 1, 3]
    else:
        button.background_color = [1, 1, 1, 1]
    return button.background_color
