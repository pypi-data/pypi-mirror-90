# oracle_kernel

![PyPI version](https://img.shields.io/pypi/pyversions/oracle_kernel.svg)
![Github license](https://img.shields.io/github/license/Hourout/oracle_kernel.svg)
[![PyPI](https://img.shields.io/pypi/v/oracle_kernel.svg)](https://pypi.python.org/pypi/oracle_kernel)
![PyPI format](https://img.shields.io/pypi/format/oracle_kernel.svg)
![contributors](https://img.shields.io/github/contributors/Hourout/oracle_kernel)
![downloads](https://img.shields.io/pypi/dm/oracle_kernel.svg)

Oracle Kernel for Jupyter

[中文介绍](document/chinese.md)

## Installation

#### step1:
```
pip(3) install oracle_kernel
```

To get the newest one from this repo (note that we are in the alpha stage, so there may be frequent updates), type:

```
pip(3) install git+git://github.com/Hourout/oracle_kernel.git
```

#### step2:
Add kernel to your jupyter:

```
python(3) -m oracle_kernel.install
```

ALL DONE! 🎉🎉🎉

## Uninstall

#### step1:

View and remove oracle kernel
```
jupyter kernelspec list
jupyter kernelspec remove oracle
```

#### step2:
uninstall oracle kernel:

```
pip(3) uninstall oracle-kernel
```

ALL DONE! 🎉🎉🎉


## Using

```
jupyter notebook
```
<img src="image/oracle1.png"  />

### step1: you should set oracle host and port

### step2: write your oracle code
![](image/oracle2.png)

## Quote 
kernel logo

<img src="https://sensorstechforum.com/wp-content/uploads/2017/01/oracle-logo-1024x559.png" width = "32" height = "32" />

- https://sensorstechforum.com/oracle-fixed-270-security-flaws-products/
