import customtkinter as ctk
from PIL import Image

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

def update_count():
    count = sum(1 for cb in checkboxes1 if cb.get() == 1)
    count_label.configure(text=f"Selected: {count}", font=("Arial", 18))

"""def distrubtion_averages():
    box2_label.configure(text=f"Average Height: {height_mean}")
    box2_label.configure(text=f"Average Width: {width_mean}")
    """

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

box3 = ctk.CTkFrame(left_container, fg_color="light grey", corner_radius=20)
box3.grid(row=2, column=0, sticky="nsew", pady=5)
#ctk.CTkLabel(box3, text=f"Amount of images being used: {number_of_images} font=("Arial", 18)).pack(pady=(10, 5))

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
    light_image=Image.open("test_imahe.jpeg"),
    size=(400, 400)
)

img2_label = ctk.CTkLabel(img1, text="")
img2_label.pack(expand=True)

ctk.CTkLabel(img2, image=image, text="").pack(expand=True)

root.mainloop()
