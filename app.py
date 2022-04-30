import streamlit as st
from transcribe import *
import time
import zipfile
from zipfile import ZipFile
from io import BytesIO

st.header("Subtitling Tool")
st.subheader("Generate your subtitles with AssemblyAI. You are given 3 hours of free conversion per month.")

api_key = st.text_input("Enter your AssemblyAI API key", type="password")

fileObjects = st.file_uploader(label = "Please upload your file", accept_multiple_files = True)

if fileObjects is not None:

	# create zipfile

	zf = zipfile.ZipFile('subtitles.zip', "w")

	for fileObject in fileObjects:
		token = api_key
		token, t_id = upload_file(fileObject, token)
		result = {}
		#polling
		sleep_duration = 1
		percent_complete = 0
		progress_bar = st.progress(percent_complete)
		st.text("Currently in queue")
		while result.get("status") != "processing":
		    percent_complete += sleep_duration
		    time.sleep(sleep_duration)
		    progress_bar.progress(percent_complete/10)
		    result = get_text(token,t_id)

		sleep_duration = 0.01

		for percent in range(percent_complete,101):
		    time.sleep(sleep_duration)
		    progress_bar.progress(percent)

		with st.spinner("Processing....."):
		    while result.get("status") != 'completed':
		        result = get_text(token,t_id)


		result = write_srt(token,t_id)

		file_name = fileObject.name.split('.')[0]

		st.write(f"Subtitle file for {file_name} created")

		# Write into zip file

		zf.writestr(f"{file_name}.srt", result)



	zf.close()


	with open("subtitles.zip", "rb") as fp:
	    btn = st.download_button(
	        label="Download ZIP",
	        data=fp,
	        file_name="subtitled_files.zip",
	        mime="application/zip"
	    )

	st.success('All subtitles created!')
