import streamlit as st
import pandas as pd
import subprocess
import tempfile 
import os
import streamlit.components.v1 as components
import numpy as np
import trimesh
from PIL import Image
import itkwidgets as itk



def displayfunc1():
    im=Image.open("./6/6.jpg")
    displacement_map = Image.open("./6/6_dpmap_14.png")  # Load the displacement map
    mesh = trimesh.load('./6/6.obj',process=False)

    #im = Image.open("./demo/output/temp_img/temp_img.jpg") #the texture 
    #displacement_map = Image.open("./demo/output/temp_img/temp_img_dpmap.png")  # Load the displacement map

    #mesh = trimesh.load('./demo/output/temp_img/temp_img.obj',process=False)
    tex = trimesh.visual.TextureVisuals(image=im)
    mesh.visual.texture = tex
    displacement_array = np.array(displacement_map)
    print("displacement_array shape:", displacement_array.shape)
    print("displacement_array dtype:", displacement_array.dtype)

    print("mesh.vertices shape:", mesh.vertices.shape)
    print("mesh.vertices dtype:", mesh.vertices.dtype)

    
    
    mesh.show()

def displayfunc():
    im = Image.open("./6/6.jpg")
    displacement_map = Image.open("./6/6_dpmap_14.png").convert("L")  # Load and convert to grayscale
    mesh = trimesh.load('./6/6.obj', process=False)

    # Convert texture to grayscale
    im_gray = im.convert("L")
    
    # Convert the grayscale texture to numpy array
    texture_array = np.array(im_gray)
    
    # Resize the texture array to match the displacement map
    resized_texture_array = np.array(displacement_map.resize((mesh.vertices.shape[0], mesh.vertices.shape[1])))
    
    # Apply the displacement to the texture
    displaced_texture_array = texture_array + resized_texture_array
    
    # Apply the displaced texture to the mesh
    tex = trimesh.visual.TextureVisuals(image=displaced_texture_array)
    mesh.visual.texture = tex

    mesh.show()




st.title("3D Mesh Generator")
st.write("Here's our first attempt :")
uploaded_file=st.file_uploader("choose a file")
if uploaded_file is not None :
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)


if st.button("generate 3d mesh"):
    st.info("Generating 3D mesh please wait...")
     # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    # Save the uploaded image inside the temporary directory
    temp_image_path = os.path.join(temp_dir, "temp_img.png")
    
    with open(temp_image_path,"wb") as f:
        f.write(uploaded_file.read())
    
    #defining the command and its arguments 
    command = [
                "python",
                "main.py",
                "--name", "dpmap_single",
                "--input", temp_dir,  # Use the temporary image path as input
                "--output", "./demo/output",
                "--gpu_ids", "0",
                "--render"
            ]
    print(temp_image_path)
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # Wait for the process to complete and capture outputs
    process.wait()
    output_directory = "./demo/output/temp_img"
    obj_path = os.path.join(output_directory, "temp_img.obj")
    mtl_path = os.path.join(output_directory, "temp_img.obj.mtl")
    texture_path = os.path.join(output_directory, "temp_img.jpg")


 # Check the return code to determine if the command executed successfully
    if process.returncode == 0:
        st.success("3D mesh generation successful!")
        st.title("3D Mesh Display")
        displayfunc1()
        





    else:
        st.error("3D mesh generation failed!")
        
