---
title: "Introduction to Snakemake"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::: questions

- What are Snakemake rules?
- Why do Snakemake rules not always run?

::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::: objectives

- Write a single-rule Snakefile and execute it with Snakemake
- Predict whether the rule will run or not

::::::::::::::::::::::::::::::::::::::::

## Snakemake

Snakemake is a workflow tool. It takes as input
a description of the work that you would like the computer
to do, and when run, does the work that you have
asked for.

The description of the work takes the form of a
series of rules, written in a special format into a
Snakefile. Rules have outputs, and the Snakefile
and generated output files make up the system state.

## Write a Snakemake rule file

Open your favorite editor, do the thing.

## Run Snakemake

Throw the switch!

:::::::::::::::::::::::::::::: challenge

Remove the output file, and run Snakemake. Then
run it again. Edit the output file, and run it
a third time. For which of these invocations
does Snakemake do non-trivial work?

:::::::::::::::: solution

The rule does not get executed the second time. The
Snakemake infrastructure is stateful, and knows that
the required outputs are up to date.

The rule also does not get executed the third time.
The output is not the output from the rule, but the
Snakemake infrastructure doesn't know that, it only
checks the file time-stamp. Editing Snakemake-manipulated
files can get you into an inconsistent state.

:::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::: keypoints

- Snakemake is an indirect way of running executables
- Snakemake has a notion of system state, and can be fooled.

::::::::::::::::::::::::::::::::::::::::
