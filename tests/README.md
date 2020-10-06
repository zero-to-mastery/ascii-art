#### [Unittest](https://docs.python.org/3/library/unittest.html)
The tests.py is a simple example of using unittest. 

Just have fun adding some new tests, modify them, etc :)

Usage:
`python -m unittest -v tests.Testing`


---

### [Coverage](https://coverage.readthedocs.io/en/coverage-5.3/)
Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.

Usage:

Run:
`coverage run ../community-version.py ../ztm-logo.png`

See the report: 
`coverage report`

See the report in html with a view of what was tested:
```
coverage html
(this command will create a folder 'htmlcov' with the test report in html)
```
