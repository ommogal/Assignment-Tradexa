import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import ValidationError, recommend_box


def health(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
def recommend(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        payload = json.loads(request.body)
        result = recommend_box(
            payload.get("products", []),
            payload.get("boxes", []),
        )

        if result is None:
            return JsonResponse(
                {"message": "No suitable box found"},
                status=422,
            )

        return JsonResponse(result, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except ValidationError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
