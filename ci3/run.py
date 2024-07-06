import boto3
import click
from ci3.src.handlers import DeploymentAssetHandler
from ci3.src.controllers import coordinate_asset_cleanup


@click.group()
def cli():
    pass


@cli.command(
    help="Plan a cleanup of S3. Lists out deploy hashes and the actions that will be taken"
)
@click.option("--bucket-name", help="Name of S3 Bucket to use", required=True)
@click.option(
    "--keep-count",
    type=click.IntRange(min=1),
    help="How many deployments to keep",
    required=True,
)
def plan_cleanup(bucket_name: str, keep_count: int):
    client = boto3.client("s3")
    handler = DeploymentAssetHandler(s3_bucket=bucket_name, abstract_client=client)
    for result in coordinate_asset_cleanup(handler, keep_count, dry_run=True):
        print(result)


@cli.command(help="Clean deployments from S3 bucket")
@click.option("--bucket-name", help="Name of S3 Bucket to use", required=True)
@click.option(
    "--keep-count",
    type=click.IntRange(min=1),
    help="How many deployments to keep",
    required=True,
)
@click.option(
    "--auto-approve",
    is_flag=True,
    help="Provide flag to skip user input prior to deleting files",
)
def cleanup(bucket_name: str, keep_count: int, auto_approve: bool):
    client = boto3.client("s3")
    handler = DeploymentAssetHandler(s3_bucket=bucket_name, abstract_client=client)
    for result in coordinate_asset_cleanup(handler, keep_count, dry_run=True):
        print(result)
    if not auto_approve:
        confirmation = input("Please confirm 'y' to continue: ")
        if confirmation != "y":
            print("confirmation not y...exiting")
            return
    coordinate_asset_cleanup(handler, keep_count, dry_run=False)
