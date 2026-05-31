---
title: "Processing lists of inputs"
teaching: 50
exercises: 30
---

::: questions

- "How do I process multiple files at once?"
- "How do I combine multiple files together?"

:::

::: objectives

- "Use Snakemake to process all our samples at once"
- "Make a scalability plot that brings our results together"

:::

We created a rule that can generate a single output file, but we're not going to
create multiple rules for every output file. We want to generate all of the run
files with a single rule if we could, well Snakemake can indeed take a list of
input files:

```python
rule generate_run_files:
    output: "p_{parallel_proportion}_runs.txt"
    input:  "p_{parallel_proportion}/runs/amdahl_run_2.json", "p_{parallel_proportion}/runs/amdahl_run_6.json"
    shell:
        "echo {input} done > {output}"
```

That's great, but we don't want to have to list all of the files we're
interested in individually. How can we do this?

## Defining a list of samples to process

To do this, we can define some lists as Snakemake **global variables**.

Global variables should be added before the rules in the Snakefile.

```python
# Task sizes we wish to run
NTASK_SIZES = [1, 2, 3, 4, 5]
```

- Unlike with variables in shell scripts, we can put spaces around the `=` sign,
  but they are not mandatory.
- The lists of quoted strings are enclosed in square brackets and
  comma-separated. If you know any Python you'll recognise this as Python list
  syntax.
- A good convention is to use capitalized names for these variables, but this is
  not mandatory.
- Although these are referred to as variables, you can't actually change the
  values once the workflow is running, so lists defined this way are more like
  constants.

## Using a Snakemake rule to define a batch of outputs

Now let's update our Snakefile to leverage the new global variable and create a
list of files:

```python
rule generate_run_files:
    output: "p_{parallel_proportion}_runs.txt"
    input:  expand("p_{{parallel_proportion}}/runs/amdahl_run_{count}.json", count=NTASK_SIZES)
    shell:
        "echo {input} done > {output}"
```

The `expand(...)` function in this rule generates a list of filenames, by taking
the first thing in the single parentheses as a template and replacing `{count}`
with all the `NTASK_SIZES`. Since there are 5 elements in the list, this will
yield 5 files we want to make. Note that we had to protect our wildcard in a
second set of parentheses so it wouldn't be interpreted as something that needed
to be expanded.

In our current case we still rely on the file name to define the value of the
wildcard `parallel_proportion` so we can't call the rule directly, we still need
to request a specific file:

```bash
snakemake --profile cluster_profile/ p_0.999_runs.txt
```

If you don't specify a target rule name or any file names on the command line
when running Snakemake, the default is to use **the first rule** in the
Snakefile as the target.

::: callout
## Rules as targets

Giving the name of a rule to Snakemake on the command line only works when that
rule has *no wildcards* in the outputs, because Snakemake has no way to know
what the desired wildcards might be. You will see the error "Target rules may
not contain wildcards." This can also happen when you don't supply any explicit
targets on the command line at all, and Snakemake tries to runthe first rule
defined in the Snakefile.

:::

## Rules that combine multiple inputs

Our `generate_run_files` rule is a rule which takes a list of input files. The
length of that list is not fixed by the rule, but can change based on
`NTASK_SIZES`.

In our workflow the final step is to take all the generated files and combine
them into a plot. To do that, you may have heard that some people use a python
library called `matplotlib`. It's beyond the scope of this tutorial to write
the python script to create a final plot, so we provide you with the script as
part of this lesson. You can download it with

```bash
curl -O https://ocaisa.github.io/hpc-workflows/files/plot_terse_amdahl_results.py
```

The script `plot_terse_amdahl_results.py` needs a command line that looks like:

```bash
python plot_terse_amdahl_results.py --output <output image filename> <1st input file> <2nd input file> ...
```

Let's introduce that into our `generate_run_files` rule:

```python
rule generate_run_files:
    output: "p_{parallel_proportion}_runs.txt"
    input:  expand("p_{{parallel_proportion}}/runs/amdahl_run_{count}.json", count=NTASK_SIZES)
    shell:
        "python plot_terse_amdahl_results.py --output {output} {input}"
```

::: challenge

This script relies on `matplotlib`, is it available as an environment module?
Add this requirement to our rule.

:::::: solution

```python
rule generate_run_files:
    output: "p_{parallel_proportion}_scalability.jpg"
    input:  expand("p_{{parallel_proportion}}/runs/amdahl_run_{count}.json", count=NTASK_SIZES)
    envmodules:
      "matplotlib"
    shell:
        "python plot_terse_amdahl_results.py --output {output} {input}"
```

::::::

:::

Now we finally get to generate a scaling plot! Run the final Snakemake command:

```bash
snakemake --profile cluster_profile/ p_0.999_scalability.jpg
```

::: challenge

Generate the scalability plot for all values from 1 to 10 cores.

:::::: solution

```python
NTASK_SIZES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

::::::

:::

::: challenge

Rerun the workflow for a `p` value of 0.8

:::::: solution

```bash
snakemake --profile cluster_profile/ p_0.8_scalability.jpg
```

::::::

:::

::: challenge

## Bonus round

Create a final rule that can be called directly and generates a scaling plot for
3 different values of `p`.
:::

::: keypoints

- "Use the `expand()` function to generate lists of filenames you want to combine"
- "Any `{input}` to a rule can be a variable-length list"

:::
