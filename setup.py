import setuptools

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdp-visualizer-justanothercoder-sserov-fortsandmills",
    version="0.0.1",
    author="Sergey Ivanov, Sergey Serov, Viktor Yanush",
    author_email="qbrick@mail.ru",
    description="A small gui app to visualize simple mdp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Scrat-the-Agent/mdp-visualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'gym>=0.17.0',
        'numpy>=1.18.0',
        'PyQt5>=5.14.0',
        'scipy>=1.4.0'
    ]
)