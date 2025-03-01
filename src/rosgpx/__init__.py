"""A tiny ROS(2)-less tool for the conversion of ROS(2) NavSatFix messages to .gpx."""

import argparse
from pathlib import Path

import rosgpx.rosgpx as rosgpx


def main() -> None:
    """Rosgpx main function that handles argument parsing and conversion."""
    parser = argparse.ArgumentParser(
        description="A tiny ROS(2)-less tool for the conversion of ROS(2) NavSatFix messages to .gpx",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--bag", type=Path, help="Path to the input ROS 2 bag file", required=True)
    parser.add_argument("--output", type=Path, help="Path to the output GPX file")
    parser.add_argument("--topic", type=str, help="The topic name to filter", required=True)
    parser.add_argument("--min-valid-state", type=int, help="The topic name to filter", default=0)
    parser.add_argument(
        "--stuff",
        action=argparse.BooleanOptionalAction,
        help="Stuff the output GPX file into the rosbag directory (Only supported in ros2)",
    )
    parser.add_argument(
        "--force",
        action=argparse.BooleanOptionalAction,
        help="Force overwriting existing output GPX file",
    )
    parser.add_argument("--frame-id", type=str, default=None, help="Frame ID to filter by")

    args = parser.parse_args()
    if args.stuff:
        args.output = args.bag / args.output

    assert args.bag.exists(), f"ERROR: {args.bag} doesn't exist."
    assert args.bag.is_file() or args.stuff, "ERROR: --stuff is only supported for ros2 bags"
    assert not args.output.exists() or args.force, (
        f"ERROR: {args.output} exists. Not overwriting, unless --force is passed"
    )
    assert args.min_valid_state >= -1 and args.min_valid_state <= 2, (
        "--min-valid-state must match NavSatStatus definition: -1 -> 2"
    )

    gpx = rosgpx.parse_navsatfix(
        args.bag, topic=args.topic, min_valid_state=args.min_valid_state, frame_id=args.frame_id
    )

    rosgpx.write_gpx(gpx, args.output)

    print(f"INFO: GPX data has been written to {args.output}")
