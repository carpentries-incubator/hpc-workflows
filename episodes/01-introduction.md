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
First, create an empty `Snakefile` in your working directory:

::: group-tab

### Linux

```bash
touch Snakefile
```

### macOS

```bash
touch Snakefile
```

### Windows

```powershell
New-Item -Name "Snakefile" -ItemType "file"
```

:::

Now open the file in an editor of your choice:

::: group-tab

### Linux

```bash
nano Snakefile
```

### macOS

```bash
open -a TextEdit Snakefile
```

### Windows

```powershell
notepad Snakefile
```

:::

and add the following content to the `Snakefile`:

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

Back in the shell we'll can run our new rule with the following command: 

```bash
snakemake --jobs 1 --printshellcmds hostname_login
# or in short
snakemake -j1 -p hostname_login
```

If there were any missing quotes, bad indents, etc., we may see an error.
The `--jobs` (`-j`) option sets the maximum number of parallel jobs to run,
and `--printshellcmds` (`-p`) prints each shell command as it is executed,
which is useful for debugging. To explore all available options:

```bash
snakemake --help
```

To look up a specific option, pipe the help output into `less`:

```bash
snakemake --help | less
```

Then type `/` followed by the option you want, e.g. `/-p`, and press Enter to
jump to the first match. Press `n` to jump to the next match, and `q` to quit.

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
If everything is set up, try to run the command again:
```bash
snakemake -j1 -p hostname_login
```
:::

::: challenge
## Running Snakemake

Run `snakemake --help | less` to explore the available options.
What does the `--dryrun` option do?

1. Deletes output files from previous runs
1. Shows what rules would be run without actually executing them
1. Runs only the first rule in the Snakefile
1. Downloads any missing input files automatically

:::::: hint
Type `/-dryrun` and press <kbd>Enter</kbd> to jump straight to it,
and quit back to the shell with <kbd>q</kbd>.
::::::

:::::: solution
(2) Shows what rules would be run without actually executing them 

`--dryrun` (or `-n`) is a useful Snakemake options that lets you check whether 
your workflow is set up correctly before committing to a full run. It is good 
practice to always do a dry run first, especially on an HPC cluster where jobs 
consume real resources and queue time.
::::::
:::

::: keypoints

- "Before running Snakemake you need to write a Snakefile"
- "A Snakefile is a text file which defines a list of rules"
- "Rules have inputs, outputs, and shell commands to be run"
- "You tell Snakemake what file to make and it will run the shell command
  defined in the appropriate rule"

:::
