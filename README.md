## Cleanup Isle 3
Cleanup deployments in AWS S3

This script is designed as a CLI tool which can be run manually or part of a CICD process.

The script has a couple different ways to test.  Unit tests can be run according to the documentation below.  There
are also visual tests that can be performed using the `plan-cleanup` command which can be used to quickly confirm
changes that will be made.

The minimum amount of deployments to keep is set to 1.  To change this, update the MINIMUM_KEEP_COUNT in the `src/constants.py`.

Unit tests will need to be updated accordingly to test this.

To make unit testing more consistent it would probably be beneficial to import the constant in `run.py` and pass the MINIMUM_KEEP_COUNT constant to the coordinator.  This would make mocking easier and allow unit tests to use a general pattern for testing even if the constant is changed. 


## Usage
Since the package is not in PyPI, install using git and pip

```shell
# clone the project
git clone https://...
# cd into the project directory
cd dir
# create a virtuaenv
python -m venv .venv
# Activate the virtualenv
source .venv/bin/activate
# Install using the setup.py
pip install .

# ci3 should now be accessible when the virtualenv is activate
> ci3 --help

Usage: ci3 [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cleanup           Clean deployments from S3 bucket
  plan-cleanup      Plan a cleanup of S3

```

It's also possible to build and run it in Docker
```shell
docker build -t ci3:latest .
docker run -it --rm \
  -v $(pwd)/.aws:/home/python/.aws ci3 \
  sh -c 'plan-cleanup --bucket-name <my_bucket> --aws-region-us-west-2'
```

Each command has its own arguments.  You can find out more about each command using the following syntax:
`ci3 <command> --help`

You can use the `ci3` to inspect the objects in S3, or the deploy_hashes.  Deploy hashes are the root folders at the base of the S3 Bucket.

You can use the `plan-cleanup` to see what `ci3` plans to delete given the arguments passed.

The `cleanup` command includes a plan output.  The `cleanup` command will also prompt for a 'y' to confirm the changes after the plan is shown.  To skip the confirmation, provide an `--auto-approve` flag with the command.

## Run tests
```shell
# For Linux/Mac
source .venv/bin/activate
pip install -r tests/requirements.txt
pytest -v --cov=ci3
```

## Assumptions
- All files under a deploy hash will have (generally) the same timestamp as part of a deployment.
The age of the deployment can be determined by only needing to look at one file that exists under the deploy_hash path.
  - Part of the assumption if incorrect could potentially remove the wrong deployments, so it would be beneficial to make sure of this assumption prior to general usage of the script.
  - If the assumption is incorrect, then we could list all files in the deployment and potentially take the oldest or newest timestamp to determine the age of the deployment.
- The structure of deployments in s3 is according to this pattern: `s3://<s3_bucket_name>/<deploy_hash>`
