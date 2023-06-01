---
title: "More Complicated Snakefiles"
teaching: 10
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions 

- What is a task graph?
- How does the Snakemake file express a task graph?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Write a multiple-rule Snakefile with dependent rules
- Translate between a task graph and rule set


:::::::::::::::::::::::::::::::::::::

## Snakemake and Workflow

A Snakefile can contain multiple rules. In the trivial
case, there will be no dependencies between the rules, and
they can all run concurrently.

A more interesting case is when there are dependencies between
the rules, e.g. when one rule takes the output of another rule
as its input. In this case, the dependent rule (the one that needs
another rule's output) cannot run until the rule it depends on 
has completed. 

It's possible to express this relationship by means of 
a task graph, whose nodes are tasks, and whose arcs are 
input-output relationships between the tasks.

A Snakemake file is textual description of a task
graph.

## Write a multi-rule Snakemake rule file

Open your favorite editor, do the thing.

## Run Snakemake

Throw the switch!

::::::::::::::::::::::::::::::::::::: challenge

Draw the task graph for your Snakefile.

Given an example task graph, write a Snakefile that
implements it.

:::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: solution

The rules in the snakefile are nodes in the task
graph. Two rules are connected by an arc in the task
graph if the output of one rule is the input to the
other. The task graph is directed, so the arc points
from the rule that generates a file as output to the rule
that consumes the same file as input.

A rule with an output that no other rules consumes is
a terminal rule.

::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints 

- Snakemake rule files can be mapped to task graphs 
- Tasks are executed as required in dependency order
- Where possible, tasks may run concurrently.

::::::::::::::::::::::::::::::::::::::::::::::::
