from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import open3d as o3d
from tqdm.auto import trange
import matplotlib
import numpy as np
import cv2


@dataclass
class Vehicle:
    # Unique id for each vehicle to track it from frame to frame.
    vehicle_id: int = -1
    # XYZ position
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    # XYZ velocity (difference in position from previous frame)
    mvec_x: float = 0.0
    mvec_y: float = 0.0
    mvec_z: float = 0.0
    # 3D Bounding Box
    bbox_x_min: float = 0.0
    bbox_x_max: float = 1.0
    bbox_y_min: float = 0.0
    bbox_y_max: float = 1.0
    bbox_z_min: float = 0.0
    bbox_z_max: float = 1.0

    @classmethod
    def csv_header(cls):
        return ",".join(cls.__annotations__.keys())

    def csv_row(self):
        return ",".join([str(self.__dict__[field]) for field in self.__annotations__.keys()])


def write_csv_helper(file: Path, vehicles: Iterable[Vehicle]):
    # Start with header by inspecting field names of the Vehicle class; if the list of vehicles is
    # empty then we need a new default Vehicle for the header:
    with open(file, "w") as f:
        f.write(Vehicle.csv_header() + "\n")
        for v in vehicles:
            f.write(v.csv_row() + "\n")


def load_point_cloud(path_to_cloud: Path) -> o3d.geometry.PointCloud:
    return o3d.io.read_point_cloud(path_to_cloud)


def main(
    data_path: Path,
    output_path: Path = "perception_results",
    start_index: int = 0,
    end_index: int = -1,
    # YOU MAY ADD OTHER ARGUMENTS HERE.
    # IF YOU DO, SUPPLY GOOD DEFAULTS BOTH HERE AND IN THE ARGUMENT PARSER.
):
    if end_index < 0:
        end_index = len(list(data_path.glob("*.pcd"))) + end_index

    # Load each point cloud and display it
    for frame_number in trange(start_index, end_index + 1, desc="Processing Frames"):
        vehicles: list[Vehicle] = []

        # Loading point cloud
        pcd = load_point_cloud(data_path / f"{frame_number}.pcd")

        # YOUR CODE HERE: do whatever to populate the list of vehicles for this frame. You may use
        # any functions available in open3d for background subtraction, road surface detection,
        # clustering, etc.
        plane_model, inliers = o3d.geometry.PointCloud.segment_plane(pcd, ransac_n=3, num_iterations=1000)
        select_by_index = pcd.select_by_index(inliers)

        # Write list of vehicles as a CSV
        write_csv_helper(output_path / f"{frame_number}.csv", vehicles)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "data_path",
        type=Path,
        help="Directory containing .pcd files",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=Path,
        default=Path("perception_results"),
        help="Directory where .csv outputs will be saved",
    )
    parser.add_argument(
        "-s",
        "--start_index",
        type=int,
        default=0,
        help="Index of first frame",
    )
    parser.add_argument(
        "-e",
        "--end_index",
        type=int,
        default=-1,
        help="Index of last frame (defaults to -1 for last frame)",
    )
    args = parser.parse_args()

    args.output_path.mkdir(parents=True, exist_ok=True)
    main(**vars(args))
