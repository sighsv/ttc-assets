#!/usr/bin/env python3
import numpy as np
import cv2
from PIL import Image, ImageDraw
from collections import namedtuple
import math
import argparse


RectSides = namedtuple("RectSides", "top right bottom left")


def detect_edges(image_filename, canny_a=200, canny_b=100):
    image = cv2.imread(image_filename, cv2.IMREAD_GRAYSCALE)
    assert image is not None, (
        "File could not be read."
    )
    return cv2.Canny(image, canny_a, canny_b)


# this loop thing is somehow faster than np.argmax and works more reliably
def find_boundary_edges(edges, margins, reverse_margins):
    top = []
    for x in range(margins.left, edges.shape[1]):
        for y in range(margins.top, edges.shape[0] - reverse_margins.top):
            if edges[y, x]:
                top.append((x, y))
                break

    bottom = []
    for x in range(margins.left, edges.shape[1]):
        for y in range(edges.shape[0] - 1 - margins.bottom, reverse_margins.bottom, -1):
            if edges[y, x]:
                bottom.append((x, y))
                break

    right = []
    for y in range(margins.top, edges.shape[0]):
        for x in range(edges.shape[1] - 1 - margins.right, reverse_margins.right, -1):
            if edges[y, x]:
                right.append((x, y))
                break

    left = []
    for y in range(margins.top, edges.shape[0]):
        for x in range(margins.left, edges.shape[1] - reverse_margins.left):
            if edges[y, x]:
                left.append((x, y))
                break

    return RectSides(
        np.array(top),
        np.array(right),
        np.array(bottom),
        np.array(left)
    )


# f is like
# [ [x, y],
#   [x, y],
#   ...
# ]
def linear_approx(f, is_y=False):
    f = np.array(f)
    x = f[::,0]
    y = f[::,1]
    if is_y:
        x, y = y, x
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    return m, c # m*x + c


# Return the selection vector for inliers
def inliers_zscore(data, constant=0.6745, threshold=3.5):
    # https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
    deviation = np.abs(data - np.median(data))
    median_absolute_deviation = np.median(deviation)
    # no deviation, no outliers
    if median_absolute_deviation == 0:
        modified_z_scores = np.zeros(len(data))
    else:
        modified_z_scores = (constant * deviation) / median_absolute_deviation
    return modified_z_scores < threshold


def clean_noise(f, is_y=False):
    i = 0 if is_y else 1
    return f[inliers_zscore(f[::,i])]


mag = lambda v: math.sqrt(v[0]**2 + v[1]**2)
norm = lambda v: (v[0] / mag(v), v[1] / mag(v))


def line_points(m, c, is_y=False):
    line = lambda x: (m * x + c, x) if is_y else (x, m * x + c)
    return line(0), line(1)


def line_slope(p1, p2, is_y=False):
    ai, bi = (1, 0) if is_y else (0, 1)
    m = (p2[bi] - p1[bi]) / (p2[ai] - p1[ai])
    c = p2[bi] - m*p2[ai]
    return m, c


def backoff_line_points(p1, p2, backoff):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    distance = mag((dx, dy))
    coeff = backoff / distance
    cx = coeff * dy
    cy = coeff * dx
    return (
        (p1[0] + cx, p1[1] + cy),
        (p2[0] + cx, p2[1] + cy),
    )


def backoff_quad(top, right, bottom, left, backoffs):
    return RectSides(
        backoff_line_points(*top, -backoffs.top),
        backoff_line_points(*right, backoffs.right),
        backoff_line_points(*bottom, backoffs.bottom),
        backoff_line_points(*left, -backoffs.left),
    )


def z_score_reject(top, right, bottom, left):
    return RectSides(
        clean_noise(top),
        clean_noise(right, True),
        clean_noise(bottom),
        clean_noise(left, True),
    )


def linear_regression(top, right, bottom, left):
    return RectSides(
        line_points(*linear_approx(top)),
        line_points(*linear_approx(right, True), True),
        line_points(*linear_approx(bottom)),
        line_points(*linear_approx(left, True), True),
    )


# Find intersection of line defined by pair1 with pair2
# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
def line_intersect(pair1, pair2):
    x1 = pair1[0][0]
    x2 = pair1[1][0]
    x3 = pair2[0][0]
    x4 = pair2[1][0]
    y1 = pair1[0][1]
    y2 = pair1[1][1]
    y3 = pair2[0][1]
    y4 = pair2[1][1]
    det = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    x = ((x1 * y2 - y1 * x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / det
    y = ((x1 * y2 - y1 * x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / det
    return (x, y)


def quad_intersect(top, right, bottom, left):
    top_left = line_intersect(top, left)
    top_right = line_intersect(top, right)
    bottom_left = line_intersect(bottom, left)
    bottom_right = line_intersect(bottom, right)
    return top_left, top_right, bottom_right, bottom_left


def quad_bbox(top, right, bottom, left):
    x1 = min([top[0], right[0], bottom[0], left[0]])
    y1 = min([top[1], right[1], bottom[1], left[1]])
    x2 = max([top[0], right[0], bottom[0], left[0]])
    y2 = max([top[1], right[1], bottom[1], left[1]])
    return (x1, y1), (x2, y2)


def margins_n_to_four(margins):
    assert len(margins) != 0, "Margins cannot be empty"
    if len(margins) == 1:
        return RectSides(margins[0], margins[0], margins[0], margins[0])
    if len(margins) == 2:
        return RectSides(margins[0], margins[1], margins[0], margins[1])
    if len(margins) == 3:
        return RectSides(margins[0], margins[1], margins[2], margins[1])
    return RectSides(*margins[:4])


# (y, x), (top, right, bottom, left)
def margins_auto(dimensions, margins):
    margins = margins_n_to_four(margins)
    override = lambda margin, dimension: (
        int(dimension * margin) if (-1 < margin < 1) else int(margin)
    )
    return RectSides(
        override(margins.top, dimensions[0]),
        override(margins.right, dimensions[1]),
        override(margins.bottom, dimensions[0]),
        override(margins.left, dimensions[1]),
    )


def debug_edges(edges, noisy):
    image = np.zeros(edges.shape, dtype=np.uint8)
    for edge in noisy:
        for x, y in edge:
            image[y, x] = 255
    return image


def debug_clean_edges(edges, noisy):
    image = np.zeros(edges.shape, dtype=np.uint8)
    for edge in noisy:
        for x, y in edge:
            image[y, x] = 255
    return image


def debug_lines(source, lines, rect):
    draw = ImageDraw.Draw(source)
    red = (255, 0, 0)
    magenta = (255, 0, 255)
    line = lambda a, b, color: draw.line(a + b, fill=color, width=3)
    # Calculate the slope and expand out a point-point line
    def expanded_line(a, b, color, is_y=False):
        ai = 0
        bi = 1
        if is_y:
            ai, bi = bi, ai
        c = a[bi]
        m = (b[bi] - c) / b[ai]
        b = (source.size[ai], m * source.size[ai] + c)
        if is_y:
            b = (b[1], b[0])
        line(a, b, color)
    expanded_line(*lines[0], red)
    expanded_line(*lines[1], red, True)
    expanded_line(*lines[2], red)
    expanded_line(*lines[3], red, True)
    line(rect[0], rect[1], magenta)
    line(rect[1], rect[2], magenta)
    line(rect[2], rect[3], magenta)
    line(rect[3], rect[0], magenta)
    return source


def main():
    parser = argparse.ArgumentParser(
        description="Detect the outline of a playing card and rectify it."
    )
    parser.add_argument("filename")
    parser.add_argument("output")
    parser.add_argument("--margins", "-m",
        nargs="+", type=float,
        default=(0.025, 0.025, 0.025, 0.025),
        help=(
            "Margins to virtually remove from the image before edge detection."
            " Uses CSS order: top, right, bottom, left, (and for less than 4)."
            " Values less than 1 from 0 are percentages of the image size."
        )
    )
    parser.add_argument("--reverse_margins", "-r",
        nargs="+", type=float,
        default=(0.5, 0.5, 0.5, 0.5),
        help="Virtually remove this much of the image from each edge"
    )
    parser.add_argument("--backoff", "-b",
        nargs="+", type=float,
        default=(5, 5, 5, 5),
        help="Shift lines back by this distance "
    )
    parser.add_argument("--canny_x", "-x",
        type=float, default=200,
        help="Threshold 1 for Canny edge detection."
    )
    parser.add_argument("--canny_y", "-y",
        type=float, default=100,
        help="Threshold 1 for Canny edge detection."
    )
    # debugging/diagnostic
    parser.add_argument("--canny_edges", "-c", action="store_true",
        help="Output the initial Canny edge detection image and exit."
    )
    parser.add_argument("--noisy_edges", "-n", action="store_true",
        help=(
            "Output the filtered edges and exit"
            ", which should be a noisy bounding of the four edges of the image."
        )
    )
    parser.add_argument("--clean_edges", "-C", action="store_true",
        help=(
            "Output the noise filtered edges and exit"
            ", which should be just the four surrounding edges of the image."
        )
    )
    parser.add_argument("--debug_lines", "-d", action="store_true",
        help=(
            "Output the final surrounding lines on a copy of the image"
            " and exit."
        )
    )
    args = parser.parse_args()

    edges = detect_edges(args.filename, args.canny_x, args.canny_y)

    if args.canny_edges:
        cv2.imwrite(args.output, edges)
        return

    margins = margins_auto(edges.shape, args.margins)
    reverse_margins = margins_auto(edges.shape, args.reverse_margins)
    backoffs = margins_auto(edges.shape, args.backoff)

    noisy_edges = find_boundary_edges(edges, margins, reverse_margins)
    if args.noisy_edges:
        cv2.imwrite(args.output, debug_edges(edges, noisy_edges))
        return

    clean_edges = z_score_reject(*noisy_edges)
    if args.clean_edges:
        cv2.imwrite(args.output, debug_edges(edges, clean_edges))
        return

    lines_tight = linear_regression(*clean_edges)
    lines = backoff_quad(*lines_tight, backoffs)
    corners = quad_intersect(*lines)
    bbox = quad_bbox(*corners)
    size = (
        int(bbox[1][0] - bbox[0][0]),
        int(bbox[1][1] - bbox[0][1])
    )
    image = Image.open(args.filename)
    
    if args.debug_lines:
        debug_lines(image, lines_tight, corners)
        image.save(args.output)
        return

    out = image.transform(
        size,
        Image.Transform.QUAD,
        corners[0] + corners[3] + corners[2] + corners[1]
    )
    out.save(args.output)


if __name__ == "__main__":
    main()
