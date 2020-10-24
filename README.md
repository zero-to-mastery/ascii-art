<img src="https://raw.githubusercontent.com/dawsonbooth/ascii-art/master/logo.png" width="400" align="right"/>

# ASCII Art - Hacktoberfest 2020✔

Welcome to this years Python challenge for Hacktoberfest ([What is Hacktoberfest?](https://github.com/zero-to-mastery/coding_challenge-31/blob/master/README.md#what-is-hacktoberfest)) A project with beginners and aspiring developers in mind, utilizing Python to convert images into ASCII Art.

#### What is ASCII Art❓
> ASCII art is a graphic design technique that uses computers for presentation and consists of pictures pieced together from the 95 printable characters defined by the ASCII Standard from 1963 and ASCII compliant character sets with proprietary extended characters.
~ [Wikipedia](https://en.wikipedia.org/wiki/ASCII_art)


## How to get Started:
In order to get started on this project, it is recommended that you watch the section on **Scripting** in the [Python course](https://academy.zerotomastery.io/p/complete-python-developer-zero-to-mastery?utm_source=github&utm_campaign=ascii-art-hf20). We talk about ```sys.argv``` and ```Pillow```(https://pillow.readthedocs.io/en/stable/) library (Image processing) in that section which would help you!

> If you've never made a pull request before, or participated in an open-source project, we recommend taking a look at our [Start Here Guidelines](https://github.com/zero-to-mastery/start-here-guidelines). This repo has everything you need to learn about open-source, with a step-by-step guide to making your very first PR.
> Once you've got your feet wet, you're ready to come back and dive into Hacktoberfest fun!

1. First up you need to fork (make a copy) of this repo to your Github account.
2. Clone (download) your fork to your computer
3. Set your streams so you can sync your clone with the original repo (get the latest updates)
    - `git remote add upstream https://github.com/zero-to-mastery/ascii-art.git`
    - `git pull upstream master`
    - The above 2 commands will synchronize your forked version of the project with the actual repository.
4. Make sure you have [Python 3](https://www.python.org/downloads/) installed on your machine.

5. Install project dependencies, for example with `pip`:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the  example code with the command: `python3 example/make_art.py example/ztm-logo.png example`
7. Stare with amazement 😮

## How to contribute?
> For more extensive instruction on how to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md). It has instructions about setting up a package as a developer (instead of a user of the package).

Now that you see how this command line tool works, let's see how we can evolve it with our ZTM community help!! Maybe we want to display this on an HTML web page where users can submit images and we convert it to ASCII art? Maybe we want to improve how the Command Line Tool works/make it more customizeable? Or maybe modify the script to do many other types of art beyond ASCII. 

The options are endless and there is no wrong answer. This is all for fun, so try to customize the tool whichever way you think would be best and let's see what we get at the end of the month! Enjoy! 

0. Run `pip install -e .` in your environment to install the ascii_art package. This way your changes to it will reflect without needing a reinstall.
1. Examine the code in `ascii_art/`, figure out what improvements your fellow community members have made. 
    > Run `ascii_art --help` to see how the program works and play around with it.
    > The interesting files in ascii_art/ are: `ascii_art.py`, `cli.py`
    > `ascii_art.py` has the implementation of creating ascii art.
    > 'cli.py` implements how the commandline interaction is handled. It uses `ascii_art.py` to do the actual work.
2. Make an improvement, it doesnt have to be elaborate
3. Test the program to ensure you haven't broken the existing functionality (this will help you catch a lot of mistakes before making your changes public)
4. Commit your changes and push to your remote repository
```bash
git push origin <branch>
```
5. Create a pull request
6. [Tweet about making your first Hacktoberfest pull request](https://ctt.ac/bbIct)

> Congratulations! You are now one pull request closer to getting that free t-shirt. Repeat these steps until you have made at least 4 qualifying pull requests. You can check how many qualifying pull requests you have made at <https://hacktoberfest.digitalocean.com/profile> Have Fun and Happy Coding!

### Bonus Task➕
Looking for a challenge?
We have left the original code which was written in Python 2 under the `example/make_art_python2.py` file. See what happens when you run it with Python 3. See all of the errors? Can you fix it so it works with python 3? The answer is with the `example/make_art.py` file which is written in Python 3.

**All discussions around this event can now be had in our #hacktoberfest-2020 channel on Discord!**

## Disclaimer🔴
Zero To Mastery receive no commission or incentives for your participating in either this project or entering the Hacktoberfest event. 
