# Kongfigurator

I could have named it something else.

## How to use

```
usage: kongfigurator.py [-h] [-o OUTFILE] [-s SERVICES] [-r ROUTES] [-c CONSUMERS] [-t TAGS]

feed me your desired config

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Name of file to write to.
  -s SERVICES, --services SERVICES
                        number of services you want (default is 1)
  -r ROUTES, --routes ROUTES
                        number of routes PER service (default is 1)
  -c CONSUMERS, --consumers CONSUMERS
                        number of consumers (default is 0)
  ```

These will expand and perhaps change soon. Always use `./kongfigurator.py -h` to get the latest options.

## What's it do?

Creates randomized kong.yaml based on your parameter inputs. 

Once your kong.yaml file is created use it as any other: sync the config or start up with it. 