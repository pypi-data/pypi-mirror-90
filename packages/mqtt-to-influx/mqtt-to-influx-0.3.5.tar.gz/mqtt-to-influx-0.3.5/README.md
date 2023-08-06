This is a tool that 

- digests mqtt messages
- tries to detect their types
- applies some conversion to known types
- and ingests them into influx

# Install
```
python3 setup.py sdist 
pip3 install dist/mqtt-to-influx-<version>tar.gz 
```
