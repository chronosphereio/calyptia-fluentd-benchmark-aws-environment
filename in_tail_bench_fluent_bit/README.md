# in\_tail Scenario Benchmark for Fluent Bit

## Introduction

This benchmark scenario is aimed to execute benchmark about the following target.

* tail-bench

In the above benchmark scenario, the following resources are monitored.

* CPU usage (fluent-bit process)
* RSS (fluent-bit process)
* VMS (fluent-bit process)
* Read Bytes
* Write Bytes
* Receive Bytes
* Send Bytes

## Directory layout

* ansible/*
  * Ansible scripts
* config/*
  * Collection of customize Windows.
* visualize/
  * Collection of plot script from *.csv

After executing benchmark, the result is collected under `ansible/output/*`.

## Execute benchmark

There are 3 steps to execute benchmark scenario.

* provisioning -  `make`
* benchmarking -  `make tail-bench`
* visualizing - `make visualize` or `make visualize-line`

#### Setup

For creating instances:

```
$ make
```

Or, only creating instances:

```
$ make apply
```

And apply provisioning playbook:

```
$ make provision
```

#### Execute Benchmarks

```
$ make tail-bench
```

#### Visualization

##### Prerequisites

* python3-seaborn
* python3-pandas

and their dependencies.

##### Box plot

```
$ make visualize
```

##### Line plot

```
$ make visualize-line
```

#### Teardown

For destroying instances:

```
$ make clean
```
