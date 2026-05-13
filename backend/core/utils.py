from django.utils import timezone
def generate_reference(prefix: str) -> str:
    return f"{prefix}-{timezone.now().strftime('%Y%m%d%H%M%S%f')}"
