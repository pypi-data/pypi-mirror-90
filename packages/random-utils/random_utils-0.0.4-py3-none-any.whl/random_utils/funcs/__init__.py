def flatten(list_to_flatten) -> iter:
    for item in list_to_flatten:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
