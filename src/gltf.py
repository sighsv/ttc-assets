import struct
import json
import base64
import io
import os
import enum


class ComponentType(enum.IntEnum):
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126


class Target(enum.IntEnum):
    ARRAY_BUFFER = 34962
    ELEMENT_ARRAY_BUFFER = 34963


def data_to_base64_uri(data):
    encoded = base64.b64encode(data).decode('ascii')
    return 'data:application/octet-stream;base64,' + encoded


def nonnumeric_empty(e):
    return not (
        e is None
        or (isinstance(e, list) and not e)
        or (isinstance(e, dict) and not e)
    )


def recursive_filter(o, f=nonnumeric_empty):
    if isinstance(o, list):
        o = [
            e for e in
            [recursive_filter(i, f) for i in o]
            if e is not None
        ]
    if isinstance(o, dict):
        o = {
            a: b for a, b in
            [(k, recursive_filter(v, f)) for k, v in o.items()]
            if b is not None
        }
    if not f(o):
        return None
    return o


class Type:
    boundary = 1
    target = None
    component_type = None
    struct_type = None
    access_type = None

    @classmethod
    def encode(cls, data):
        if cls.struct_type:
            if len(cls.struct_type) == 1:
                data = [(v,) for v in data]
            return b''.join(struct.pack('<' + cls.struct_type, *p) for p in data)
        return data

    @classmethod
    def decode(cls, data):
        if cls.struct_type:
            unpacked = list(struct.iter_unpack('<' + cls.struct_type, data))
            if len(cls.struct_type) == 1:
                unpacked = [v[0] for v in unpacked]
            return unpacked
        return data

    @classmethod
    def minmax(cls, data):
        decoded = cls.decode(data)
        return [min(decoded)], [max(decoded)]

    @classmethod
    def count(cls, size):
        if type(size) is not int:
            size = len(size)
        if not cls.struct_type:
            return 1
        mod = struct.calcsize(cls.struct_type)
        assert size % mod == 0
        return size // mod


class Image(Type):
    boundary = 1
    target = None
    component_type = ComponentType.UNSIGNED_BYTE
    struct_type = None
    access_type = None


class Byte(Type):
    boundary = 1
    target = Target.ELEMENT_ARRAY_BUFFER
    component_type = ComponentType.UNSIGNED_BYTE
    struct_type = 'h'
    access_type = 'SCALAR'


class Short(Byte):
    boundary = 2
    component_type = ComponentType.UNSIGNED_SHORT
    struct_type = 'h'


class Vec2(Type):
    boundary = 4
    target = Target.ARRAY_BUFFER
    component_type = ComponentType.FLOAT
    struct_type = 'ff'
    access_type = 'VEC2'

    @classmethod
    def minmax(cls, data):
        decoded = cls.decode(data)
        channel_count = len(decoded[0])
        channels = [[d[i] for d in decoded] for i in range(channel_count)]
        return (
            [min(c) for c in channels],
            [max(c) for c in channels],
        )


class Vec3(Vec2):
    struct_type = 'fff'
    access_type = 'VEC3'


class Vec4(Vec2):
    struct_type = 'ffff'
    access_type = 'VEC4'


class BufferView:
    def __init__(self,
            gltf, index,
            buffer_idx, buffer_obj,
            start, end,
            dtype=None):
        self.gltf = gltf
        self.index = index
        self.buffer_idx = buffer_idx
        self.buffer = buffer_obj
        self.start = start
        self.end = end
        self.dtype = dtype

    def get_data(self):
        buf = self.gltf.buffers[self.buffer_idx]
        buf.seek(self.start)
        data = buf.read(len(self))
        buf.seek(0, os.SEEK_END)
        return data

    def __len__(self):
        return self.end - self.start

    def serialize(self):
        view = {
            'buffer': self.buffer_idx,
            'byteOffset': self.start,
            'byteLength': len(self),
        }
        if self.dtype.target:
            view['target'] = self.dtype.target
        return view


class Accessor:
    def __init__(self, gltf, index, buffer_view, dtype, start, mn, mx):
        self.gltf = gltf
        self.index = index
        self.buffer_view = buffer_view
        self.dtype = dtype
        self.start = start
        self.min = mn
        self.max = mx

    def serialize(self):
        return {
            "bufferView": self.buffer_view.index,
            "byteOffset": self.start,
            "componentType": self.dtype.component_type,
            "count": self.dtype.count(self.buffer_view),
            "type": self.dtype.access_type,
            "max": self.max,
            "min": self.min,
        }


class Filter(enum.IntEnum):
    NEAREST = 9728
    LINEAR = 9729
    NEAREST_MIPMAP_NEAREST = 9984
    LINEAR_MIPMAP_NEAREST = 9985
    NEAREST_MIPMAP_LINEAR = 9986
    LINEAR_MIPMAP_LINEAR = 9987


class Wrapping(enum.IntEnum):
    CLAMP_TO_EDGE = 33071
    MIRRORED_REPEAT = 33648
    REPEAT = 10497


class Sampler:
    def __init__(self,
            gltf, index,
            mag_filter=Filter.LINEAR, min_filter=Filter.LINEAR_MIPMAP_LINEAR,
            wrap_s=Wrapping.MIRRORED_REPEAT, wrap_t=Wrapping.MIRRORED_REPEAT):
        self.gltf = gltf
        self.index = index
        self.mag_filter = mag_filter
        self.min_filter = min_filter
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t

    def serialize(self):
        return {
            'magFilter': self.mag_filter,
            'minFilter': self.min_filter,
            'wrapS': self.wrap_s,
            'wrapT': self.wrap_t,
        }


class BufferImage:
    def __init__(self, gltf, index, buffer_view, mimetype):
        self.gltf = gltf
        self.index = index
        self.buffer_view = buffer_view
        self.mimetype = mimetype

    def serialize(self):
        return {
            "mimeType": self.mimetype,
            "bufferView": self.buffer_view.index,
        }


class Texture:
    def __init__(self, gltf, index, image, sampler):
        self.gltf = gltf,
        self.index = index
        self.image = image
        self.sampler = sampler

    def serialize(self):
        return {
            'source': self.image.index,
            'sampler': self.sampler.index,
        }


class TextureReference:
    def __init__(self, gltf, texture,
            tex_coord=None, strength=None, scale=None):
        self.gltf = gltf,
        if isinstance(texture, TextureReference):
            tex_coord = texture.tex_coord
            strength = texture.strength
            scale = texture.scale
            texture = texture.texture
        self.texture = texture
        self.tex_coord = tex_coord
        self.strength = strength
        self.scale = scale

    def serialize(self):
        return recursive_filter({
            'index': self.texture.index,
            'texCoord': self.tex_coord,
            'strength': self.strength,
            'scale': self.scale,
        })


class PBRMaterial:
    def __init__(self, gltf, index, name=None,
            color=None, metallic=None, roughness=None, metallic_roughness=None,
            emissive=None, normal_map=None, occlusion_map=None,
            alpha_mode=None, alpha_cutoff=None):
        self.gltf = gltf
        self.index = index
        self.name = name
        self.color = color
        self.metallic = metallic
        self.roughness = roughness
        self.metallic_roughness = metallic_roughness
        self.emissive = emissive
        self.normal_map = normal_map
        self.occlusion_map = occlusion_map
        self.alpha_mode = alpha_mode
        self.alpha_cutoff = alpha_cutoff

    def serialize(self):
        tname = lambda n, v: n + (
            'Texture' if isinstance(v, Texture) else 'Factor'
        )
        def tval(v):
            if isinstance(v, Texture) or isinstance(v, TextureReference):
                return TextureReference(self.gltf, v).serialize()
            if isinstance(v, Color):
                return v.serialize()
            return v
        return recursive_filter({
            'name': self.name,
            'alphaMode': self.alpha_mode,
            'alphaCutoff': self.alpha_cutoff,
            'pbrMetallicRoughness': {
                tname('baseColor', self.color): tval(self.color),
                'metallicFactor': self.metallic,
                'roughnessFactor': self.roughness,
                # G = roughness
                # B = metallic
                # ignore R and A
                'metallicRoughnessTexture': tval(self.metallic_roughness),
            },
            'normalTexture': tval(self.normal_map),
            'occlusionTexture': tval(self.occlusion_map),
            tname('emissive', self.emissive): tval(self.emissive),
        })


class Primitive:
    def __init__(self, gltf,
            vertices=None,
            indices=None,
            normals=None,
            tex_coords=None,
            tangents=None,
            material=None):
        self.gltf = gltf
        self.vertices = vertices
        self.indices = indices
        self.normals = normals
        self.tex_coords = tex_coords
        self.tangents = tangents
        self.material = material

    def serialize(self):
        return recursive_filter({
            'attributes': {
                'POSITION': getattr(self.vertices, 'index', None),
                'NORMAL': getattr(self.normals, 'index', None),
                'TEXCOORD_0': getattr(self.tex_coords, 'index', None),
                'TANGENT': getattr(self.tangents, 'index', None),
            },
            'indices': getattr(self.indices, 'index', None),
            'material': getattr(self.material, 'index', None),
        })


class Mesh:
    def __init__(self, gltf, index, primitives):
        self.gltf = gltf
        self.index = index
        self.primitives = primitives

    def serialize(self):
        return {
            "primitives": [p.serialize() for p in self.primitives]
        }


class Node:
    def __init__(self, gltf, index, mesh):
        self.gltf = gltf
        self.index = index
        self.mesh = mesh

    def serialize(self):
        return {
            "mesh": self.mesh.index
        }


class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        if type(r) is str:
            r, g, b, a = self.hex_decode(r)
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def hex_decode(self, hexcode):
        channel = lambda c: int(c, 16) / 255
        hexcode = hexcode.replace('#', '').ljust(8, 'f')
        return (
            channel(hexcode[0:2]),
            channel(hexcode[2:4]),
            channel(hexcode[4:6]),
            channel(hexcode[6:8]),
        )

    def serialize(self):
        return [self.r, self.g, self.b, self.a]


class GLTF:
    def __init__(self, scene=0, generator="gltf.py"):
        self.buffers = []
        self.buffer_views = []
        self.accessors = []
        self.images = []
        self.samplers = []
        self.materials = []
        self.textures = []
        self.meshes = []
        self.nodes = []
        self.scene = scene
        self.generator = generator

    def buffer_view(self, buffer_idx, start, end, dtype):
        view = BufferView(
            self,
            len(self.buffer_views),
            buffer_idx,
            self.buffers[buffer_idx],
            start,
            end,
            dtype
        )
        self.buffer_views.append(view)
        return view

    def embed_data(self, data, dtype=Byte, padding=b'\0'):
        if not self.buffers:
            self.buffers.append(io.BytesIO())
        buf = self.buffers[-1]
        start = buf.tell()
        pad = -start % dtype.boundary
        start += pad
        buf.write(padding * pad)
        buf.write(dtype.encode(data))
        return self.buffer_view(
            len(self.buffers) - 1,
            start, buf.tell(),
            dtype
        )

    def default_sampler(self):
        if len(self.samplers) == 0:
            self.samplers.append(Sampler(self, 0))
        return self.samplers[0]

    def add_texture(self, image, mimetype, sampler=None):
        image = BufferImage(
            self, len(self.images),
            self.embed_data(image, dtype=Image), mimetype
        )
        self.images.append(image)
        sampler = sampler or self.default_sampler()
        texture = Texture(self, len(self.textures), image, sampler)
        self.textures.append(texture)
        return texture

    def pbr_material(self, **kwargs):
        material = PBRMaterial(
            self, len(self.materials), **kwargs
        )
        self.materials.append(material)
        return material

    def accessor(self, buffer_view, dtype=None):
        data = buffer_view.get_data()
        dtype = dtype or buffer_view.dtype
        mn, mx = dtype.minmax(data)
        accessor = Accessor(
            self,
            len(self.accessors),
            buffer_view,
            dtype,
            0,
            mn, mx
        )
        self.accessors.append(accessor)
        return accessor

    def add_vertices(self, vertices):
        return self.accessor(self.embed_data(vertices, dtype=Vec3))

    def add_tex_coords(self, coords):
        return self.accessor(self.embed_data(coords, dtype=Vec2))

    def add_normals(self, normals):
        return self.accessor(self.embed_data(normals, dtype=Vec3))

    def add_indices(self, indices):
        return self.accessor(self.embed_data(indices, dtype=Short))

    def add_tangents(self, tangents):
        return self.accessor(self.embed_data(tangents, dtype=Vec4))

    def primitive(self, **kwargs):
        return Primitive(self, **kwargs)

    def mesh(self, primitives):
        mesh = Mesh(self, len(self.meshes), primitives)
        self.meshes.append(mesh)
        return mesh

    def node(self, mesh):
        node = Node(self, len(self.nodes), mesh)
        self.nodes.append(node)
        return node

    def serialize(self):
        dmap = lambda iterable: [i.serialize() for i in iterable]
        return recursive_filter({
            'scene': self.scene,
            'scenes': self.scenes,
            'nodes': dmap(self.nodes),
            'meshes':  dmap(self.meshes),
            'materials': dmap(self.materials),
            'images': dmap(self.images),
            'samplers': dmap(self.samplers),
            'textures': dmap(self.textures),
            'bufferViews': dmap(self.buffer_views),
            'accessors': dmap(self.accessors),
            'asset': {
                'version': '2.0',
                'generator': self.generator,
            },
        })

    def dump_base64_gltf(self):
        obj = self.serialize()
        obj['buffers'] = [
            {
                "uri": data_to_base64_uri(b),
                "byteLength": len(b),
            }
            for b in self.buffers
        ]
        return json.dumps(obj)

    def dump_glb(self):
        MAGIC_GLTF = 0x46546C67
        CHUNK_JSON = 0x4E4F534A
        CHUNK_BIN = 0x004E4942
        assert len(self.buffers) == 1
        # read out BytesIO
        buf = self.buffers[0]
        buf.seek(0)
        buf = buf.read()
        # fill in GLB buffer specification
        obj = self.serialize()
        obj['buffers'] = [
            {
                "byteLength": len(buf)
            }
        ]
        jdata = json.dumps(
            obj,
            indent=0,
            separators=(',', ':')
        ).encode('utf8')
        # pad to 4-byte boundary
        jdata += b' ' * (-len(jdata) % 4)
        buf += b'\0' * (-len(buf) % 4)
        # pack together GLB
        header = struct.pack('<III', MAGIC_GLTF, 2,
            12 # header
            + 8 + len(jdata)
            + 8 + len(buf)
        )
        json_chunk = struct.pack('<II', len(jdata), CHUNK_JSON) + jdata
        bin_chunk = struct.pack('<II', len(buf), CHUNK_BIN) + buf
        return header + json_chunk + bin_chunk
