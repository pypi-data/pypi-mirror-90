from setuptools import setup


def readme():
	with open('README.md') as f:
		return f.read()


setup(
	name="FileInspector",
	version="0.0.1",
	license="MIT",
	description="FileInspector: Python Reusable Application.",
	long_description=readme(),
	long_description_content_type="text/markdown",
	url="https://github.com/bhojrampawar/fileinspector",
	author="Bhojram pawar",
	author_email="bhojrampawar@hotmail.com",
	packages=["fileinspector"],
	include_package_data=True,
	classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
	],
	install_requires=['pillow']
)