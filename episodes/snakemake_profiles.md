---
title: "Snakemake Profiles"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::: questions

- How can we encapsulate our desired snakemake configuration?
- How do we balance non-reptition and customizability?

::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::: objectives

- Write a Snakemake profile for the cluster
- Run the amdahl code with varying degrees of parallelism
  with the cluster profile.

::::::::::::::::::::::::::::::::::::::::

## Snakemake Profiles

Snakemake has a provision for profiles, which allow users
to collect various common settings together in a special
file that snakemake examines when it runs. This lets users
avoid repetition and possible errors of omission for common
settings, and encapsulates some of the cluster complexity
we encoutered in the previous module.

Not all settings should be in the profile. Users can
choose which ones to make static and which ones to make
adjustable. In our case, we will want to have the freedom
to choose the degree of parallelism, but most of the
cluster arguments will not change, and so can be static
in the profile.

## Write a Profile

Do the thing.

## Run Snakemake

Throw the switch!

:::::::::::::::::::::::::::::: challenge

Write a profile that allows you to choose a
different partition, in addition to the level of
parallelism.

::::::::::::::::::::::::::::::::::::::::

:::::::::::::::: solution

The profile files can have variables taken from
the rule file, and in particular can refer to
resources from a rule.

:::::::::::::::::::::::::

:::::::::::::::::::::::::::::: keypoints

- Snakemake profiles encapsulate cluster complexity.
- Retaining operational flexibliity is also important.

::::::::::::::::::::::::::::::::::::::::
