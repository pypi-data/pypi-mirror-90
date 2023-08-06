from setuptools import setup 


setup(
	name='planfix-py',
	version='0.1',
	license='MIT',
	description='Python package for working with Planfix API',

	url='https://github.com/LD31D/planfix_py',

	author='LD31D',
	author_email='artem.12m21@gmail.com',

	packages=['planfix_py'],

	install_requires=[
		"requests",
    ],

	zip_safe=False
)
