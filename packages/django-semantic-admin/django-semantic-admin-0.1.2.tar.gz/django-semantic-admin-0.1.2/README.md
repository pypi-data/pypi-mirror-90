A Django Semantic UI Admin theme
--------------------------------
Django [Semantic UI](https://semantic-ui.com/) Admin is a completely free (MIT) admin theme for Django. Actually, this is my 3rd admin theme for Django. The first used GridForms, and the second Pure CSS. Semantic UI is the best, because of its JavaScript components, 

Semantic UI is ideal for the Django admin.

Why?
----
* Looks professional, with a nice sidebar.
* JavaScript datepicker and timepicker components.
* JavaScript selects, including multiple selections, which integrate well with Django autocomplete fields.
* Semantic UI has libraries for [React](https://react.semantic-ui.com/) and [Vue](https://semantic-ui-vue.github.io/#/), in addition to jQuery. This means this package can be used to style the admin, and custom views can be added with React or Vue components with the same style.

Install
-------

Install from PyPI:

```
pip install django-semantic-admin
```

Add to `settings.py` before `django.contrib.admin`:

```
INSTALLED_APPS = [
  "semantic_admin",
  "django.contrib.admin",
  ...
]
```

Please note, this package uses [Fomantic UI](https://fomantic-ui.com/) the official community fork of Semantic UI.
