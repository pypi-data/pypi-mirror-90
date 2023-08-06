import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-easy-drf", # Replace with your own username
    version="0.0.12",
    scripts=['bin/easy-drf'],
    author="Pablo Pissi",
    author_email="pablopissi@gmail.com",
    description="A package to create boring stuff of django rest framework",
    long_description=long_description,
    install_requires=[
        'astunparse'
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/pablop94/django-easy-drf",
    packages=['django_easy_drf'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)