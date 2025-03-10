from django.http import JsonResponse
from django.db.models import Q
from .models import Skill

def search_skills(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})

    # Search for existing skills
    skills = Skill.objects.filter(
        Q(name__icontains=query)
    ).values('id', 'name', 'is_validated')[:10]

    results = list(skills)

    # If no exact match exists, add the option to create new skill
    if query and not any(s['name'].lower() == query.lower() for s in results):
        results.append({
            'id': 'new',
            'name': query,
            'is_validated': False,
            'create_option': True
        })

    return JsonResponse({'results': results})