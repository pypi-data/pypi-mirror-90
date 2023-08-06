# HOWTO: jomiel

<!-- vim-markdown-toc GFM -->

- [Build and run jomiel in a container](#build-and-run-jomiel-in-a-container)
  - [Build and run a client application in a container](#build-and-run-a-client-application-in-a-container)
- [Use a proxy](#use-a-proxy)
- [Authenticate and encrypt using CURVE](#authenticate-and-encrypt-using-curve)
  - [CURVE: jomiel (server-side)](#curve-jomiel-server-side)
  - [CURVE: yomiel (client-side)](#curve-yomiel-client-side)
- [Authenticate and encrypt using SSH](#authenticate-and-encrypt-using-ssh)
  - [SSH: jomiel (server-side)](#ssh-jomiel-server-side)
  - [SSH: yomiel (client-side)](#ssh-yomiel-client-side)
  - [SSH Notes](#ssh-notes)
- [Build a release from the repo](#build-a-release-from-the-repo)

<!-- vim-markdown-toc -->

## Build and run jomiel in a container

To run `jomiel` in a container.

- build a network that `jomiel` and the clients will use:

```shell
docker network create jomiel_network
```

- build the image; start by cloning the repository:

```shell
git clone https://github.com/guendto/jomiel
cd jomiel
docker build -t tg/jomiel -f docker/pypi/Dockerfile .
```

- start the container:

```shell
docker run \
  --network jomiel_network \
  --network-alias jomiel \
  --rm tg/jomiel
```

### Build and run a client application in a container

- make sure the `network` is available (see the steps above):

```shell
docker network ls | grep jomiel
14775a938d51        jomiel_network      bridge              local
```

- check that `jomiel` container is running (see the steps above if it
  isn't):

```shell
docker ps | grep jomiel
54bd7945001e        jomiel      "jomiel -l syslog"   11 seconds ago      Up 9 seconds     wizardly_sanderson
```

- build a new `client` image; let's use [jomiel-examples] for this
  purpose:

```shell
git clone https://github.com/guendto/jomiel-examples
cd jomiel-examples
docker build \
  -t tg/jomiel-examples/c-example \
  -f c/docker/alpine/Dockerfile .
```

- run the created image (make a note of the `-r` which is used to
  specify the `jomiel` endpoint address):

```shell
docker run \
  --network jomiel_network \
  tg/jomiel-examples/c-example \
  -r tcp://jomiel:5514 \
  https://youtu.be/PRdcZSuCpNoa
```

## Use a proxy

If you need to use a proxy with HTTP connections, you can configure
proxies by setting the environment variables http_proxy and https_proxy.

```shell
export https_proxy="https://localhost:3128"
```

**"In addition to basic HTTP proxies, Requests also supports proxies
using the SOCKS protocol. This is an optional feature that requires that
additional third-party libraries be installed before use."** --
[python-requests.org]

```shell
pip install requests[socks]
```

Once you’ve installed those dependencies, using a SOCKS proxy is just as
easy as using a HTTP one:

```shell
export https_proxy="socks5://localhost:5580"
```

The proxy string can be specified with a protocol:// prefix to specify
an alternative proxy protocol (e.g. "socks4://", "socks4a://",
"socks5://" or "socks5h://").

For more information, see the [requests documentation].

## Authenticate and encrypt using CURVE

**"[CURVE is] ... a protocol for secure messaging across the
Internet."** -- [curvezmq.org]

Generate a new public and secret CURVE keypair for both server (jomiel)
and client (yomiel):

```shell
jomiel-keygen server client
```

### CURVE: jomiel (server-side)

```shell
mkdir -p .curve
mv server.secret_key .curve   # Make server CURVE secret key usable
mv client.key .curve          # Make client CURVE public key usable
jomiel --curve-enable         # Restart jomiel with CURVE enabled
```

`jomiel` will search (by default) the .curve/ subdir for

- any **public** _client keys_ (note plural)
- the **secret** _server key_

You can override the default search paths with the options:

```plaintext
--curve-server-key-file
--curve-public-key-dir
```

### CURVE: yomiel (client-side)

```shell
mkdir -p .curve
mv client.secret_key .curve   # Make client CURVE secret key usable
mv server.key .curve          # Make server CURVE public key usable
yomiel --auth-mode curve URI  # Start yomiel with CURVE enabled
```

`yomiel` will search (by default) the .curve/ subdir for

- the **secret** _client_ key
- the **public** _server_ key

You can override the default search paths with the options:

```plaintext
--curve-server-public-key-file
--curve-client-key-file
```

## Authenticate and encrypt using SSH

### SSH: jomiel (server-side)

- Have SSH configured and running
- Have `jomiel` running

### SSH: yomiel (client-side)

```shell
yomiel --auth-mode ssh --ssh-server user@host:port URI
```

### SSH Notes

- Have either [pexpect] or [paramiko](recommended) installed
- Use --ssh-paramiko to tell `yomiel` to use it

## Build a release from the repo

```shell
git clone https://github.com/guendto/jomiel
cd jomiel
git tag -s KEYID -am 'jomiel version VERSION (INITIALS)' TAGNAME
pip install pep517
python -m pep517.build [-s|-b] .
```

[jomiel-examples]: https://github.com/guendto/jomiel-examples
[pexpect]: https://pypi.org/project/pexpect/
[paramiko]: https://pypi.org/project/paramiko/
[python-requests.org]: https://2.python-requests.org/
[requests documentation]: https://2.python-requests.org/en/master/user/advanced/#proxies
[curvezmq.org]: http://curvezmq.org
