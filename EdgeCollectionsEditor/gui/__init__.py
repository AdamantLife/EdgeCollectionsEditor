import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import EdgeCollectionsEditor as ECE
from EdgeCollectionsEditor import utils
import pathlib
import sqlite3

def collection_item_displayname(obj: sqlite3.Row)-> str:
    return f"{obj['title']}\n {obj['id']}"

class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.parent = master
        self.parent.title("Edge Collections Editor")

        self.db: sqlite3.Connection | None = None

        self.pack(fill="both", expand=True)

        self.file_location = None

        self.connect_db()
        self.setup()

    def connect_db(self):
        try:
            self.db, self.file_location = ECE.connect_to_db(file_location=self.file_location)
            print("DB Loaded from", self.file_location)
            utils.backup_database(self.file_location)
        except FileNotFoundError:
            result = self.ask_file_location()
            if not result:
                return self.master.destroy()
            return self.connect_db()
        
    def ask_file_location(self):
        messagebox.showerror("Error", "Could not find Edge Collections database.")
        self.file_location = filedialog.askopenfilename(filetypes=[("SQLite Database", ".db")])
        return self.file_location
    
    def setup(self):
        for child in self.winfo_children():
            child.destroy()
        self.collectionviewer = CollectionViewer(self)
        self.collectionviewer.pack(fill="both", expand=True)

    def show_collections(self):
        self.collectionviewer.pack(fill="both", expand=True)

    def edit_collection(self, collection: sqlite3.Row):
        self.collectionviewer.pack_forget()
        CollectionEditor(self, collection).pack(fill="both", expand=True)

    ## Commands
    def edit_collection_title(self, collection: sqlite3.Row, title: str):
        if not self.db:
            messagebox.showerror("Error", "No database connection.")
            raise RuntimeError("Lost database connection.")
        ECE.edit_collection_title(self.db, collection['id'], title)

    def delete_collection(self, collection: sqlite3.Row):
        if not self.db:
            messagebox.showerror("Error", "No database connection.")
            raise RuntimeError("Lost database connection.")
        ECE.delete_collection(self.db, collection['id'])

class CollectionViewer(ttk.Frame):
    def __init__(self, master: MainWindow, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.parent = master
        self.data = {"collections": [], "items": []}
        self.setup()
        self.load_data()

    def setup(self):
        ttk.Label(self, text="Edge Collections Editor", font=("Arial", 24)).pack(pady=10)
        
        f = ttk.Frame(self)
        f.pack(fill="both", expand=True)

        lf = ttk.Frame(f)
        self.collectionfilter = tk.StringVar()
        self.collectionfilter.trace_add("write", lambda *e: self.updatefilter("collection", *e))
        self.collectionfilterwidget = tk.Entry(lf, textvariable=self.collectionfilter)
        self.collectionfilterwidget.pack()
        self.collectionfilterwidget.pack(side='top', fill = 'x')

        ff = ttk.Frame(lf)
        ff.pack(fill="both", expand=True)

        self.collectionlist = tk.Listbox(ff, selectmode="single", exportselection=False)
        self.collectionlist.pack(side="left", fill="both", expand=True)
        clscroll = ttk.Scrollbar(ff, command=self.collectionlist.yview)
        clscroll.pack(side="right", fill="y")
        self.collectionlist.config(yscrollcommand=clscroll.set)

        mf = ttk.Frame(f)

        self.itemfilter = tk.StringVar()
        self.itemfilter.trace_add("write", lambda *e: self.updatefilter("item", *e))
        self.itemfilterwidget = tk.Entry(mf, textvariable=self.itemfilter)
        self.itemfilterwidget.pack(side='top', fill = 'x')

        ff = ttk.Frame(mf)
        ff.pack(fill="both", expand=True)

        self.itemlist = tk.Listbox(ff, selectmode="multiple", exportselection=False)
        self.itemlist.pack(side="left", fill="both", expand=True)
        ilscroll = ttk.Scrollbar(ff, command=self.itemlist.yview)
        ilscroll.pack(side="right", fill="y")
        self.itemlist.config(yscrollcommand=ilscroll.set)

        self.commandsframe = rf = ttk.Frame(f)
        self.collectioncommands = ttk.Frame(rf)
        self.collectioncommands.pack(fill="both", expand=True)
        self.itemscommands = ttk.Frame(rf)
        self.itemscommands.pack(fill="both", expand=True)

        lf.grid(row=0, column=0, sticky="nsew", padx=10)
        mf.grid(row=0, column=1, sticky="nsew", padx=10)
        rf.grid(row=0, column=2,sticky="nsew", padx=10)
        f.columnconfigure(0, weight=1)
        f.columnconfigure(1, weight=1)
        f.columnconfigure(2, weight=2)
        f.rowconfigure(0, weight=1)
        

        self.collectionlist.bind("<<ListboxSelect>>", self.collectionselect)
        self.itemlist.bind("<<ListboxSelect>>", self.itemselect)

    def load_data(self):
        self.collectionlist.delete(0, "end")
        self.itemlist.delete(0, "end")
        
        for collection in (collections := ECE.list_collections(self.parent.db)):
            self.collectionlist.insert("end", collection_item_displayname(collection))

        self.data["collections"] = collections

        items = ECE.list_items(self.parent.db)
        items = ECE.link_items_to_collections(self.parent.db, items)
        
        self.data["items"] = items

    def updatefilter(self, filter_type: str, *e):
        if filter_type == "collection":
            selection = [self.collectionlist.get(idx) for idx in self.collectionlist.curselection()]
            collection_names = [collection_item_displayname(collection) for collection in self.data["collections"]]
            self.collectionlist.delete(0, "end")
            for name in collection_names:
                if self.collectionfilter.get() in name:
                    self.collectionlist.insert("end", name)
                    if name in selection:
                        self.collectionlist.selection_set(collection_names.index(name))
        if filter_type == "item":
            selection = [self.itemlist.get(idx) for idx in self.itemlist.curselection()]
            item_names = [collection_item_displayname(item) for item in self.data["items"]]
            self.itemlist.delete(0, "end")
            for name in item_names:
                if self.itemfilter.get() in name:
                    self.itemlist.insert("end", name)
                    if name in selection:
                        self.itemlist.selection_set(item_names.index(name))

    def collectionselect(self, *e):
        ## Collection Listbox unselects when items are selected
        if not self.collectionlist.curselection(): return
        self.reload_items()
        
        self.load_collection_commands()

    def reload_items(self):
        select = self.collectionlist.get(self.collectionlist.curselection()[0])
        name,id = select.split("\n", maxsplit=1)
        id = id.strip()
        itemfilter = self.itemfilter.get().strip()

        self.itemlist.delete(0, "end")
        for item in self.data["items"]:
            for relationship in item['collections_items_relationships']:
                if relationship["parent_id"] == id and (itemfilter == "" or itemfilter in collection_item_displayname(item)):
                    self.itemlist.insert("end", collection_item_displayname(item))
                    break
    def load_collection_commands(self):
        for child in self.collectioncommands.winfo_children()+self.itemscommands.winfo_children():
            child.destroy()

        cc = self.collectioncommands
        ttk.Button(cc, text="Edit Collection", command=self.edit_collection).pack()

    def itemselect(self, *e):
        for child in self.itemscommands.winfo_children():
            child.destroy()
        ## TODO: load commands for this item

## Commands
    def edit_collection(self):
        collection = self.data["collections"][self.collectionlist.curselection()[0]]
        self.parent.edit_collection(collection)

class CollectionEditor(ttk.Frame):
    def __init__(self, parent: MainWindow, collection: sqlite3.Row):
        super().__init__(parent)
        self.parent = parent
        self.collection = collection
        self.pack(fill="both", expand=True)
        self.setup()

    def setup(self):
        for child in self.winfo_children():
            child.destroy()
        f = ttk.Frame(self)
        ttk.Label(f, text="Title:").grid(row=0, column=0)
        self.title = ttk.Entry(f)
        self.title.grid(row=0, column=1)
        ttk.Button(f, text="Save", command=self.savetitle).grid(row=0, column=2)
        f.pack()

        ttk.Button(self, text="Delete", command=self.delete).pack()

        ttk.Button(self, text="Back", command=self.unload).pack()

    def unload(self):
        self.parent.show_collections()
        self.destroy()
    def savetitle(self):
        value = self.title.get()
        if not value.strip():
            messagebox.showerror("Error", "Title cannot be empty.")
            return
        self.parent.edit_collection_title(self.collection, value)
        messagebox.showinfo("Success", "Collection title updated.")
        
    def delete(self):
        response = messagebox.askyesno("Confirm", "Are you sure you want to delete this collection?")
        if response:
            self.parent.delete_collection(self.collection)
            messagebox.showinfo("Success", "Collection deleted.")
            self.unload()

def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()