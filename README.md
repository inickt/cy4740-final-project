# cy4740-final-project

## Running the Proxy

### Using the container

Using your container of choice, run the container using the given `Containerfile`, forwarding port
8080 to the host.

For example, with Docker this can be done with:  
`docker run -it -p 8080:8080 -v $(pwd)/tmp:/home/appuser/.mitmproxy $(docker build -f Containerfile . -q)`

If you want to use the same certificates for both pipenv and container runs, you should use:  
`docker run -it -p 8080:8080 -v $HOME/.mitmproxy:/home/appuser/.mitmproxy $(docker build -f Containerfile . -q)`

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
     dedicated browser will be collected (instead of your whole system).

2. Go to [http://mitm.it](http://mitm.it) once you have the proxy configured to download the root
   certificate and add it to your root trust store.

## Browser setup

We used Firefox for easy proxy configuration and the ability to disable telemetry to avoid muddling
our results. After the proxy server is running, set the HTTP and HTTPS proxies in Firefox's settings
to `127.0.0.1:8080`. It is also recommended in `Privacy & Security` to switch
`Enhanced Tracking Protection` to `Custom` and disable all of the trackers (so the proxy can capture
"the true web"). We also disabled OSCP and disabled all telemetry using
[these instructions](https://www.howtogeek.com/557929/how-to-see-and-disable-the-telemetry-data-firefox-collects-about-you/).

## Proxy usage

After the proxy is started, it will forward requests but not start recording. Each time you want to
group new data (usually a single website), you need to assign a new label (by pressing 1). Every
request from that point on will be grouped under that label, until a new label is set or the proxy
is closed. When you are done collecting data, press 2 to quit the proxy. The proxy will write a JSON
dump to the current directory with all of the captured requests inside of it.

## Processing data

The request json dumps can be analyzed through a few scripts in the repo. There are some pre-created
example dumps provided in `dumps`, ranging from very basic examples to 50+ sites tagged and visited.

### Generating domain network graphs

`pipenv run python src/graph.py [DUMP_FILE]`

Will generate an HTML file that, when opened in a web browser, will show each label and domain as
a node in a graph, with edges representing ever connection a site made to a certain domain.

Due to the large size of some of the graphs, it is recommended after they load to disable physics
so it is easier to look and analyze the data.

### Merging dumps

`pipenv run python src/merge_dumps.py [DUMP_FILE] [DUMP_FILE] ...`

Will combine any number of dumps into a singular merged `merge.json`, containing the data of all
given requests. If a label is the same between the dumps, the requests under that label will be
merged.

### TLS statistics

`pipenv run python src/tls_stats.py [DUMP_FILE]`

Will provide a readout on TLS version usage across sites and overall for the entire dump.

### Domain statistics

`pipenv run python src/domain_stats.py [DUMP_FILE]`

Will provide a readout on the number of requests to domains for both sites and for the overall dump.

### Certificate statistics

`pipenv run python src/cert_stats.py [DUMP_FILE]`

Will provide a readout on the most common issuers of the certificates for both sites and the
overall dump.

## Development Environment

Pipenv is used to easily manage virtual environments and dependencies. Black is the code formatter,
MyPy is used for type checking, and PyLint is used for linting. The developer dependencies can
be installed by running `pipenv install --dev`.

### Updating dependencies

When a new dependency is added, make sure to run `pipenv lock -r > src/requirements.txt` to update
the `requirements.txt` file used for the container.
