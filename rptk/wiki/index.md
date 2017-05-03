RPTK Web API Usage
==================

RPTK is a collection of tools for use by networks operators to query
data from RPSL databases and output that data in a format suitable
for consumption by network devices.
This page details the usage of the rptk web-api service provided here.

Basic Usage
-----------

### Get available formats
To list the available output formats, query:
```
/formats
```
e.g. [`/formats`](/formats)

### Get available policies
To list the available resolution policies, query:
```
/policies
```
e.g. [`/policies`](/policies)

### Get prefix-list
To get a prefix-list for object `<obj>` in format `<fmt>`
optionally providing a resolution policy `<policy>`:
```
/<fmt>/<object>[/<policy>]
```
e.g. [`/ios/AS-WOLCOMM`](/ios/AS-WOLCOMM) or [`/ios/AS-WOLCOMM/loose`](/ios/AS-WOLCOMM/loose)
