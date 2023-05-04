def main(results: list) -> list:
    no_cats = []
    for result in results:
        if not result['contains_cat']:
            no_cats.append(result['image_name'])
    return no_cats