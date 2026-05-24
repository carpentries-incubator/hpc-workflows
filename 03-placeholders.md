---
title: "Placeholders"
teaching: 40
exercises: 30
---

::: questions

- "How do I make a generic rule?"

:::

::: objectives

- "See how Snakemake deals with some errors"

:::

Our Snakefile has some duplication. For example, the names of text
files are repeated in places throughout the Snakefile rules. Snakefiles are
a form of code and, in any code, repetition can lead to problems (e.g. we rename
a data file in one part of the Snakefile but forget to rename it elsewhere).

::: callout
## D.R.Y. (Don't Repeat Yourself)

In many programming languages, the bulk of the language features are
there to allow the programmer to describe long-winded computational
routines as short, expressive, beautiful code.  Features in Python,
R, or Java, such as user-defined variables and functions are useful in
part because they mean we don't have to write out (or think about)
all of the details over and over again.  This good habit of writing
things out only once is known as the "Don't Repeat Yourself"
principle or D.R.Y.
:::

Let us set about removing some of the repetition from our Snakefile.

## Placeholders

To make a more general-purpose rule we need **placeholders**. Let's take a look
at what a placeholder looks like

```python
rule hostname_remote:
    output: "hostname_remote.txt"
    input:
    shell:
        "hostname > {output}"

```

As a reminder, here's the previous version from the last episode:

```python
rule hostname_remote:
    output: "hostname_remote.txt"
    input:
    shell:
        "hostname > hostname_remote.txt"

```

The new rule has replaced explicit file names with things in `{curly brackets}`,
specifically `{output}` (but it could also have been `{input}`...if that had
a value and were useful).

### `{input}` and `{output}` are **placeholders**

Placeholders are used in the `shell` section of a rule, and Snakemake will
replace them with appropriate values - `{input}` with the full name of the input
file, and
`{output}` with the full name of the output file -- before running the command.

`{resources}` is also a placeholder, and we can access a named element of the
`{resources}` with the notation `{resources.runtime}` (for example).

:::keypoints

- "Snakemake rules are made more generic with placeholders"
- "Placeholders in the shell part of the rule are replaced with values based on
  the chosen wildcards"

:::
