import streamlit as st
import os
import yaml
from pathlib import Path
import ruamel.yaml



#ak
from pathlib import Path

fname_meta = os.path.join(Path.cwd(), 'config' , "models_meta.yml")

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=6, sequence=4)
with open(fname_meta) as fp:
    config = yaml.load(fp)


def get_availble_models():
   list_models = [] 
   for key, value in config.items():
       for model in value:
           available = model['available']
           if bool(available) == True:
            list_models.append(model)
   return list_models
        

def print_list():
   st.write("entering print_list")
   models = get_availble_models()
   for model in models:
       st.write("Currently enabled model")
       st.write(model['id'])
       st.write(model['name'])
       st.write(model['available'])

#print_list()

def get_default_models():
   st.write(" get_default_models ")
   models = get_availble_models()
   model = models[0] 
   st.write(model['id'])
   st.write(model['name'])
   st.write(model['available'])

def get_actions():
   #models = get_availble_models()
   #model = models[0] 
   classified_action =  "Archery"
   #classified_action =  "Basketball"
   #st.write ("Default model Id",model_id )
  
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        
       # st.write(type(config))
        
        actions = {} 
        
        for key in config:
            st.write("key ----->", key)
            if key == classified_action: 
               for item in config[key]:
                default = bool(item['default'])
                if (default):
                    actions.__setitem__(key,[item['d_model_file'], item['g_model_file']])
                    # st.write(item['version'])
                    # st.write(item['descr'])
                    # st.write(item['default'])
                    # st.write(item['d_model_file'])
                    # st.write(item['g_model_file'])
               break
               #
            #st.write("actions ", actions)
        return actions

st.write("Get actions output ")   
#sget_actions()


def get_versions_for_ganpage(classified_action):
   #models = get_availble_models()
   #model = models[0] 
   #classified_action =  "Archery"
   #classified_action =  "Basketball"
   #st.write ("Default model Id",model_id )
  
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        
       # st.write(type(config))
        
        actions = ["N/A"] 
        
        for key in config:
           # st.write("key ----->", key)
            if key == classified_action: 
               for item in config[key]:
                    if item['default'] == True:
                        actions.append(item['version'] + ":" + " (Default) ")
                    else:
                        actions.append(item['version'])                                                
                # st.write(item['version'])
                # st.write(item['descr'])
                # st.write(item['default'])
                # st.write(item['d_model_file'])
                # st.write(item['g_model_file'])
               break
               #
        #st.write("actions for gan page", actions)
        return actions

get_versions_for_ganpage("Archery")

def get_version_details_for_ganpage(classified_action, classified_version):
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        
       # st.write(type(config))
        
        actions = [] 
        
        for key in config:
           # st.write("key ----->", key)
            if key == classified_action: 
               for item in config[key]:
               # st.write(classified_version)
                out = classified_version.split(":")
                #st.write(" out ", out[0])
                if out[0] == item['version']:
                   if item['default'] == True:
                        actions.append(item['descr'] + " : (Default) ")
                   else:
                      actions.append(item['descr'])
                    # st.write(item['version'])
                    # st.write(item['descr'])
                # st.write(item['default'])
                # st.write(item['d_model_file'])
                # st.write(item['g_model_file'])
               break
               #
        #st.write("actions for gan page", actions)
        return actions
   
def get_version_models_for_ganpage(classified_action, classified_version):
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        default_config_found=False
        actions_models = [] 
        for key in config:
            st.write("key ----->", key)
            if key == classified_action: 
               for item in config[key]:
                st.write("-->classified_version ", classified_version)
                out = classified_version.split("_")
                st.write("--> out ", out[1])
                source = item['version'].split("_")
                st.write("--> source['version'] ",source[1])    
                st.write("--> compare ", out[1] == source[1]) 
                if out[1] == source[1]:
                   st.write("entering  out == source  - true")
                   #if bool(item['default']) == True:
                   st.write("item['default']", item['default'])
                   actions_models.append(item['d_model_file'])
                   actions_models.append(item['g_model_file'])
                   default_config_found = True
                   break
            
        if default_config_found == False:
            st.write("No default models fosund. Please make one model as a default ones", actions_models)
        else:
            st.write("Loading these modules", actions_models)
        return actions_models

#get_version_model_details_for_ganpage()

#st.write ("Action- Version details for the GAN page")
#get_version_model_details_for_ganpage("Archery", "Archery_20120515-155045")


# def gen_video(): 
#     L = "Basketball"
#     actions =get_actions()

#     if L in actions:
#        st.write("gen_actions")
#        d_model_file = os.path.join(get_content_path(), actions[L][0])
#        g_model_file = os.path.join(get_content_path(), actions[L][1])
#        st.write(d_model_file)
#        st.write(g_model_file)

#     #   g_model_file = os.path.join(get_content_path(), actions[L]["g_model_file"])

# gen_video()

# Completed
def get_action_list():
   action_fname = os.path.join(Path.cwd(), 'config' , "action_config.yml")
   yaml = ruamel.yaml.YAML()
   yaml.indent(mapping=6, sequence=4)
   with open(action_fname) as fp:
        config = yaml.load(fp)
        actions = ["N/A"]
        for key in config:
            actions.append(key)        
   return actions



                                    

                                      
                                      
selected_action = st.selectbox("Select Actions", options=tuple(list(get_action_list())))
selected_version = st.selectbox("Select Versions", options=tuple(list(get_versions_for_ganpage(selected_action))))
with st.container():
    list = get_version_details_for_ganpage(selected_action, selected_version)  
    if len(list) > 0:
        st.write("Description: ")
        st.write(list[0])

with st.form(key='my_form'):   
    submit_button = st.form_submit_button(label='Classify')
    if submit_button:
        if "(Default)" in selected_version:
            out = selected_version.split(":")
            st.write("Default selected", out[0])        
            list = get_version_models_for_ganpage(selected_action, out[0])
        else:
            st.write("Non Default selected")
            list = get_version_models_for_ganpage(selected_action, selected_version)  
            #get_version_model_details_for_ganpage(selected_action, selected_version)
