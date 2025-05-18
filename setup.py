from setuptools import setup, find_packages

setup(
    name='bank_deposit',
    version='0.0.1',
    description='QuickBooks-style bank deposit app for ERPNext',
    author='Faisal Alkuwari',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'frappe>=15.0.0',
    ],
    zip_safe=False
)
