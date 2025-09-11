#!/usr/bin/env python3
import gltf
import argparse


def add_cuboid_mesh(g, dimensions, texture_dimensions, top_material, material=None):
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

    ot = 1/3
    tt = 2/3
    vtop = [vtsw, vtnw, vtne, vtse,]
    ntop = (0, 1, 0)
    ttop = [(ot, 0.5), (ot, 1), (tt, 1), (tt, 0.5)]
    vnorth = [vtnw, vbnw, vbne, vtne,]
    nnorth = (0, 0, 1)
    tnorth = [(tt, 0), (tt, 0.5), (1, 0.5), (1, 0)]
    vsouth = [vtse, vbse, vbsw, vtsw,]
    nsouth = (0, 0, -1)
    tsouth = [(0, 0), (0, 0.5), (ot, 0.5), (ot, 0)]
    vbottom = [vbnw, vbsw, vbse, vbne,]
    nbottom = (0, -1, 0)
    tbottom = [(1, 1), (1, 0.5), (tt, 0.5), (tt, 1)]
    vwest = [vtsw, vbsw, vbnw, vtnw,]
    nwest = (-1, 0, 0)
    twest = [(ot, 0), (ot, 0.5), (tt, 0.5), (tt, 0)]
    veast = [vtne, vbne, vbse, vtse,]
    neast = (1, 0, 0)
    teast = [(0, 0.5), (0, 1), (ot, 1), (ot, 0.5)]

    indices = [
        0, 1, 2,
        2, 3, 0,
    ]

    u = texture_dimensions[0]
    v = texture_dimensions[1]
    tex_coords_param = [
        (0, 0),
        (0, v),
        (u, v),
        (u, 0),
    ]

    indices = g.add_indices(indices)
    tex_coords = None
    if material is not None:
        tex_coords = g.add_tex_coords(tex_coords_param)

    def get_tex_coords(t):
        if tex_coords is None:
            return g.add_tex_coords(t)
        return tex_coords

    primitive = lambda v, n, t, m: g.primitive(
        vertices=g.add_vertices(v), indices=indices,
        tex_coords=get_tex_coords(t), normals=g.add_normals([n, n, n, n]),
        material=m
    )

    material = material or top_material
    primitives = [
        primitive(vtop, ntop, ttop, top_material),
        primitive(vbottom, nbottom, tbottom, material),
        primitive(vnorth, nnorth, tnorth, material),
        primitive(vsouth, nsouth, tsouth, material),
        primitive(veast, neast, teast, material),
        primitive(vwest, nwest, twest, material),
    ]

    return g.mesh(primitives)


def main():
    parser = argparse.ArgumentParser(
        description='Create cuboids.'
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
        help='PNG image for the texture.'
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
    parser.add_argument('--single', '-s', action='store_true',
        help='If set, use a single material.'
            ' If not, the texture will only be on the top face.'
    )
    parser.add_argument('--alpha', '-a', action='store_true',
        help='If set, use one-bit alpha in the top material.'
            ' Half to fully transparent pixels in the image will show through.'
    )
    parser.add_argument('--tr', default=0.3,
        help='Top roughness (or all if single material).'
    )
    parser.add_argument('--br', default=0.8,
        help='Bottom/side roughness.'
    )
    args = parser.parse_args()

    g = gltf.GLTF()

    with open(args.image, 'rb') as f:
        png_data = f.read()

    texture = g.add_texture(png_data, 'image/png')

    top_material = g.pbr_material(
        name=args.name + '.top',
        color=texture,
        metallic=0.0,
        roughness=args.tr,
        alpha_mode='MASK' if args.alpha else 'OPAQUE'
    )

    material = None
    if not args.single:
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
