---
title: "Chaining rules"
teaching: 40
exercises: 30
---

::: questions

- "How do I combine rules into a workflow?"
- "How do I make a rule with multiple inputs and outputs?"

:::

::: objectives

- ""

:::

## A pipeline of multiple rules

We now have a rule that can generate output for any value of `-p` and any number
of tasks, we just need to call Snakemake with the parameters that we want:

```bash
snakemake --profile cluster_profile p_0.999/runs/amdahl_run_6.json
```

That's not exactly convenient though, to generate a full dataset we have to run
Snakemake lots of times with different output file targets. Rather than that,
let's create a rule that can generate those files for us.

Chaining rules in Snakemake is a matter of choosing filename patterns that
connect the rules.
There's something of an art to it - most times there are several options that
will work:

```python
rule generate_run_files:
    output: "p_{parallel_proportion}_runs.txt"
    input:  "p_{parallel_proportion}/runs/amdahl_run_6.json"
    shell:
        "echo {input} done > {output}"
```

::: challenge

The new rule is doing no work, it's just making sure we create the file we want.
It's not worth executing on the cluster. How do ensure it runs on the login node
only?

:::::: solution

We need to add the new rule to our `localrules`:

```python
localrules: hostname_login, generate_run_files
```

:::

:::

Now let's run the new rule (remember we need to request the output file by name
as the `output` in our rule contains a wildcard pattern):

```bash
[ocaisa@node1 ~]$ snakemake --profile cluster_profile/ p_0.999_runs.txt
```

```output
Using profile cluster_profile/ for setting default command line arguments.
Building DAG of jobs...
Retrieving input from storage.
Using shell: /cvmfs/software.eessi.io/versions/2023.06/compat/linux/x86_64/bin/bash
Provided remote nodes: 3
Job stats:
job                   count
------------------  -------
amdahl_run                1
generate_run_files        1
total                     2

Select jobs to execute...
Execute 1 jobs...

[Tue Jan 30 17:39:29 2024]
rule amdahl_run:
    output: p_0.999/runs/amdahl_run_6.json
    jobid: 1
    reason: Missing output files: p_0.999/runs/amdahl_run_6.json
    wildcards: parallel_proportion=0.999, parallel_tasks=6
    resources: mem_mb=1000, mem_mib=954, disk_mb=1000, disk_mib=954,
               tmpdir=<TBD>, mem_mb_per_cpu=3600, runtime=2, mpi=mpiexec, tasks=6

mpiexec -n 6 amdahl --terse -p 0.999 > p_0.999/runs/amdahl_run_6.json
No SLURM account given, trying to guess.
Guessed SLURM account: def-users
Job 1 has been submitted with SLURM jobid 342 (log: /home/ocaisa/.snakemake/slurm_logs/rule_amdahl_run/342.log).
[Tue Jan 30 17:47:31 2024]
Finished job 1.
1 of 2 steps (50%) done
Select jobs to execute...
Execute 1 jobs...

[Tue Jan 30 17:47:31 2024]
localrule generate_run_files:
    input: p_0.999/runs/amdahl_run_6.json
    output: p_0.999_runs.txt
    jobid: 0
    reason: Missing output files: p_0.999_runs.txt;
            Input files updated by another job: p_0.999/runs/amdahl_run_6.json
    wildcards: parallel_proportion=0.999
    resources: mem_mb=1000, mem_mib=954, disk_mb=1000, disk_mib=954,
               tmpdir=/tmp, mem_mb_per_cpu=3600, runtime=2

echo p_0.999/runs/amdahl_run_6.json done > p_0.999_runs.txt
[Tue Jan 30 17:47:31 2024]
Finished job 0.
2 of 2 steps (100%) done
Complete log: .snakemake/log/2024-01-30T173929.781106.snakemake.log
```

Look at the logging messages that Snakemake prints in the terminal.
What has happened here?

1. Snakemake looks for a rule to make `p_0.999_runs.txt`
1. It determines that "generate_run_files" can make this if
   `parallel_proportion=0.999`
1. It sees that the input needed is therefore `p_0.999/runs/amdahl_run_6.json`
1. Snakemake looks for a rule to make `p_0.999/runs/amdahl_run_6.json`
1. It determines that "amdahl_run" can make this if `parallel_proportion=0.999`
   and `parallel_tasks=6`
1. Now Snakemake has reached an available input file (in this case, no input
   file is actually required), it runs both steps to get the final output

This, in a nutshell, is how we build workflows in Snakemake.

1. Define rules for all the processing steps
1. Choose `input` and `output` naming patterns that allow Snakemake to link the
   rules
1. Tell Snakemake to generate the final output file(s)

If you are used to writing regular scripts this takes a little
getting used to. Rather than listing steps in order of execution, you are alway
**working backwards** from the final desired result. The order of operations is
determined by applying the pattern matching rules to the filenames, not by the
order of the rules in the Snakefile.

::: callout

## Outputs first?

The Snakemake approach of working backwards from the desired output to determine
the workflow is why we're putting the `output` lines first in all our rules - to
remind us that these are what Snakemake looks at first!

Many users of Snakemake, and indeed the official documentation, prefer to have
the `input` first, so in practice you should use whatever order makes sense to
you.

:::

::: callout 

## `log` outputs in Snakemake

Snakemake has a dedicated rule field for outputs that are
[log files](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#log-files),
and these are mostly treated as regular outputs except that log files are not
removed if the job produces an error. This means you can look at the log to help
diagnose the error. In a real workflow this can be very useful, but in terms of
learning the fundamentals of Snakemake we'll stick with regular `input` and
`output` fields here.

:::

::: callout

## Errors are normal

Don't be disheartened if you see errors when first testing
your new Snakemake pipelines. There is a lot that can go wrong when writing a
new workflow, and you'll normally need several iterations to get things just
right. One advantage of the Snakemake approach compared to regular scripts is
that Snakemake fails fast when there is a problem, rather than ploughing on
and potentially running junk calculations on partial or corrupted data. Another
advantage is that when a step fails we can safely resume from where we left off.

:::



::: keypoints

- "Snakemake links rules by iteratively looking for rules that make missing
  inputs"
- "Rules may have multiple named inputs and/or outputs"
- "If a shell command does not yield an expected output then Snakemake will
  regard that as a failure"

:::
