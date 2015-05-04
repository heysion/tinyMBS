from setuptools import setup,find_packages
setup(
    name="pymbs",
    version="0.0.1",
    description="Python tiny message bus servce",
    keywords='pymbs',
    author='Heysion Yuan',
    license='Expat license',
    py_modules=['pymbs'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    packages = find_packages(exclude=["*.test.*", "test.*", "test"]),
)
