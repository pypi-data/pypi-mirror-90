#
# Copyright 2019-2020 Thomas Kramer.
#
# This source describes Open Hardware and is licensed under the CERN-OHL-S v2.
#
# You may redistribute and modify this documentation and make products using it
# under the terms of the CERN-OHL-S v2 (https:/cern.ch/cern-ohl).
# This documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY,
# INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A PARTICULAR PURPOSE.
# Please see the CERN-OHL-S v2 for applicable conditions.
#
# Source location: https://codeberg.org/tok/librecell
#
import logging
import time
from typing import Dict, List, Tuple, Union
from klayout import db
import itertools
import os

from .writer import Writer
from ..layout import layers

logger = logging.getLogger(__name__)


class Label:
    def __init__(self, layer_name: str, text_source: Tuple[int, int], polygon_source: Tuple[int, int]):
        assert isinstance(polygon_source, tuple) and len(polygon_source) == 2, "source must be a 2-tuple"
        assert isinstance(text_source, tuple) and len(polygon_source) == 2, "source must be a 2-tuple"
        self.layer_name = layer_name
        self.text_source = text_source
        self.polygon_source = polygon_source


class Layer:
    def __init__(self, layer_name: str, polygon_source: Tuple[int, int]):
        assert isinstance(polygon_source, tuple) and len(polygon_source) == 2, "source must be a 2-tuple"

        self.layer_name = layer_name
        self.polygon_source = polygon_source


def _decompose_polygon(polygon: db.Polygon, ignore_non_rectilinear: bool = False) -> List[db.Box]:
    """
    Decompose a `db.Region` of multiple `db.Polygon`s into non-overlapping rectangles (`db.Box`).
    :param polygon:
    :param ignore_non_rectilinear:
    :return:
    """
    return _decompose_region(db.Region(polygon), ignore_non_rectilinear)


def _decompose_region(region: db.Region, ignore_non_rectilinear: bool = False) -> List[db.Box]:
    """
    Decompose a `db.Region` of multiple `db.Polygon`s into non-overlapping rectangles (`db.Box`).
    :param region:
    :param ignore_non_rectilinear: If set to `True` then non-rectilinear polygons are skipped.
    :return: Returns the list of rectangles.
    """
    trapezoids = region.decompose_trapezoids_to_region()
    logger.debug("Number of trapezoids: {}".format(trapezoids.size()))
    rectangles = []
    for polygon in trapezoids.each():
        box = polygon.bbox()

        if db.Polygon(box) != polygon:
            msg = "Cannot decompose into rectangles. Something is not rectilinear!"
            if not ignore_non_rectilinear:
                logger.error(msg)
                assert False, msg
            else:
                logger.warning(msg)

        rectangles.append(box)
    return rectangles


def _format_rect(box: db.Box) -> str:
    """
    Format a rectangle as a string of the form as it is required for .mag files: "xbot ybot xtop ytop"
    :param box: The rectangle.
    :return: Returns the formatted string.
    """
    lower_left = box.p1
    upper_right = box.p2
    xbot, ybot = lower_left.x, lower_left.y
    xtop, ytop = upper_right.x, upper_right.y

    assert xbot <= xtop
    assert ybot <= ytop

    rect_str = "{} {} {} {}".format(xbot, ybot, xtop, ytop)
    return rect_str


def store_layout_to_magic_file(tech_name: str,
                               output_map: Dict[str, Union[str, List[str]]],
                               layout: db.Layout,
                               pin_geometries: Dict[str, List[Tuple[str, db.Shape]]],
                               top_cell: db.Cell,
                               output_file: str,
                               ignore_non_rectilinear: bool = False,
                               scale_factor: int = 1):
    """
    Write the cell layout to a file in the Magic (.mag) format.

    Documentation of the magic file format: http://opencircuitdesign.com/magic/manpages/mag_manpage.html
    :param layout:
    :param top_cell:
    :param output_file:
    :param ignore_non_rectilinear:
    :param gds_path: Path of the source GDS2 file. This will be written into the comment of the .mag file.
    :return:
    """

    layer_config = []
    for source_layer_name, destinations in output_map.items():
        assert isinstance(destinations, str) or isinstance(destinations, List), \
            'Destination layer must either be as string or a list of strings.'

        if not isinstance(destinations, List):
            destinations = [destinations]

        for dest_name in destinations:
            # Convert layer name into (index, datatype).
            layer_config.append(
                Layer(dest_name, layers.layermap[source_layer_name])
            )

    logger.info("Number of layers: {}".format(layout.layers()))
    logger.info("Processing cell: {}".format(top_cell.name))

    mag_lines = ["magic",
                 "# Generated by librecell",
                 "tech {}".format(tech_name),
                 "timestamp {}".format(int(time.time()))
                 ]

    mag_labels = []

    transformation = db.DCplxTrans(scale_factor)

    for layer in layer_config:
        text_layer_gds_index = layer.polygon_source
        idx = layout.layer(*text_layer_gds_index)
        layer_info = layout.get_info(idx)

        layer_number = layer_info.layer
        layer_datatype = layer_info.datatype
        assert text_layer_gds_index == (layer_number, layer_datatype)

        # Fetch geometry of layer
        region = db.Region(top_cell.shapes(idx))

        line = "<< {} >>".format(layer.layer_name)
        mag_lines.append(line)

        # Scale the region.
        region = region.transformed(transformation)

        # Convert region into rectangles.
        boxes = _decompose_region(region, ignore_non_rectilinear=ignore_non_rectilinear)
        # Format rectangle strings.
        rect_lines = ["rect {}".format(_format_rect(box)) for box in boxes]
        mag_lines.extend(rect_lines)

    port_counter = itertools.count(1)
    for pin_name, pins in pin_geometries.items():
        for layer_name, pin_shapes in pins:
            pin_region = db.Region()
            pin_region.insert(pin_shapes)
            # Convert pin shape into rectangles.
            for pin_shape in pin_region.each_merged():
                pin_shape = transformation.trans(pin_shape)
                rectangles = _decompose_polygon(pin_shape, ignore_non_rectilinear)
                rectangles_str = [_format_rect(r) for r in rectangles]

                for rect_str in rectangles_str:
                    text_orientation = 0  # 0: center
                    mag_labels.append("rlabel {} {} {} {}".format(layer_name,
                                                                  rect_str,
                                                                  text_orientation,
                                                                  pin_name))

                    # TODO: is this correct?
                    mag_labels.append("port {} se".format(next(port_counter)))

    # Appends 'labels' section if there are any.
    if len(mag_labels) > 0:
        mag_lines.append("<< labels >>")
        mag_lines.extend(mag_labels)

    mag_lines.append("<< end >>\n")

    with open(output_file, "w") as mag_file:
        logger.info("Writing MAG file: {}".format(output_file))
        mag_data = "\n".join(mag_lines)
        mag_file.write(mag_data)


class MagWriter(Writer):

    def __init__(self, tech_name: str, output_map: Dict[str, str], scale_factor: float = 1):
        """

        :param tech_name:
        :param output_map:
        :param scale_factor: Scale all coordinates by this number (rounding down to next integer).
        """
        self.tech_name = tech_name
        self.output_map = output_map
        self.scale_factor = scale_factor

    def write_layout(self,
                     layout: db.Layout,
                     pin_geometries: Dict[str, List[Tuple[str, db.Shape]]],
                     top_cell: db.Cell,
                     output_dir: str,
                     ) -> None:
        mag_file_name = '{}.mag'.format(top_cell.name)
        mag_out_path = os.path.join(output_dir, mag_file_name)

        store_layout_to_magic_file(
            self.tech_name,
            self.output_map,
            layout,
            pin_geometries,
            top_cell,
            mag_out_path,
            ignore_non_rectilinear=False,
            scale_factor=self.scale_factor)
