from celery import shared_task
import requests
from django.conf import settings

@shared_task(bind=True)
def generate_image(self, prompt):
    try:
        response = requests.post(
            f"{settings.STABILITY_API_HOST}/v1/generation/{settings.STABILITY_ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {settings.STABILITY_API_KEY}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()
        image_data = data["artifacts"][0]["base64"]

        print(f"Image generated for prompt: {prompt}")
        print(f"Image data length: {len(image_data)}")

        return image_data
    except Exception as exc:
        print(f"Error generating image: {exc}")
        return None