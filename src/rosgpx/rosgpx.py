"""rosgpx helper functions."""

from pathlib import Path
from typing import Optional

import gpxpy
import gpxpy.gpx
from rosbags.highlevel import AnyReader


def valid(msg, min_valid_state: int) -> bool:  # noqa
    """
    Check validity of message based on NavSatStatus value.

    Args:
        msg: rosbags message type
        min_valid_state: minimum valid state (NavSatStatus)

    Return:
        true is status matches min_valid_state requirements and lat/lon sanity checks, false otherwise
    """
    return msg.status.status >= min_valid_state or (abs(msg.latitude) <= 90.0 and abs(msg.longitude) <= 90.0)


def parse_navsatfix(bag: Path, topic: str, min_valid_state: int, frame_id: Optional[str]) -> gpxpy.gpx.GPX:
    """
    Parse NavSatFix messages from a ROS2 bag file into GPX format.

    Args:
        bag: Path to bag file to parse
        topic: Name of the topic containing NavSatFix messages
        frame_id: Optional filter for specific frame IDs
        min_valid_state: minimum valid state (NavSatStatus)

    Returns:
        GPX object containing waypoints from NavSatFix messages
    """
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    with AnyReader([bag]) as reader:
        print(
            f"INFO: Opened {bag.name} with {reader.message_count} messages. "
            f"Total recording time: {reader.duration * 1e-9 / 60:.2f} minutes "
        )

        connections = [x for x in reader.connections if x.topic == topic]
        for connection, _, rawdata in reader.messages(connections=connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
            if frame_id and msg.header.frame_id != frame_id:
                continue

            if valid(msg, min_valid_state):
                gpx_segment.points.append(
                    gpxpy.gpx.GPXTrackPoint(
                        latitude=msg.latitude,
                        longitude=msg.longitude,
                        elevation=msg.altitude,
                    )
                )
            else:
                print(
                    f"WARN: skipped {msg.latitude:.2f} {msg.longitude:.2f} "
                    f"{msg.altitude:.2f} with status {msg.status.status}"
                )

    return gpx


def write_gpx(gpx: gpxpy.gpx.GPX, output: Path) -> None:
    """
    Write gpx GPX-object to file as xml.

    Args:
        gpx: GPX-object
        output: Path to the output file
    """
    if not gpx.tracks[-1].segments[-1].points:
        print("WARN: no measurements detected. Have you set --frame_id correctly? How about --min-valid-state?")

    with open(output, "w") as f:
        f.write(gpx.to_xml())
