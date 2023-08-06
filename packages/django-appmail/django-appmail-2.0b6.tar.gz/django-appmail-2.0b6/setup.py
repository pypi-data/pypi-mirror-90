# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appmail', 'appmail.migrations']

package_data = \
{'': ['*'],
 'appmail': ['templates/*',
             'templates/admin/appmail/emailtemplate/*',
             'templates/admin/appmail/loggedmessage/*',
             'templates/appmail/*',
             'tests/fixtures/*']}

install_requires = \
['django>=3.0,<4.0']

setup_kwargs = {
    'name': 'django-appmail',
    'version': '2.0b6',
    'description': 'Django app for managing localised email templates.',
    'long_description': '# Django-AppMail\n\nDjango app for managing transactional email templates.\n\n## Compatibility\n\nThis project now requires Django 3.0+ and Python 3.7+. If you require a previous\nversion you will have to refer to the relevant branch or tag.\n\n## Background\n\nThis project arose out of a project to integrate a large transactional Django\napplication with Mandrill, and the lessons learned. It also owes a minor h/t\nto this project from 2011 (https://github.com/hugorodgerbrown/AppMail).\n\nThe core requirement is to provide an easy way to add / edit email templates\nto a Django project, in such a way that it doesn\'t require a developer to make\nchanges. The easiest way to use templated emails in Django is to rely on the\nin-built template structure, but that means that the templates are held in\nfiles, under version control, which makes it very hard for non-developers to\nedit.\n\nThis is **not** a WYSIWYG HTML editor, and it doesn\'t do anything clever. It\ndoesn\'t handle the sending of the emails - it simply provides a convenient\nmechanism for storing and rendering email content.\n\n```python\nfrom appmail.models import EmailTemplate, AppmailMessage\n\ndef send_order_confirmation(order_id):\n    order = Orders.objects.get(id=order_id)\n    template = EmailTemplate.objects.current(\'order_confirmation\')\n    context = { "order": order }\n    message = AppmailMessage(\n        template=template,\n        context=context,\n        to=[order.recipient.email]\n    )\n    message.send()\n```\n\nThe core requirements are:\n\n1. List / preview existing templates\n2. Edit subject line, plain text and HTML content\n3. Use standard Django template syntax\n4. Support base templates\n5. Template versioning\n6. Language support\n7. Send test emails\n\n**Template properties**\n\nIndividual templates are stored as model objects in the database. The\nstandard Django admin site is used to view / filter templates. The templates\nare ordered by name, language and version. This combination is unique. The\nlanguage and version properties have sensible defaults (\n`version=settings.LANGUAGE_CODE` and `version=0`) so don\'t need to set if you\ndon\'t require it. There is no inheritance or relationship between different\nlanguages and versions - they are stored as independent objects.\n\n```python\n# get the default order_summary email (language = settings.LANGUAGE_CODE)\ntemplate = EmailTemplate.objects.current(\'order_summary\')\n# get the french version\ntemplate = EmailTemplate.objects.current(\'order_summary\', language=\'fr\')\n# get a specific version\ntemplate = EmailTemplate.objects.version(\'order_summary\', 1)\n```\n\n**Template syntax**\n\nThe templates themselves use standard Django template syntax, including\nthe use of tags, filters. There is nothing special about them, however there\nis one caveat - template inheritance.\n\n**Template inheritance**\n\nAlthough the template content is not stored on disk, without re-engineering\nthe template rendering methods any parent templates must be. This is annoying,\nbut there is a valid assumption behind it - if you are changing your base\ntemplates you are probably involving designers and developers already, so\nhaving to rely on a developer to make the changes is acceptable.\n\n**Sending test emails**\n\nYou can send test emails to an email address through the admin list view.\n\n<img src="screenshots/appmail-test-email-action.png" alt="EmailTemplate admin change form" />\n\nThe custom admin action \'Send test emails\' will redirect to an intermediate\npage where you can enter the recipient email address and send the email:\n\n<img src="screenshots/appmail-test-email-send.png"/>\n\nThere is also a linkon individual template admin pages (top-right, next to the history link):\n\n<img src="screenshots/appmail-template-change-form.png" alt="EmailTemplate admin change form" />\n\n## Tests\n\nThere is a test suite for the app, which is best run through ``tox``.\n\n## License\n\nMIT\n\n## Contributing\n\nUsual rules apply:\n\n1. Fork to your own account\n2. Fix the issue / add the feature\n3. Submit PR\n\nPlease take care to follow the coding style - and PEP8.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
