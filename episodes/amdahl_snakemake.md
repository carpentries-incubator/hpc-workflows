---
title: "Amdahl Parallel Runs"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::: questions

- How can we collect data on Amdahl run times?

::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::: objectives

- Collect systematic data on the runtime of the amdahl code

::::::::::::::::::::::::::::::::::::::::

## Systematic Data Collection

Using what we have learned so far, including Snakemake
profiles and rules, we will now compose a Snakefile
that runs the Amdahl example code over a range of
parallel widths. This workflow will generate the
data we will use in the next module to demonstrate
the diminishing returns of increasing parallelism.

## Write a File

Compose the Snakemake file that does what we want.

We can put the widths in a list and iterate over
them. We will use the profile generated previously
to ensure that the jobs run on the cluster.

## Run Snakemake

Throw the switch!

:::::::::::::::::::::::::::::: challenge

Our example has a single paramter, the parallelism,
that we vary. How would you generalize this to arbitrary
parameters?

:::::::::::::::: solution

Arbitrary parameters are still finite, so you could
just generate a flat list of all the combinations, and iterate
over that. Or you could generate two lists and do a nested
loop.

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::: keypoints

- A relatively compact snakemake file collects interesting data.

::::::::::::::::::::::::::::::::::::::::
