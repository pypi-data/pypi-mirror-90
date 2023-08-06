from penvy.container.diservice import diservice
from penvy.container.dicontainer import Container as PenvyContainer


class Container(PenvyContainer):
    @diservice
    def get_databricks_connect_detector(self):
        from benvy.databricks.DatabricksConnectDetector import DatabricksConnectDetector

        return DatabricksConnectDetector()

    @diservice
    def get_winutils_downloader(self):
        from benvy.hadoop.WinutilsDownloader import WinutilsDownloader

        return WinutilsDownloader(self._parameters["project"]["venv_dir"], self._parameters["hadoop"]["winutils_url"], self.get_logger())

    @diservice
    def get_java_setup(self):
        from benvy.java.JavaSetup import JavaSetup

        return JavaSetup(self._parameters["java"]["version"], self._parameters["java"]["install_dir"], self.get_logger())

    @diservice
    def get_databricks_connect_config_creator(self):
        from benvy.databricks.DatabricksConnectConfigCreator import DatabricksConnectConfigCreator

        return DatabricksConnectConfigCreator(self.get_logger())

    @diservice
    def get_bin_executable_flag_setter(self):
        from benvy.databricks.BinExecutableFlagSetter import BinExecutableFlagSetter

        return BinExecutableFlagSetter(
            self._parameters["conda"]["executable_path"], self._parameters["project"]["venv_dir"], self.get_logger()
        )

    @diservice
    def get_libgit2_installer(self):
        from benvy.git.Libgit2Installer import Libgit2Installer

        return Libgit2Installer(self.get_logger())
