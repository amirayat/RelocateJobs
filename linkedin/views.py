from django.http import JsonResponse

from .models import OAUTH


def linkedin_callback(request):
    # 1. Get the code from LinkedIn's redirect
    code = request.GET.get('code')  # THIS IS CRUCIAL
    state = request.GET.get('state')

    # 2. Validate state (security check)
    if state != "linkedin_auth":
        return JsonResponse(
                {'error': 'Invalid state!'},
                status=400  # Bad Request status code
            )
    
    # 3. Update the code
    oauth_record, created = OAUTH.objects.update_or_create(
        id=1,  # This assumes you want to maintain just one record
        defaults={
            'code': code
        }
    )
    return JsonResponse({
            'status': 'success',
            'action': 'created' if created else 'updated',
        })