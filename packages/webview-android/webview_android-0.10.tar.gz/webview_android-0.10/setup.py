import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webview_android", 
    version="0.10",
    author="Edilson Pineda",
    author_email="edilsonpineda011@gmail.com",
    description="Simple WebView for android with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
    ],
    keywords='webview android kivy kivymd Android WebView python-for-android python',
    install_requires=['pyjnius'],
    python_requires='>=3',
)
