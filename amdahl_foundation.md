---
title: "Running a Parallel Application on the Cluster"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions 

- What output does the Amdahl code generate?
- Why does parallelizing the amdahl code make it faster?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Run the amdahl parallel code on the cluster
- Note what output is generated, and where it goes
- Predict the trend of execution time vs parallelism

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

A high-performance computing cluster offers powerful
computational resources to its users, but taking advantage
of these resources is not always straightforward. The
cluster system does not work in the same way as systems
you may be more familiar with.

The software we will use in this lesson is a model of
the kind of parallel task that is well-adapted to
high-performance computing resources. It's called "amdahl",
named for Eugene Amdahl, a famous computer scientist who
coined "Amdahl's Law", which is about the advantages and
limitations of parallelism in code execution.


:::::::::::::::::::::::::::::::::: callout

[Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law) is
a statement about how much benefit you can expect to get by
parallelizing a computer program.

The limitation arises from the fact that, in any application,
there is some fraction of the work to be done which is inherently
serial, and some fraction which is amenable to parallelization.
The law is a quantitative expression of the fact that, by
parallelizing the code, you can only ever make the parallel
part faster, you cannot reduce the execution time of the
serial part.

As a practical matter, this means that developer effort spent
on parallelization has diminishing returns on the overall
reduction in execution time.

:::::::::::::::::::::::::::::::::::::

## The Amdahl Code

Download it and install it, via pip.

## Running It on the Cluster

Use the `sacct` command to see the run-time. The run-time
is also recorded in the output itself.

::::::::::::::::::::::::::::::::::::: challenge

Run the amdhal code with a few (small!) levels
of parallelism. Make a quantitative estimate of
how much faster the code will run with 3 processors
than 2. The naive estimate would be that it would run
1.5x the speed, or equivalently, that it would
complete in 2/3 the time.

::::::::::::::::::::::::::::::::::::: solution

The amdahl code runs faster with 3 processors than with
2, but the speed-up is less than 1.5x.

:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints 

- The amdahl code is a model of a parallel application
- The execution speed depends on the degree of parallelism

::::::::::::::::::::::::::::::::::::::::::::::::
