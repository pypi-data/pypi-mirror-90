import setuptools, sys, shutil, os
import abbrs

package_name = 'abbrs' # abbrs.current_path()
description = 'Abbreviations'
abbrs.write_file("README.md",f'''# {package_name}

{description}

`abbrs/__init__.py`:

```python
{abbrs.read_file('{}/__init__.py'.format(package_name))}
```''')

long_description = abbrs.read_file("README.md")

sys.argv.extend('sdist bdist_wheel'.split())

try:
	shutil.rmtree('dist')
except FileNotFoundError:
	pass

setuptools.setup(
	name=package_name,
	version=abbrs.next_version(),
	author="YAN Hui Hang, GDUFS",
	author_email="yanhuihang@126.com",
	description=description,
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/yanhuihang/{}".format(package_name),
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		# "License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)

os.system('python -m twine upload dist/*')