import requests
from celery import shared_task, group
from django.conf import settings
import base64
from django.core.files.base import ContentFile
from django.apps import apps
from celery import shared_task, group
from celery.result import GroupResult

@shared_task
def generate_images(prompts):
    task_group = group(generate_image.s(prompt) for prompt in prompts)
    group_result = task_group.apply_async()
    GroupResult.save(group_result)
    return group_result.id

@shared_task
def generate_image(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {settings.STABILITY_AI_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }

        response = requests.post(settings.STABILITY_AI_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            image_data = result['artifacts'][0]['base64']

            GeneratedImage = apps.get_model('image_generator', 'GeneratedImage')

            generated_image = GeneratedImage(prompt=prompt)

            image_data = base64.b64decode(image_data)
            file_name = f"generated_image_{generated_image.id}.png"

            generated_image.image.save(file_name, ContentFile(image_data), save=False)

            generated_image.save()

            return f"Image generated and saved with ID: {generated_image.id}"
        else:
            raise ValueError(f"API request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        # Log the error here if you have logging set up
        raise ValueError(f"Error generating image: {str(e)}")