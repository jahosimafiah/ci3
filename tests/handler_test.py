from tests.helpers import generate_mock_client_and_class_attributes
from unittest import TestCase
from ci3.src.handlers import DeploymentAssetHandler


# Test the handler using the boto3 mock
class TestHandler(TestCase):
    # Use setUp method to configure the mock
    def setUp(self):
        generate_mock_client_and_class_attributes(self)

    def test_all_hashes_shown(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        for deploy_hash in handler.deploy_hashes:
            self.assertIn(deploy_hash[0], ["deploy_newest/", "deploy_new/", "deploy_old/"])

    def test_dt_value_parsed_correctly(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        for deploy_hash in handler.deploy_hashes:
            self.assertIn(
                deploy_hash[1],
                [self.deploy_new_dt, self.deploy_newest_dt, self.deploy_old_dt],
            )

    def test_delete_old_object_removed_correctly(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        files = [f for f in self.files if f.startswith("deploy_old")]
        handler.delete_deploy_files("deploy_old/")
        self.assertEqual(set(files).intersection(set(self.files)), set())

    def test_delete_old_and_new_objects_removed_correctly(self):
        handler = DeploymentAssetHandler(
            s3_bucket=self.bucket, abstract_client=self.client
        )
        expected_files = [
            f
            for f in self.files
            if f.startswith("deploy_old/") and f.startswith("deploy_new/")
        ]
        for dh in ["deploy_old/", "deploy_new/"]:
            handler.delete_deploy_files(dh)
        self.assertEqual(set(expected_files).intersection(set(self.files)), set())
