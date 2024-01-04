# Tame Your Workflow with Snakemake

In [HPC Intro][hpc-intro], learners explored the scheduler on their cluster by
launching a program called [`amdahl`][amdahl]. The objective of this lesson is
to adapt the manual job submission process into a repeatable, reusable workflow
with minimal human intervention. This is accomplished using
[Snakemake][snakemake], a modern workflow engine.

If you are interested in learning more about workflow tools, please visit
[The Workflows Community][workflows-community].

> ## Snakemake is best for single-node jobs
>
> NERSC's [Snakemake docs][nersc-snake] lists Snakemake's "cluster mode" as a
> _disadvantage_, since it submits each "rule" as a separate job, thereby
> spamming the scheduler with dependent tasks. The main Snakemake process also
> resides on the login node until all jobs have finished, occupying some
> resources.
>
> If you wish to adapt your Python-based program for multi-node cluster
> execution, consider applying the workflow principles learned from this lesson
> to the [Parsl][parsl] framework. Again, NERSC's [Parsl docs][nersc-parsl]
> provide helpful tips.

## Contributing

This is a translation of the [old HPC Workflows lesson][workflows] using
[The Carpentries Workbench][workbench] and [R Markdown (Rmd)][rmd].
You are cordially invited to contribute! Please check the list of
[issues][issues] if you're unsure where to start.

### Building Locally

If you edit the lesson, it is important to verify that the changes are rendered
properly in the online version. The best way to do this is to build the lesson
locally. You will need an R environment to do this: as described in the
[`{sandpaper}` docs][sandpaper], the environment can be either your terminal or
RStudio.

#### Setup

The `environment.yml` file describes a [Conda][conda] virtual environment that
includes [R][r-project], [Snakemake][snakemake], [amdahl][amdahl],
[pandoc][pandoc], and [termplotlib][termplotlib]: the tools you'll need to
develop and run this lesson, as well as some depencencies. To prepare the
environment, install [Miniconda][miniconda] following the official
instructions. Then open a shell application and create a new environment:

``` shell
you@yours:~$ cd path/to/local/hpc-workflows
you@yours:hpc-workflows$ conda env create -f environment.yaml
```

> _N.B.:_ the environment will be named "workflows" by default.
> If you prefer another name, add `-n «alternate_name»` to the command.

#### {sandpaper}

[{sandpaper}][sandpaper] is the engine behind The Carpentries Workbench lesson
layout and static website generator. It is an R package, and has not yet been
installed. Paraphrasing the installation instructions, start R or
[radian][radian], then install:

``` shell
you@yours:hpc-workflows$ R --no-restore --no-save
```

``` R
install.packages(c("sandpaper", "varnish", "pegboard", "tinkr"),
 repos = c("https://carpentries.r-universe.dev/", getOption("repos")))
```

Now you can render the site! From your R session,

``` R
library("sandpaper")
sandpaper::serve()
```

This should output something like the following:

``` plain
Output created: hpc-workflows/site/docs/index.html
To stop the server, run servr::daemon_stop(1) or restart your R session
Serving the directory hpc-workflows/site/docs at http://127.0.0.1:4321
```

Click on the link to <http://127.0.0.1:4321> or copy and paste it in your
browser. You should see any changes you've made to the lesson on the
corresponding page(s). If it looks right, you're set to proceed!

<!-- HPC Carpentry links -->

[amdahl]: https://github.com/hpc-carpentry/amdahl
[hpc-intro]: https://carpentries-incubator.github.io/hpc-intro/
[issues]: https://github.com/carpentries-incubator/hpc-workflows/issues
[workflows]: https://github.com/hpc-carpentry/hpc-workflows.old

<!-- The Carpentries links -->
[workbench]: https://carpentries.github.io/sandpaper-docs/

<!-- world-wide web links -->
[conda]: https://docs.conda.io/en/latest/
[miniconda]: https://docs.conda.io/projects/miniconda/en/latest/
[nersc-parsl]: https://docs.nersc.gov/jobs/workflow/parsl/
[nersc-snake]: https://docs.nersc.gov/jobs/workflow/snakemake/
[pandoc]: https://pandoc.org
[parsl]: http://parsl-project.org
[r-project]: https://www.r-project.org
[radian]: https://github.com/randy3k/radian
[rmd]: https://rmarkdown.rstudio.com
[sandpaper]: https://carpentries.github.io/sandpaper-docs/
[snakemake]: https://snakemake.readthedocs.io/en/stable/
[termplotlib]: https://github.com/nschloe/termplotlib
[workflows-community]: https://workflows.community
