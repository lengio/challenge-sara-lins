## Taken Decisions 

- I chose to use Python because it is a language that I'm confortable with.
- I didn't use any framework because it is a simple project, and a framework would generate a lot of boilerplate code.
- I didn't put the token directly in the code because I didn't want to make it public for a matter of security.

**Note:** To understand the code easily, you can follow from line 97.

## Complexity

- The total time complexity is: O(n) + O(n x m_log_m) + O(n x m) = **O(n x m_log_m)**, where n is the number of users and m is the number of activities for each user


## How to run the code

### Running locally

- Install [Python](https://www.python.org/downloads/) if you don't have it already.
- Go to the project's directory and run the following command:
  - `pip install -r requirements.txt`
- Add a environment variable called `API_TOKEN` with the API's token.
  - If you don't know how to do that, simply run: `API_TOKEN=<token> python3 main.py`
- Run: `python main.py` (or `python3 main.py`) 

### Using Docker

If for some weird reason you don't have a python interpreter, but do have Docker installed, you can run this code through it.
Run the following commands:

- `docker build -t testslang .`
- `docker run -e API_TOKEN=<token> -it testslang`, where `<token>` is the API's token.



