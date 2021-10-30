from setuptools import setup, find_packages


setup(  name='aifactory_alpha',

        version='1.0.1',

        description='alpha version of AI Factory client api package',

        author='yoosunyoung',

        author_email='luysunyoung@aifactory.page',

        url='https://www.aifactory.space',

        license='MIT',

        py_modules=['API', 'FileUtilities', 'Authentification', 'constants', 'greetings', 'submit'],

        python_requires='>=3.0',

        install_requires=['pycryptodomex', 'requests'],

        package_dir={'': "src/"},

        packages=find_packages('src'),

        scripts=['bin/aifactory-submit', 'bin/aifactory-leader-board'],

        include_package_data=True,

        package_data={'submission': ['formats/training_recipe_format.json']}
)
