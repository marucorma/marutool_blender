#### 選択したオブジェクトの情報を取得しjsonで出力
# そのjsonを読み込み再度生成するスクリプト ####
# V2はメッシュ、UV、スムーズシェードの情報を取得し生成
## copyObject.py 
# 選択したオブジェクトのオブジェクトの頂点、辺、面の情報を取得しobj_info.json に出力するスクリプト
## pasteObject.py 
# JSONファイルを読み込み、オブジェクトを生成するスクリプト

import bpy
import json
import os

# JSONファイルのパスを指定
file_path = os.path.join(bpy.path.abspath("//CopyObjectData//"), "obj_info.json")

# ファイルが存在するか確認
if not os.path.exists(file_path):
    print(f"ファイル '{file_path}' が見つかりません。まずscriptA.pyを実行してください。")
else:
    # JSONファイルを読み込む
    with open(file_path, 'r') as infile:
        obj_data = json.load(infile)

    # 新しいメッシュオブジェクトを作成
    mesh = bpy.data.meshes.new(name=obj_data["name"])
    obj = bpy.data.objects.new(name=obj_data["name"], object_data=mesh)
    bpy.context.collection.objects.link(obj)

    # メッシュデータを設定
    mesh.from_pydata(obj_data["vertices"], obj_data["edges"], obj_data["faces"])
    mesh.update()

    # UV情報の設定
    if obj_data["uvs"]:
        uv_layer = mesh.uv_layers.new(name="UVMap")
        for i, uv in enumerate(mesh.uv_layers.active.data):
            uv.uv = obj_data["uvs"][i]

    # スムーズシェードの設定
    for i, use_smooth in enumerate(obj_data["smooth_shading"]):
        mesh.polygons[i].use_smooth = use_smooth

    print(f"オブジェクト '{obj_data['name']}' が生成されました。")
