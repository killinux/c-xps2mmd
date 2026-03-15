# ============================================================
# 01_rename_bones.py  —  XPS 骨骼重命名 → MMD 日文名
# ============================================================
import bpy

XPS_TO_MMD = {
    'root ground':'全ての親','root hips':'センター',
    'spine lower':'下半身','spine middle':'上半身','spine upper':'上半身2',
    'head neck lower':'首','head neck upper':'頭',
    'head eyeball left':'目.L','head eyeball right':'目.R',
    'head jaw':'Jaw Bone','head tongue 1':'Tongue 1',
    'head tongue 2':'Tongue 2','head tongue 3':'Tongue 3',
    'head lip upper middle':'QQ9','head lip upper left':'QQ9.001','head lip upper right':'QQ9.002',
    'head lip lower middle':'QQ15','head lip lower left':'QQ14','head lip lower right':'QQ14.001',
    'head mouth corner left':'QQ11','head mouth corner right':'QQ11.001',
    'head eyebrow left root':'QQ1','head eyebrow left 1':'QQ2','head eyebrow left 2':'QQ3','head eyebrow left 3':'QQ4',
    'head eyebrow right root':'QQ1.001','head eyebrow right 1':'QQ2.001','head eyebrow right 2':'QQ3.001','head eyebrow right 3':'QQ4.001',
    'head eyelid upper left':'QQ7','head eyelid lower left':'QQ8',
    'head eyelid upper right':'QQ7.001','head eyelid lower right':'QQ8.001',
    'head cheek left 1':'QQ6','head cheek left 2':'QQ5',
    'head cheek right 1':'QQ6.001','head cheek right 2':'QQ5.001',
    'head nose nostril left':'QQ10','head nose nostril right':'QQ10.001',
    'head boob left 1':'乳奶1.L','head boob left 2':'乳奶2.L',
    'head boob right 1':'乳奶1.R','head boob right 2':'乳奶2.R',
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
}

CORE = ['全ての親','センター','下半身','上半身','上半身2','首','頭',
        '目.L','目.R','足.L','ひざ.L','足首.L','つま先.L',
        '足.R','ひざ.R','足首.R','つま先.R',
        '肩.L','腕.L','ひじ.L','手首.L','肩.R','腕.R','ひじ.R','手首.R']

def rename_bones(armature_name='Armature'):
    arm = bpy.data.objects.get(armature_name)
    if not arm:
        print(f"[错误] 找不到骨骼: {armature_name}")
        return
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    renamed = 0
    for bone in arm.data.edit_bones:
        if bone.name in XPS_TO_MMD:
            bone.name = XPS_TO_MMD[bone.name]
            renamed += 1
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"✅ 重命名: {renamed} 根")
    # 验证
    bones = {b.name for b in arm.data.bones}
    missing = [b for b in CORE if b not in bones]
    if missing:
        print(f"❌ 缺少: {missing}")
    else:
        print(f"✅ 核心骨骼全部验证通过")

rename_bones('Armature')
