import setuptools

setuptools.setup(
    name="vtkpython_cbl",
    version="2021.01.05",
    author="Martin Genet",
    author_email="martin.genet@polytechnique.edu",
    description=open("README.md", "r").readlines()[1][:-1],
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/mgenet/vtkpython_cbl",
    packages=["vtkpython_cbl"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy", "vtk", "myPythonLibrary", "myVTKPythonLibrary"],
)

# python -m keyring set https://upload.pypi.org/legacy/ username

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
