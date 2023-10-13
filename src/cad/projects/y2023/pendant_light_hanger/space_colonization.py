import math
import pathlib
import random
import subprocess
import time
from dataclasses import dataclass

import cv2
import euclid3
import numpy as np
import rtree
import shapelysmooth
import solid
from fontTools.ttLib import TTFont
from shapely.affinity import *
from shapely.geometry import *
from shapely.ops import *
from solid import utils

from cad.projects.y2023.pendant_light_hanger.common import (
    Model,
    MultipartModel,
    s_poly_to_scad,
    skeleton_to_polys,
)

# from cad.common.helper import *


# random.seed(0)


class Attractor:
    def __init__(self, position):
        self.position = position
        self.reached = False


class Node:
    def __init__(self, parent=None, position=None, isTip=False, thickness=1):
        self.parent = parent
        self.position = position
        self.isTip = isTip
        self.thickness = thickness

        self.influencedBy = []

    def getNextNode(self, averageAttractorDirection, segmentLength):
        nextNode = Node()
        nextNode.position = self.position + averageAttractorDirection * segmentLength
        nextNode.parent = self
        nextNode.isTip = True

        return nextNode


class Network:
    defaults = {
        "VenationType": "Open",
        "AttractionDistance": 15,
        "KillDistance": 2.5,
        "EnableCanalization": False,
        "SegmentLength": 2.5,
    }

    def __init__(self, container, settings=None):
        self.attractors = []
        self.nodes = []
        self.container = container

        self.settings = self.defaults.copy()
        if settings:
            self.settings.update(settings)

        self.index = rtree.index.Index()
        self.timeSpentBuildingSpatialIndices = 0

        self.buildSpatialIndices()

    def update(self):
        # Associate attractors with nearby nodes to figure out where growth should occur
        for attractorID, attractor in enumerate(self.attractors):
            if self.settings["VenationType"] == "Open":
                closestNode = self.getClosestNode(
                    attractor, self.getNodesInAttractionZone(attractor)
                )
                if closestNode is not None:
                    closestNode.influencedBy.append(attractorID)
                    attractor.influencingNodes = [closestNode]

            elif self.settings["VenationType"] == "Closed":
                neighborhoodNodes = self.getRelativeNeighborNodes(attractor)
                nodesInKillZone = self.getNodesInKillZone(attractor)

                nodesToGrow = [
                    neighborNode
                    for neighborNode in neighborhoodNodes
                    if neighborNode not in nodesInKillZone
                ]

                attractor.influencingNodes = neighborhoodNodes

                if nodesToGrow:
                    attractor.fresh = False

                    for node in nodesToGrow:
                        node.influencedBy.append(attractorID)

        # Grow the network by adding new nodes onto any nodes being influenced by attractors
        for node in self.nodes:
            if node.influencedBy:
                averageDirection = self.getAverageDirection(
                    node, [self.attractors[id] for id in node.influencedBy]
                )
                nextNode = node.getNextNode(
                    averageDirection, self.settings["SegmentLength"]
                )

                # Only allow root nodes inside of defined bounds
                if self.container.contains(
                    Point(nextNode.position.x, nextNode.position.y)
                ):
                    self.nodes.append(nextNode)

            node.influencedBy = []

            # Perform auxin flux canalization (line segment thickening)
            if node.isTip and self.settings["EnableCanalization"]:
                current_node = node

                while current_node.parent:
                    # When there are multiple child nodes, use the thickest of them all
                    if current_node.parent.thickness < current_node.thickness + 0.07:
                        current_node.parent.thickness = current_node.thickness + 0.03

                    current_node = current_node.parent

        # Remove any attractors that have been reached by their associated nodes
        attractors_to_remove = []
        for attractorID, attractor in enumerate(self.attractors):
            if self.settings["VenationType"] == "Open":
                if attractor.reached:
                    attractors_to_remove.append(attractorID)

            elif self.settings["VenationType"] == "Closed":
                if attractor.influencingNodes and not attractor.fresh:
                    all_nodes_reached = all(
                        node.position.distance(attractor.position)
                        <= self.settings["KillDistance"]
                        for node in attractor.influencingNodes
                    )

                    if all_nodes_reached:
                        attractors_to_remove.append(attractorID)

        for attractorID in reversed(attractors_to_remove):
            self.attractors.pop(attractorID)

        # Rebuild spatial indices
        self.buildSpatialIndices()

    def buildSpatialIndices(self):
        start = time.time()
        # Clear the existing R-tree index
        self.index = rtree.index.Index()

        # Add nodes to the R-tree index for efficient spatial queries
        for idx, node in enumerate(self.nodes):
            x, y = node.position.x, node.position.y
            # Use the node's index (idx) as its ID for the R-tree index
            self.index.insert(idx, (x, y, x, y))

        self.timeSpentBuildingSpatialIndices += time.time() - start

    def addNode(self, node):
        self.nodes.append(node)
        self.buildSpatialIndices()

    def getClosestNode(self, attractor, nearbyNodes):
        closestNode = None
        closestDistance = float("inf")

        for nodeId in nearbyNodes:
            node = self.nodes[nodeId]
            distance = attractor.position.distance(node.position)
            if distance < self.settings["KillDistance"]:
                attractor.reached = True
                closestNode = None
            elif distance < closestDistance:
                closestNode = node
                closestDistance = distance

        return closestNode

    def getAverageDirection(self, node, nearbyAttractors):
        averageDirection = euclid3.Vector2(0, 0)

        for attractor in nearbyAttractors:
            direction = attractor.position - node.position
            direction.normalize()
            averageDirection += direction

        # Add a small amount of random jitter to avoid getting stuck between two attractors and edlessly generating nodes in the same place
        averageDirection += euclid3.Vector2(
            random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
        )

        # This was in jasonwebb's js implementation but I can't see how it will have any effect given that we imediately normalize the vector
        # averageDirection /= len(node.influencedBy)

        averageDirection.normalize()

        return averageDirection

    def getNodesInAttractionZone(self, attractor):
        return list(
            self.index.intersection(
                (
                    attractor.position.x - self.settings["AttractionDistance"],
                    attractor.position.y - self.settings["AttractionDistance"],
                    attractor.position.x + self.settings["AttractionDistance"],
                    attractor.position.y + self.settings["AttractionDistance"],
                )
            )
        )

    def getNodesInKillZone(self, attractor):
        return list(
            self.index.intersection(
                (
                    attractor.position.x - self.settings["KillDistance"],
                    attractor.position.y - self.settings["KillDistance"],
                    attractor.position.x + self.settings["KillDistance"],
                    attractor.position.y + self.settings["KillDistance"],
                )
            )
        )

    def getRelativeNeighborNodes(self, attractor):
        fail = False

        nearbyNodes = self.getNodesInAttractionZone(attractor)
        relativeNeighbors = []
        attractorToP0 = None
        attractorToP1 = None
        p0ToP1 = None

        for p0NodeId in nearbyNodes:
            fail = False
            p0 = self.nodes[p0NodeId]
            attractorToP0 = attractor.position - p0.position

            for p1NodeId in nearbyNodes:
                if p1NodeId == p0NodeId:
                    continue

                p1 = self.nodes[p1NodeId]

                attractorToP1 = attractor.position - self.nodes[p1NodeId].position

                if (
                    attractorToP0.magnitude_squared()
                    < attractorToP1.magnitude_squared()
                ):
                    continue

                p0ToP1 = p0.position - p1.position

                if attractorToP0.magnitude_squared() > p0ToP1.magnitude_squared():
                    fail = True
                    break

            if not fail:
                relativeNeighbors.append(p0)

        return relativeNeighbors


def test():
    container = unary_union(
        [
            box(0, 0, 30, 100),
            box(0, 70, 100, 100),
            box(70, 0, 100, 100),
        ]
    )
    network = Network(
        container,
        settings={
            "VenationType": "Closed",
            "AttractionDistance": 30,
            "KillDistance": 5,
        },
    )

    # Add root node
    network.addNode(Node(position=euclid3.Point2(15, 5)))
    network.addNode(Node(position=euclid3.Point2(85, 5)))
    network.addNode(Node(position=euclid3.Point2(50, 85)))

    # Add attractors
    for i in range(300):
        # Randomly generate a point within the container
        x = random.uniform(container.bounds[0], container.bounds[2])
        y = random.uniform(container.bounds[1], container.bounds[3])
        if not container.contains(Point(x, y)):
            continue

        network.attractors.append(Attractor(euclid3.Point2(x, y)))

    start = time.time()
    last_node_size = 0
    for i in range(500):
        network.update()

        if i % 10 == 0:
            new_node_size = len(network.nodes)

            if new_node_size == last_node_size:
                break

            last_node_size = new_node_size
            print(i, new_node_size)

    end = time.time()
    print(
        "Time spent building spatial indices: ", network.timeSpentBuildingSpatialIndices
    )
    print("Total time: ", end - start)

    skeleton = []
    for node in network.nodes:
        if node.parent:
            skeleton.append(
                (
                    (node.position.x, node.position.y, 1000),
                    (node.parent.position.x, node.parent.position.y, 1000),
                )
            )

    for i in range(len(container.exterior.coords)):
        a = container.exterior.coords[i]
        b = container.exterior.coords[(i + 1) % len(container.exterior.coords)]
        skeleton += [((a[0], a[1], 1000), (b[0], b[1], 1000))]

    print("Skeletonizing")
    polys = skeleton_to_polys(
        skeleton, im_scale=8.0, blur=11, margin=20, threshold=15, debug_image=False
    )

    model = Model()
    model.add_poly(unary_union(polys))
    return model


model = MultipartModel()

model.add_model(
    test(),
)

top_level_geom = model.render_full()

model.render_single_svg(__file__ + ".svg")
model.render_single_dxf(__file__ + ".dxf")

print("Saving File")
with open(__file__ + ".scad", "w") as f:
    f.write(solid.scad_render(top_level_geom))
