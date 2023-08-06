import setuptools

setuptools.setup(
    name="musurgia",
    version="1.10.8b",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="tools for algorithmic composition",
    url="https://github.com/alexgorji/musurgia.git",
    packages=setuptools.find_packages(),
    install_requires=['quicktions==1.9',
                      'prettytable==0.7.2',
                      'musicscore',
                      'fpdf2 == 2.0.3',
                      'diff-pdf-visually == 1.4.1'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
