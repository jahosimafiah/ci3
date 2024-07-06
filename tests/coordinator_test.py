from tests.helpers import generate_mock_client_and_class_attributes
from unittest import TestCase
from ci3.src.handlers import DeploymentAssetHandler
from ci3.src.controllers import coordinate_asset_cleanup


# Test the coordinator using the boto3 mock
class TestCoordinator(TestCase):
    # Use setUp method to configure the mock
    def setUp(self):
        generate_mock_client_and_class_attributes(self)

    def test_no_deployments_are_deleted_when_keep_count_arg_equals_keep_count_actual(
        self,
    ):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        expected_file_count = len(self.files)
        coordinate_asset_cleanup(handler, keep_count=3, dry_run=False)
        self.assertEqual(
            expected_file_count,
            len(self.files),
            "Files were deleted when they should not have been",
        )

    def test_files_are_not_deleted_when_dry_run_is_set(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        expected_file_count = len(self.files)
        coordinate_asset_cleanup(handler, keep_count=1, dry_run=True)
        self.assertEqual(expected_file_count, len(self.files))

    def test_2_deployments_are_deleted_when_keep_count_is_1_and_s3_has_3_deploys(
        self,
    ):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        expected_files = [f for f in self.files if f.startswith('deploy_newest/')]
        coordinate_asset_cleanup(handler, keep_count=1, dry_run=False)
        self.assertEqual(
            len(expected_files),
            len(self.files),
            "Files were deleted when they should not have been",
        )

    def test_when_1_deploy_is_present_nothing_happens(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        self.files = [f for f in self.files if f.startswith('deploy_newest/')]
        expected_file_count = len(self.files)
        coordinate_asset_cleanup(handler, keep_count=2, dry_run=False)
        self.assertEqual(expected_file_count, len(self.files))

    def test_keep_count_arg_of_0_raises(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        with self.assertRaises(ValueError):
            coordinate_asset_cleanup(handler, keep_count=0, dry_run=False)

    def test_plan_output_ordered_correctly(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        plan_output = coordinate_asset_cleanup(handler, keep_count=3, dry_run=True)
        deploy_newest_str = next(plan_output)
        self.assertIn('[KEEP]', deploy_newest_str) and self.assertIn(' deploy_newest/ ', deploy_newest_str)
        deploy_new_str = next(plan_output)
        self.assertIn('[KEEP]', deploy_new_str) and self.assertIn(' deploy_new/ ', deploy_new_str)
        deploy_old_str = next(plan_output)
        self.assertIn('[KEEP]', deploy_old_str) and self.assertIn(' deploy_old/ ', deploy_old_str)