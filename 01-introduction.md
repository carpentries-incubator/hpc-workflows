---
title: "Running commands with Snakemake"
teaching: 30
exercises: 30
---

::: questions

- "How do I run a simple command with Snakemake?"

:::

:::objectives

- "Create a Snakemake recipe (a Snakefile)"

:::

## What is the workflow I'm interested in?

In this lesson we will make an experiment that takes an application which runs
in parallel and investigate it's scalability. To do that we will need to gather
data, in this case that means running the application multiple times with
different numbers of CPU cores and recording the execution time. Once we've
done that we need to create a visualisation of the data to see how it compares
against the ideal case.

From the visualisation we can then decide at what scale it
makes most sense to run the application at in production to maximise the use of
our CPU allocation on the system.

We could do all of this manually, but there are useful tools to help us manage
data analysis pipelines like we have in our experiment. Today we'll learn about
one of those: Snakemake.

In order to get started with Snakemake, let's begin by taking a simple command
and see how we can run that via Snakemake. Let's choose the command `hostname`
which prints out the name of the host where the command is executed:

```bash
[ocaisa@node1 ~]$ hostname
```

```output
node1.int.jetstream2.hpc-carpentry.org
```

That prints out the result but Snakemake relies on files to know the status of
your workflow, so let's redirect the output to a file:

```bash
[ocaisa@node1 ~]$ hostname > hostname_login.txt
```

## Making a Snakefile

Edit a new text file named `Snakefile`.

Contents of `Snakefile`:

```python
rule hostname_login:
    output: "hostname_login.txt"
    input:  
    shell:
        "hostname > hostname_login.txt"
```

::: callout

## Key points about this file

1. The file is named `Snakefile` - with a capital `S` and no file extension.
1. Some lines are indented. Indents must be with space characters, not tabs. See
   the setup section for how to make your text editor do this.
1. The rule definition starts with the keyword `rule` followed by the rule name,
   then a colon.
1. We named the rule `hostname_login`. You may use letters, numbers or
   underscores, but the rule name must begin with a letter and may not be a
   keyword.
1. The keywords `input`, `output`, and `shell` are all followed by a colon (":").
1. The file names and the shell command are all in `"quotes"`.
1. The output filename is given before the input filename. In fact, Snakemake
   doesn't care what order they appear in but we give the output first
   throughout this course. We'll see why soon.
1. In this use case there is no input file for the command so we leave this
   blank.

:::

Back in the shell we'll run our new rule. At this point, if there were any
missing quotes, bad indents, etc., we may see an error.

```bash
snakemake -j1 -p hostname_login
```

::: callout

## `bash: snakemake: command not found...`

If your shell tells you that it cannot find the command `snakemake` then we need
to make the software available somehow. In our case, this means searching for
the module that we need to load:

```bash
module spider snakemake
```

```output
[ocaisa@node1 ~]$ module spider snakemake

--------------------------------------------------------------------------------------------------------
  snakemake:
--------------------------------------------------------------------------------------------------------
     Versions:
        snakemake/8.2.1-foss-2023a
        snakemake/8.2.1 (E)

Names marked by a trailing (E) are extensions provided by another module.


--------------------------------------------------------------------------------------------------------
  For detailed information about a specific "snakemake" package (including how to load the modules) use the module's full name.
  Note that names that have a trailing (E) are extensions provided by other modules.
  For example:

     $ module spider snakemake/8.2.1
--------------------------------------------------------------------------------------------------------
```

Now we want the module, so let's load that to make the package available

```bash
[ocaisa@node1 ~]$ module load snakemake
```

and then make sure we have the `snakemake` command available

```bash
[ocaisa@node1 ~]$ which snakemake
```

```output
/cvmfs/software.eessi.io/host_injections/2023.06/software/linux/x86_64/amd/zen3/software/snakemake/8.2.1-foss-2023a/bin/snakemake
```

```bash
snakemake -j1 -p hostname_login
```
:::

::: challenge
## Running Snakemake

Run `snakemake --help | less` to see the help for all available options.
What does the `-p` option in the `snakemake` command above do?

1. Protects existing output files
1. Prints the shell commands that are being run to the terminal
1. Tells Snakemake to only run one process at a time
1. Prompts the user for the correct input file

:::::: hint
You can search in the text by pressing <kbd>/</kbd>,
and quit back to the shell with <kbd>q</kbd>.
::::::

:::::: solution
(2) Prints the shell commands that are being run to the terminal

This is such a useful thing we don't know why it isn't the default! The `-j1`
option is what tells Snakemake to only run one process at a time, and we'll
stick with this for now as it makes things simpler. Answer 4 is a total
red-herring, as Snakemake never prompts interactively for user input.
::::::
:::

::: keypoints

- "Before running Snakemake you need to write a Snakefile"
- "A Snakefile is a text file which defines a list of rules"
- "Rules have inputs, outputs, and shell commands to be run"
- "You tell Snakemake what file to make and it will run the shell command
  defined in the appropriate rule"

:::
