import tkinter as tk
from MultiListbox import MultiListbox

class Item:
    def __init__(self,label='[No Label]',cat='[No Category]',subcat='[No Subcategory]',parent=None):
        self.label          = label
        self.cat            = cat
        self.subcat         = subcat

class GUI:
    def __init__(self):
        self.filename = 'data.txt'                  # data are saved in here
        self.changed = False                        # if the user made changes in data
        self.item_list = []                         # list of item to display
        self.load()                                 # load item from from data.txt
        
        # root. Main screen
        self.root = tk.Tk()
        self.root.title("Item Manager by KNP")
        self.root.columnconfigure(0,minsize=600,weight=1)
        self.root.rowconfigure(1,minsize=600,weight=1)
        # tool frame
        frm_tool    = tk.Frame(master=self.root)
        frm_tool.grid(row=0,column=0,sticky="nsew")
        frm_tool.columnconfigure([0,1,2,3],minsize=100,weight=1)
        # tool frame - tools
        btn_add     = tk.Button(master=frm_tool,text='Add',command=self.add_window)
        btn_add.grid(row=0,column=0,sticky="ew",padx=5, pady=5)
        btn_del     = tk.Button(master=frm_tool,text='Delete',command=self.delete)
        btn_del.grid(row=0,column=1,sticky="ew",padx=5, pady=5)
        btn_edt     = tk.Button(master=frm_tool,text='Edit', command=self.edit_window)
        btn_edt.grid(row=0,column=2,sticky="ew",padx=5, pady=5)
        btn_cls     = tk.Button(master=frm_tool,text='Save & Close',command=self.saveclose)
        btn_cls.grid(row=0,column=3,sticky="ew",padx=5, pady=5)
        
        self.show_item_list()           # show items from item_list using multi column listbox
        self.root.mainloop()            # keep the main screen running
        
    def show_item_list(self):
        # listbox of item
        self.itemsbox = MultiListbox(self.root,["Items","Cateogry","Sub-Category"],width=1)
        for i in self.item_list:
            self.itemsbox.add_data([i.label,i.cat,i.subcat])
        self.itemsbox.grid(row=1,column=0,sticky="nsew",padx=5, pady=5)
        
    def sub_window(self):
        """
        a sub window that appear when edit or add is clicked
        """
        root      = tk.Tk()
        # fields and entry
        fields = ["Name","Category","Sub-Category"]
        ents = []
        root.columnconfigure([0,1],minsize=200,weight=1)
        for i,f in enumerate(fields):
            lbl_r = tk.Label(master=root,text=f)
            ent_r = tk.Entry(master=root,width = 20)
            lbl_r.grid(row=i,column=0,padx=5, pady=5)
            ent_r.grid(row=i,column=1,padx=5, pady=5)
            ents.append(ent_r)
        add = tk.Button(master=root,text="Click")
        add.grid(row=3,column=1,padx=5, pady=5,sticky="nsew")
        
        # dropdown list of category
        if self.item_list:
            category = []
            for i in self.item_list:
                cat_name = i.cat+':'+i.subcat
                if cat_name not in category:
                    category.append(cat_name)
            category.sort()
            var = tk.StringVar(root)
            var.set(category[0])
            cat_dd = tk.OptionMenu(root,var, *category, command=lambda var: self.select_cat(var,ents))
            cat_dd.grid(row = 3, column =0, padx=5, pady=5,sticky="nsew")
        
        return root,ents,add
    
    def select_cat(self,var,ents):
        """ call when an option is selected in drop down list"""
        ents[1].delete(0,tk.END)
        ents[2].delete(0,tk.END)
        ents[1].insert( tk.END, var[:var.index(':')] )
        ents[2].insert( tk.END, var[var.index(':')+1:] )
        
    def add_window(self):
        """ sub_window when add is pressed"""
        root,ents,add = self.sub_window()
        root.title("Add Item")
        add['text'] = 'Finish'
        add['command'] = lambda: self.add(ents,root)
        root.mainloop()
        
    def add(self,ents,root):
        """adding item"""
        if ents[0].get() != '':
            self.changed = True
            i_new = Item(label=ents[0].get(),cat=ents[1].get(),subcat=ents[2].get())
            self.item_list.append(i_new)
            self.itemsbox.destroy()
            self.show_item_list()
        root.destroy()
        
    def delete(self):
        """deleting item"""
        self.changed = True
        r = self.itemsbox.curselection()
        if r == None: return
        self.item_list.pop(r)
        self.itemsbox.destroy()
        self.show_item_list()
        
    def edit_window(self):
        """sub window when edit is clicked"""
        
        # if not selected, do nothing
        r = self.itemsbox.curselection()
        if r == None: return
        item = self.item_list[r]
        
        root,ents,add = self.sub_window()
        root.title("Edit Item")
        add['text'] = 'Finish'
        ents[0].insert(tk.END,item.label)
        ents[1].insert(tk.END,item.cat)
        ents[2].insert(tk.END,item.subcat)
        add['command'] = lambda: self.edit(item,ents,root)
        root.mainloop()
        
    def edit(self,item,ents,root):
        """change item"""
        if ents[0].get() != '':
            self.changed = True
            item.label = ents[0].get()
            item.cat = ents[1].get()
            item.subcat = ents[2].get()
            self.itemsbox.destroy()
            self.show_item_list()
        root.destroy()
        
    def load(self):
        """ load from data.txt"""
        try: # read file if exist
            file = open(self.filename, 'r')
        except:
            return
        lines = file.readlines()
        for line in lines:
            info = line.split(',')
            i_new = Item(info[0],info[1],info[2])
            self.item_list.append(i_new)
        file.close()
        
    def saveclose(self):
        """items are saved to data.txt"""
        if self.changed:
            file = open(self.filename,'w')
            for i in self.item_list:
                file.write(i.label+','+i.cat+','+i.subcat+'\n')
            file.close()
        self.root.destroy()
        
m = GUI()