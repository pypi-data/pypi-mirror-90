A Django Semantic UI Admin theme
--------------------------------
Django [Semantic UI](https://semantic-ui.com/) Admin is a completely free (MIT) admin theme for Django. Actually, this is my 3rd admin theme for Django. The first was with GridForms, and the second Pure CSS.

Semantic UI is best for the Django admin, because of its responsive design and its JavaScript components.

Why?
----
* Looks professional, with a nice sidebar.
* Resonsive design, even [tables can stack](https://semantic-ui.com/collections/table.html#stacking) responsively on mobile.
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
