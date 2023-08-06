from __future__ import absolute_import

import hashlib
import os
import re
import tarfile
import tempfile

from datetime import datetime

import six
import uuid
from odps import DataFrame as ODPSDataFrame
from odps.models import Table
from odps.models.partition import Partition

odps_table_re = (
    r"odps://(?P<project>[^/]+)/tables/(?P<table_name>[^/]+)(?P<partition>.*)"
)


PAI_PIPELINE_RUN_ID_PLACEHOLDER = "${pai_system_run_id}"
PAI_PIPELINE_NODE_ID_PLACEHOLDER = "${pai_system_node_id}"


def md5_digest(raw_data):
    return hashlib.md5(raw_data).hexdigest()


def ensure_str(val):
    if isinstance(val, six.string_types):
        return val
    elif isinstance(val, six.integer_types):
        return str(val)
    else:
        raise ValueError("ensure_str: not support type:%s" % type(val))


def ensure_unix_time(t):
    if isinstance(t, datetime):
        return (t - datetime(1970, 1, 1)).total_seconds()
    elif isinstance(t, six.integer_types):
        return t
    else:
        raise ValueError(
            "not support format, unable to convert to unix timestamp(%s:%s)"
            % (type(t), t)
        )


def extract_odps_table_info(data):
    if isinstance(data, ODPSDataFrame):
        data = data.data

    if isinstance(data, Table):
        return "%s.%s" % (data.project.name, data.name), None
    elif isinstance(data, Partition):
        return "%s.%s" % (data.table.project.name, data.table.name), data.spec
    elif isinstance(data, six.string_types):
        return _extract_odps_table_info_from_url(data)
    else:
        raise ValueError("Not support ODPSTable input(type:%s)" % type(data))


def _extract_odps_table_info_from_url(resource):
    matches = re.match(odps_table_re, resource)
    if not matches:
        raise ValueError("Not support ODPSTable resource schema.")

    project, table, partition = (
        matches.group("project"),
        matches.group("table_name"),
        matches.group("partition").strip("/"),
    )
    return project, table, partition


def ensure_unicode(t):
    return six.ensure_text(t)


def gen_temp_table(prefix="pai_temp_"):
    return "{prefix}{identifier}".format(
        prefix=prefix,
        identifier=uuid.uuid4().hex,
    )


def gen_run_node_scoped_placeholder(suffix=None):
    if suffix:
        return "{0}_{1}_{2}".format(
            PAI_PIPELINE_NODE_ID_PLACEHOLDER, PAI_PIPELINE_RUN_ID_PLACEHOLDER, suffix
        )
    else:
        return "{0}_{1}".format(
            PAI_PIPELINE_NODE_ID_PLACEHOLDER, PAI_PIPELINE_RUN_ID_PLACEHOLDER
        )


def iter_with_limit(iterator, limit):
    if not isinstance(limit, six.integer_types) or limit <= 0:
        raise ValueError("'limit' should be positive integer")
    idx = 0
    for item in iterator:
        yield item
        idx += 1
        if idx >= limit:
            return


def tar_source_files(source_files, target=None):
    if target is None:
        target = tempfile.mktemp()

    with tarfile.open(target, "w:gz") as tar:
        for name in source_files:
            tar.add(name, arcname=os.path.basename(name))
    return target


def file_checksum(file_name, hash_type="md5"):
    if hash_type.lower() != "md5":
        raise ValueError("not support hash type")

    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(256 * 1024), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def to_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(path)


def extract_file_name(file_or_path):
    _, tail = os.path.split(file_or_path)
    return tail.strip()


def makedirs(path_dir, mode=0o777):
    if not os.path.exists(path_dir):
        # argument `exist_ok` not support in Python2
        os.makedirs(path_dir, mode=mode)
