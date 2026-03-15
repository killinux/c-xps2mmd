# 01_rename_bones.py - XPS骨骼重命名
import bpy
XPS_TO_MMD = {
    'root ground': '全ての親', 'root hips': 'センター',
    'spine lower': '下半身', 'spine middle': '上半身', 'spine upper': '上半身2',
    'head neck lower': '首', 'head neck upper': '頭',
    'head eyeball left': '目.L', 'head eyeball right': '目.R',
    'head jaw': 'Jaw Bone', 'head tongue 1': 'Tongue 1', 'head tongue 2': 'Tongue 2', 'head tongue 3': 'Tongue 3',
    'head lip upper middle': 'QQ9', 'head lip upper left': 'QQ9.001',
    'head lip lower middle': 'QQ15', 'head lip lower left': 'QQ14', 'head lip lower right': 'QQ14.001',
    'head mouth corner left': 'QQ11', 'head mouth corner right': 'QQ11.001',
    'head eyebrow left root': 'QQ1', 'head eyebrow left 1': 'QQ2', 'head eyebrow left 2': 'QQ3', 'head eyebrow left 3': 'QQ4',
    'head eyebrow right root': 'QQ1.001', 'head eyebrow right 1': 'QQ2.001', 'head eyebrow right 2': 'QQ3.001', 'head eyebrow right 3': 'QQ4.001',
    'head eyelid upper left': 'QQ7', 'head eyelid lower left': 'QQ8',
    'head eyelid upper right': 'QQ7.001', 'head eyelid lower right': 'QQ8.001',
    'head cheek left 1': 'QQ6', 'head cheek left 2': 'QQ5', 'head cheek right 1': 'QQ6.001', 'head cheek right 2': 'QQ5.001',
    'leg left thigh': '足.L', 'leg left knee': 'ひざ.L', 'leg left ankle': '足首.L', 'leg left toes': 'つま先.L',
    'leg right thigh': '足.R', 'leg right knee': 'ひざ.R', 'leg right ankle': '足首.R', 'leg right toes': 'つま先.R',
    'arm left shoulder 1': '肩.L', 'arm left shoulder 2': '腕.L', 'arm left elbow': 'ひじ.L', 'arm left wrist': '手首.L',
    'arm left finger 1a': '親指０.L', 'arm left finger 1b': '親指１.L', 'arm left finger 1c': '親指２.L',
    'arm left finger 2a': '人指１.L', 'arm left finger 2b': '人指２.L', 'arm left finger 2c': '人指３.L',
    'arm left finger 3a': '中指１.L', 'arm left finger 3b': '中指２.L', 'arm left finger 3c': '中指３.L',
    'arm left finger 4a': '薬指１.L', 'arm left finger 4b': '薬指２.L', 'arm left finger 4c': '薬指３.L',
    'arm left finger 5a': '小指１.L', 'arm left finger 5b': '小指２.L', 'arm left finger 5c': '小指３.L',
    'arm right shoulder 1': '肩.R', 'arm right shoulder 2': '腕.R', 'arm right elbow': 'ひじ.R', 'arm right wrist': '手首.R',
    'arm right finger 1a': '親指０.R', 'arm right finger 1b': '親指１.R', 'arm right finger 1c': '親指２.R',
    'arm right finger 2a': '人指１.R', 'arm right finger 2b': '人指２.R', 'arm right finger 2c': '人指３.R',
    'arm right finger 3a': '中指１.R', 'arm right finger 3b': '中指２.R', 'arm right finger 3c': '中指３.R',
    'arm right finger 4a': '薬指１.R', 'arm right finger 4b': '薬指２.R', 'arm right finger 4c': '薬指３.R',
    'arm right finger 5a': '小指１.R', 'arm right finger 5b': '小指２.R', 'arm right finger 5c': '小指３.R',
    'boob left 1': '乳奶1.L', 'boob left 2': '乳奶2.L', 'boob right 1': '乳奶1.R', 'boob right 2': '乳奶2.R',
    'skirt left 01': 'スカート_0_0', 'skirt left 02': 'スカート_1_0', 'skirt left 03': 'スカート_2_0',
    'skirt left 04': 'スカート_3_0', 'skirt left 05': 'スカート_4_0', 'skirt left 06': 'スカート_5_0', 'skirt left 07': 'スカート_6_0',
    'skirt front left 01': 'スカート_0_1', 'skirt front left 02': 'スカート_1_1', 'skirt front left 03': 'スカート_2_1', 'skirt front left 04': 'スカート_3_1',
    'skirt back left 01': 'スカート_0_2', 'skirt back left 02': 'スカート_1_2', 'skirt back left 03': 'スカート_2_2', 'skirt back left 04': 'スカート_3_2',
    'skirt right 01': 'スカート_0_4', 'skirt right 02': 'スカート_1_4', 'skirt right 03': 'スカート_2_4',
    'skirt right 04': 'スカート_3_4', 'skirt right 05': 'スカート_4_4', 'skirt right 06': 'スカート_5_4', 'skirt right 07': 'スカート_6_4',
    'skirt front right 01': 'スカート_0_5', 'skirt front right 02': 'スカート_1_5', 'skirt front right 03': 'スカート_2_5', 'skirt front right 04': 'スカート_3_5',
    'skirt back right 01': 'スカート_0_6', 'skirt back right 02': 'スカート_1_6', 'skirt back right 03': 'スカート_2_6', 'skirt back right 04': 'スカート_3_6',
    'skirt back middle left 1': 'スカート_0_3', 'skirt back middle left 2': 'スカート_1_3',
    'skirt back middle right 1': 'スカート_0_7', 'skirt back middle right 2': 'スカート_1_7',
}
arm = bpy.data.objects.get('Armature')
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode='EDIT')
renamed = 0
for bone in arm.data.edit_bones:
    if bone.name in XPS_TO_MMD:
        bone.name = XPS_TO_MMD[bone.name]; renamed += 1
bpy.ops.object.mode_set(mode='OBJECT')
print(f"✅ 骨骼重命名完成: {renamed} 根")
