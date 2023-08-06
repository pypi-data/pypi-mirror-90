# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semantic_admin',
 'semantic_admin.filters',
 'semantic_admin.templatetags',
 'semantic_admin.views',
 'semantic_admin.widgets']

package_data = \
{'': ['*'],
 'semantic_admin': ['static/admin/js/*',
                    'static/admin/js/admin/*',
                    'static/admin_ordering/*',
                    'static/semantic_admin/*',
                    'static/semantic_admin/themes/basic/assets/fonts/*',
                    'static/semantic_admin/themes/default/assets/fonts/*',
                    'static/semantic_admin/themes/default/assets/images/*',
                    'templates/admin/*',
                    'templates/admin/auth/user/*',
                    'templates/admin/edit_inline/*',
                    'templates/admin/includes/*',
                    'templates/admin/widgets/*',
                    'templates/registration/*',
                    'templates/semantic_ui/forms/widgets/*']}

install_requires = \
['django-taggit>=1.3.0,<2.0.0', 'django>=3.0']

setup_kwargs = {
    'name': 'django-semantic-admin',
    'version': '0.1.4',
    'description': 'Django Semantic UI Admin theme',
    'long_description': 'A Django Semantic UI Admin theme\n--------------------------------\nDjango [Semantic UI](https://semantic-ui.com/) Admin is a completely free (MIT) admin theme for Django. Actually, this is my 3rd admin theme for Django. The first was with GridForms, and the second Pure CSS.\n\nSemantic UI is best for the Django admin, because of its responsive design and its JavaScript components.\n\nWhy?\n----\n* Looks professional, with a nice sidebar.\n* Resonsive design, even [tables can stack](https://semantic-ui.com/collections/table.html#stacking) responsively on mobile.\n* JavaScript datepicker and timepicker components.\n* JavaScript selects, including multiple selections, which integrate well with Django autocomplete fields.\n* Semantic UI has libraries for [React](https://react.semantic-ui.com/) and [Vue](https://semantic-ui-vue.github.io/#/), in addition to jQuery. This means this package can be used to style the admin, and custom views can be added with React or Vue components with the same style.\n\nInstall\n-------\n\nInstall from PyPI:\n\n```\npip install django-semantic-admin\n```\n\nAdd to `settings.py` before `django.contrib.admin`:\n\n```\nINSTALLED_APPS = [\n  "semantic_admin",\n  "django.contrib.admin",\n  ...\n]\n```\n\nPlease note, this package uses [Fomantic UI](https://fomantic-ui.com/) the official community fork of Semantic UI.\n',
    'author': 'Alex',
    'author_email': 'globophobe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/globophobe/django-semantic-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
