# gwordlist 

gwordlists creates wordlists from top N search queries from google driven by a custom keyword file. 

Use gwordlist to supplement your wordlists with custom keyword specific wordlists. 

## Install / Setup

You can run gwordlist with the help of python3-venv:
```
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip3 install -r requirements.txt
$ ./gwordlist -h
```

Or, use the Dockerfile. Build the gwordlist container in the project's folder:

```
docker build -t gwordlist . 
```

Since gwordlist.py is symlinked to /usr/bin in the container, we can then use the container in any directory on the system by exposing the current directory as `/data`, setting it as the workdir and running the python script directly:

```
docker run --rm -it -v $(pwd):/data -w /data gwordlist gwordlist.py  -n 10 keywords.txt foo
```


## Usage

Checkout `./gwordlist.py -h` or `docker run --rm -it -v $(pwd):/data -w /data gwordlist gwordlist.py -h`