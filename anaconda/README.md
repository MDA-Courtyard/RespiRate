To create a duplicate python virtual environment, use
```
conda env create -f <file_name>
```
where `<file_name>` is either
1. `gen_environment.yml` (for easiest builds), or
2. `environment.yml` (for an exactly identical environment)

Most likely you should chose gen_environment.yml as it allows you to install the
same python package versions immediately, but with python builds that anaconda
thinks are appropriate for your system. In contrast, environment.yml provides
the exact package build numbers used on my machine, which mean installing on a
different platform will be difficult and will most likely fail.
