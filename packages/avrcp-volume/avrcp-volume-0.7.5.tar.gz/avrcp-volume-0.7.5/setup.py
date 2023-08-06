
import setuptools

from avrcp_volume import APP_NAME

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = APP_NAME,
	version = '0.7.5',
	python_requires = '>=3.8',
	install_requires = [
		'dbus-next>=0.1.3',
		'desktop-notify>=1.2.1',
		'pulsectl>=20.4.3',
	],
	entry_points = {
		'console_scripts': [
			APP_NAME + ' = avrcp_volume:main',
		],
	},
	package_data={
		'': ['resources/' + APP_NAME + '.service'],
	},
	author = 'hxss',
	author_email = 'hxss@ya.ru',
	description = 'Avrcp volume controller',
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = 'https://gitlab.com/hxss-linux/avrcp-volume',
	packages = setuptools.find_packages(),
	classifiers = [
		'Programming Language :: Python :: 3.8',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux',
		'Topic :: Utilities',
	],
)
