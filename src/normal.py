#!/usr/bin/env python3
import numpy as np
import math
import random
from PIL import Image
import argparse


# Grayscale bump map (0 to 1) -> tangent normal map
def bump_to_normal(bump, strength=1):
    dy, dx = np.gradient(-bump)

    vectors = np.dstack([dx, dy, np.ones(bump.shape) / strength])
    magnitude = np.linalg.norm(vectors, axis=2)
    # normalize
    vectors[:, :, 0] /= magnitude
    vectors[:, :, 1] /= magnitude
    vectors[:, :, 2] /= magnitude

    return (vectors + 1) / 2 * 255


def main():
    parser = argparse.ArgumentParser(
        description='Create normal maps from height/bump maps.'
    )
    parser.add_argument('--function', '-f',
        help='Function of x and y (defined on [0, 1]) which produces a value [0, 1].'
    )
    parser.add_argument('--width', '-x', type=int,
        help='Width of output image (for function defined maps).'
    )
    parser.add_argument('--height', '-y', type=int,
        help='Height of output image (for function defined maps).'
    )
    parser.add_argument('--input', '-i',
        help='Input bump map.'
    )
    parser.add_argument('--bump', '-b', action='store_true',
        help='If set, output bump map and exit.'
    )
    parser.add_argument('--output', '-o',
        help='Output normal map.'
    )
    parser.add_argument('--seed', '-r', type=int,
        help='Random seed.'
    )
    parser.add_argument('--scale', '-s', type=float, default=10,
        help='Normal map scale.'
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.function:
        f = eval(args.function)
        bump = np.array([
            [
                f(x / args.width - 0.5, y / args.height - 0.5)
                for x in range(args.width)
            ] for y in range(args.height)
        ])
    elif args.input:
        bump = np.asarray(Image.open(args.input))

    if args.bump:
        normal = (bump * 255).round().astype(np.uint8)
    else:
        normal = bump_to_normal(bump, args.scale).round().astype(np.uint8)

    output = Image.fromarray(normal)
    output.save(args.output)


if __name__ == '__main__':
    main()
