from setuptools import setup, find_packages
import os

setup(  name='aifactory_alpha',

        version='0.2.0',

        description='alpha version of AI Factory client api package',

        author='yoosunyoung',

        author_email='luysunyoung@aifactory.page',

        url='https://www.aifactory.space',

        license='MIT',

        py_modules=['API', 'FileUtilities', 'Authentification', 'constants', 'greetings'],

        python_requires='>=3.0',

        install_requires=['pycryptodomex', 'requests'],

        package_dir={'': "src/"},

        packages=find_packages('src'),

        scripts=['bin/aifactory-submit'],

        include_package_data=True,

        package_data={'submission': ['formats/training_recipe_format.json']}
)
