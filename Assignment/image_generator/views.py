from django.http import JsonResponse
from .tasks import generate_image
from celery import group

def generate_images(request):
    prompts = [
        "A red flying dog",
        "A piano ninja",
        "A footballer kid"
    ]

    # Create a group of tasks to run in parallel
    task_group = group(generate_image.s(prompt) for prompt in prompts)
    result = task_group.apply_async()

    try:
        image_data = result.get(timeout=60)  # Wait for up to 60 seconds
    except Exception as e:
        return JsonResponse({
            "error": f"Failed to generate images: {str(e)}"
        }, status=500)

    return JsonResponse({
        "message": "Images generated successfully",
        "image_data_lengths": [len(data) if data else 0 for data in image_data]
    })