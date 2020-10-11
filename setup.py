from setuptools import setup, find_packages
import pathlib

base_dir = pathlib.Path(__file__).parent.resolve()

long_description = (base_dir/"README.md").read_text(encoding="utf-8")


setup(
    name="VaishnavismNotifyTBot",
    version="0.1",
    description="A telegram bot for the Vaishnavism",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="s_j_u_k_d_o_m",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Licence :: OSI Approved :: MIT Licence"
    ],
    keywords="telegram, bot",
    packages=find_packages(),
    python_requires=">=3.8.5"
)