# rosgpx

A tiny ROS(2)-less tool for the conversion of ROS(2) NavSatFix messages to .gpx.

(I also needed an excuse to test [uv](https://docs.astral.sh/uv/))

## Install

```
uv pip install git+https://github.com/juliangaal/rosgpx
```

## Run

```
usage: rosgpx [-h] [--bag BAG] [--output OUTPUT] [--topic TOPIC] [--stuff | --no-stuff] [--force | --no-force]
              [--frame-id FRAME_ID]

A tiny ROS(2)-less tool for the conversion of ROS(2) NavSatFix messages to .gpx

options:
  -h, --help           show this help message and exit
  --bag BAG            Path to the input ROS 2 bag file (default: None)
  --output OUTPUT      Path to the output GPX file (default: None)
  --topic TOPIC        The topic name to filter (default: None)
  --stuff, --no-stuff  Stuff the output GPX file into the rosbag directory (Only supported in ros2) (default: None)
  --force, --no-force  Force overwriting existing output GPX file (default: None)
  --frame-id FRAME_ID  Frame ID to filter by (default: None)
```

with uv: `uv run rosgpx`

## GPX

Visualize the gpx in, e.g., [https://evrignaud.github.io/gpx-viewer/](https://evrignaud.github.io/gpx-viewer/)

## Acknowlegments

Thanks to [rosbags](https://ternaris.gitlab.io/rosbags/) for parsing and [gpxpy](https://pypi.org/project/gpxpy/) for handling the xml part.
