import argparse

from pathlib import Path

import numpy as np

from chunk import TransformChunk
from geodesic import geodetic2ned


def test(args):
    chunk = TransformChunk()
    chunk.load_poses(args.poses)

    poses = chunk.get_poses()

    positions = poses[["latitude", "longitude", "altitude"]].to_numpy()

    lats = positions[:, 0]
    lons = positions[:, 1]
    alts = positions[:, 2]
    
    ref_lats = np.full(lats.shape, lats.mean())
    ref_lons = np.full(lons.shape, lons.mean())
    ref_alts = np.full(alts.shape, 0.0)

    n, e, d = geodetic2ned(lats, lons, alts, ref_lats, ref_lons, ref_alts)

    print(n.shape)
    print(e.shape)
    print(d.shape)

    print("North: \n{0}".format(n))
    print("East: \n{0}".format(e))
    print("Down: \n{0}".format(d))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--poses", 
            type=Path, 
            required=True,  
            help="path to csv file of poses"
        )

    test(parser.parse_args())


if __name__ == "__main__":
    main()
