from django.core.management.base import BaseCommand
from skill.models import Skill

class Command(BaseCommand):
    help = 'Import skills from skills.txt file'

    def handle(self, *args, **kwargs):
        try:
            with open('skills.txt', 'r', encoding='utf-8') as file:
                skills = set()
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('//'):
                        skills.add(line)

                existing_skills = set(Skill.objects.values_list('name', flat=True))
                new_skills = []
                
                for skill_name in skills:
                    if skill_name.lower() not in {s.lower() for s in existing_skills}:
                        new_skills.append(Skill(
                            name=skill_name,
                            is_validated=True
                        ))

                if new_skills:
                    Skill.objects.bulk_create(new_skills)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully imported {len(new_skills)} skills'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS('No new skills to import')
                    )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('skills.txt file not found')
            )