# THIS PACKAGE IS UNDER DEVELOPMENT, DO NOT USE IN PRODUCTION


django-advanced-wallet
---
<dl>
    <table>
      <tr>
        <th>Summary</th>
        <td>An extensible wallet package for quick integration into your Django project.</td>
      </tr> 
      <tr> 
        <th>Django Packages</th>
        <td><a href="https://djangopackages.org/packages/p/django-initials-avatar/">packages/django-initials-avatar</a></td>
      </tr>
    </table>
</dl>

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/riquedevbr)

## Installing
First add the application to your Python path. The easiest way is to use pip:

```shell
pip install django-advanced-wallet
```

Check the [Release History](https://pypi.org/project/django-initials-avatar/#history) tab on the PyPI package page for
pre-release versions. These can be downloaded by specifying the version.

You can also install by downloading the source and running:

```shell
python setup.py install
```

## Configuring

Make sure you have add the django_advanced_wallet application to your INSTALLED_APPS list:

```python
INSTALLED_APPS = (
    ...
    'django_advanced_wallet',
)
```