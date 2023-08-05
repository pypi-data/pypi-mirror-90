#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""Use command line to operate on datasets through click."""

import logging
import os
import sys
from configparser import ConfigParser
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, Iterator, List, Tuple, Union

import click

from .. import __version__
from ..dataset import Data, Segment
from ..utility import TBRN, TBRNType
from .dataset import FusionSegmentClient, SegmentClient
from .gas import GAS

_ACCESSKEY_PREFIX = "Accesskey-"


def _config_filepath() -> str:
    """Get the path of the config file.

    :return: the path of the config file
    """
    home = "HOMEPATH" if os.name == "nt" else "HOME"
    return os.path.join(os.environ[home], ".gasconfig")


def _read_config(config_filepath: str, config_name: str) -> Tuple[str, str]:
    """Read accessKey and url from the config file.

    :param config_filepath: the file containing config info
    :param config_name: the environment to login
    :returns:
        the accessKey of config_name read from the config file
        the url of config_name read from the config file
    """
    if not os.path.exists(config_filepath):
        click.echo(
            f"{config_filepath} not exist"
            "\n\nPlease use 'gas config <accessKey>' to create config file",
            err=True,
        )
        sys.exit(1)

    config_parser = ConfigParser()
    config_parser.read(config_filepath)
    access_key = config_parser[config_name]["accessKey"]
    url = config_parser[config_name]["url"] if "url" in config_parser[config_name] else ""
    return access_key, url


def _gas(access_key: str, url: str, config_name: str) -> GAS:
    """Load an object of class <GAS>.

    :param access_key: the accessKey of gas
    :param url: the login url
    :param config_name: the environment to login
        We will read accessKey and url from the appointed config_name and login gas.
    :return: the loaded gas client
    """
    if not access_key and not url:
        access_key, url = _read_config(_config_filepath(), config_name)

    if not access_key:
        click.echo("accessKey should be appointed", err=True)
        sys.exit(1)

    return GAS(access_key, url)


@click.group()
@click.version_option(version=__version__, message="%(version)s")
@click.option("-k", "--key", "access_key", type=str, default="", help="The accessKey of gas.")
@click.option("-u", "--url", type=str, default="", help="The login url.")
@click.option(
    "-c",
    "--config",
    "config_name",
    type=str,
    default="default",
    help="The environment to login.",
)
@click.option("-d", "--debug", is_flag=True, help="Debug mode.")
@click.pass_context
def cli(ctx: click.Context, access_key: str, url: str, config_name: str, debug: bool) -> None:
    """You can use 'gas' + COMMAND to operate on your dataset.\f

    :param ctx: the context to be passed as first argument
    :param access_key: the accessKey of gas
    :param url: the login url
    :param config_name: the environment to login
    :param debug: debug mode flag
    """
    ctx.obj = {
        "access_key": access_key,
        "url": url,
        "config_name": config_name,
    }

    if debug:
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.argument("name", type=str)
@click.pass_obj
def create(obj: Dict[str, str], name: str) -> None:
    """Create a dataset.\f

    :param obj: a dictionary including config info
    :param name: the name of the dataset to be created, like "tb:KITTI"
    """
    info = TBRN(tbrn=name)
    if info.type != TBRNType.DATASET:
        click.echo(f'"{name}" is not a dataset', err=True)
        sys.exit(1)
    _gas(**obj).create_dataset(info.dataset_name)


@cli.command()
@click.argument("name", type=str)
@click.argument("message", type=str)
@click.argument("tag", type=str, required=False)
@click.pass_obj
def commit(obj: Dict[str, str], name: str, message: str, tag: str) -> None:
    """Commit a dataset.\f

    :param obj: a dictionary including config info
    :param name: the name of the dataset to be committed, like "tb:KITTI"
    :param message: the message of the dataset to be committed
    :param tag: the tag of the dataset to be committed
    """
    info = TBRN(tbrn=name)
    if info.type != TBRNType.DATASET:
        click.echo(f'"{name}" is not a dataset', err=True)
        sys.exit(1)
    dataset = _gas(**obj)._get_dataset(info.dataset_name)  # pylint: disable=protected-access
    dataset.commit(message, tag)


@cli.command()
@click.argument("name", type=str)
@click.option("-y", "--yes", is_flag=True, help="Confirm to delete the dataset completely.")
@click.pass_obj
def delete(obj: Dict[str, str], name: str, yes: bool) -> None:
    """Delete a dataset.\f

    :param obj: a dictionary including config info
    :param name: the name of the dataset to be deleted, like "tb:KITTI"
    :param yes: confirm to delete the dataset completely
    """
    info = TBRN(tbrn=name)
    if info.type != TBRNType.DATASET:
        click.echo(f'"{name}" is not a dataset', err=True)
        sys.exit(1)

    if not yes:
        click.confirm(
            f'Dataset "{name}" will be completely deleted.\nDo you want to continue?', abort=True
        )

    _gas(**obj).delete_dataset(info.dataset_name)


@cli.command()
@click.argument("local_paths", type=str, nargs=-1)
@click.argument("tbrn", type=str, nargs=1)
@click.option(
    "-r", "--recursive", "is_recursive", is_flag=True, help="Copy directories recursively."
)
@click.option("-j", "--jobs", type=int, default=1, help="The number of threads.")
@click.option(
    "-s",
    "--skip_uploaded_files",
    "skip_uploaded_files",
    is_flag=True,
    help="Whether to skip the uploaded files.",
)
@click.pass_obj
def cp(  # pylint: disable=invalid-name, too-many-arguments
    obj: Dict[str, str],
    local_paths: Tuple[str],
    tbrn: str,
    is_recursive: bool,
    jobs: int,
    skip_uploaded_files: bool,
) -> None:
    """Copy local data to a remote path.\f

    :param obj: a dictionary including config info
    :param local_paths: a tuple of local paths containing data to be uploaded
    :param tbrn: the path to save the uploaded data, like "tb:KITTI:seg1"
    :param is_recursive: whether copy directories recursively
    :param jobs: number of threads to upload data
    :param skip_uploaded_files: Set it to `True` to skip the uploaded files
    """
    info = TBRN(tbrn=tbrn)

    if info.type == TBRNType.DATASET:
        click.echo("Error: SEGMENT is required", err=True)
        sys.exit(1)

    if info.type in [TBRNType.SEGMENT, TBRNType.NORMAL_FILE]:
        remote_path = info.remote_path if info.type == TBRNType.NORMAL_FILE else ""

        dataset = _gas(**obj).get_dataset(info.dataset_name)
        local_abspaths: List[str] = [os.path.abspath(local_path) for local_path in local_paths]
        if (
            len(local_abspaths) == 1
            and not os.path.isdir(local_abspaths[0])
            and remote_path
            and not remote_path.endswith("/")
        ):
            dataset.get_or_create_segment(info.segment_name).upload_data(
                local_abspaths[0], remote_path
            )
            return

        segment = _get_segment_object(info.segment_name, local_abspaths, remote_path, is_recursive)
        dataset.upload_segment_object(segment, jobs=jobs, skip_uploaded_files=skip_uploaded_files)
        return

    click.echo(f'"{tbrn}" is an invalid path', err=True)
    sys.exit(1)


def _get_segment_object(
    segment_name: str,
    local_abspaths: List[str],
    remote_path: str,
    is_recursive: bool,
) -> Segment:
    """Get the pair of local_path and remote_path.

    :param segment_name: the name of the segment these data belong to
    :param local_abspaths: a list of local abstract paths, could be folder or file
    :param remote_path: the remote object path, not necessarily end with '/'
    :param is_recursive: whether copy directories recursively
    :return: a segment containing mapping data
    """
    segment = Segment(segment_name)
    for local_abspath in local_abspaths:
        if not os.path.isdir(local_abspath):
            data = Data(
                local_abspath,
                remote_path=str(PurePosixPath(remote_path, os.path.basename(local_abspath))),
            )
            segment.append(data)
            continue

        if not is_recursive:
            click.echo(
                "Error: local paths include directories, please use -r option",
                err=True,
            )
            sys.exit(1)

        local_abspath = os.path.normpath(local_abspath)
        folder_name = os.path.basename(local_abspath)
        for root, _, filenames in os.walk(local_abspath):
            relpath = os.path.relpath(root, local_abspath) if root != local_abspath else ""
            for filename in filenames:
                data = Data(
                    os.path.join(root, filename),
                    remote_path=str(
                        PurePosixPath(Path(remote_path, folder_name, relpath, filename))
                    ),
                )
                segment.append(data)
    return segment


def _echo_segment(
    dataset_name: str,
    segment_name: str,
    segment: Union[SegmentClient, FusionSegmentClient],
    list_all_files: bool,
) -> None:
    """Echo a segment.

    :param dataset_name: the name of the dataset
    :param segment_name: the name of the segment
    :param segment: a normal/fusion segment
    :param list_all_files: only works when segment is a fusion one
        if False, list frame indexes only
        if True, list sensors and files, too
    """
    if isinstance(segment, SegmentClient):
        _echo_data(dataset_name, segment_name, segment.list_data())
    else:
        frames = segment.list_frame_objects()
        if not list_all_files:
            for index in range(len(frames)):
                click.echo(TBRN(dataset_name, segment_name, index).get_tbrn())
        else:
            for frame in frames:
                for data in frame.values():
                    click.echo(data.tbrn)


def _echo_data(dataset_name: str, segment_name: str, data_iter: Iterable[str]) -> None:
    """Echo files in data_iter under 'tb:dataset_name:segment_name'.

    :param dataset_name: the name of the dataset the segment belongs to
    :param segment_name: the name of the segment
    :param data_iter: iterable data to be echoed
    """
    for data in data_iter:
        click.echo(TBRN(dataset_name, segment_name, remote_path=data).get_tbrn())


def _ls_dataset(gas: GAS, info: TBRN, list_all_files: bool) -> None:
    dataset = gas._get_dataset(info.dataset_name)  # pylint: disable=protected-access
    segment_names = dataset.list_segments()
    if not list_all_files:
        for segment_name in segment_names:
            click.echo(TBRN(info.dataset_name, segment_name).get_tbrn())
        return

    for segment_name in segment_names:
        segment = dataset.get_segment(segment_name)
        _echo_segment(info.dataset_name, segment_name, segment, list_all_files)


def _ls_segment(gas: GAS, info: TBRN, list_all_files: bool) -> None:
    dataset = gas._get_dataset(info.dataset_name)  # pylint: disable=protected-access
    _echo_segment(
        info.dataset_name, info.segment_name, dataset.get_segment(info.segment_name), list_all_files
    )


def _ls_frame(gas: GAS, info: TBRN, list_all_files: bool) -> None:
    dataset = gas.get_fusion_dataset(info.dataset_name)
    fusion_segment = dataset.get_segment(info.segment_name)
    frame = fusion_segment.list_frame_objects()[info.frame_index]

    if not list_all_files:
        for sensor_name in frame:
            click.echo(TBRN(info.dataset_name, info.segment_name, info.frame_index, sensor_name))
    else:
        for data in frame.values():
            click.echo(data.tbrn)


def _ls_sensor(
    gas: GAS,
    info: TBRN,
    list_all_files: bool,  # pylint: disable=unused-argument
) -> None:
    dataset = gas.get_fusion_dataset(info.dataset_name)
    fusion_segment = dataset.get_segment(info.segment_name)
    frame = fusion_segment.list_frame_objects()[int(info.frame_index)]
    data = frame[info.sensor_name]
    click.echo(data.tbrn)


def _ls_fusion_file(
    gas: GAS,
    info: TBRN,
    list_all_files: bool,  # pylint: disable=unused-argument
) -> None:
    dataset = gas.get_fusion_dataset(info.dataset_name)
    fusion_segment = dataset.get_segment(info.segment_name)
    frame = fusion_segment.list_frame_objects()[info.frame_index]

    if frame[info.sensor_name].remote_path != info.remote_path:
        click.echo(f'No such file: "{info.remote_path}"!', err=True)
        sys.exit(1)

    click.echo(info)


def _ls_normal_file(  # pylint: disable=unused-argument
    gas: GAS, info: TBRN, list_all_files: bool
) -> None:
    dataset = gas.get_dataset(info.dataset_name)
    segment = dataset.get_segment(info.segment_name)
    _echo_data(
        info.dataset_name,
        info.segment_name,
        _filter_data(segment.list_data(), info.remote_path),
    )


_LS_FUNCS = {
    TBRNType.DATASET: _ls_dataset,
    TBRNType.SEGMENT: _ls_segment,
    TBRNType.NORMAL_FILE: _ls_normal_file,
    TBRNType.FRAME: _ls_frame,
    TBRNType.FRAME_SENSOR: _ls_sensor,
    TBRNType.FUSION_FILE: _ls_fusion_file,
}


@cli.command()
@click.argument("tbrn", type=str, default="")
@click.option(
    "-a", "--all", "list_all_files", is_flag=True, help="List all files under the segment."
)
@click.pass_obj
def ls(  # pylint: disable=invalid-name
    obj: Dict[str, str], tbrn: str, list_all_files: bool
) -> None:
    """List data under the path. If path is empty, list the names of all datasets.\f

    :param obj: a dictionary including config info
    :param tbrn: path to be listed, like "tb:KITTI:seg1". If empty, list names of all datasets.
    :param list_all_files: if list all files under the segment
    """
    gas = _gas(**obj)

    if not tbrn:
        for dataset_name in gas.list_datasets():
            click.echo(TBRN(dataset_name).get_tbrn())
        return

    info = TBRN(tbrn=tbrn)
    _LS_FUNCS[info.type](gas, info, list_all_files)


def _filter_data(
    data_list: List[str], remote_path: str, is_recursive: bool = True
) -> Iterator[str]:
    """Get a list of paths under the remote_path.

    :param data_list: a list of candidate paths
    :param remote_path: the remote path to filter data
    :param is_recursive: whether to filter data recursively
    :return: a list of paths under the given remote_path
    """
    if is_recursive:
        return (
            filter(lambda x: x.startswith(remote_path), data_list)
            if remote_path.endswith("/")
            else filter(lambda x: x.startswith(remote_path + "/") or x == remote_path, data_list)
        )
    return filter(lambda x: x == remote_path, data_list)


@cli.command()
@click.argument("tbrn", type=str)
@click.option(
    "-r", "--recursive", "is_recursive", is_flag=True, help="Remove directories recursively."
)
@click.option("-f", "--force", "force_delete", is_flag=True, help="Force to delete any segment.")
@click.pass_obj
# pylint: disable=invalid-name
def rm(obj: Dict[str, str], tbrn: str, is_recursive: bool, force_delete: bool) -> None:
    """Remove the remote paths.\f

    :param obj: a dictionary including config info
    :param tbrn: path to be removed, like "tb:KITTI:seg1".
    :param is_recursive: whether remove directories recursively
    :param force_delete: sensor and its objects will also be deleted if True,
      else only segment with no sensor can be deleted.
    """
    gas = _gas(**obj)
    info = TBRN(tbrn=tbrn)
    dataset = gas.get_dataset(info.dataset_name)

    if info.type == TBRNType.DATASET:
        if not is_recursive:
            click.echo("Error: please use -r option to remove the whole dataset", err=True)
            sys.exit(1)
        segment_names = dataset.list_segments()
        dataset.delete_segments(segment_names, force_delete)
        return

    if info.type == TBRNType.SEGMENT:
        if not is_recursive:
            click.echo("Error: please use -r option to remove the whole segment", err=True)
            sys.exit(1)
        dataset.delete_segments(info.segment_name, force_delete)
        return

    if info.type == TBRNType.NORMAL_FILE:
        if not is_recursive and info.remote_path.endswith("/"):
            click.echo("Error: please use -r option to remove recursively", err=True)
            sys.exit(1)

        segment = dataset.get_segment(info.segment_name)
        filter_data = list(_filter_data(segment.list_data(), info.remote_path, is_recursive))
        if not filter_data:
            echo_info = "file or directory" if is_recursive else "file"
            click.echo(f'Error: no such {echo_info} "{tbrn}" ', err=True)
            sys.exit(1)
        segment.delete_data(filter_data)
        return

    click.echo(f'"{tbrn}" is an invalid path to remove', err=True)
    sys.exit(1)


@cli.command()
@click.argument("access_key", type=str, default="")
@click.argument("url", type=str, default="")
@click.pass_obj
def config(obj: Dict[str, str], access_key: str, url: str) -> None:
    """Configure the accessKey (and url) of gas.\f

    :param obj: a dictionary including config info
    :param access_key: the accessKey of gas to write into config file
    :param url: the url of gas to write into config file
    """
    config_file = _config_filepath()
    config_parser = ConfigParser()
    config_parser.read(config_file)

    if not access_key:
        for config_name in config_parser.sections():
            click.echo(f"[{config_name}]")
            for key, value in config_parser[config_name].items():
                click.echo(f"{key} = {value}")
        return

    if not access_key.startswith(("Accesskey-", "ACCESSKEY-")):
        click.echo("Error: Wrong accesskey format", err=True)
        sys.exit(1)

    config_name = obj["config_name"]
    if config_name not in config_parser:
        config_parser.add_section(config_name)

    config_parser[config_name]["accessKey"] = access_key
    if url:
        config_parser[config_name]["url"] = url
    else:
        config_parser.remove_option(config_name, "url")

    with open(config_file, "w") as fp:
        config_parser.write(fp)

    click.echo(f"Success!\nConfiguration has been written into: {config_file}")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
