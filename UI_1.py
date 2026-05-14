import customtkinter as ctk
import os
from PIL import Image
from eda.eda import edaData as eda
from images.images import ImageManipulation
import random

eda = eda()
ctk.set_appearance_mode("light")

root = ctk.CTk()
root.state("zoomed")

#Setting up the grid
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=2)
root.grid_columnconfigure(3, weight=3)

root.grid_rowconfigure(0, weight=1) 
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=3)


def completed_EDA_image():
    img = Image.open("bug test.jpeg") 

    EDA_image = ctk.CTkImage(
        light_image=img,
        size=(300, 300)
    )
    img1_label.configure(text="", image=EDA_image)

def grid_image():
    img = Image.open("EDA_grid_image.jpeg") 

    EDA_image = ctk.CTkImage(
        light_image=img,
        size=(300, 300)
    )
    img2_label.configure(text="", image=EDA_image)

species_list = []
dict_checkboxes1 = {
        ".!ctkframe2.!ctkcheckbox": "Asellus sp", 
        ".!ctkframe2.!ctkcheckbox2": "Baetidae sp", 
        ".!ctkframe2.!ctkcheckbox3": "Elmis sp", 
        ".!ctkframe2.!ctkcheckbox4": "Ephemerellidae", 
        ".!ctkframe2.!ctkcheckbox5": "Erpobdella sp", 
        ".!ctkframe2.!ctkcheckbox6": "Gammarus sp", 
        ".!ctkframe2.!ctkcheckbox7": "Hydropsychidae sp", 
        ".!ctkframe2.!ctkcheckbox8": "Leptophlebiidae sp", 
        ".!ctkframe2.!ctkcheckbox9": "Leuctra sp", 
        ".!ctkframe2.!ctkcheckbox10": "Limnius sp", 
        ".!ctkframe2.!ctkcheckbox11": "Lymnea sp", 
        ".!ctkframe2.!ctkcheckbox12": "Nemoura sp", 
        ".!ctkframe2.!ctkcheckbox13": "Oligochaeta sp", 
        ".!ctkframe2.!ctkcheckbox14": "Sericostomatidae sp", 
        ".!ctkframe2.!ctkcheckbox15": "Sialis sp", 
        ".!ctkframe2.!ctkcheckbox16": "Simuliidae sp", 
        ".!ctkframe2.!ctkcheckbox17": "Sphaerium sp", 
}


def set_species_list(checkbox1_var):
    checkbox1_var = str(checkbox1_var)
    if checkbox1_var in dict_checkboxes1.keys() and dict_checkboxes1[checkbox1_var] not in species_list:
        species_list.append(dict_checkboxes1[checkbox1_var])


def update_count():
    count = sum(1 for cb in checkboxes1 if cb.get() == 1)
    count_label.configure(text=f"Selected: {count}", font=("Arial", 18))
    for cb in checkboxes1:
        if cb.get() == 1:
            set_species_list(cb)

def distrubtion_averages():
    for species in species_list:
        height_mean, width_mean = eda.mean_height_width(species)
        ctk.CTkLabel(box2, text=f"{species}, average height: {height_mean}, average width: {width_mean}", font=("Arial", 18)).pack(pady=(10, 5))

def on_select():
    distrubtion_averages()
    global rep_image 
    rep_image = rep_images()
    show_summary_table()
    show_grid_images()


def summary_table_values(lst: list[str]):
    lst_len = len(lst)
    string_value = ""
    for item in lst:
        if item != lst[lst_len-1]:
            string_value += f"{item} | "
        else:
            string_value += f"{item}"
    return string_value

def show_summary_table():
    summary_dataframe = eda.summary_table(species_list)
    summary_columns = summary_dataframe.columns.values
    summary_rows = summary_dataframe.index.values
    column_text_value = summary_table_values(summary_columns)
    column_text_value = "Species | " + column_text_value
    ctk.CTkLabel(box3, text=column_text_value, font=("Arial", 18)).pack(pady=(10, 5))
    for species in species_list:
        row_text_value = species + " | "
        for column in summary_columns:
            to_str_val = summary_dataframe.loc[species][column]
            if column != summary_columns[len(summary_columns)-1]:
                row_text_value += str(to_str_val) + " | "
            else:
                row_text_value += str(to_str_val)
        ctk.CTkLabel(box3, text=row_text_value, font=("Arial", 18)).pack(pady=(10, 5))


#Title
title = ctk.CTkLabel(root, text="Macroinvertebrate Image Analysis System", fg_color="light grey", corner_radius=20, font=("Arial", 30))
title.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

#Creating container for (left side info)
left_container = ctk.CTkFrame(root, fg_color="transparent")
left_container.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

#3 boxes for left side container
left_container.grid_rowconfigure((0, 1, 2), weight=1)
left_container.grid_columnconfigure(0, weight=1)

box1 = ctk.CTkFrame(left_container, fg_color="light grey", corner_radius=20)
box1.grid(row=0, column=0, sticky="nsew", pady=5)

count_label = ctk.CTkLabel(box1, text="Selected: 0", font=("Arial", 18))
count_label.pack(expand=True)

for i in range(1, 3):
    ctk.CTkFrame(left_container, fg_color="light grey", corner_radius=20).grid(row=i, column=0, sticky="nsew", pady=5)

box2 = ctk.CTkFrame(left_container, fg_color="light grey", corner_radius=20)
box2.grid(row=1, column=0, sticky="nsew", pady=5)
ctk.CTkLabel(box2, text="Average distrubtion of image widths and heights:", font=("Arial", 18)).pack(pady=(10, 5))
# ctk.CTkLabel(box2, text=f"{} average height: {height_mean}, average width: {width_mean}", font=("Arial", 18)).pack(pady=(10, 5))

box3 = ctk.CTkFrame(left_container, fg_color="light grey", corner_radius=20)
box3.grid(row=2, column=0, sticky="nsew", pady=5)

#Selecting bugs
list1 = ctk.CTkFrame(root, fg_color="light grey", corner_radius=30)
list1.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
ctk.CTkLabel(list1, text="Select bug classes to be used:", font=("Arial", 18)).pack(pady=(10, 5))

#Setting up tickable checkboxes to decide bugs used
items1 = ["Asellus sp", "Baetidae sp", "Elmis sp", "Ephemerellidae", "Erpobdella sp",
          "Gammarus sp", "Hydropsychidae sp", "Leptophlebiidae sp", "Leuctra sp",
          "Limnius sp", "Lymnea sp", "Nemoura sp", "Oligochaeta sp",
          "Sericostomatidae sp", "Sialis sp", "Simuliidae sp", "Sphaerium sp"]

checkboxes1 = []
for item in items1:
    cb = ctk.CTkCheckBox(list1, text=item, command=update_count)
    cb.pack(anchor="w", padx=10, pady=3)
    checkboxes1.append(cb)


#Selecting EDA processes
list2 = ctk.CTkFrame(root, fg_color="light grey", corner_radius=30)
list2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
ctk.CTkLabel(list2, text="Select one EDA process to be completed:", font=("Arial", 18)).pack(pady=(10, 5))

#Setting up tickable checkboxes to decide EDA processes used
items2 = ["Black And White", "Flip Upside Down", "16 Bitify", "Contrast Enhancement", "Brightness Enhancement"]

dict_checkboxes2 = {
    ".!ctkframe3.!ctkcheckbox": items2[0],
    ".!ctkframe3.!ctkcheckbox1": items2[1],
    ".!ctkframe3.!ctkcheckbox2": items2[1],
    ".!ctkframe3.!ctkcheckbox3": items2[2],
    ".!ctkframe3.!ctkcheckbox4": items2[3],
    ".!ctkframe3.!ctkcheckbox5": items2[4],
}
checkboxes2 = []
for item in items2:
    item = ctk.CTkCheckBox(list2, text=item)
    item.pack(anchor="w", padx=10, pady=3)
    checkboxes2.append(item)

options_list = []
def set_options_list():
    for checkbox2_var in checkboxes2:
        if checkbox2_var.get() == 1:
            checkbox2_var = str(checkbox2_var)
            if checkbox2_var in dict_checkboxes2.keys() and dict_checkboxes2[checkbox2_var] not in options_list:
                options_list.append(dict_checkboxes2[checkbox2_var])


#EDA processes box
img1 = ctk.CTkFrame(root, fg_color="light grey", corner_radius=30)
img1.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)


img1_label = ctk.CTkLabel(img1, text="")
img1_label.pack(expand=True)

#Grid image display
img2 = ctk.CTkFrame(root, fg_color="light grey", corner_radius=30)
img2.grid(row=2, column=2, columnspan=2, sticky="nsew", padx=10, pady=10)

#Making grid image display a box
def make_square(event):
    size = min(event.width, event.height)
    img2.configure(width=size, height=size)

img2.bind("<Configure>", make_square)

display_label = ctk.CTkLabel(img2, text="")
display_label.pack(expand=True)

#Image
def rep_images():
    i = 0
    rep_images = {}
    if species_list != []:
        while i <= 4:
            for species in species_list:
                i += 1
                rep_images[species] = eda.representative_images(species, num_per_species=1)
            break
        return rep_images


def show_grid_images():
    if rep_image != None:
        for species in rep_image.keys():
            try: 
                image = ctk.CTkImage(
                    # light_image=Image.open(f"./insects_dataset/{species}/{rep_image[species][0]}"),
                    light_image=Image.open(os.path.join( "insects_dataset", species, rep_image[species][0] )),
                    size=(100, 100)
                )
                ctk.CTkLabel(img2, image=image, text=species).pack(expand=True)
            except KeyError:
                break

def image_manipulations():
    set_options_list()
    dataset_path = os.path.join(os.getcwd(), "insects_dataset")
    rand_species = species_list[random.randint(0, len(species_list)-1)]
    save_path = os.path.join(rand_species)
    species_img = rep_image[rand_species][0]
    species_img_path = os.path.join(dataset_path, save_path, species_img)
    image = ImageManipulation(species_img_path, save_path)
    for option in options_list:
        option = option.lower()
        if option == "black and white":
            image.black_and_white()
        if option == "flip upside down":
            image.upside_down()
        if option == "16 bitify":
            image.sixteen_bit()
        if option == "contrast enhancement":
            image.contrast()
        if option == "brightness enhancement":
            image.brightness()
    display_image = ctk.CTkImage(
        light_image=image.return_image(),
        size=(300, 300)
    )
    img1_label.configure(text="", image=display_image)
    image.save_image()

img2_label = ctk.CTkLabel(img1, text="")
img2_label.pack(expand=True)

def button_event():

    img1_label.configure(text="Processing... Please wait.")

    on_select() #distrubtion_averages
    if species_list != []:
        root.after(2000, image_manipulations) 

button = ctk.CTkButton(list2, text="Continue", command=button_event)
button.pack(pady=10)


root.mainloop()
