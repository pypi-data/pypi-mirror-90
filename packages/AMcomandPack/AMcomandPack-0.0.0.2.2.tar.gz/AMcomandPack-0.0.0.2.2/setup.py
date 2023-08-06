from setuptools import setup, find_packages

setup(
    name = "AMcomandPack",
    packages=["AMcomandPack/geo",
              "AMcomandPack",
              "AMcomandPack/geo/extensions"],
    version="0.0.0.2.2",
    license='wtfpl',
    description="clean implementation of functions from AM class at fgz",
    long_description="""
    geo -= rendering =-
        -  cleaner tkinter Canvas
            - add a clean implementation of the Canvas addons to stuff
        -  cleaner tkinter Tk 
            - nothing as of yet same a tkinter.Tk
        - extensions scripting utils
            - Xmas egsample with falling snow flakes
    
    update:
        added render axis to goeCanvas
    """,
    include_package_data = True,
    author = 'Julian Wandhoven',                   # Type in your name
    author_email = 'julian.wandhoven@fgz.ch',

    url="https://github.com/JulianWww/AMCommandPack2",
    download_url="https://github.com/JulianWww/AMCommandPack2/archive/Canvas.tar.gz",
    keywords=["am", "utils", "aid"],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3'],#Specify which pyhton versions that you want to support
)
