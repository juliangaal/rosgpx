"""rosgpx helper functions."""

from pathlib import Path
from typing import Optional

import gpxpy
import gpxpy.gpx
from rosbags.highlevel import AnyReader


def parse_navsatfix(bag: Path, topic: str, frame_id: Optional[str] = None) -> gpxpy.gpx.GPX:
    """
    Parse NavSatFix messages from a ROS2 bag file into GPX format.

    Args:
        bag: Path to bag file to parse
        topic: Name of the topic containing NavSatFix messages
        frame_id: Optional filter for specific frame IDs

    Returns:
        GPX object containing waypoints from NavSatFix messages
    """
    gpx = gpxpy.gpx.GPX()

    with AnyReader([bag]) as reader:
        print(
            f"INFO: Opened {bag.name} with {reader.message_count} messages."
            f"Total recording time: {reader.duration * 1e-9 / 60:.2f} minutes"
        )

        connections = [x for x in reader.connections if x.topic == topic]
        for connection, _, rawdata in reader.messages(connections=connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
            if frame_id and msg.header.frame_id != frame_id:
                continue

            gpx.waypoints.append(
                gpxpy.gpx.GPXWaypoint(
                    latitude=msg.latitude,
                    longitude=msg.longitude,
                    elevation=msg.altitude,
                )
            )

    return gpx


def write_gpx(gpx: gpxpy.gpx.GPX, output: Path) -> None:
    """
    Write gpx GPX-object to file as xml.

    Args:
        gpx: GPX-object
        output: Path to the output file
    """
    if not gpx.waypoints:
        print("WARN: no waypoints detected. Have you use --frame_id correctly?")

    with open(output, "w") as f:
        f.write(gpx.to_xml())
