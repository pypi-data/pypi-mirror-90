# django-easy-drf

A simple package that makes for you the repetitive work of creating Serializers, ViewSets and urls for django rest framework.

## Installation
On a virtualenv run:
```
pip install django-easy-drf
```

## Usage
On the same virtualenv, you will have *easy-drf* command available, so run:
```
easy-drf
```
This command will create serializers.py, views.py and urls.py files on the same directory, with all the classes created.

Note: requires that a file called models.py exists on the current directory.

#### Future developments
- [x] Warn users about files override.
- [x] Allow users to force script without prompt.
- [ ] Allow users to create just one specific file.
- [ ] Allow users to create just one model.
- [ ] Allow users to specify different models file.
- [ ] Allow users to specify different results file names.


### Contributing
If you have an idea or an implementation, let me know by submitting an issue or a PR.
