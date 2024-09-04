from stl import mesh
import os

# Define the root directory containing the subfolders
root_directory = "/users/shay/Downloads/100_Cads"
output_directory = "/users/shay/Downloads/100_Scripts"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Iterate over all subfolders in the root directory
for subfolder_name in os.listdir(root_directory):
    subfolder_path = os.path.join(root_directory, subfolder_name)

    if os.path.isdir(subfolder_path):  # Check if it's a folder
        # Iterate over all files in the subfolder
        for filename in os.listdir(subfolder_path):
            if filename.endswith(".stl"):
                stl_path = os.path.join(subfolder_path, filename)

                # Load the STL file using numpy-stl
                your_mesh = mesh.Mesh.from_file(stl_path)

                # Extract vertices and faces
                vertices = your_mesh.vectors.reshape(-1, 3)
                faces = [(i, i + 1, i + 2) for i in range(0, len(vertices), 3)]

                # Generate Python script content
                script = "import bpy\n\n"
                script += "mesh = bpy.data.meshes.new(name='GeneratedMesh')\n"
                script += "obj = bpy.data.objects.new(name='GeneratedObject', object_data=mesh)\n"
                script += "bpy.context.collection.objects.link(obj)\n\n"
                script += f"vertices = {vertices.tolist()}\n"
                script += f"faces = {faces}\n\n"
                script += "mesh.from_pydata(vertices, [], faces)\n"
                script += "mesh.update()\n"

                # Create a unique output filename
                output_filename = f"{subfolder_name}_script.py"
                output_file = os.path.join(output_directory, output_filename)

                # Write the script to a file in the output directory
                with open(output_file, "w") as f:
                    f.write(script)

                print(f"Generated Python script for {filename} in folder {subfolder_name}")

print("All files processed.")
