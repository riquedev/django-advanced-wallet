import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_advanced_wallet",
    version="0.0.1",
    author="Henrique da Silva Santos",
    author_email="henrique.santos@4u360.com.br",
    description="An extensible wallet package for quick integration into your Django project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://github.com/riquedev/django-initials-avatar",
    keywords="wallet, framework, django",
    project_urls={
        "Bug Tracker": "https://github.com/riquedev/django-advanced-wallet/issues",
        "Repository": "https://github.com/riquedev/django-advanced-wallet",
    },
    install_requires=[
        'Django>=3.2.14',
    ],
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.6"
)
