import setuptools

from subjectively_better_profanity import __version__

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subjectively_better_profanity",
    version=__version__,
    author="John Wuller",
    author_email="847785bd-d466-47cd-a536-eae4096d241d@anonaddy.me",
    description="A more stringent fork of better_profanity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/2br-2b/subjectively_better_profanity",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires="==3.*",
    packages=setuptools.find_packages(),
    data_files=[
        ("wordlist", ["subjectively_better_profanity/profanity_wordlist.txt"]),
        ("unicode_characters", ["subjectively_better_profanity/alphabetic_unicode.json"]),
    ],
    package_data={
        "subjectively_better_profanity": ["profanity_wordlist.txt", "alphabetic_unicode.json"]
    },
    include_package_data=True,
)
