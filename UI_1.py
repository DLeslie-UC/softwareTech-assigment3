import customtkinter as ctk
from PIL import Image
from eda.images import edaData as eda

eda = eda()
ctk.set_appearance_mode("light")

root = ctk.CTk()
# TODO: set back to "zoomed"
root.state("normal")

#Setting up the grid
root.grid_columnconfigure(0, weight=1)  
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=2)
root.grid_columnconfigure(3, weight=3)

root.grid_rowconfigure(0, weight=1) 
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=3)

def button_event():

    img1_label.configure(text="Processing... Please wait.")

    root.after(2000, completed_EDA_image) 
    root(grid_image) #distrubtion_averages

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
dict_checkboxes = {
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
    if checkbox1_var in dict_checkboxes.keys() and dict_checkboxes[checkbox1_var] not in species_list:
        species_list.append(dict_checkboxes[checkbox1_var])


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
    show_summary_table()

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
# TODO: 
# Work out how to add the images to the grid of images part
# Add the image processing parts to setup


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
# TODO: Change species to work
# ctk.CTkLabel(box3, text=f"Amount of images being used: {eda.number_of_image("Limnius sp")}", font=("Arial", 18)).pack(pady=(10, 5))

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
# TODO: Change names to actual options and what they do
items2 = ["option 1", "option 2", "option 3", "option 4", "option 5"]

checkboxes2 = []
for item in items2:
    cb = ctk.CTkCheckBox(list2, text=item)
    cb.pack(anchor="w", padx=10, pady=3)
    checkboxes2.append(cb)

#EDA processes box
img1 = ctk.CTkFrame(root, fg_color="light grey", corner_radius=30)
img1.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

button = ctk.CTkButton(list2, text="Continue", command=button_event)
button.pack(pady=10)

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
image = ctk.CTkImage(
    light_image=Image.open("./insects_dataset/Elmis sp/CPH-Elmis sp.-503-t.png"),
    size=(400, 400)
)

img2_label = ctk.CTkLabel(img1, text="")
img2_label.pack(expand=True)

ctk.CTkLabel(img2, image=image, text="").pack(expand=True)

button1 = ctk.CTkButton(list1, text="Select", command=distrubtion_averages)
button1.pack(pady=10)


root.mainloop()
