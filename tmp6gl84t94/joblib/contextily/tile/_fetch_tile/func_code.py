# first line: 250
@memory.cache
def _fetch_tile(tile_url, wait, max_retries):
    request = _retryer(tile_url, wait, max_retries)
    with io.BytesIO(request.content) as image_stream:
        image = Image.open(image_stream).convert("RGBA")
        array = np.asarray(image)
        image.close()
    return array
