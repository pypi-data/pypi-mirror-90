import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplemc",
    version="0.0.2",
    author="Elflanded",
    author_email="Elflanded@gmail.com",
    description="A simple API for the game Minecraft.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elflanded/simplemc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# pypi-AgENdGVzdC5weXBpLm9yZwIkMDk5MGRhMjEtMjM2OS00MDdkLWI3OWYtZmYwMjBjODEwZjRhAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiBidtqRrZXJmLXAQnJKBTrvNzbO_LSctsftbFQct_YNYQ