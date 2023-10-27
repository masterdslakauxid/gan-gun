import streamlit as st
import time

from pages.scripts.app import predict_resume_with_rf, predict_resume_with_xgb, predict_resume_with_lgb 
from pages.scripts.content.util import get_classified_lable_file_path
from pages.scripts.app2 import generate_video_new
from pages.scripts.content.util import get_action_list

import yaml
from pathlib import Path
import ruamel.yaml
import os


progress_text = "Loading in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()


#------ Functions --------
def get_master_action_list():
   action_fname = os.path.join(Path.cwd(), 'config' , "action_master_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        actions = ["N/A"]
        for key in config:
            #st.write("key---------------------> ", key, str(config[key][0]['enabled']))
            if config[key][0]['enabled'] == True:
                actions.append(key)   

        if len(actions) == 1:            
            actions.clear()  
   return actions

#get_master_action_list()

def get_versions_for_ganpage(classified_action):
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        actions = ["N/A"] 
        for key in config:
            if key == classified_action: 
               for item in config[key]:
                    if item['default'] == True:
                        actions.append(item['version'] + ":" + " (Default) ")
                    else:
                        actions.append(item['version'])                                                
               break
        return actions
   
def get_version_details_for_ganpage(classified_action, classified_version):
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        
        actions = [] 
        
        for key in config:
           # st.write("key ----->", key)
            if key == classified_action: 
               for item in config[key]:
               # st.write(classified_version)
                out = classified_version.split(":")
                #st.write(" out ", out[0])
                if out[0] == item['version']:
                #    if item['default'] == True:
                        # actions.append(item['descr'] + " : (Default) ")
                #    else:
                    actions.append(item['descr'])
               break
        return actions
#----------------------------------

tabs_font_css = """
<style>
div[class*="stTextInput"] label p {
  font-size: 1rem;
  color: black;
}
</style>
"""
st.write(tabs_font_css, unsafe_allow_html=True)
st.header("Generate video using DCGAN")

st.subheader("Executing Text Classification")
with st.container():
    # Using the "with" syntax
    with st.form(key='my_form'):
        
        user_input = st.text_input("#1 Enter the Activity description", help="Example: A man playing archery in front of the garage in the morning", placeholder="A person playing Archery or A person playing football" )
        st.write("#2 Employ the model for classification.")
        model = st.radio(
        "select the model",
        ["RandomForest", "XGBoost", "Microsoft LGBM"],
        index=None,horizontal=True
        )
        button_clicked = False
        invalid_user_input = False
        model_selected = True
        classified_label = ""
        submit_button = st.form_submit_button(label='Classify')
        if submit_button:
            button_clicked = True
            if len(user_input) > 0: 
                if model == "RandomForest":
                    pred_action_label_rf = predict_resume_with_rf(user_input)
                    classified_label = pred_action_label_rf[0]
                elif model == "XGBoost":    
                    # Predicting the unknown action label
                    pred_action_label_xgb = predict_resume_with_xgb(user_input)
                    classified_label = pred_action_label_xgb[0]
                elif model == "Microsoft LGBM":  
                    # Predicting the unknown action label
                    pred_action_label_lgb = predict_resume_with_lgb(user_input)
                    classified_label = pred_action_label_lgb[0]
                else:
                    model_selected = False
            else:
                invalid_user_input = True
        if button_clicked == True:
            if invalid_user_input == True:
                st.error("Enter the activity")
            elif model_selected == False:
                st.error("Select the model")
            elif len(classified_label) > 0: 
                #st.success("Result : "+ classified_label)
                st.markdown(f'Result <font style="color:blue;font-size:15px;">{classified_label}</font>', unsafe_allow_html=True)
            else:
                st.warning("No matching action generated")

st.subheader("Executing the GAN Model")
with st.container():
    with st.container():
        
        st.write("#3 Generate the video")
        with st.expander("Advanced options for action versions"):    
            #New............................AK    
            with open(get_classified_lable_file_path(), 'r') as f:
                classified_label = f.read()
            st.markdown(f'The classified text for generating the video: <font style="color:blue;font-size:15px;">{classified_label}</font>', unsafe_allow_html=True)
            
            # Choosing a version from various other versions
            manually_selected_action = ""
            enabled_actions = get_master_action_list()
            if len(enabled_actions) > 1:
                manually_selected_action = st.selectbox("Select Action", options=tuple(list(enabled_actions)))
            else:
                st.write("No action labels have been enabled. Pls refer to the action_master_config.yml")

            available_versions_for_selected_action = get_versions_for_ganpage(manually_selected_action)
            
            default_ix = 0
            for action_version in available_versions_for_selected_action:
                try: 
                    if "Default" in action_version:
                        default_action_version = action_version
                        default_ix = available_versions_for_selected_action.index(default_action_version)
                        break
                except ValueError:
                    print("List does not contain value", action_version)

            selected_version = st.selectbox("Select Versions", options=tuple(list(available_versions_for_selected_action)), index = default_ix)
            list = get_version_details_for_ganpage(manually_selected_action, selected_version)  
            if len(list) > 0:
                st.write("Description: ")
                st.write(list[0])

        with st.form(key='my_form1'):           
            with st.expander("Advanced options for output"):    
                #custom_customized_label = st.text_input("Enter the activity", help="Name of the action like PlayingTabla or Football", placeholder="Enter the exact action class")
                show_images = st.checkbox("Show images")
        
            submit_button = st.form_submit_button(label='Generate Video')
            if submit_button:
                if manually_selected_action == "N/A":
                    if len(classified_label) > 0:
                        generate_video_new(classified_label, selected_version, show_images, True)  # Load the default model
                    else:
                        st.error("No classified labels found to generate videos")
                else:
                    if "(Default)" in selected_version:
                        out = selected_version.split(":")
                        st.write("Default selected", out[0])        
                        selected_version_final =  out[0]
                        generate_video_new(manually_selected_action, selected_version_final, show_images, False)  # Load the selected model
                    else:
                        st.write("Non Default selected")
                        generate_video_new(manually_selected_action, selected_version, show_images, False)  # Load the selected model
                        #get_version_model_details_for_ganpage(selected_action, selected_version)
                    


 