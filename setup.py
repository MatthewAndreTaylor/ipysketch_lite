from setuptools import setup, find_packages

with open('sketch.html', 'r') as file:
    template_content = file.read()

gen_template_content = f'''\
template = """{template_content}"""
'''

with open('ipysketch_lite/gen/__init__.py', 'w') as new_file:
    new_file.write(gen_template_content)

setup(
    packages=find_packages(),
    include_package_data=True,
)
