# ============================================================
# run_all.py  —  XPS → MMD 一键转换
# 用法：在 Blender 脚本编辑器中打开并运行
# 前提：XPS 骨骼对象名为 'Armature'，场景中有 toon01.bmp
# ============================================================
import bpy, math, time

XPS_ARMATURE = 'Armature'
def log(msg): print(f"[{time.strftime('%H:%M:%S')}] {msg}")

# ---- Step 1: 骨骼重命名 ------------------------------------
def step1_rename_bones():
    log(">>> Step 1: 骨骼重命名 XPS → MMD")
    XPS_TO_MMD = {
        'root ground':'全ての親','root hips':'センター',
        'spine lower':'下半身','spine middle':'上半身','spine upper':'上半身2',
        'head neck lower':'首','head neck upper':'頭',
        'head eyeball left':'目.L','head eyeball right':'目.R',
        'head jaw':'Jaw Bone','head tongue 1':'Tongue 1','head tongue 2':'Tongue 2','head tongue 3':'Tongue 3',
        'head lip upper middle':'QQ9','head lip upper left':'QQ9.001',
        'head lip lower middle':'QQ15','head lip lower left':'QQ14','head lip lower right':'QQ14.001',
        'head mouth corner left':'QQ11','head mouth corner right':'QQ11.001',
        'head eyebrow left root':'QQ1','head eyebrow left 1':'QQ2','head eyebrow left 2':'QQ3','head eyebrow left 3':'QQ4',
        'head eyebrow right root':'QQ1.001','head eyebrow right 1':'QQ2.001','head eyebrow right 2':'QQ3.001','head eyebrow right 3':'QQ4.001',
        'head eyelid upper left':'QQ7','head eyelid lower left':'QQ8',
        'head eyelid upper right':'QQ7.001','head eyelid lower right':'QQ8.001',
        'head cheek left 1':'QQ6','head cheek left 2':'QQ5','head cheek right 1':'QQ6.001','head cheek right 2':'QQ5.001',
        'leg left thigh':'足.L','leg left knee':'ひざ.L','leg left ankle':'足首.L','leg left toes':'つま先.L',
        'leg right thigh':'足.R','leg right knee':'ひざ.R','leg right ankle':'足首.R','leg right toes':'つま先.R',
        'arm left shoulder 1':'肩.L','arm left shoulder 2':'腕.L','arm left elbow':'ひじ.L','arm left wrist':'手首.L',
        'arm left finger 1a':'親指０.L','arm left finger 1b':'親指１.L','arm left finger 1c':'親指２.L',
        'arm left finger 2a':'人指１.L','arm left finger 2b':'人指２.L','arm left finger 2c':'人指３.L',
        'arm left finger 3a':'中指１.L','arm left finger 3b':'中指２.L','arm left finger 3c':'中指３.L',
        'arm left finger 4a':'薬指１.L','arm left finger 4b':'薬指２.L','arm left finger 4c':'薬指３.L',
        'arm left finger 5a':'小指１.L','arm left finger 5b':'小指２.L','arm left finger 5c':'小指３.L',
        'arm right shoulder 1':'肩.R','arm right shoulder 2':'腕.R','arm right elbow':'ひじ.R','arm right wrist':'手首.R',
        'arm right finger 1a':'親指０.R','arm right finger 1b':'親指１.R','arm right finger 1c':'親指２.R',
        'arm right finger 2a':'人指１.R','arm right finger 2b':'人指２.R','arm right finger 2c':'人指３.R',
        'arm right finger 3a':'中指１.R','arm right finger 3b':'中指２.R','arm right finger 3c':'中指３.R',
        'arm right finger 4a':'薬指１.R','arm right finger 4b':'薬指２.R','arm right finger 4c':'薬指３.R',
        'arm right finger 5a':'小指１.R','arm right finger 5b':'小指２.R','arm right finger 5c':'小指３.R',
        'boob left 1':'乳奶1.L','boob left 2':'乳奶2.L','boob right 1':'乳奶1.R','boob right 2':'乳奶2.R',
        'skirt left 01':'スカート_0_0','skirt left 02':'スカート_1_0','skirt left 03':'スカート_2_0',
        'skirt left 04':'スカート_3_0','skirt left 05':'スカート_4_0','skirt left 06':'スカート_5_0','skirt left 07':'スカート_6_0',
        'skirt front left 01':'スカート_0_1','skirt front left 02':'スカート_1_1','skirt front left 03':'スカート_2_1','skirt front left 04':'スカート_3_1',
        'skirt back left 01':'スカート_0_2','skirt back left 02':'スカート_1_2','skirt back left 03':'スカート_2_2','skirt back left 04':'スカート_3_2',
        'skirt right 01':'スカート_0_4','skirt right 02':'スカート_1_4','skirt right 03':'スカート_2_4',
        'skirt right 04':'スカート_3_4','skirt right 05':'スカート_4_4','skirt right 06':'スカート_5_4','skirt right 07':'スカート_6_4',
        'skirt front right 01':'スカート_0_5','skirt front right 02':'スカート_1_5','skirt front right 03':'スカート_2_5','skirt front right 04':'スカート_3_5',
        'skirt back right 01':'スカート_0_6','skirt back right 02':'スカート_1_6','skirt back right 03':'スカート_2_6','skirt back right 04':'スカート_3_6',
        'skirt back middle left 1':'スカート_0_3','skirt back middle left 2':'スカート_1_3',
        'skirt back middle right 1':'スカート_0_7','skirt back middle right 2':'スカート_1_7',
    }
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    renamed = sum(1 for b in arm.data.edit_bones if b.name in XPS_TO_MMD and setattr(b, 'name', XPS_TO_MMD[b.name]) is None)
    bpy.ops.object.mode_set(mode='OBJECT')
    log(f"✅ 完成: {renamed} 根骨骼重命名")

# ---- Step 2: 顶点组同步 ------------------------------------
def step2_sync_vgroups():
    log(">>> Step 2: 顶点组同步")
    def copy(obj, src, dst):
        if not obj.vertex_groups.get(src): return
        if not obj.vertex_groups.get(dst): obj.vertex_groups.new(name=dst)
        s, d = obj.vertex_groups[src], obj.vertex_groups[dst]
        for v in obj.data.vertices:
            try: d.add([v.index], s.weight(v.index), 'REPLACE')
            except: pass
    meshes = [o for o in bpy.data.objects if o.type=='MESH' and o.find_armature() and o.find_armature().name==XPS_ARMATURE]
    fixed = 0
    for obj in meshes:
        vg = {v.name for v in obj.vertex_groups}
        for src, dst in [('足.L','ひざ.L'),('足.R','ひざ.R'),('腕.L','ひじ.L'),('腕.R','ひじ.R'),('首','頭')]:
            if src in vg and dst not in vg: copy(obj, src, dst); fixed += 1
    log(f"✅ 完成: 补全 {fixed} 个顶点组")


# ---- Step 3b: T-Pose → A-Pose ----------------------------------
def step3b_tpose_to_apose():
    log(">>> Step 3b: T-Pose → A-Pose（手臂下倾45°）")
    A = math.radians(45)
    arm = bpy.data.objects.get(XPS_ARMATURE)

    # Step 1: Pose Mode 设置旋转
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.rot_clear(); bpy.ops.pose.loc_clear()
    for side, sign in [('L', -1), ('R', 1)]:
        pb = arm.pose.bones.get(f'肩.{side}')
        if pb:
            pb.rotation_mode = 'XYZ'
            pb.rotation_euler[0] = sign * A
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode='OBJECT')

    # Step 2: 对每个网格 Apply Armature Modifier + 重新绑定
    meshes = [o for o in bpy.data.objects
              if o.type == 'MESH' and o.find_armature()
              and o.find_armature().name == XPS_ARMATURE]
    for obj in meshes:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        arm_mod = next((m for m in obj.modifiers if m.type == 'ARMATURE'), None)
        if arm_mod:
            bpy.ops.object.modifier_apply(modifier=arm_mod.name)
        new_mod = obj.modifiers.new(name='Armature', type='ARMATURE')
        new_mod.object = arm

    # Step 3: Apply Pose as Rest Pose
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    dz = arm.data.bones['肩.L'].head_local.z - arm.data.bones['手首.L'].head_local.z
    log(f"✅ 完成: 手臂下倾 {dz:.3f} {'✅' if dz > 0.1 else '❌'} 网格+骨骼已烘焙")

# ---- Step 3: T-Pose → I-Pose --------------------------------
def step3b_tpose_to_apose()
step3_apose_to_ipose():
    log(">>> Step 3: 手臂姿态修正")
    A = math.radians(25)
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.rot_clear(); bpy.ops.pose.loc_clear()
    for side, sign in [('L',-1),('R',1)]:
        for bname, angle in [(f'腕.{side}', sign*A), (f'ひじ.{side}', -sign*A)]:
            pb = arm.pose.bones.get(bname)
            if pb: pb.rotation_mode='XYZ'; pb.rotation_euler[2]=angle
    bpy.context.view_layer.update()
    bpy.ops.pose.select_all(action='SELECT')
    bpy.ops.pose.armature_apply(selected=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    log("✅ 完成: 手臂下倾 25°，已 Apply as Rest Pose")

# ---- Step 4: 材质转换 ----------------------------------------
def step4_convert_materials():
    log(">>> Step 4: 材质转换")
    MAT = {
        '24_Object003_1_16_16':        ('pc_a08_hd_body1_rgbx_albedo.png',  'pc_a08_hd_body1_rgbx_lmap.png'),
        '24_Object006_0.25_16_16':     ('pc_a_nk_face_rgbx_albedo.png',     'pc_a_nk_face_rgbx_lmap.png'),
        '24_Object007_1_16_16':        ('pc_common_tooth_rgbx_albedo.png',  'pc_common_tooth_rgbx_lmap.png'),
        '24_Object008_1_16_16':        ('pc_a_ld_eyes_rgbx_albedo.png',     'lmap.png'),
        '25_+armor.Object004_1_16_16': ('pc_a08_hd_body2_rgbx_albedo.png',  'pc_a08_hd_body2_rgbx_lmap.png'),
        '25_Object005_0.25_16_16':     ('pc_a_nk_hair_rgbx_albedo.png',     'lmap.png'),
        '7_Object009_0.1_16_16':       ('pc_a_nk_eyebrow_rgbx_albedo.png',  None),
        '24_+sword.Object001_1_16_16': ('wp_a08_rgbx_albedo.png',            'wp_a08_rgbx_mga.png'),
        '24_+sword.Object002_1_16_16': ('wp_a08_rgbx_albedo.png',            'wp_a08_rgbx_mga.png'),
    }
    toon = bpy.data.images.get('toon01.bmp')
    def build(mat, albedo, lmap):
        mat.use_nodes = True
        ns, ls = mat.node_tree.nodes, mat.node_tree.links
        ns.clear()
        out  = ns.new('ShaderNodeOutputMaterial'); out.location  = (600,0)
        bsdf = ns.new('ShaderNodeBsdfPrincipled'); bsdf.location = (300,0)
        bsdf.inputs['Specular'].default_value=0; bsdf.inputs['Roughness'].default_value=0.9
        ls.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        ai = bpy.data.images.get(albedo)
        if ai:
            n=ns.new('ShaderNodeTexImage'); n.location=(-200,100); n.image=ai; n.label='Albedo'
            ls.new(n.outputs['Color'],bsdf.inputs['Base Color']); ls.new(n.outputs['Alpha'],bsdf.inputs['Alpha'])
            mat.blend_method='CLIP'
        if toon:
            n=ns.new('ShaderNodeTexImage'); n.location=(-200,-150); n.image=toon; n.label='Toon'
        if lmap:
            li=bpy.data.images.get(lmap)
            if li:
                n=ns.new('ShaderNodeTexImage'); n.location=(-200,-350); n.image=li; n.label='LightMap'
    cnt = 0
    for mname,(albedo,lmap) in MAT.items():
        mat=bpy.data.materials.get(mname)
        if mat: build(mat,albedo,lmap); cnt+=1
    log(f"✅ 完成: {cnt} 个材质转换")

# ---- 验证 ---------------------------------------------------
def verify():
    log(">>> 验证")
    arm = bpy.data.objects.get(XPS_ARMATURE)
    bones = {b.name for b in arm.data.bones}
    core = ['全ての親','センター','下半身','上半身','上半身2','首','頭',
            '目.L','目.R','足.L','ひざ.L','足首.L','つま先.L',
            '足.R','ひざ.R','足首.R','つま先.R',
            '肩.L','腕.L','ひじ.L','手首.L','肩.R','腕.R','ひじ.R','手首.R']
    missing = [b for b in core if b not in bones]
    log(f"  骨骼: {'✅ 全部通过' if not missing else '❌ 缺少: '+str(missing)}")

# ---- 主流程 -------------------------------------------------
t = time.time()
log("=" * 44)
log("  XPS → MMD 转换开始")
log("=" * 44)
step1_rename_bones()
step2_sync_vgroups()
step3b_tpose_to_apose()
step3_apose_to_ipose()
step4_convert_materials()
verify()
log("=" * 44)
log(f"  完成！耗时 {time.time()-t:.1f}s  下一步：mmd_tools 导出 PMX")
log("=" * 44)
