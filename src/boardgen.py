#!/usr/bin/env python3
import gltf
import argparse


def add_cuboid_mesh(g, dimensions, texture_dimensions, top_material, material):
    x = dimensions[0] / 2
    y = dimensions[1] / 2
    z = dimensions[2] / 2

    vtne = (x, y, z)
    vtnw = (-x, y, z)
    vtse = (x, y, -z)
    vtsw = (-x, y, -z)
    vbne = (x, -y, z)
    vbnw = (-x, -y, z)
    vbse = (x, -y, -z)
    vbsw = (-x, -y, -z)

    vtop = [vtsw, vtnw, vtne, vtse,]
    ntop = (0, 1, 0)
    vnorth = [vtnw, vbnw, vbne, vtne,]
    nnorth = (0, 0, 1)
    vsouth = [vtse, vbse, vbsw, vtsw,]
    nsouth = (0, 0, -1)
    vbottom = [vbnw, vbsw, vbse, vbne,]
    nbottom = (0, -1, 0)
    vwest = [vtsw, vbsw, vbnw, vtnw,]
    nwest = (-1, 0, 0)
    veast = [vtne, vbne, vbse, vtse,]
    neast = (1, 0, 0)

    indices = [
        0, 1, 2,
        2, 3, 0,
    ]

    u = texture_dimensions[0]
    v = texture_dimensions[1]
    tex_coords = [
        (0, 0),
        (0, v),
        (u, v),
        (u, 0),
    ]

    indices = g.add_indices(indices)
    tex_coords = g.add_tex_coords(tex_coords)

    primitive = lambda v, n, m: g.primitive(
        vertices=g.add_vertices(v), indices=indices,
        tex_coords=tex_coords, normals=g.add_normals([n, n, n, n]),
        material=m
    )

    primitives = [
        primitive(vtop, ntop, top_material),
        primitive(vbottom, nbottom, material),
        primitive(vnorth, nnorth, material),
        primitive(vsouth, nsouth, material),
        primitive(veast, neast, material),
        primitive(vwest, nwest, material),
    ]

    return g.mesh(primitives)


def main():
    parser = argparse.ArgumentParser(
        description='Create cuboid game boards from a PNG image.'
    )
    parser.add_argument('-x', type=float,
        help='Size on the X dimension.'
    )
    parser.add_argument('-y', type=float,
        help='Size on the Y dimension (height).'
    )
    parser.add_argument('-z', type=float,
        help='Size on the Z dimension.'
    )
    parser.add_argument('-u', type=float, default=1.0,
        help='Texture U dimension'
             ' (width percent of image, e.g. 0.5 for a tall image).'
    )
    parser.add_argument('-v', type=float, default=1.0,
        help='Texture V dimension'
             ' (height percent of image, e.g. 0.5 for a wide image).'
    )
    parser.add_argument('--image', '-i',
        help='PNG image to use for the top of the board.'
    )
    parser.add_argument('--output', '-o',
        help='Output filename.'
    )
    parser.add_argument('--glb', '-b', action='store_true',
        help='If set, write a GLB format file instead of a GLTF.'
    )
    parser.add_argument('--name', '-n', default='board',
        help='Name of the board, used to differentiate the materials.'
    )
    parser.add_argument('--background', '-c', default="#4D2A24",
        help='Color for the sides and bottom of the board.'
    )
    parser.add_argument('--tr', default=0.3,
        help='Top roughness.'
    )
    parser.add_argument('--br', default=0.8,
        help='Bottom/side roughness.'
    )
    args = parser.parse_args()

    g = gltf.GLTF(generator='myriad board generator')

    with open(args.image, 'rb') as f:
        png_data = f.read()

    texture = g.add_texture(png_data, 'image/png')

    top_material = g.pbr_material(
        name=args.name + '.top',
        color=texture,
        metallic=0.0,
        roughness=args.tr,
    )

    material = g.pbr_material(
        name=args.name + '.bottom',
        color=gltf.Color(args.background),
        metallic=0.0,
        roughness=args.br,
    )

    dimensions = (args.x, args.y, args.z)
    texture_dimensions = (args.u, args.v)
    board = add_cuboid_mesh(
        g,
        dimensions, texture_dimensions,
        top_material, material
    )

    g.scenes = [
        {'nodes': [g.node(board).index]}
    ]

    if args.glb:
        with open(args.output, "wb") as f:
            f.write(g.dump_glb())
    else:
        with open(args.output, "w") as f:
            f.write(g.dump_base64_gltf())


if __name__ == '__main__':
    main()
