import json
from tkinter import Tk, Label, Entry, Button, Listbox, StringVar, END

class ShoppingListApp:
    def __init__(self, master):
        self.master = master
        master.title("Liste de courses")

        # Initialisation des données
        self.lists = self.load_data()
        self.current_list = "Principale"

        # Interface principale
        self.label = Label(master, text="Nom de l'article :")
        self.label.pack()

        self.new_item_text = StringVar()
        self.entry = Entry(master, textvariable=self.new_item_text)
        self.entry.pack()

        self.add_button = Button(master, text="Ajouter", command=self.add_item)
        self.add_button.pack()

        self.listbox = Listbox(master)
        self.listbox.pack(fill="both", expand=True)

        self.delete_button = Button(master, text="Supprimer", command=self.delete_selected)
        self.delete_button.pack()

        # Charger les articles de la liste actuelle
        self.update_list()

    def load_data(self):
        try:
            with open("shopping_lists.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"Principale": []}

    def save_data(self):
        with open("shopping_lists.json", "w") as f:
            json.dump(self.lists, f)

    def add_item(self):
        item_text = self.new_item_text.get().strip()
        if not item_text:
            return
        self.lists[self.current_list].append({"name": item_text, "checked": False})
        self.update_list()
        self.new_item_text.set("")
        self.save_data()

    def update_list(self):
        self.listbox.delete(0, END)
        for item in self.lists[self.current_list]:
            text = item["name"] + (" (✔)" if item["checked"] else "")
            self.listbox.insert(END, text)

    def delete_selected(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            del self.lists[self.current_list][selected_index[0]]
            self.update_list()
            self.save_data()

    def toggle_item(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.lists[self.current_list][index]["checked"] = not self.lists[self.current_list][index]["checked"]
            self.update_list()
            self.save_data()

if __name__ == "__main__":
    root = Tk()
    app = ShoppingListApp(root)
    root.mainloop()
