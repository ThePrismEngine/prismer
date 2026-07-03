from platformdirs import PlatformDirs

app_dir = PlatformDirs("prismer", "ThePrismEngine").user_data_path
versions_dir = app_dir / "versions"
