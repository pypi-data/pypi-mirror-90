# Yandex to Lightroom
Python Script to download images from Yandex.Images for using in Adobe Lightroom.

# Features
* Checking for captcha presence
* Many filters
* Multiproccessing is available (option `--num-workers`)
* Existing images can be skipped.  
* Set search keywords as Lightroom keywords.
* Set image url as creator web address (IPTC)

# Main requirements
* Python 3.9+ 
* Selenium Wire 2.1.2+  
* Exiftool 12.13+
* Chrome, Firefox, Safari and Edge are supported. 

# Installation
1. [Python](https://www.python.org/downloads/)
2. PIP 
   * Windows
        * python -m pip install --upgrade pip
   * macOS
        * curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py  
        * python get-pip.py
3. [Selenium Wire](https://pypi.org/project/selenium-wire/) 
    * pip install selenium-wire
4. [Selenium driver executable](https://www.selenium.dev/downloads/)  
   Get the right driver for your browser (see browser section on the link above)
   and platform. Firefox, Chrome, Safari and Edge are supported.   
   Use option `--driver-path` to specify the driver's path or add the executable in your PATH.  
   Additional helpful pages:
    * [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/downloads)
    * [How To Run Test On macOS Using Selenium Safari Driver](https://www.lambdatest.com/blog/selenium-safaridriver-macos/)
5. [Exiftool](https://exiftool.org)  
   The exiftool executable must added in your PATH. For macOS, it is done automatically by putting it into
   /usr/local/bin. For Windows, you must extend your PATH variable. 

# Examples
Simple example using [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/):

```$ yandex2lightroom Chrome --keywords "vodka, bears, balalaika" --limit 10```

Example of using keywords from input file with specific image extension/format:

```$ yandex2lightroom Chrome --keywords_from_file input_example.txt --itype=png```

All other information can be obtained with the `--help` argument.

# Use case textures for Photoshop
Yandex2Lightroom sets keywords in the images after download. The keywords are the same as you define for the searches
itself.
To build a useful library for wall textures in Lightroom we need different searches with meaningful keywords.
We should place these searches - better: the corresponding Yandex2Lightroom commands - into a batch or shell script file.
Thereby, we are able to repeat the download commands to a later point in time again.
For Windows ``y2lr-texture-wall.bat``

    @echo off
    rem brick, cracked
    yandex2lightroom Chrome --keywords "wall white brick cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red brick cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black brick cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow brick cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    rem brick, old
    yandex2lightroom Chrome --keywords "wall white old brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red old brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black old brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow old brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    rem concrete cracked
    yandex2lightroom Chrome --keywords "wall white concrete cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red concrete cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black concrete cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow concrete cracked" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    rem concrete old
    yandex2lightroom Chrome --keywords "wall white old concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red old concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black old concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow old concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    rem brick, new
    yandex2lightroom Chrome --keywords "wall white new brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red new brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black new brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow new brick" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    rem concrete, new
    yandex2lightroom Chrome --keywords "wall white new concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall red new concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall black new concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls
    yandex2lightroom Chrome --keywords "wall yellow new concrete" --limit 50 --isize large --skip-existing  --output-directory D:\Users\johndoe\Lightroom\Yandex\photos\library\texture\walls

For macOS ``y2lr-texture-wall.sh``

    #!/usr/bin/env bash
    # brick, cracked
    yandex2lightroom Chrome --keywords "wall white brick cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red brick cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black brick cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow brick cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    # brick, old
    yandex2lightroom Chrome --keywords "wall white old brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red old brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black old brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow old brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    # concrete cracked
    yandex2lightroom Chrome --keywords "wall white concrete cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red concrete cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black concrete cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow concrete cracked" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    # concrete old
    yandex2lightroom Chrome --keywords "wall white old concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red old concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black old concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow old concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    # brick, new
    yandex2lightroom Chrome --keywords "wall white new brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red new brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black new brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow new brick" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    # concrete, new
    yandex2lightroom Chrome --keywords "wall white new concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall red new concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall black new concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls
    yandex2lightroom Chrome --keywords "wall yellow new concrete" --limit 50 --isize large --skip-existing  --output-directory /Users/johndoe/Lightroom/Yandex/photos/library/texture/walls


After the images were downloaded, import them into LR:
* Just add, of course.
* Maybe not use your standard metadata preset.

Please check the keywords. Sometimes LR does not import them all. In Adobe Bridge they are fine, but not in LR. If so,
select all images and read in the metadata again.   
Also, some images may have no keywords because the exiftool run into a problem. There is a smart collection in LR to 
look for images without keywords. So at least you have a chance to set keywords manually.

# See also
The Lightroom plugin [Import From Yandex](https://github.com/sto3014/LRImportFromYandex) offers an integration of
Yandex to Lightroom into Lightroom.

# Acknowledgements
Special thanks to Alexander Kozlov (https://pypi.org/project/yandex-images-download/). He did most of the work through 
his project.

