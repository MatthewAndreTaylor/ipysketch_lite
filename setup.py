from setuptools import setup, find_packages
import os

with open('sketch.html', 'r') as file:
    template_content = file.read()

gen_template_content = f'''\
template = """{template_content}"""
'''

if not os.path.exists('ipysketch_lite/gen'):
    os.makedirs('ipysketch_lite/gen')

with open('ipysketch_lite/gen/__init__.py', 'w') as new_file:
    new_file.write(gen_template_content)

setup(
    packages=find_packages(),
    include_package_data=True,
)
