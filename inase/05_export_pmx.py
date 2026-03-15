# ============================================================
# 05_export_pmx.py
# 用 mmd_tools 导出 PMX 文件
# 前提：已运行 run_all.py 完成骨骼/顶点组/姿态/材质转换
# ============================================================
import bpy, os, shutil

MODEL_NAME  = 'XPS_Model'   # ROOT 对象名（可修改）
OUTPUT_DIR  = os.path.expanduser('~/Downloads/mywork/xps2mmd_work/output')
TOON_PATH   = '/Users/bytedance/Downloads/blender_mmd_tools-4.5.9/mmd_tools/externals/MikuMikuDance/toon01.bmp'

def setup_hierarchy():
    """建立 mmd_tools 需要的层级: ROOT → Armature → Meshes"""
    # 创建或获取 ROOT
    root = bpy.data.objects.get(MODEL_NAME)
    if not root:
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
        root = bpy.context.active_object
        root.name = MODEL_NAME
    root.mmd_type = 'ROOT'
    root.mmd_root.name   = MODEL_NAME
    root.mmd_root.name_e = MODEL_NAME

    arm = bpy.data.objects.get('Armature')
    arm.parent = root

    meshes = [o for o in bpy.data.objects
              if o.type == 'MESH' and o.find_armature()
              and o.find_armature().name == 'Armature']
    for obj in meshes:
        obj.parent = arm

    print(f"✅ 层级建立完成: ROOT({root.name}) → Armature → {len(meshes)} 个网格")
    return root

def fix_texture_paths():
    """把相对贴图路径转为绝对路径，修复 toon01.bmp"""
    toon = bpy.data.images.get('toon01.bmp')
    if toon and os.path.exists(TOON_PATH):
        toon.filepath = TOON_PATH

    for img in bpy.data.images:
        if img.filepath and img.filepath.startswith('//'):
            abs_path = bpy.path.abspath(img.filepath)
            if os.path.exists(abs_path):
                img.filepath = abs_path
    print("✅ 贴图路径修复完成")

def export_pmx(root):
    """执行 PMX 导出"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f'{MODEL_NAME}.pmx')

    bpy.ops.object.select_all(action='DESELECT')
    root.select_set(True)
    bpy.context.view_layer.objects.active = root

    result = bpy.ops.mmd_tools.export_pmx(
        filepath      = output_path,
        scale         = 1.0,
        copy_textures = True,
        sort_materials= False,
        log_level     = 'DEBUG',
        save_log      = False,
    )

    size = os.path.getsize(output_path) / 1024
    print(f"✅ PMX 导出完成: {output_path}  ({size:.1f} KB)")
    return output_path

def copy_textures():
    """手动复制所有贴图到 textures/ 子目录"""
    tex_dir = os.path.join(OUTPUT_DIR, 'textures')
    os.makedirs(tex_dir, exist_ok=True)
    copied = 0
    for img in bpy.data.images:
        if not img.filepath: continue
        src = os.path.normpath(img.filepath)
        if not os.path.exists(src): continue
        dst = os.path.join(tex_dir, os.path.basename(src))
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            copied += 1
    print(f"✅ 贴图复制完成: {copied} 个文件 → {tex_dir}")

# 主流程
print("=== 开始导出 PMX ===")
fix_texture_paths()
root = setup_hierarchy()
export_pmx(root)
copy_textures()
print("\n✅ 全部完成！")
print(f"   PMX: {OUTPUT_DIR}/{MODEL_NAME}.pmx")
print(f"   贴图: {OUTPUT_DIR}/textures/")
