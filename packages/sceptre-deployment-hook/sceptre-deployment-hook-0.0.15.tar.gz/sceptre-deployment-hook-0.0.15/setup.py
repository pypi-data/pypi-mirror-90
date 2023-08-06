import sys


if sys.version_info < (3,7):
    sys.exit('Sorry, Python < 3.7 is not supported')

from setuptools import find_packages
from distutils.core import setup

setup(
    name='sceptre-deployment-hook',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['tests']),
    version="0.0.15",
    license='Apache-2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Sceptre hook to measure stack deployment time',  # Give a short description about your library
    author='Vereniging COIN',  # Type in your name
    author_email='devops@coin.nl',  # Type in your E-Mail
    url='https://gitlab.com/verenigingcoin/open-source/sceptre-hooks/deployment-hook',
    # Provide either the link to your github or to your website
    keywords=['COIN', 'AWS', 'Sceptre'],  # Keywords that define your package best
    python_requires='>=3.7',
    zip_safe=False,
    platforms='any',
    entry_points={
        'sceptre.hooks': [
            'stack_deploy_time = hook.hook:CustomHook',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.7',
    ],
)
