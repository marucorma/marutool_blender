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

# 現在の選択オブジェクトを取得
obj = bpy.context.active_object

# オブジェクトが選択されているかを確認
if obj is None or obj.type != 'MESH':
    print("メッシュオブジェクトを選択してください。")
else:
    # オブジェクトのデータを取得
    vertices = [v.co[:] for v in obj.data.vertices]
    edges = [[e.vertices[0], e.vertices[1]] for e in obj.data.edges]
    faces = [[v for v in p.vertices] for p in obj.data.polygons]
    smooth_shading = [p.use_smooth for p in obj.data.polygons]

    # UV情報を取得
    uv_layer = obj.data.uv_layers.active.data if obj.data.uv_layers.active else None
    uvs = [[uv.uv[0], uv.uv[1]] for uv in uv_layer] if uv_layer else []

    # オブジェクトのデータを辞書にまとめる
    obj_data = {
        "name": obj.name,
        "vertices": vertices,
        "edges": edges,
        "faces": faces,
        "smooth_shading": smooth_shading,
        "uvs": uvs
    }

    # JSONファイルとして保存
    file_path = os.path.join(bpy.path.abspath("//CopyObjectData//"), "obj_info.json")
    with open(file_path, 'w') as outfile:
        json.dump(obj_data, outfile, indent=4)

    print(f"オブジェクト情報が '{file_path}' に保存されました。")
