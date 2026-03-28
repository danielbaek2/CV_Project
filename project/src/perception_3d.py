import open3d
import matplotlib.pyplot as plt
import numpy as np
import cv2
import tqdm


def preprocess_pointcloud(pcd):
    # remove ground / crop region
    point_cloud = open3d.geometry.PointCloud()
    indices = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    filtered_points = point_cloud.select_by_index(indices)
    return filtered_points


def cluster_vehicles(points):
    # DBSCAN clustering
    return clusters


def compute_vehicle_position(cluster):
    # centroid of cluster
    return position


def compute_bounding_box(cluster):
    # Open3D bounding box
    return bbox


def compute_velocity(current_pos, previous_pos):
    return current_pos - previous_pos


def process_frame(pcd, previous_positions):
    # run all steps for one frame
    return vehicles

def main():
    0

main()