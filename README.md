# cy4740-final-project

## Running the Proxy

### Using the container

### Using your local development environment

1. Run `pipenv install` to set up the 

## Development Environment

Pipenv is used to easily manage virtual environments and dependencies. Black is the code formatter,
MyPy is used for type checking, and PyLint is used for linting. The developer dependencies can
be installed by running `pipenv install --dev`.

### Updating dependencies

When a new dependency is added, make sure to run `pipenv lock -r > src/requirements.txt` to update
the `requirements.txt` file used for the container.
