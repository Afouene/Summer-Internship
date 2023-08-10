import streamlit as st
import pandas as pd
import subprocess
import tempfile 
import os
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
            
    # Check the return code to determine if the command executed successfully
    if process.returncode == 0:
        st.success("3D mesh generation successful!")
    else:
        st.error("3D mesh generation failed!")
    




