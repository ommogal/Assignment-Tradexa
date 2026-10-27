from itertools import permutations


class ValidationError(Exception):
    pass


def volume(item):
    return item["length"] * item["width"] * item["height"]


def orientations(item):
    dims = (item["length"], item["width"], item["height"])
    return list(set(permutations(dims)))


def validate_item(item, kind):
    required = ["length", "width", "height"]
    if kind == "product":
        required += ["weight"]
    else:
        required += ["max_weight", "cost"]

    missing = [key for key in required if key not in item]
    if missing:
        raise ValidationError(f"{kind} is missing: {', '.join(missing)}")

    for key in required:
        if not isinstance(item[key], (int, float)) or item[key] <= 0:
            raise ValidationError(f"{kind}.{key} must be greater than 0")


def can_fit_product(product, box):
    return any(
        p[0] <= box["length"]
        and p[1] <= box["width"]
        and p[2] <= box["height"]
        for p in orientations(product)
    )


def recommend_box(products, boxes):
    if not products:
        raise ValidationError("products must not be empty")
    if not boxes:
        raise ValidationError("boxes must not be empty")

    for product in products:
        validate_item(product, "product")
    for box in boxes:
        validate_item(box, "box")

    total_weight = sum(p["weight"] for p in products)
    valid = []

    for box in boxes:
        if total_weight > box["max_weight"]:
            continue

        # Fast necessary checks.
        if any(not can_fit_product(p, box) for p in products):
            continue

        # Conservative volume check followed by a simple packing heuristic.
        if sum(volume(p) for p in products) > volume(box):
            continue

        if pack_products(products, box):
            unused = volume(box) - sum(volume(p) for p in products)
            valid.append({
                "box": box,
                "unused_volume": unused,
            })

    if not valid:
        return None

    valid.sort(key=lambda x: (x["box"]["cost"], x["unused_volume"]))
    return {
        "selected_box": valid[0]["box"],
        "candidates": [
            {
                "box": item["box"],
                "unused_volume": item["unused_volume"],
            }
            for item in valid
        ],
    }


def pack_products(products, box):
    """
    Simple deterministic shelf/layer heuristic.

    Products are placed in descending volume order. Each layer has a
    fixed height equal to the tallest product in that layer. Within a
    layer, products are arranged left-to-right, then a new row is used.
    This is intentionally explainable and suitable for the assignment's
    small system; it is not an optimal 3-D packing algorithm.
    """
    items = sorted(products, key=volume, reverse=True)

    # Try each permutation of the first product orientation as the
    # layer's base direction. Subsequent products may rotate freely.
    for first_orientation in orientations(items[0]):
        if first_orientation[0] > box["length"] or first_orientation[1] > box["width"]:
            continue

        layers = []
        success = True

        for product in items:
            placed = False
            for layer in layers:
                for dims in orientations(product):
                    if (
                        dims[2] <= layer["height"]
                        and layer["used_x"] + dims[0] <= box["length"]
                        and dims[1] <= layer["max_y"]
                    ):
                        layer["used_x"] += dims[0]
                        placed = True
                        break
                if placed:
                    break

            if placed:
                continue

            for dims in orientations(product):
                if dims[0] <= box["length"] and dims[1] <= box["width"]:
                    current_height = sum(layer["height"] for layer in layers)
                    if current_height + dims[2] <= box["height"]:
                        layers.append({
                            "height": dims[2],
                            "used_x": dims[0],
                            "max_y": dims[1],
                        })
                        placed = True
                        break

            if not placed:
                success = False
                break

        if success:
            return True

    return False
