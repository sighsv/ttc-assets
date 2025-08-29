#!/usr/bin/env python3
import struct
import base64
import json
import argparse
import sys

def pack_vertices_indices(vertices, indices, tex_coords, normals):
    buf = b''
    for i in indices:
        buf += struct.pack('<hhh', *i)
    index_len = len(buf)
    float_start = index_len
    if float_start % 4 != 0:
        buf += b'hi'
        float_start += 2
    tex_coord_start = float_start
    for t in tex_coords:
        buf += struct.pack('<ff', *t)
    normal_start = len(buf)
    for n in normals:
        buf += struct.pack('<fff', *n)
    vertex_start = len(buf)
    for v in vertices:
        buf += struct.pack('<fff', *v)
    return buf, index_len, tex_coord_start, normal_start, vertex_start

def data_to_base64_uri(data):
    encoded = base64.b64encode(data).decode('ascii')
    return f'data:application/octet-stream;base64,{encoded}'

def buffer_views_from_packed(buf, index_len, tex_coord_start, normal_start, vertex_start):
    indices = {
        "buffer": 0,
        "byteOffset": 0,
        "byteLength": index_len,
        "target": 34963
    }
    tex_coords = {
        "buffer": 0,
        "byteOffset": tex_coord_start,
        "byteLength": normal_start - tex_coord_start,
        "target": 34962
    }
    normals = {
        "buffer": 0,
        "byteOffset": normal_start,
        "byteLength": vertex_start - normal_start,
        "target": 34962
    }
    vertices = {
        "buffer": 0,
        "byteOffset": vertex_start,
        "byteLength": len(buf) - vertex_start,
        "target": 34962
    }
    return [indices, tex_coords, normals, vertices]

def buffer_accessors(vertices, indices_top, indices, tex_coords, normals):
    topcount = len(indices_top) * 3
    indices_top = {
        "bufferView": 0,
        "byteOffset": 0,
        "componentType": 5123,
        "count": topcount,
        "type": "SCALAR",
        "max": [max(max(i) for i in indices_top)],
        "min": [min(min(i) for i in indices_top)],
    }
    indices = {
        "bufferView": 0,
        "byteOffset": topcount * 2,
        "componentType": 5123,
        "count": len(indices) * 3,
        "type": "SCALAR",
        "max": [max(max(i) for i in indices)],
        "min": [min(min(i) for i in indices)],
    }
    getc = lambda vertices, i: (v[i] for v in vertices)
    tex_coords = {
        "bufferView": 1,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(tex_coords),
        "type": "VEC2",
        "max": [max(getc(tex_coords, 0)), max(getc(tex_coords, 1))],
        "min": [min(getc(tex_coords, 0)), min(getc(tex_coords, 1))],
    }
    vertices = {
        "bufferView": 3,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(vertices),
        "type": "VEC3",
        "max": [max(getc(vertices, 0)), max(getc(vertices, 1)), max(getc(vertices, 2))],
        "min": [min(getc(vertices, 0)), min(getc(vertices, 1)), min(getc(vertices, 2))],
    }
    normals = {
        "bufferView": 2,
        "byteOffset": 0,
        "componentType": 5126,
        "count": len(normals),
        "type": "VEC3",
        "max": [max(getc(normals, 0)), max(getc(normals, 1)), max(getc(normals, 2))],
        "min": [min(getc(normals, 0)), min(getc(normals, 1)), min(getc(normals, 2))],
    }
    return [indices_top, indices, tex_coords, normals, vertices]

def gltf_from_verts_indices(
        vertices,
        indices_top, indices,
        normals,
        tex_coords, texture_buffer, texture_mime, materials):
    buf, index_len, tex_coord_start, normals_start, vertex_start = pack_vertices_indices(
        vertices, indices_top + indices, tex_coords, normals)

    bufferViews = buffer_views_from_packed(buf, index_len, tex_coord_start, normals_start, vertex_start)
    bufferViews += [
        {
            "buffer": 0,
            "byteOffset": len(buf),
            "byteLength": len(texture_buffer),
        }
    ]

    accessors = buffer_accessors(vertices, indices_top, indices, tex_coords, normals)

    gltf = {
        "scene": 0,
        "scenes": [{"nodes": [0, 1]}],
        "nodes": [{"mesh": 0}, {"mesh": 1}],
        "meshes": [
            {
                "primitives": [{
                    "attributes": {"POSITION": 4, "NORMAL": 3, "TEXCOORD_0" : 2},
                    "indices": 0,
                    "material": 0
                }]
            },
            {
                "primitives": [{
                    "attributes": {"POSITION": 4},
                    "indices": 1,
                    "material": 1
                }]
            }
        ],
        "materials": materials,
        "textures": [{
            "sampler": 0,
            "source": 0
        }],
        "images": [{
            "mimeType": texture_mime,
            "bufferView": 4
        }],
        "samplers": [{
            "magFilter": 9729,
            "minFilter": 9987,
            "wrapS": 33648,
            "wrapT": 33648,
        }],
        "bufferViews": bufferViews,
        "accessors": accessors,
        "asset": {
            "version": "2.0",
            "generator": "myriad board generator"
        }
    }
    return buf + texture_buffer, gltf

def texture_from_image(image):
    with open(image, "rb") as f:
        buf = f.read()
    return buf, "image/png"

def gltf_from_buf_gltf(buf, gltf):
    gltf["buffers"] = [
        {
            "uri": data_to_base64_uri(buf),
            "byteLength": len(buf)
        }
    ]
    return json.dumps(gltf, indent=2)

def glb_from_buf_gltf(buf, gltf):
    gltf["buffers"] = [
        {
            "byteLength": len(buf)
        }
    ]
    jdata = json.dumps(gltf, indent=0, separators=(',', ':')).encode('utf8')
    jdata += b' ' * (-len(jdata) % 4)
    buf += b'\0' * (-len(buf) % 4)
    header = struct.pack('<III', 0x46546C67, 2,
        12 # header
        + 8 + len(jdata)
        + 8 + len(buf)
    )
    json_chunk = struct.pack('<II', len(jdata), 0x4E4F534A) + jdata
    bin_chunk = struct.pack('<II', len(buf), 0x004E4942) + buf
    return header + json_chunk + bin_chunk


def generate_geometry(x, y, z, tex_x, tex_y):
    # we need positions, there will be 8
    bx = -(x / 2)
    tx = (x / 2)
    by = -(y / 2)
    ty = (y / 2)
    bz = -(z / 2)
    tz = (z / 2)
    # y up, z north, x east
    positions = (
        (bx, by, bz), # bottom southwest
        (bx, by, tz), # bottom northwest
        (tx, by, bz), # bottom southeast
        (tx, by, tz), # bottom northeast
        (bx, ty, bz), # top southwest
        (bx, ty, tz), # top northwest
        (tx, ty, bz), # top southeast
        (tx, ty, tz), # top northeast
    )
    normals = (
        (0.0, -1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, -1.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
    )
    bsw = 0
    bnw = 1
    bse = 2
    bne = 3
    tsw = 4
    tnw = 5
    tse = 6
    tne = 7
    # indices will use the 8 positions to form triangles
    indices_top = (
        (tsw, tnw, tne), (tne, tse, tsw), # top
    )
    ty = tex_y
    tx = tex_x
    tex_coords_top = (
        (0.0, 0.0),
        (0.0, ty),
        (tx, 0.0),
        (tx, ty),
        (0.0, 0.0),
        (0.0, ty),
        (tx, 0.0),
        (tx, ty),
    )
    indices = (
        (bnw, bsw, bse), (bse, bne, bnw), # bottom
        (bne, tne, tnw), (tnw, bnw, bne), # north
        (bsw, tsw, tse), (tse, bse, bsw), # south
        (bse, tse, tne), (tne, bne, bse), # east
        (bnw, tnw, tsw), (tsw, bsw, bnw), # west
    )
    return positions, indices_top, indices, tex_coords_top, normals

def hex_rgba_float(hexcode):
    channel = lambda c: int(c, 16) / 255
    hexcode = hexcode.replace('#', '').ljust(8, 'f')
    return [
        channel(hexcode[0:2]),
        channel(hexcode[2:4]),
        channel(hexcode[4:6]),
        channel(hexcode[6:8]),
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-x', type=float)
    parser.add_argument('-y', type=float)
    parser.add_argument('-z', type=float)
    parser.add_argument('--tx', type=float, default=1.0)
    parser.add_argument('--ty', type=float, default=1.0)
    parser.add_argument('--image', '-i')
    parser.add_argument('--output', '-o')
    parser.add_argument('--glb', '-b', action="store_true")
    parser.add_argument('--name', '-n', default="board")
    parser.add_argument('--background', '-c', default="#4D2A24")
    args = parser.parse_args()

    materials = [
        {
            "name": args.name + ".top",
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0},
                "baseColorFactor": [ 1.0, 1.0, 1.0, 1.0 ],
                "metallicFactor": 0.0,
                "roughnessFactor": 0.3
            }
        },
        {
            "name": args.name + ".bottom",
            "pbrMetallicRoughness": {
                "baseColorFactor": hex_rgba_float(args.background),
                "metallicFactor": 0.0,
                "roughnessFactor": 0.8
            }
        }
    ]
    
    vertices, indices_top, indices, tex_coords_top, normals = generate_geometry(
        args.x, args.y, args.z,
        args.tx, args.ty
    )
    texture_buffer, texture_mime = texture_from_image(args.image)
    gltf = gltf_from_verts_indices(
        vertices,
        indices_top, indices,
        normals,
        tex_coords_top, texture_buffer, texture_mime, materials
    )
    if args.glb:
        glb = glb_from_buf_gltf(*gltf)
        with open(args.output, "wb") as f:
            f.write(glb)
    else:
        gltf = gltf_from_buf_gltf(*gltf)
        with open(args.output, "w") as f:
            f.write(gltf)

if __name__ == '__main__':
    main()
