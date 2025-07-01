import os
import shutil
import subprocess
import tempfile

from loguru import logger

from llm_twin.domain.documents import RepositoryDocument, UserDocument

from .selenium_crawler import SeleniumCrawler


class GitHubCrawler(SeleniumCrawler[RepositoryDocument]):
    model = RepositoryDocument

    def __init__(
        self, ignore: tuple[str, ...] | str = (".git", ".toml", ".lock", ".png")
    ) -> None:
        super().__init__()

        self._ignore: tuple[str, ...] | str = ignore

    def extract(self, url: str, /, **kwargs) -> None:
        record = self.model.find(url=url)

        if record:
            logger.info(f"Starting scraping GitHub repository: {url}")
            return

        repo_name: str = url.rstrip("/").split("/")[-1]

        local_temp_dir = tempfile.mkdtemp()

        try:
            os.chdir(local_temp_dir)
            subprocess.run(["git", "clone", url])

            repo_path: str = os.path.join(local_temp_dir, os.listdir(local_temp_dir)[0])
            tree: dict[str, str] = {}

            for root, _, files in os.walk(repo_path):
                _dir = root.replace(repo_path, "").lstrip("/")
                if _dir.startswith(self._ignore):
                    continue

                for file in files:
                    if file.endswith(self._ignore):
                        continue

                    file_path = os.path.join(_dir, file)
                    with open(os.path.join(root, file_path), "r", errors="ignore") as f:
                        tree[file_path] = f.read().replace(" ", "")

            user: UserDocument = kwargs["user"]
            instance = self.model.model_construct(
                content=tree,
                name=repo_name,
                url=url,
                platform="GitHub",
                author_id=user.id,
                author_full_name=user.full_name,
            )
            instance.save()

        except Exception:
            raise
        finally:
            shutil.rmtree(local_temp_dir)

        logger.info(f"Finished scraping GitHub Repository: {url}")
