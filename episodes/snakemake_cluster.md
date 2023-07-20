---
title: "Snakemake and the Cluster"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::: questions

- How can we express a one-task cluster operation in Snakemake?

::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::: objectives

- Write a Snakefile that executes a job on the cluster
- Use MPI options to ensure the job runs in parallel

::::::::::::::::::::::::::::::::::::::::

## Snakemake and the Cluster

Snakemake has provisions for operating on an HPC cluster.

Various command-line arguments can be provided to tell
Snakemake not to run things locally, but do run things
via the queuing system instead.

In this lesson, we will repeat the first module, running
the admahl code on the cluster, but will use snakemake
to make it happen.

## Write a cluster Snakemake rule file

Open your favorite editor, do the thing.
Specify resources. Provide command line arguments
to do the cluster operations by hand.

## Run Snakemake

Throw the switch!

:::::::::::::::::::::::::::::: challenge

How can you control the degree of parallelism
of your cluster task?

:::::::::::::::: solution

Use the "mpi" option in the resource block of
the Snakemake rule, and specify the number of tasks.
This will be mapped to the `-n` argument of the
equivalent `sbatch` command.

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::: keypoints

- Snakemake rule files can submit cluster jobs.
- There are a lot of options.

::::::::::::::::::::::::::::::::::::::::
