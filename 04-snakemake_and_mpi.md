---
title: "MPI applications and Snakemake"
teaching: 30
exercises: 20
---

::: objectives

- "Define rules to run locally and on the cluster"

:::

::: questions

- "How do I run an MPI application via Snakemake on the cluster?"

:::

Now it's time to start getting back to our real workflow. We can execute a
command on the cluster, but what about executing the MPI application we are
interested in? Our application is called `amdahl` and is available as an
environment module.

::: challenge

Locate and load the `amdahl` module and then _replace_ our `hostname_remote`
rule with a version that runs `amdahl`. (Don't worry about parallel MPI just
yet, run it with a single CPU, `mpiexec -n 1 amdahl`).

Does your rule execute correctly? If not look through the log files to find out
why?

::::::solution

```bash
module spider amdahl
module load amdahl
```

will locate and then load the `amdahl` module. We can then update/replace our
rule to run the `amdahl` application:

```python
rule amdahl_run:
    output: "amdahl_run.txt"
    input:
    shell:
        "mpiexec -n 1 amdahl > {output}"
```

However, when we try to execute the rule we get an error (unless you already
have a different version of `amdahl` available in your path). Snakemake
reports the
location of the logs and if we look inside we can (eventually) find

```output
...
mpiexec -n 1 amdahl > amdahl_run.txt
--------------------------------------------------------------------------
mpiexec was unable to find the specified executable file, and therefore
did not launch the job.  This error was first reported for process
rank 0; it may have occurred for other processes as well.

NOTE: A common cause for this error is misspelling a mpiexec command
      line parameter option (remember that mpiexec interprets the first
      unrecognized command line token as the executable).

Node:       tmpnode1
Executable: amdahl
--------------------------------------------------------------------------
...
```

So, even though we loaded the module before running the workflow, our
Snakemake rule didn't find the executable. That's because the Snakemake rule
is running in a clean _runtime environment_, and we need to somehow tell it to
load the necessary environment module before trying to execute the rule.

::::::
:::

## Snakemake and environment modules

Our application is called `amdahl` and is available on the system via an
environment module, so we need to
tell Snakemake to load the module before it tries to execute the rule. Snakemake
is aware of environment modules, and these can be specified via (yet another)
option:

```python
rule amdahl_run:
    output: "amdahl_run.txt"
    input:
    envmodules:
      "mpi4py",
      "amdahl"
    input:
    shell:
        "mpiexec -n 1 amdahl > {output}"
```

Adding these lines are not enough to make the rule execute however. Not only do
you have to tell Snakemake what modules to load, but you also have to tell it to
use environment modules in general (since the use of environment modules is 
considered to make your runtime environment less reproducible as the available
modules may differ from cluster to cluster). This requires you to give Snakemake
an additonal option

```bash
snakemake --profile cluster_profile --use-envmodules amdahl_run
```

::: challenge

We'll be using environment modules throughout the rest of tutorial, so make that
a default option of our profile (by setting it's value to `True`)

::::::solution

Update our cluster profile to

```yaml
printshellcmds: True
jobs: 3
executor: slurm
default-resources:
  - mem_mb_per_cpu=3600
  - runtime=2
use-envmodules: True
```

If you want to test it, you need to erase the output file of the rule and rerun
Snakemake.

::::::

:::

## Snakemake and MPI

We didn't really run an MPI application in the last section as we only ran on
one core. How do we request to run on multiple cores for a single rule?

Snakemake has general support for MPI, but the only executor that currently
explicitly supports MPI is the Slurm executor (lucky for us!). If we look back
at our Slurm to Snakemake translation table we notice the relevant options
appear near the bottom:

| SLURM             | Snakemake         | Description                                                    |
|-------------------|-------------------|----------------------------------------------------------------|
| ...               | ...               | ...                                                            |
| `--ntasks`        | `tasks`           | number of concurrent tasks / ranks                             |
| `--cpus-per-task` | `cpus_per_task`   | number of cpus per task (in case of SMP, rather use `threads`) |
| `--nodes`         | `nodes`           | number of nodes                                                |

The one we are interested is `tasks` as we are only going to increase the number
of ranks. We can define these in a `resources` section of our rule and refer to
them using placeholders:

```python
rule amdahl_run:
    output: "amdahl_run.txt"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi='mpiexec',
      tasks=2
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl > {output}"
```

That worked but now we have a bit of an issue. We want to do this for a few
different values of `tasks` that would mean we would need a different output
file for every run. It would be great if we can somehow indicate in the `output`
the value that we want to use for `tasks`...and have Snakemake pick that up.

We could use a _wildcard_ in the `output` to allow us to
define the `tasks` we wish to use. The syntax for such a wildcard looks like

```python
output: "amdahl_run_{parallel_tasks}.txt"
```

where `parallel_tasks` is our wildcard.

::: callout
## Wildcards

Wildcards are used in the `input` and `output` lines of the rule to represent
parts of filenames.
Much like the `*` pattern in the shell, the wildcard can stand in for any text
in order to make up
the desired filename. As with naming your rules, you may choose any name you
like for your
wildcards, so here we used `parallel_tasks`. Using the same wildcards in the
input and output is what tells Snakemake how to match input files to output
files.

If two rules use a wildcard with the same name then Snakemake will treat them as
different entities - rules in Snakemake are self-contained in this way.

In the `shell` line you can reference the wildcard with
`{wildcards.parallel_tasks}`
:::

## Snakemake order of operations

We're only just getting started with some simple rules, but it's worth thinking
about exactly what Snakemake is doing when you run it. There are three distinct
phases:

1. Prepares to run:
    1. Reads in all the rule definitions from the Snakefile
1. Plans what to do:
    1. Sees what file(s) you are asking it to make
    1. Looks for a matching rule by looking at the `output`s of all the rules
       it knows
    1. Fills in the wildcards to work out the `input` for this rule
    1. Checks that this input file (if required) is actually available
1. Runs the steps:
    1. Creates the directory for the output file, if needed
    1. Removes the old output file if it is already there
    1. Only then, runs the shell command with the placeholders replaced
    1. Checks that the command ran without errors *and* made the new output
       file as expected

::: callout
## Dry-run (`-n`) mode

It's often useful to run just the first two phases, so that Snakemake will plan out the jobs to
run, and print them to the screen, but never actually run them. This is done with the `-n`
flag, eg:

```bash
> $ snakemake -n ...
```

:::

The amount of checking may seem pedantic right now, but as the workflow gains more steps this will
become very useful to us indeed.

## Using wildcards in our rule

We would like to use a wildcard in the `output` to allow us to
define the number of `tasks` we wish to use. Based on what we've seen so far,
you might imagine this could look like

```python
rule amdahl_run:
    output: "amdahl_run_{parallel_tasks}.txt"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi="mpiexec",
      tasks="{parallel_tasks}"
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl > {output}"
```

but there are two problems with this:

- The only way for Snakemake to know the value of the wildcard is for the user
  to explicitly request a concrete output file (rather than call the rule):

```bash
  snakemake --profile cluster_profile amdahl_run_2.txt
  ```

  This is perfectly valid, as Snakemake can figure out that it has a rule that
  can match that filename.
  
- The bigger problem is that even doing that does not work, it seems we cannot
  use a wildcard for `tasks`:
  
  ```output
  WorkflowError:
  SLURM job submission failed. The error message was sbatch:
  error: Invalid numeric value "{parallel_tasks}" for --ntasks.
  ```

Unfortunately for us, there is no direct way for us to access the wildcards
for `tasks`.
The reason for this is that Snakemake tries to use the value of `tasks` during its
initialisation stage, which is before we know the value of the wildcard. We need
to defer the determination of `tasks` to later on. This can be achieved by
specifying an input function instead of a value for this
scenario. The solution then is to write a one-time use function to manipulate
Snakemake into doing this for us. Since the function is specifically for the
rule, we can use a one-line function without a name. These kinds of functions
are called either anonymous functions or lamdba functions (both mean the same
thing), and are a feature of Python (and other programming languages).

To define a lambda function in python, the general syntax is as follows:

```python
lambda x: x + 54
```

Since our function _can_ take the wildcards as arguments, we can use that to set
the value for `tasks`:

```python
rule amdahl_run:
    output: "amdahl_run_{parallel_tasks}.txt"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi="mpiexec",
      # No direct way to access the wildcard in tasks, so we need to do this
      # indirectly by declaring a short function that takes the wildcards as an
      # argument
      tasks=lambda wildcards: int(wildcards.parallel_tasks)
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl > {output}"
```

Now we have a rule that can be used to generate output from runs of an
arbitrary number of parallel tasks.

::: callout

## Comments in Snakefiles

In the above code, the line beginning `#` is a comment line. Hopefully you are
already in the habit of adding comments to your own scripts. Good comments make
any script more readable, and this is just as true with Snakefiles.

:::

Since our rule is now capable of generating an arbitrary number of output files
things could get very crowded in our current directory. It's probably best then
to put the runs into a separate folder to keep things tidy. We can add the
folder directly to our `output` and Snakemake will take of directory creation
for us:

```python
rule amdahl_run:
    output: "runs/amdahl_run_{parallel_tasks}.txt"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi="mpiexec",
      # No direct way to access the wildcard in tasks, so we need to do this
      # indirectly by declaring a short function that takes the wildcards as an
      # argument
      tasks=lambda wildcards: int(wildcards.parallel_tasks)
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl > {output}"
```

::: challenge

Create an output file (under the `runs` folder) for the case where we have 6
parallel tasks

(HINT: Remember that Snakemake needs to be able to match the requested file to
the `output` from a rule)

:::::: solution

```bash
snakemake --profile cluster_profile runs/amdahl_run_6.txt
```

::::::

:::

Another thing about our application `amdahl` is that we ultimately want to
process the output to generate our scaling plot. The output right now is useful
for reading but makes processing harder. `amdahl` has an option that actually
makes this easier for us. To see the `amdahl` options we can use

```bash
[ocaisa@node1 ~]$ module load amdahl
[ocaisa@node1 ~]$ amdahl --help
```

```output
usage: amdahl [-h] [-p [PARALLEL_PROPORTION]] [-w [WORK_SECONDS]] [-t] [-e]

options:
  -h, --help            show this help message and exit
  -p [PARALLEL_PROPORTION], --parallel-proportion [PARALLEL_PROPORTION]
                        Parallel proportion should be a float between 0 and 1
  -w [WORK_SECONDS], --work-seconds [WORK_SECONDS]
                        Total seconds of workload, should be an integer greater than 0
  -t, --terse           Enable terse output
  -e, --exact           Disable random jitter
```

The option we are looking for is `--terse`, and that will make `amdahl` print
output in a format that is much easier to process, JSON. JSON format in a file
typically uses the file extension `.json` so let's add that option to our 
`shell` command _and_ change the file format of the `output` to match our new
command:

```python
rule amdahl_run:
    output: "runs/amdahl_run_{parallel_tasks}.json"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi="mpiexec",
      # No direct way to access the wildcard in tasks, so we need to do this
      # indirectly by declaring a short function that takes the wildcards as an
      # argument
      tasks=lambda wildcards: int(wildcards.parallel_tasks)
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl --terse > {output}"
```

There was another parameter for `amdahl` that caught my eye. `amdahl` has an
option `--parallel-proportion` (or `-p`) which we might be interested in
changing as it changes the behaviour of the code,and therefore has an impact on
the values we get in our results. Let's add
another directory layer to our output format to reflect a particular choice for
this value. We can use a wildcard so we done have to choose the value right
away:

```python
rule amdahl_run:
    output: "p_{parallel_proportion}/runs/amdahl_run_{parallel_tasks}.json"
    input:
    envmodules:
      "amdahl"
    resources:
      mpi="mpiexec",
      # No direct way to access the wildcard in tasks, so we need to do this
      # indirectly by declaring a short function that takes the wildcards as an
      # argument
      tasks=lambda wildcards: int(wildcards.parallel_tasks)
    input:
    shell:
        "{resources.mpi} -n {resources.tasks} amdahl --terse -p {wildcards.parallel_proportion} > {output}"
```

::: challenge

Create an output file for a value of `-p` of 0.999 (the default value is 0.8)
for the case where we have 6 parallel tasks.

:::::: solution

```bash
snakemake --profile cluster_profile p_0.999/runs/amdahl_run_6.json
```

::::::

:::

::: keypoints

- "Snakemake chooses the appropriate rule by replacing wildcards such that the
  output matches the target"
- "Snakemake checks for various error conditions and will stop if it sees a
  problem"

:::
