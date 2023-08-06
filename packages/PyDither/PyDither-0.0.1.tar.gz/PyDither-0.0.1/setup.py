from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
     name='PyDither',
     version='0.0.1',
     author="utkarsh-deshmukh",
     author_email="utkarsh.deshmukh@gmail.com",
     description="python - image dithering",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Utkarsh-Deshmukh/image-dithering-python",
     download_url="https://github.com/Utkarsh-Deshmukh/image-dithering-python/archive/main.zip",
     install_requires=['numpy==1.19.0', 'opencv-python'],
     license='MIT',
     keywords=['image dithering'],
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )