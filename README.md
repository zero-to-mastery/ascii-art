<img src="https://raw.githubusercontent.com/dawsonbooth/ascii-art/master/logo.png" width="250" align="right"/>

# [![ASCII ART](https://img.shields.io/badge/PYTHON%20PROJECT-ASCII%20ART-blue?style=for-the-badge&logo=Python)](https://github.com/zero-to-mastery/ascii-art)

Welcome to this years Python challenge for Hacktoberfest, a project with beginners and aspiring developers in mind, utilizing Python to convert images into ASCII Art.

## ❇️ Getting Started with Hacktoberfest

Hacktoberfest is a month-long celebration of open source, organised by Digital Ocean. ([More details here](https://github.com/zero-to-mastery/Hacktoberfest-2024/blob/master/README.md))

If you've never made a pull request before, or participated in an open-source project, we recommend taking a look at:

- Our [Start Here Guidelines](https://github.com/zero-to-mastery/start-here-guidelines)
- Our [Youtube Video](https://www.youtube.com/watch?v=uQLNFRviB6Q).

These two resources have everything you need to learn about open-source, with a step-by-step guide to making your very first PR. Once you've got your feet wet, you're ready to come back and dive into Hacktoberfest fun!

---

<img src="https://images.ctfassets.net/aq13lwl6616q/51gDR7DozuNea9fltdgHIc/0c8577f24eaa1b33c40656a522f2d1db/hacktoberfest_discord_banner.png?h=250" align="center" />

---

## ❇️ But what is ASCII Art?

> ASCII art is a graphic design technique that uses computers for presentation and consists of pictures pieced together from the 95 printable characters defined by the ASCII Standard from 1963 and ASCII compliant character sets with proprietary extended characters.
> ~ [Wikipedia](https://en.wikipedia.org/wiki/ASCII_art)

## ❇️ How to get started:

In order to get started on this project, it is recommended that you watch the section on **Scripting** in the [Python course](https://zerotomastery.io/courses/learn-python/?utm_source=github&utm_campaign=ascii-art-hf24). We talk about `sys.argv` and `Pillow` library (Image processing) in that section which would help you!

1. First up you need to fork (make a copy) of this repo to your Github account.
2. Clone (download) your fork to your computer
3. Set your streams so you can sync your clone with the original repo (get the latest updates)

   - `git remote add upstream https://github.com/zero-to-mastery/ascii-art.git`
   - `git pull upstream master`
   - The above 2 commands will synchronize your forked version of the project with the actual repository.

4. Make sure you have Python 3 installed on your machine
5. Install necessary dependencies by running `pip3 install -r requirements.txt`.
6. Run the example code with the command: `python3 example/make_art.py example/ztm-logo.png`
7. Stare with amazement 😮
8. Start chatting with other ZTM students in the #hacktoberfest-2024 channel on our Discord to get help, work together, and share your contributions!

## ❇️ How to contribute?

Now that you see how this command line tool works, let's see how we can evolve it with our ZTM community help!! Maybe we want to display this on an HTML web page where users can submit images and we convert it to ASCII art? Maybe we want to improve how the Command Line Tool works/make it more customizeable? Or maybe modify the script to do many other types of art beyond ASCII.

The options are endless and there is no wrong answer. This is all for fun, so try to customize the tool whichever way you think would be best and let's see what we get at the end of the month! Enjoy!

> ⚠ Please do **not** make changes to the files in the example directory, These files should remain intact for future contributors to examine and compare with the community version! Pull requests with changes to these files will be closed.

1. Examine the code in `community-version.py`, figure out what improvements your fellow community members have made (check out `FEATURES.md` for a list of existing features you can add to or improve).
2. Make an improvement, it doesnt have to be elaborate
3. Create a pull request
4. [Tweet about making your first Hacktoberfest pull request](https://ctt.ac/36L1C)

> Congratulations! You are now one pull request closer. Repeat these steps until you have made at least 4 qualifying pull requests. You can check how many qualifying pull requests you have made at <https://hacktoberfest.digitalocean.com/profile> Have Fun and Happy Coding!

### Bonus Task

Looking for a challenge?
We have left the original code which was written in Python 2 under the `example/make_art_python2.py` file. See what happens when you run it with Python 3. See all of the errors? Can you fix it so it works with python 3? The answer is with the `example/make_art.py` file which is written in Python 3.

**All discussions around this event can now be had in our dedicated Hacktoberfest channel on Discord!**
