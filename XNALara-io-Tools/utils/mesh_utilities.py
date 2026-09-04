import bpy


def create_split_normals(mesh_object: bpy.types.Object, normals: list[tuple[float, float, float]]):
    mesh_data: bpy.types.Mesh = mesh_object.data
    b_mesh_was_corrected = False

    if (bpy.app.version[:2] in [(3, 6), (4, 0)]):
        mesh_data.create_normals_split()
        b_mesh_was_corrected = mesh_data.validate(clean_customdata=False)
        mesh_data.update(calc_edges=True)
        mesh_data.normals_split_custom_set_from_vertices(normals)
        mesh_data.use_auto_smooth = True

    else:
        b_mesh_was_corrected = mesh_data.validate(clean_customdata=False)
        mesh_data.update(calc_edges=True)
        mesh_data.normals_split_custom_set_from_vertices(normals)

    return b_mesh_was_corrected
