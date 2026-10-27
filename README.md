# AI-Assisted Box Selection System

A small Django REST-style application that recommends the most suitable shipping box for an ecommerce order.

## Problem

Each product has dimensions and weight. Each box has internal dimensions, maximum weight capacity, and cost. The system checks which boxes can contain the ordered products and recommends the most suitable valid box.

## Approach

1. Validate product and box dimensions/weights.
2. Treat product orientation as rotatable.
3. For a single-product order, check whether at least one orientation fits inside a box.
4. For multiple products, use a simple deterministic packing heuristic:
   - Sort products by volume descending.
   - Place each product into the first available layer/position where an orientation fits.
   - Track remaining rectangular spaces.
5. Reject boxes that cannot contain all products or exceed weight capacity.
6. Rank valid boxes by:
   - lowest cost,
   - then lowest unused volume.

This is intentionally a small, explainable heuristic rather than an optimal 3-D bin-packing solver.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## API

### Health check

`GET /api/health/`

### Recommend a box

`POST /api/recommend/`

Example:

```json
{
  "products": [
    {"name": "Keyboard", "length": 30, "width": 15, "height": 5, "weight": 1.2},
    {"name": "Mouse", "length": 12, "width": 7, "height": 4, "weight": 0.2}
  ],
  "boxes": [
    {"name": "Small", "length": 35, "width": 20, "height": 10, "max_weight": 3, "cost": 50},
    {"name": "Medium", "length": 50, "width": 30, "height": 20, "max_weight": 8, "cost": 80}
  ]
}
```

## Response

A successful request returns the selected box and the ranked valid candidates.

## Testing

Run:

```bash
python manage.py test
```

See `TEST_OUTPUT.md` for a sample structure. Replace it with your own actual terminal output before submission.

## Important submission notes

The hiring assignment asks for an AI usage record, test cases, test output, and an exported chat transcript. The chat transcript and the "What did you learn?" section should be written/exported by the candidate as required by the assignment.
