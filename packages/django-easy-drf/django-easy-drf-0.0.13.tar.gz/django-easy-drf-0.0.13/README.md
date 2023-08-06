# django-easy-drf

A package that makes for you the repetitive work of creating Serializers, ViewSets and urls for django rest framework.

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

##### Forcing creation
If you want to avoid command prompt, you can force it:
```
easy-drf --force
```
or less verbose:
```
easy-drf -f
```
##### Creating only one file
Sometimes you don't need all files (views, serializers and urls) so you can specify which ones should be created. Options are:
- 's' for serializers.py
- 'v' for views.py
- 'u' for urls.py

For example, this command will create serializers.py and views.py
```
easy-drf --files s v
```
If you don't specify --files argument, all files will be created.

##### Getting help
For help, type:
```
easy-drf --help
```
or less verbose:
```
easy-drf -h
```
This command will list the available cli options.

#### Future developments
- [x] Warn users about files override.
- [x] Allow users to force script without prompt.
- [x] Allow users to create just one specific file.
- [ ] Allow users to create just one model.
- [ ] Allow users to specify different models file.
- [ ] Allow users to specify different results file names.


### Contributing
If you have an idea or an implementation, let me know by submitting an issue or a PR.
