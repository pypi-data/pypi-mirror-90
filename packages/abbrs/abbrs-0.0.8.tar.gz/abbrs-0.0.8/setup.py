import abbrs

package_name = abbrs.current_path()

abbrs.pypi_setup('Abbreviations', f'''`{package_name}/__init__.py`:

```python
{abbrs.read_file('{}/__init__.py'.format(package_name))}
```''')