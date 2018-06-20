
# coding: utf-8

# In[12]:


import os  

def grab_file_name(file_dir):   
    with open('val.txt', 'w') as f:
        for root, dirs, files in os.walk(file_dir):   
            for file_name in files:
                abs_path = os.path.join(file_dir, file_name)
                print(abs_path)
                f.write(abs_path + '\n')

grab_file_name('/home/ilab/CV_Project/xqqds-0620-val/images')



