---
title: "Running Snakemake on the cluster"
teaching: 30
exercises: 20
---

::: objectives

- "Define rules to run locally and on the cluster"

:::

::: questions

- "How do I run my Snakemake rule on the cluster?"

:::

What happens when we want to make our rule run on the cluster rather than the
login node? The cluster we are using uses Slurm, and it happens that Snakemake
has built in support for Slurm, we just need to tell it that we want to use it.

Snakemake uses the `executor` option to allow you to select the plugin that you
wish to execute the rule. The quickest way to apply this to your Snakefile is to
define this on the command line. Let's try it out

```bash
[ocaisa@node1 ~]$ snakemake -j1 -p --executor slurm hostname_login
```

```output
Building DAG of jobs...
Retrieving input from storage.
Nothing to be done (all requested files are present and up to date).
```

Nothing happened! Why not? When it is asked to build a target, Snakemake checks
the 'last modification time' of both the target and its dependencies. If any
dependency has been updated since the target, then the actions are re-run to
update the target. Using this approach, Snakemake knows to only rebuild the
files that, either directly or indirectly, depend on the file that changed. This
is called an _incremental build_.

::: callout
## Incremental Builds Improve Efficiency

By only rebuilding files when required, Snakemake makes your processing
more efficient.
:::

::: challenge
## Running on the cluster

We need another rule now that executes the `hostname` on the _cluster_. Create
a new rule in your Snakefile and try to execute it on cluster with the option
`--executor slurm` to `snakemake`.

:::::: solution
The rule is almost identical to the previous rule save for the rule name and
output file:

```python
rule hostname_remote:
    output: "hostname_remote.txt"
    input:
    shell:
        "hostname > hostname_remote.txt"
```

You can then execute the rule with

```bash
[ocaisa@node1 ~]$ snakemake -j1 -p --executor slurm hostname_remote
```

```output
Building DAG of jobs...
Retrieving input from storage.
Using shell: /cvmfs/software.eessi.io/versions/2023.06/compat/linux/x86_64/bin/bash
Provided remote nodes: 1
Job stats:
job                count
---------------  -------
hostname_remote        1
total                  1

Select jobs to execute...
Execute 1 jobs...

[Mon Jan 29 18:03:46 2024]
rule hostname_remote:
    output: hostname_remote.txt
    jobid: 0
    reason: Missing output files: hostname_remote.txt
    resources: tmpdir=<TBD>

hostname > hostname_remote.txt
No SLURM account given, trying to guess.
Guessed SLURM account: def-users
No wall time information given. This might or might not work on your cluster.
If not, specify the resource runtime in your rule or as a reasonable default
via --default-resources. No job memory information ('mem_mb' or 
'mem_mb_per_cpu') is given - submitting without.
This might or might not work on your cluster.
Job 0 has been submitted with SLURM jobid 326 (log: /home/ocaisa/.snakemake/slurm_logs/rule_hostname_remote/326.log).
[Mon Jan 29 18:04:26 2024]
Finished job 0.
1 of 1 steps (100%) done
Complete log: .snakemake/log/2024-01-29T180346.788174.snakemake.log
```

Note all the warnings that Snakemake is giving us about the fact that the rule
may not be able to execute on our cluster as we may not have given enough
information. Luckily for us, this actually works on our cluster and we can take
a look in the output file the new rule creates, `hostname_remote.txt`:

```bash
[ocaisa@node1 ~]$ cat hostname_remote.txt
```

```output
tmpnode1.int.jetstream2.hpc-carpentry.org
```

::::::

:::

## Snakemake profile

Adapting Snakemake to a particular environment can entail many flags and
options. Therefore, it is possible to specify a configuration profile to be used
to obtain default options. This looks like

```bash
snakemake --profile myprofileFolder ...
```

The profile folder must contain a file called `config.yaml` which is what will
store our options. The folder may also contain other files necessary for the
profile. Let's create the file `cluster_profile/config.yaml` and insert some of
our existing options:

```yaml
printshellcmds: True
jobs: 3
executor: slurm
```

We should now be able rerun our workflow by pointing to the profile rather than
the listing out the options. To force our workflow to rerun, we first need to
remove the output file `hostname_remote.txt`, and then we can try out our new
profile

```bash
[ocaisa@node1 ~]$ rm hostname_remote.txt
[ocaisa@node1 ~]$ snakemake --profile cluster_profile hostname_remote
```

The profile is extremely useful in the context of our cluster, as the Slurm
executor has lots of options, and sometimes you need to use them to be able to
submit jobs to the cluster you have access to. Unfortunately, the names of the
options in Snakemake are not _exactly_ the same as those of Slurm, so we need
the help of a translation table:

| SLURM             | Snakemake         | Description                                                    |
|-------------------|-------------------|----------------------------------------------------------------|
| `--partition`     | `slurm_partition` | the partition a rule/job is to use                             |
| `--time`          | `runtime`         | the walltime per job in minutes                                |
| `--constraint`    | `constraint`      | may hold features on some clusters                             |
| `--mem`           | `mem, mem_mb`     | memory a cluster node must                                     |
|                   |                   | provide (mem: string with unit), mem_mb: int                   |
| `--mem-per-cpu`   | `mem_mb_per_cpu`  | memory per reserved CPU                                        |
| `--ntasks`        | `tasks`           | number of concurrent tasks / ranks                             |
| `--cpus-per-task` | `cpus_per_task`   | number of cpus per task (in case of SMP, rather use `threads`) |
| `--nodes`         | `nodes`           | number of nodes                                                |

The warnings given by Snakemake hinted that we may need to provide these
options. One way to do it is to provide them is as part of the Snakemake rule
using the keyword `resources`,
e.g.,

```python
rule:
    input: ...
    output: ...
    resources:
        partition = <partition name>
        runtime = <some number>
```

and we can also use the profile to define default values for these options to
use with our project, using the keyword `default-resources`. For example, the
available memory on our cluster is about 4GB per core, so we can add that to our
profile:

```yaml
printshellcmds: True
jobs: 3
executor: slurm
default-resources:
  - mem_mb_per_cpu=3600
```

:::challenge
We know that our problem runs in a very short time. Change the default length of
our jobs to two minutes for Slurm.

::::::solution

```yaml
printshellcmds: True
jobs: 3
executor: slurm
default-resources:
  - mem_mb_per_cpu=3600
  - runtime=2
```

::::::

:::

There are various `sbatch` options not directly supported by the resource
definitions in the table above. You may use the `slurm_extra` resource to
specify any of these additional flags to `sbatch`:

```python
rule myrule:
    input: ...
    output: ...
    resources:
        slurm_extra="--mail-type=ALL --mail-user=<your email>"
```

## Local rule execution

Our initial rule was to
get the hostname of the login node. We always want to run that rule on the login
node for that to make sense. If we tell Snakemake to run all rules via the
Slurm executor (which is what we are doing via our new profile) this
won't happen any more. So how do we force the rule to run on
the login node?

Well, in the case where a Snakemake rule performs a trivial task job submission
might be overkill (e.g., less than 1 minute worth of compute time). Similar to
our case, it would be a better
idea to have these rules execute locally (i.e. where the `snakemake` command is
run) instead of as a job. Snakemake lets you indicate which rules should always
run locally with the `localrules` keyword. Let's define `hostname_login` as a
local rule near the top of our `Snakefile`.

```python
localrules: hostname_login
```

::: keypoints

- "Snakemake generates and submits its own batch scripts for your scheduler."
- "You can store default configuration settings in a Snakemake profile"
- "`localrules` defines rules that are executed locally, and never submitted to a cluster."

:::
