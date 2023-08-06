# """
# A .dada file is two files:
#     - 1: any old file and
#     - 2: a `.dada` file containing json data including the file's metadata as well as dada-specific fields (including source, theme, folders, tags, macro, task, etc)

# A .dada file can exist in five places:
#     - loc_ext (somewhere on your loc machine)
#     - loc_int (saved in the loc .dada/ cache)
#     - s3_ext (on a s3 bucket other than the one managed by this dada instance)
#     - s3_int (on the s3 bucket managed by this dada instance)
#     - web (somewhere on a publically accessible website)
import gzip
from typing import Optional, Any

from botocore.exceptions import ClientError

import dada_settings
from dada_utils import dates, etc, path
from dada_types import T, SerializableObject
import dada_http
import dada_archive
import dada_serde
import dada_text
import dada_stor
from dada_log import DadaLogger

from dada_file import schema, partition

GZ_COMPRESSION_EXCLUDES = frozenset(
    ["mp4", "webm"] + dada_settings.BUNDLE_DEFAULTS_VALID_EXT
)

DADA_FILE_EXT = "dada.gz"
log = DadaLogger()


class DadaData(etc.AttrDict):
    pass


class DadaUrlSet(etc.AttrDict):
    pass


class DadaFile(SerializableObject):

    # default metadata

    ensure_check_sum = False
    local_stor = path.get_full(dada_settings.LOCAL_DIR)
    global_stor = dada_stor.DadaStor()

    def __init__(
        self,
        url: Optional[T.url.py] = None,
        location: Optional[str] = None,
        ensure_check_sum: Optional[bool] = None,
        local_stor: str = None,
        global_stor: Any = None,
        **dada,
    ):
        # ensure local directory endslash
        self.local_dir = local_stor or self.local_stor
        if not self.local_dir.endswith("/"):
            self.local_dir = self.local_dir + "/"

        # determine location
        self.location = location
        self.ensure_check_sum = ensure_check_sum or self.ensure_check_sum

        # if this is a url based loader, do its thing.
        self.url = None
        self.dada_url = None
        self.dada = DadaData({"entity_type": "file"})
        if self.global_stor is None and global_stor is not None:
            self.global_stor = global_stor

        if not self.global_stor:
            raise ValueError(
                "Must subclass DadaFile and set a persisent global_stor or pass in an explicit global_stor at initialization."
            )

        if url is not None:
            self.url = url

            # for fetching dada data files from other dada-lake instances
            self.dada_url = self._get_dada_url_from_input_url(url)

            # ensure name, slug, and extension are set by default
            dada.setdefault("file_name", path.get_name(url))
            dada.setdefault("slug", dada_text.get_slug(path.get_name(url)))
            dada.setdefault("ext", path.get_ext(url))

            # determine compression
            self.is_gz = self.url.endswith(".gz")

            # extract partitioned url dada data
            self.is_part_url = partition.is_partition_url(self.url)
            if self.is_part_url:
                self.dada.update(partition.extract(self.url))

        # update dada with overrides
        self.dada.update(dada)

    def _get_dada_url_from_input_url(self, url):
        """
        infer the data url from the input url
        """
        return f"{path.get_dir(self.url)}{path.get_name(self.url)}.{DADA_FILE_EXT}"

    # methods to overwrite

    def download_dada(self) -> None:
        """
        The download file method is responsible for downloading a url into the local store,
        locating any associated `.dada` files
        and updating internal dada data before we construct the partitions
        """
        raise NotImplementedError("A DadaFile must implement a `download_dada` method")

    def download_file(self, from_url, to_url) -> None:
        """
        The download file method is responsible for downloading a url into the local store,
        locating any associated `.dada` files
        and updating internal dada data before we construct the partitions
        """
        raise NotImplementedError("A DadaFile must implement a `download_file` method")

    def fetch_dada(self):
        """
        Fetch the dada file.
        """
        self.dada.update(self.download_dada())

    # properties / urls

    @property
    def id_partition(self):
        """ the partition for all versions of this file (eg e=file/t=audio/s=track/x=mp3/i=1/) """
        return partition.create(**self.dada)

    @property
    def version_partition(self):
        """ the partition for current version of this file (eg e=file/t=audio/s=track/x=mp3/i=1/v=3820740923482-fldjkasfd) """
        return f"{self.id_partition}{partition.version(**self.dada)}/"

    @property
    def latest_partition(self):
        """ the partition for the latest version of this file (eg e=file/t=audio/s=track/x=mp3/i=1/v=latest) """
        return f"{self.id_partition}v=latest/"

    @property
    def file_name(self):
        return f"{self.dada.slug}.{self.dada.ext}"

    @property
    def file_name_gz(self):
        if self.dada.ext not in GZ_COMPRESSION_EXCLUDES:
            return f"{self.file_name}.gz"
        return self.file_name

    @property
    def dada_file_name(self):
        return f"{self.dada.slug}.dada.gz"

    @property
    def dirs(self):
        return DadaUrlSet(
            {
                "loc": DadaUrlSet(
                    {
                        "latest": path.join(self.local_dir + self.latest_partition),
                        "version": path.join(self.local_dir + self.version_partition),
                    }
                ),
                "loc_bundle": DadaUrlSet(
                    {
                        "latest": path.join(
                            self.local_dir, self.version_partition, "bundle/"
                        )
                    }
                ),
                "glob": DadaUrlSet(
                    {
                        "latest": self.global_stor.s3_prefix + self.latest_partition,
                        "version": self.global_stor.s3_prefix + self.version_partition,
                    }
                ),
                "global_bundle": DadaUrlSet(
                    {
                        "latest": self.global_stor.s3_prefix
                        + self.latest_partition
                        + "bundle/",
                    }
                ),
            }
        )

    @property
    def local_bundle_urls(self):
        """ a list of bundle urls locally """
        return [
            path.join(self.dirs.loc_bundle.latest, f)
            for f in self.dada.get("fields", {}).get("bundle_contents", [])
        ]

    @property
    def global_bundle_urls(self):
        """ a list of bundle urls on s3 """
        return [
            path.join(self.dirs.glob_bundle.latest, f)
            for f in self.dada.get("fields", {}).get("bundle_contents", [])
        ]

    @property
    def urls(self):
        """
        store uncompressed files locally listening / usage / processing
        store compressed files on s3 for performance / savings
        """
        return DadaUrlSet(
            {
                "input": DadaUrlSet(
                    {
                        "file": DadaUrlSet({"latest": self.url}),
                        "dada": DadaUrlSet({"latest": self.dada_url}),
                    }
                ),
                "loc": DadaUrlSet(
                    {
                        "file": DadaUrlSet(
                            {
                                "latest": self.dirs.loc.latest + self.file_name,
                                "version": self.dirs.loc.version + self.file_name,
                            }
                        ),
                        "dada": DadaUrlSet(
                            {
                                "latest": self.dirs.loc.latest + self.dada_file_name,
                                "version": self.dirs.loc.version + self.dada_file_name,
                            }
                        ),
                    }
                ),
                "glob": DadaUrlSet(
                    {
                        "file": DadaUrlSet(
                            {
                                "latest": self.dirs.glob.latest + self.file_name_gz,
                                "version": self.dirs.glob.version + self.file_name_gz,
                            }
                        ),
                        "dada": DadaUrlSet(
                            {
                                "latest": self.dirs.glob.latest + self.dada_file_name,
                                "version": self.dirs.glob.version + self.dada_file_name,
                            }
                        ),
                    }
                ),
            }
        )

    # helpers for checking for existence in various locations

    def version_exists_locally(self) -> bool:
        """ does this version exist locally """
        return path.exists(self.urls.loc.file.version)

    def latest_exists_locally(self) -> bool:
        """ does the latest version exist locally """
        return path.exists(self.urls.loc.file.latest)

    def version_exists_globally(self) -> bool:
        """ does this version exist globally """
        return self.global_stor.exists(self.urls.glob.file.version)

    def latest_exists_globally(self) -> bool:
        """ does the latest version exist globally """
        return self.global_stor.exists(self.urls.glob.file.latest)

    def exists_locally(self) -> bool:
        """ does this file exist locally """
        return self.latest_exists_locally() and self.version_exists_locally()

    def exists_globally(self) -> bool:
        """ does this file exist globally """
        return self.version_exists_globally() and self.latest_exists_globally()

    def exists(self) -> bool:
        """ does this file exist globally + locally """
        return self.exists_globally() and self.exists_locally()

    # serializable data representation
    def to_dict(self) -> dict:
        return {**self.dada, "urls": self.urls}

    # metadata ensurance #

    def _ensure_created_at(self, tmp_file):

        # ensure created at from file
        if self.dada.get("created_at", None) is None:
            self.dada["created_at"] = dates.from_string(path.get_created_at(tmp_file))

        # ensure created in dada
        elif isinstance(self.dada.get("created_at"), str):
            self.dada["created_at"] = dates.from_string(self.dada.get("created_at"))

    def _ensure_updated_at(self, tmp_file):

        # ensure updated at
        if self.dada.get("updated_at", None) is None:
            self.dada["updated_at"] = dates.from_string(path.get_updated_at(tmp_file))

        elif isinstance(self.dada.get("updated_at"), str):
            self.dada["updated_at"] = dates.from_string(self.dada.get("updated_at"))

    def _ensure_date_partitions(self):

        # ensure created / updated hour / day / month / minute / etc
        if self.dada.get("created_day", None) is None:
            self.dada.update(
                schema.get_dada_date_attributes_from_file_metadata(**self.dada)
            )

    def _ensure_core_file_attributes(self, tmp_file):

        # ensure check sum
        if self.dada.get("check_sum", None) is None:
            self.dada["check_sum"] = path.get_check_sum(tmp_file)

        # ensure size
        if self.dada.get("size", None) is None:
            self.dada["size"] = path.get_size(tmp_file)

        # ensure mimetype
        if self.dada.get("mimetype", None) is None:
            ext, mt = path.get_ext_and_mimetype(tmp_file)
            self.dada["mimetype"] = mt
            if self.dada.get("ext", None) is None:
                self.dada["ext"] = ext

        # ensure id
        if self.dada.get("id", None) is None:
            self.dada["id"] = None

    def _ensure_dada_file_types(self):

        # dada file types
        if self.dada.get("file_type", None) is None:
            self.dada["file_type"] = schema.get_dada_type_from_file_metadata(
                **self.dada
            )

            if self.dada.get("file_subtype", None) is None:
                self.dada[
                    "file_subtype"
                ] = schema.get_default_dada_subtype_for_dada_type(
                    self.dada.get("file_type")
                )

    def ensure_dada(self, tmp_file):
        """
        ensure that crucial metadata is set for every file, no matter the source.
        """
        self._ensure_created_at(tmp_file)
        self._ensure_updated_at(tmp_file)
        self._ensure_core_file_attributes(tmp_file)
        self._ensure_date_partitions()
        self._ensure_dada_file_types()

    def save_locally(self, overwrite=True):
        """ save a file and metadata into the local store. """
        if overwrite or not self.exists_locally():
            self.internal_set_timer_start("save_locally")
            tmp_file = path.join(path.get_tempdir(), self.file_name)
            self.download_file(self.url, tmp_file)
            if self.is_gz:
                tmp_file = self._extract_gzip_file(tmp_file)

            # okay, now, no matter the source we should have an uncompressed
            # file which we can extract dada data from and import, let's go to work

            # ensure core metadata
            self.ensure_dada(tmp_file)

            # write the file locally
            self._save_file(tmp_file)

            # extract bundles
            if self.dada.file_type == "bundle":
                self._extract_bundle()

            # write dada
            self._save_dada()

    def share_globally(self, overwrite: bool = True):
        """ write local versions of a file and dada data to global store"""
        if overwrite or not self.exists_glocally():
            self.internal_set_timer_start("share_globally")

            # gzip the file before sharing it
            is_tmp_file = False
            if self.dada.ext not in GZ_COMPRESSION_EXCLUDES:
                is_tmp_file = True
                to_upload = path.join(path.get_tempdir(), self.file_name_gz)
                dada_serde.file_to_gz(self.urls.loc.file.version, to_upload)

            else:
                to_upload = self.urls.loc.file.version

            self._share_file(to_upload)
            self._share_dada()

            if self.dada.file_type == "bundle":
                self._share_bundle()

            # cleanup
            if is_tmp_file:
                path.remove(to_upload)
            self.internal_set_timer_end("share_globally")
            log.debug(
                f"[dada-global] job took {self.internal_timers['share_globally']['human']}"
            )

    # UTILITIES #

    def _extract_gzip_file(self, tmp_file):
        """ if input file is a gzip, extract it """
        # remove 'gz' from ext in dada data, thereby updating the url properties
        if self.dada.ext is not None:
            self.dada.ext = path.get_ungzipped_name(self.dada.ext)

        # ungzip to a new tempfile
        tmp_file_gz = tmp_file
        tmp_file_ungzipped = path.get_ungzipped_name(tmp_file)
        dada_serde.gz_to_file(tmp_file_gz, tmp_file_ungzipped)

        # update tmpfile var with new information
        tmp_file = tmp_file_ungzipped

        # remove the gzipped file
        path.remove(tmp_file_gz)
        return tmp_file

    def _save_file(self, tmp_file):
        """ write a file to to the local store """
        # copy tmpfile to local version
        log.debug(f"[dada-import] Importing {tmp_file} to {self.urls.loc.file.version}")
        path.copy(tmp_file, self.urls.loc.file.version)

        log.debug(
            f"[dada-import] backing up {self.urls.loc.file.version} to {self.urls.loc.file.latest}"
        )
        path.copy(self.urls.loc.file.version, self.urls.loc.file.latest)
        path.remove(tmp_file)

    def _save_dada(self):
        """ write file dada to the local store """
        log.debug(f"[dada-import] Writing dada data to {self.urls.loc.dada.version}")
        with open(self.urls.loc.dada.version, "wb") as f:
            f.write(self.to_jsongz())

        log.debug(f"[dada-import] backing up dada data to {self.urls.loc.dada.latest}")
        path.copy(self.urls.loc.dada.version, self.urls.loc.dada.latest)

    def _extract_bundle(self):
        """
        in the instance that this file is a "bundle"
        we'll want to extract its contents and also add those to the file store.
        however, these files will not be versioned themselves and will instead be considered
        part of the original "bundle" version, and nested under an associated "bundle" directory
        in the file's `id_partition`

        each time a new version of a `bundle` file is imported, its contents will be added to the local store
        as well as to s3. this way we can serve the contents of a bundle together.
        for instance, a bundle might constitute an entire website. in this case, we'd
        want to retain the directory structure of the bundle so as to ensure that
        relative path references work appropriately
        """
        log.debug(
            f"extracting bundle contents from {self.urls.loc.file.latest} to {self.dirs.local_bundle.latest}"
        )
        path.make_dir(self.dirs.local_bundle.latest)

        extracted_files = list(
            dada_archive.extract_all(
                self.urls.loc.file.latest,
                self.dirs.loc_bundle.latest,
                backend="auto" if self.dada.ext != "zip" else "zip",
            )
        )
        log.debug(f"[dada-import] {extracted_files}")

        rel_files = [
            f.replace(self.dirs.loc_bundle.latest, "") for f in extracted_files
        ]

        # set the bundle contents as a field
        if "fields" not in self.dada:
            self.dada["fields"] = {}

        self.dada["fields"]["bundle_contents"] = rel_files

    def _share_file(self, to_upload):
        """ write file to global store"""
        log.debug(
            f"[dada-global] uploading {to_upload} to {self.urls.glob.file.version}"
        )

        self.global_stor.upload(to_upload, self.urls.glob.file.version)
        log.debug(
            f"[dada-global] copying {self.urls.glob.file.version} to {self.urls.glob.file.latest}"
        )
        self.global_stor.copy(self.urls.glob.file.version, self.urls.glob.file.latest)

    def _share_dada(self):
        """ write dada to global store"""
        log.debug(
            f"[dada-global] uploading file dada from {self.urls.loc.dada.version} to {self.urls.loc.dada.latest}"
        )
        self.global_stor.upload(self.urls.loc.dada.version, self.urls.glob.dada.version)

        log.debug(
            f"[dada-global] copying file dada from {self.urls.glob.dada.version} to {self.urls.glob.dada.latest}"
        )
        self.global_stor.copy(self.urls.glob.dada.version, self.urls.glob.dada.latest)

    def _share_bundle(self):
        """ write bundle contents to global store"""
        for from_url, to_url in zip(self.local_bundle_urls, self.global_bundle_urls):
            log.debug(f"[dada-global] copying bundle file {from_url} to {to_url}")
            self.global_stor.upload(from_url, to_url)


class S3ExtFile(DadaFile):
    def download_dada(self):
        return dada_serde.jsongz_to_obj(
            self.global_stor.external_get_contents(self.dada_url)
        )

    def download_file(self, from_url, to_url):
        try:
            self.dada.update(self.download_dada())
            self.global_stor.external_download(from_url, to_url)
        except ClientError as e:
            log.warning(
                f"WARNING could not fetch [s3_ext] dada_url {self.dada_url} because of: {e}"
            )


class S3IntFile(DadaFile):
    def download_dada(self):
        if self.global_stor.exists(self.dada_url):
            log.debug(f"[dada-s3_int] fetching dada data from {self.dada_url}")
            return dada_serde.jsongz_to_obj(
                self.global_stor.get_contents(self.dada_url)
            )
        return {}

    def download_file(self, from_url, to_url):
        self.dada.update(self.download_dada())
        self.global_stor.download(from_url, to_url)


class LocExtFile(DadaFile):
    location = "loc_ext"

    def download_dada(self):
        if path.exists(self.dada_url):
            log.debug(
                f"[dada-{self.location}-download_file] fetching dada data from {self.dada_url}"
            )
            with open(self.dada_url, "rb") as f:
                return dada_serde.jsongz_to_obj(f.read())
        return {}

    def download_file(self, from_url, to_url):
        self.dada.update(self.download_dada())
        path.copy(from_url, to_url)


class LocIntFile(LocExtFile):
    location = "loc_int"


class WebFile(DadaFile):

    session = dada_http.get_session()

    def download_dada(self):
        if dada_http.exists(self.dada_url):
            log.debug(f"[dada-web_ext] fetching dada data from {self.dada_url}")
            r = self.session.get(self.dada_url)
            r.raise_for_status()
            return dada_serde.jsongz_to_obj(r.content)
        return {}

    def download_file(self, from_url, to_url):
        self.dada.update(self.download_dada())
        dada_http.download_file(from_url, to_url)
