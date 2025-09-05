#!/usr/bin/env python3
import math
import itertools
import gltf
import argparse


def circle_points(number, radius=1, direction=1):
    angle = direction * 2 / number * math.pi
    coord = lambda th: (math.cos(th) * radius, math.sin(th) * radius)
    return [
        coord(angle * i) for i in range(number)
    ]


def circle_mesh(points, radius=1, reverse=False):
    vertices = circle_points(points, radius)
    tri = (
        (lambda i: (0, i + 1, i))
        if reverse else
        (lambda i: (0, i, i + 1))
    )
    indices = [
        tri(i) for i in range(1, points + 1)
    ]
    indices = list(itertools.chain.from_iterable(indices))
    return [(0, 0)] + vertices + [vertices[0]], indices


mag = lambda v: math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
norm = lambda v: (v[0] / mag(v), v[1] / mag(v), v[2] / mag(v))


# caps_only will map the top and bottom to the same circle centered in UV space
# if false the UV map will have the sides in the upper half of the image,
# with top/bottom being in the lower left, and lower right, respectively
def add_cylinder_mesh(
        g,
        points,
        radius, height,
        material,
        wiggle=0.01,
        caps_only=False,
        handedness=-1):
    # caps
    vt, it = circle_mesh(points, radius, reverse=True)
    vb, ib = circle_mesh(points, radius, reverse=False)
    # Shift vertices to match specified height
    vt = [(a, height / 2, b) for a, b in vt]
    vb = [(a, -height / 2, b) for a, b in vb]
    # Combine vertices and indices
    vertices = g.add_vertices(vt + vb)
    indices = g.add_indices(it + [points + i + 2 for i in ib])
    # Simple fixed normals
    cap_normals = g.add_normals(
        [(0, 1, 0) for _ in range(points + 2)]
        + [(0, -1, 0) for _ in range(points + 2)]
    )
    if caps_only:
        # Assign the caps to the same circle centered in the image
        scale = radius * 1 / (0.5 - wiggle / 2)
        vt_tex = [(a / scale + 0.5, c / scale + 0.5) for a, b, c in vt]
        vb_tex = [(a / scale + 0.5, -c / scale + 0.5) for a, b, c in vb]
    else:
        # Assign the top to the bottom left quarter, bottom to bottom right
        scale = radius * 1 / (0.25 - wiggle / 2)
        vt_tex = [(a / scale + 0.25, c / scale + 0.75) for a, b, c in vt]
        vb_tex = [(a / scale + 0.75, -c / scale + 0.75) for a, b, c in vb]
    cap_tex_coords = g.add_tex_coords(vt_tex + vb_tex)
    # These point at an arbitrary tangent
    cap_tangents = g.add_tangents(
        [(1, 0, 0, handedness) for _ in range(2 * points + 4)]
    )

    # top start, top end
    ts = 1
    te = points + 2
    # bottom start, bottom end
    bs = points + 3
    be = 2 * points + 4
    # Like clamp, but modulo
    rmod = lambda value, start, end: (value - start) % (end - start) + start
    tube_indices = [
        # viewing the face with normal pointing at viewer
        # bottom left, top left, top right
        # top right, bottom right, bottom left
        (rmod(i + bs, bs, be), rmod(i + ts, ts, te), rmod(i + ts + 1, ts, te),
         rmod(i + ts + 1, ts, te), rmod(i + bs + 1, bs, be), rmod(i + bs, bs, be))
        for i in range(points)
    ]
    tube = g.add_indices(list(itertools.chain.from_iterable(tube_indices)))
    normlist = lambda l: [norm((v[0], 0, v[2])) for v in l]
    # Assign the center top and center bottom vertices to their fixed values
    # Then normalize the x/y coordinates of the rim vertices to result in
    # Smooth cylindrical normals
    tube_normals = g.add_normals(
        [(0, 1, 0)]
        + normlist(vt[1:])
        + [(0, -1, 0)]
        + normlist(vb[1:])
    )
    if not caps_only:
        # Assign the sides to the upper 50% of the image
        tube_tex_coords = g.add_tex_coords(
            [(1, 1)]
            + [(i / points, 0 + wiggle / 2) for i in range(points, -1, -1)]
            + [(1, 1)]
            + [(i / points, 0.5 - wiggle / 2) for i in range(points, -1, -1)]
        )
    else:
        # these need to exist, but can be arbitrary
        tube_tex_coords = g.add_tex_coords(
            [(0.5, 0.5) for _ in range(2 * points + 4)]
        )
    # These tangents just point upwards
    tube_tangents = g.add_tangents(
        [(0, 1, 0, handedness) for _ in range(2 * points + 4)]
    )

    caps = g.primitive(
        vertices=vertices, indices=indices,
        normals=cap_normals, tex_coords=cap_tex_coords, tangents=cap_tangents,
        material=material
    )
    sides = g.primitive(
        vertices=vertices, indices=tube,
        normals=tube_normals, tex_coords=tube_tex_coords, tangents=tube_tangents,
        material=material
    )
    return g.mesh([caps, sides])


def main():
    parser = argparse.ArgumentParser(
        description='Create textured cylinders.'
    )
    parser.add_argument('--points', '-p', type=int, default=32,
        help='Number of points on the circles.'
    )
    parser.add_argument('--radius', '-r', type=float, default=0.5,
        help='Cylinder radius.'
    )
    parser.add_argument('--height', '-y', type=float, default=1,
        help='Cylinder height.'
    )
    parser.add_argument('--texture', '-t',
        help='Input texture.'
    )
    parser.add_argument('--wiggle', '-w', type=float, default=0.01,
        help='Shrink UV islands by this much to prevent overlap.'
    )
    parser.add_argument('--normal_map', '-n',
        help='Input normal map.'
    )
    parser.add_argument('--flip_handedness', '-f', action='store_true',
        help='Flip tangent handedness, for normal mapping.'
    )
    parser.add_argument('--name', '-N',
        help='Material name.'
    )
    parser.add_argument('--color', '-C', default='#ffffff',
        help='Material color.'
    )
    parser.add_argument('--metallic', '-M', type=float,
        help='Metallic factor of the material.'
    )
    parser.add_argument('--roughness', '-R', type=float,
        help='Roughness factor of the material.'
    )
    parser.add_argument('--caps_only', '-c', action='store_true',
        help='If set, the UV map will only map the top and bottom.'
    )
    parser.add_argument('--output', '-o',
        help='Output GLB file.'
    )
    args = parser.parse_args()
    g = gltf.GLTF()

    texture = None
    if args.texture:
        with open(args.texture, 'rb') as f:
            data = f.read()
        texture = g.add_texture(data, 'image/png')

    normal_map = None
    if args.normal_map:
        with open(args.normal_map, 'rb') as f:
            data = f.read()
        normal_map = g.add_texture(data, 'image/png')

    material = g.pbr_material(
        name=args.name,
        color=texture or gltf.Color(args.color),
        metallic=args.metallic,
        roughness=args.roughness,
        normal_map=normal_map
    )

    mesh = add_cylinder_mesh(
        g,
        args.points,
        args.radius, args.height,
        material,
        caps_only=args.caps_only,
        handedness=1 if args.flip_handedness else -1,
        wiggle=args.wiggle,
    )

    g.scenes = [
        {'nodes': [g.node(mesh).index]}
    ]

    with open(args.output, 'wb') as f:
        f.write(g.dump_glb())


if __name__ == '__main__':
    main()
