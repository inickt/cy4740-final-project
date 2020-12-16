# cy4740-final-project

## Running the Proxy

### Using the container

Using your container of choice, run the container using the given `Containerfile`, forwarding port
8080 to the host.

For example, with Docker this can be done with:  
`docker run -it -p 8080:8080 -v $(pwd)/tmp:/home/appuser/.mitmproxy $(docker build -f Containerfile . -q)`

If you want to use the same certificates for both pipenv and container runs, you should use:  
`-v $HOME/.mitmproxy:/home/appuser/.mitmproxy`

### Using your local development environment

1. Run `pipenv install` to set up the dependencies needed to run the proxy.
2. Run `pipenv run python src/proxy.py` to start the proxy and capture plugin.

## Setting up the proxy connection

1. Configure the HTTP proxy. mitmproxy provides some high level details
[here](https://docs.mitmproxy.org/stable/concepts-modes/#regular-proxy).
   - You can connect locally or from another device, just figure out your local IP address and use
     port 8080.
   - If possible, only configure a dedicated browser instead of your whole computer to use the 
     proxy. That way, during development, your main browser will still work, and only traffic from your
     dedicated browser will be colleted (instead of your whole system).

2. Go to [http://mitm.it](http://mitm.it) once you have the proxy configured to download the root
   certificate and add it to your root trust store.

## Development Environment

Pipenv is used to easily manage virtual environments and dependencies. Black is the code formatter,
MyPy is used for type checking, and PyLint is used for linting. The developer dependencies can
be installed by running `pipenv install --dev`.

### Updating dependencies

When a new dependency is added, make sure to run `pipenv lock -r > src/requirements.txt` to update
the `requirements.txt` file used for the container.
