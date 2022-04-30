import logging
import sys

from django.db import connection

from dds.services.hardcode_data import GROUPS, ARTICLES


def drop_migrations():
    query = 'DELETE FROM django_migrations;'
    with connection.cursor() as cursor:
        cursor.execute(query)


def deploy_script():
    import django.apps
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_finance.settings")

    django.setup()

    from django.contrib.auth.models import Group, Permission
    from dds.models import Article

    for article in ARTICLES:
        art, created = Article.objects.get_or_create(
            type_operation=article[0],
            name=article[1],
        )
        logging.info(f'Article {article[0]}-{article[1]} was created') if created else logging.info(f'Article {article[0]}-{article[1]} already exist')

    admin, created_admin = Group.objects.get_or_create(name='admin')
    user, created_user = Group.objects.get_or_create(name='user')
    admin_to_create = []
    user_to_create = []
    for perm in Permission.objects.all():
        if perm.name in GROUPS['admin']:
            admin_to_create.append(perm)
            logging.info(f'Perm {perm.name} added to admin group')
        if perm.name in GROUPS['user']:
            user_to_create.append(perm)
            logging.info(f'Perm {perm.name} added to user group')
    admin.permissions.set(admin_to_create)
    user.permissions.set(user_to_create)


if __name__ == '__main__':
    sys.argv.pop(0)
    command = sys.argv[0]
    if command == 'deploy_script':
        deploy_script()
    elif command == 'drop_migrations':
        drop_migrations()
    else:
        logging.error(f'Command "{command}" not found. Try "deploy_script" or "drop_migrations"')
