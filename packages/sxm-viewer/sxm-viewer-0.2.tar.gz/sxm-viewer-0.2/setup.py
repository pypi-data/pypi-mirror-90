import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sxm-viewer",
    version="0.2",
    author="Cocca Guo",
    author_email="guojiadong@bnu.edu.cn",
    description="a PyQt5 based tool for inspecting *.sxm files and save them as figures swiftly.",
    url="https://github.com/CoccaGuo/sxm-viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
     package_data={
        '': ['icon.png']
     },
    entry_points={
            "console_scripts": [
                "sxmv=sxm_viewer.main:main"
            ],
        },
    install_requires=[
    'pySPM',
    'PyQt5',
    'matplotlib'
    ],
    python_requires='>=3',
)