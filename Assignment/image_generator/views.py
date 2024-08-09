from django.shortcuts import render
from django.http import JsonResponse
from .tasks import generate_images
from django.views.decorators.csrf import ensure_csrf_cookie
from celery.result import GroupResult, AsyncResult
from .models import GeneratedImage


@ensure_csrf_cookie
def generate_images_view(request):
    if request.method == 'POST':
        prompts = [
            request.POST.get('prompt1'),
            request.POST.get('prompt2'),
            request.POST.get('prompt3')
        ]
        prompts = [p for p in prompts if p]  # Remove any empty prompts

        if prompts:
            try:
                group_id = generate_images.delay(prompts)
                return JsonResponse({
                    "group_id": str(group_id),
                    "message": f"Image generation tasks started for {len(prompts)} prompts"
                })
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    return render(request, 'image_generator/generate.html')


def check_task_status(request, group_id):
    group_result = GroupResult.restore(group_id)
    if group_result is None:
        # If GroupResult is not found, try to get individual task result
        task = AsyncResult(group_id)
        if task.ready():
            if task.successful():
                return JsonResponse({
                    "status": "completed",
                    "successful_results": [task.result],
                    "failed_results": []
                })
            else:
                return JsonResponse({
                    "status": "failed",
                    "successful_results": [],
                    "failed_results": [str(task.result)]
                })
        else:
            return JsonResponse({"status": "pending"})

    if group_result.ready():
        successful_results = []
        failed_results = []
        for task in group_result.results:
            if task.successful():
                successful_results.append(task.result)
            elif task.failed():
                failed_results.append(str(task.result))

        return JsonResponse({
            "status": "completed",
            "successful_results": successful_results,
            "failed_results": failed_results
        })
    else:
        return JsonResponse({"status": "pending"})


def show_generated_images(request):
    images = GeneratedImage.objects.all().order_by('-created_at')
    return render(request, 'image_generator/show_images.html', {'images': images})