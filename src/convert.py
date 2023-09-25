# https://alliance-wsu.esploro.exlibrisgroup.com/esploro/outputs/dataset/Apple-Dataset-Benchmark-from-Orchard-Environment/99900502619401842

import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    # project_name = "Apple Dataset Benchmark"
    dataset_path = "/home/grokhi/rawdata/apple-dataset-benchmark-from-orchard-environment"
    batch_size = 30
    imgs_ext = ".png"
    anns_ext = ".txt"
    ds_name = "ds"


    def create_ann(image_path):
        labels = []

        tag = sly.Tag(folder_to_tag[subfolder])

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        bboxes = im_name_to_boxes.get(get_file_name_with_ext(image_path))

        if bboxes is not None:
            for bbox in bboxes:
                if len(bbox) == 4:
                    left = int(bbox[0])
                    right = int(bbox[0]) + int(bbox[2])
                    top = int(bbox[1])
                    bottom = int(bbox[1]) + int(bbox[3])
                    rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                    label = sly.Label(rectangle, obj_class)
                    labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[tag])


    obj_class = sly.ObjClass("apple", sly.Rectangle)
    artificial = sly.TagMeta("artificial light", sly.TagValueType.NONE)
    estimation = sly.TagMeta("crop load estimation", sly.TagValueType.NONE)
    robot2016 = sly.TagMeta("harvesting robot 2016", sly.TagValueType.NONE)
    robot2017 = sly.TagMeta("harvesting robot 2017", sly.TagValueType.NONE)

    folder_to_tag = {
        "ArtificialLight": artificial,
        "CropLoadEstimation": estimation,
        "HarvestingRobot2016": robot2016,
        "HarvestingRobot2017": robot2017,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=list(folder_to_tag.values()))
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for subfolder in os.listdir(dataset_path):
        curr_ds_path = os.path.join(dataset_path, subfolder)
        if dir_exists(curr_ds_path):
            # if subfolder in ["HarvestingRobot2016", "HarvestingRobot2017"]:
            #     curr_ds_path = os.path.join(curr_ds_path, subfolder[10:])

            images_names = [
                im_name for im_name in os.listdir(curr_ds_path) if get_file_ext(im_name) == imgs_ext
            ]

            ann_name = [
                im_name for im_name in os.listdir(curr_ds_path) if get_file_ext(im_name) == anns_ext
            ]

            im_name_to_boxes = {}

            with open(os.path.join(curr_ds_path, ann_name[0])) as f:
                content = f.read().split("\n")
                for curr_data in content:
                    curr_boxes = []
                    curr_data = curr_data.strip().split(",")[:-1]
                    if len(curr_data) != 0:
                        curr_im_name = curr_data[0].split("/")[-1]
                        for i in range(1, len(curr_data) - 1, 4):
                            curr_boxes.append(curr_data[i : i + 4])
                        im_name_to_boxes[curr_im_name] = curr_boxes

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for img_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(curr_ds_path, image_path) for image_path in img_names_batch
                ]

                img_names_batch = [
                    im_path.split("/")[-2] + "_" + get_file_name_with_ext(im_path)
                    for im_path in images_pathes_batch
                ]

                img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
                img_ids = [im_info.id for im_info in img_infos]

                anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns_batch)

                progress.iters_done_report(len(img_names_batch))
    return project


