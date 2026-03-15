# ============================================================
# 04_convert_materials.py
# XPS 材质 → MMD 材质转换
# XPS 使用: albedo + normal + spec + mga
# MMD 使用: albedo + lmap + toon
# ============================================================
import bpy

# XPS材质 → 贴图映射表
MATERIAL_MAP = {
    '24_Object003_1_16_16':        {'albedo': 'pc_a08_hd_body1_rgbx_albedo.png',  'lmap': 'pc_a08_hd_body1_rgbx_lmap.png'},
    '24_Object006_0.25_16_16':     {'albedo': 'pc_a_nk_face_rgbx_albedo.png',     'lmap': 'pc_a_nk_face_rgbx_lmap.png'},
    '24_Object007_1_16_16':        {'albedo': 'pc_common_tooth_rgbx_albedo.png',  'lmap': 'pc_common_tooth_rgbx_lmap.png'},
    '24_Object008_1_16_16':        {'albedo': 'pc_a_ld_eyes_rgbx_albedo.png',     'lmap': 'lmap.png'},
    '25_+armor.Object004_1_16_16': {'albedo': 'pc_a08_hd_body2_rgbx_albedo.png',  'lmap': 'pc_a08_hd_body2_rgbx_lmap.png'},
    '25_Object005_0.25_16_16':     {'albedo': 'pc_a_nk_hair_rgbx_albedo.png',     'lmap': 'lmap.png'},
    '7_Object009_0.1_16_16':       {'albedo': 'pc_a_nk_eyebrow_rgbx_albedo.png',  'lmap': None},
    '24_+sword.Object001_1_16_16': {'albedo': 'wp_a08_rgbx_albedo.png',            'lmap': 'wp_a08_rgbx_mga.png'},
    '24_+sword.Object002_1_16_16': {'albedo': 'wp_a08_rgbx_albedo.png',            'lmap': 'wp_a08_rgbx_mga.png'},
}

def build_mmd_material(mat, albedo_name, lmap_name):
    """重建材质节点为 MMD 风格: Albedo + Toon + LightMap"""
    toon_img = bpy.data.images.get('toon01.bmp')

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # 输出
    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (600, 0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Specular'].default_value = 0.0
    bsdf.inputs['Roughness'].default_value = 0.9
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    # Albedo 贴图 → Base Color
    albedo_img = bpy.data.images.get(albedo_name)
    if albedo_img:
        n = nodes.new('ShaderNodeTexImage')
        n.location = (-200, 100)
        n.image = albedo_img
        n.label = 'Albedo'
        links.new(n.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(n.outputs['Alpha'], bsdf.inputs['Alpha'])
        mat.blend_method = 'CLIP'

    # Toon 贴图（仅展示，mmd_tools导出时识别）
    if toon_img:
        n = nodes.new('ShaderNodeTexImage')
        n.location = (-200, -150)
        n.image = toon_img
        n.label = 'Toon'

    # LightMap 贴图（仅展示）
    if lmap_name:
        lmap_img = bpy.data.images.get(lmap_name)
        if lmap_img:
            n = nodes.new('ShaderNodeTexImage')
            n.location = (-200, -350)
            n.image = lmap_img
            n.label = 'LightMap'

    print(f"  ✅ {mat.name}")

def convert_materials():
    print("=== 开始材质转换 ===")
    for mat_name, textures in MATERIAL_MAP.items():
        mat = bpy.data.materials.get(mat_name)
        if mat:
            build_mmd_material(mat, textures['albedo'], textures.get('lmap'))
        else:
            print(f"  ⚠️  找不到材质: {mat_name}")
    print("\n✅ 材质转换完成！")

convert_materials()
