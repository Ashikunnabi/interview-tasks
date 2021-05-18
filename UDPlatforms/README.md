# User App (An interview task)

An APP that stores user data.
 - Data is composed of first name, last name, address (street, city, state, and zip) 
- The app should create the following User types (Parent, Child) 
- The child cannot have an address and Must belong to a parent 
- App should have API to:  
  - Delete user data  
  - Create user data  
  - Update user data 
- Data can be saved in a file or a DB (which ever is easy)

## Programming Language & Framework

```python
Python version 3.6
Django version 3.1.3
```

## Installation
> #### Python installation

- Python 3.6 installation guide [YouTube video](https://youtu.be/dX2-V2BocqQ)  
- Python 3.x installation guide [Blog of Real Python](https://realpython.com/installing-python/)

> #### Virtual environment installation

- Virtual environment installation guide [YouTube video](https://youtu.be/APOPm01BVrk)
- Virtual environment installation guide [PyPa](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

> #### Project package installation
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the User App.

- After activating virtualenv, navigate to the project directory (where manage.py file exists). Then run the below commands :

```bash
pip install -r requirements.txt
```

## Run Project

```bash
python manage.py runserver
```
## Test Project

```bash
python manage.py test user
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)