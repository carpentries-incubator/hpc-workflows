# Tame Your Workflow with Snakemake

In [HPC Intro][hpc-intro], learners explored the scheduler on their cluster by
launching a program called [`amdahl`][amdahl]. The objective of this lesson is
to adapt the manual job submission process into a repeatable, reusable workflow
with minimal human intervention. This is accomplished using
[Snakemake][snakemake], a modern workflow engine.

If you are interested in learning more about workflow tools, please visit
[The Workflows Community][workflows-community].

> ### Snakemake is best for single-node jobs
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


<!-- HPC Carpentry links -->

[amdahl]: https://github.com/hpc-carpentry/amdahl
[hpc-intro]: https://carpentries-incubator.github.io/hpc-intro/
[workflows]: https://github.com/hpc-carpentry/hpc-workflows.old

<!-- The Carpentries links -->
[workbench]: https://carpentries.github.io/sandpaper-docs/

<!-- world-wide web links -->
[nersc-parsl]: https://docs.nersc.gov/jobs/workflow/parsl/
[nersc-snake]: https://docs.nersc.gov/jobs/workflow/snakemake/
[parsl]: http://parsl-project.org
[rmd]: https://rmarkdown.rstudio.com
[snakemake]: https://snakemake.readthedocs.io/en/stable/
[workflows-community]: https://workflows.community
