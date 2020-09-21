#!/usr/bin/env python3
# V. 1.0

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango
from gi.repository import GdkPixbuf
from os.path import expanduser
import sys

# info dialog
class DialogBox(Gtk.Dialog):
 
    def __init__(self, parent, info):
        Gtk.Dialog.__init__(self, title="Info", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
 
        self.set_default_size(150, 100)
        
        label = Gtk.Label(label=info)
 
        box = self.get_content_area()
        box.add(label)
        self.show_all()


import open_rubrica as OR
data_list = OR.open_rubrica()

if data_list == 2:
    dialog = DialogBox(None, "  Error with the file data.db  ")
    dialog.run()
    dialog.destroy()
    sys.exit()
elif data_list == 3:
    dialog = DialogBox(None, "  Cannot create the file data.db  ")
    dialog.run()
    dialog.destroy()
    sys.exit()
else:
    data_list.sort()
    

import save_rubrica as SR

import export_item as EI

import export_database as ED

import import_vcf as IV


HOME=expanduser("~")


WWIDTH=800
WHEIGHT=600
USE_HEADBAR=0

# get the window size from the config file
with open("rubrica.cfg", "r") as fconf:
    WWIDTH2 = fconf.readline().strip()
    WHEIGHT2 = fconf.readline().strip()
    USE_HEADBAR2 = fconf.readline().strip()
    if WWIDTH2.isnumeric():
        WWIDTH = int(WWIDTH2)
    if WHEIGHT2.isnumeric():
        WHEIGHT = int(WHEIGHT2)
    if USE_HEADBAR2 == "1":
        USE_HEADBAR = 1

### characters used by the filter
list_chars = ['@', 'AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP', 'QR', 'ST', 'UV', 'WX', 'YZ', '0-9']
        
list_data = ["Surname/Co.", "Name", "Telephone", "Email", "Web", "Notes"]


class App:

    def __init__(self):

        #### create main window
        self.window = Gtk.Window()
        # set title, size, position
        self.window.set_title("Contacts")
        self.window.set_default_size(WWIDTH, WHEIGHT)
        pixbuf = Gtk.IconTheme.get_default().load_icon("address-book-new", 24, 0)
        self.window.set_icon(pixbuf)
        # connect delete events to quit
        self.window.connect('delete-event', self.exit_program)
        ## for those wanting the headerbar
        if USE_HEADBAR:
            header = Gtk.HeaderBar(title="Contacts")
            header.props.show_close_button = True
            self.window.set_titlebar(header)
        
        ####
        # main vertical box
        self.vbox = Gtk.Box(orientation=1, spacing=0)
        self.window.add(self.vbox)
        
        #### box for buttons
        self.button_box = Gtk.Box(orientation=0, spacing=5)
        self.vbox.add(self.button_box)
        ## add a record button
        pixbuf = Gtk.IconTheme.get_default().load_icon("contact-new", 48, 0)
        add_rec_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.add_record_button = Gtk.Button(image=add_rec_btn)
        self.add_record_button.set_tooltip_text("Add a new record")
        self.add_record_button.connect("clicked", self.on_add_record_button)
        self.button_box.add(self.add_record_button)
        ## del the selected record button
        pixbuf = Gtk.IconTheme.get_default().load_icon("edit-delete", 48, 0)
        del_rec_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.del_record_button = Gtk.Button(image=del_rec_btn)
        self.del_record_button.set_tooltip_text("Delete the selected record")
        self.del_record_button.connect("clicked", self.on_del_record_button)
        self.button_box.add(self.del_record_button)
        self.del_record_button.set_sensitive(False)
        ## save the database button
        pixbuf = Gtk.IconTheme.get_default().load_icon("document-save", 48, 0)
        save_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.save_button = Gtk.Button(image=save_btn)
        self.save_button.set_tooltip_text("Save the database")
        self.save_button.connect("clicked", self.on_save_button)
        self.button_box.add(self.save_button)
        ## export the selected item button
        pixbuf = Gtk.IconTheme.get_default().load_icon("go-up", 48, 0)
        exp_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.export_button = Gtk.Button(image=exp_btn)
        self.export_button.set_tooltip_text("Export the selected item")
        self.export_button.connect("clicked", self.on_export_button)
        self.export_button.set_sensitive(False)
        self.button_box.add(self.export_button)
        ## export the database button
        pixbuf = Gtk.IconTheme.get_default().load_icon("go-up", 48, 0)
        exp_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.exportall_button = Gtk.Button(image=exp_btn)
        self.exportall_button.set_tooltip_text("Export the database")
        self.exportall_button.connect("clicked", self.on_exportall_button)
        self.button_box.add(self.exportall_button)
        ## import a vcf card button
        pixbuf = Gtk.IconTheme.get_default().load_icon("go-down", 48, 0)
        imp_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.import_button = Gtk.Button(image=imp_btn)
        self.import_button.set_tooltip_text("Import a vcf file")
        self.import_button.connect("clicked", self.on_import_button)
        self.button_box.add(self.import_button)
        ## application exit
        pixbuf = Gtk.IconTheme.get_default().load_icon("application-exit", 48, 0)
        close_btn = Gtk.Image.new_from_pixbuf(pixbuf)
        self.close_button = Gtk.Button(image=close_btn)
        self.close_button.set_tooltip_text("Exit")
        self.close_button.connect("clicked", self.exit_program)#Gtk.main_quit)
        self.button_box.add(self.close_button)
        
        ### horizontal box for buttons and data
        self.hbox = Gtk.Box(orientation=0, spacing=0)
        self.vbox.add(self.hbox)
        
        ## vertical box for buttons
        self.lvbox = Gtk.Box(orientation=1, spacing=0)
        self.hbox.add(self.lvbox)
        
        # buttons
        for l in list_chars:
            button = Gtk.Button(label=l)
            button.connect("clicked", self.on_button_clicked)
            self.lvbox.add(button)
        
        ## vertical box for data
        self.dvbox = Gtk.Box(orientation=1, spacing=0)
        self.vbox.add(self.dvbox)
        
        ## treeview
        self.store = Gtk.ListStore(str, str, str, str, str, str)
        
        ## data
        for item in data_list:
            self.store.append(list(item))
        
        ## data filter
        self.current_filter = None
        # the filter
        self.data_filter = self.store.filter_new()
        # the filter function
        self.data_filter.set_visible_func(self.filter_func, data=None)
        
        ## the view
        self.tree = Gtk.TreeView.new_with_model(self.data_filter)
        self.tree.set_hexpand(1)
        
        for i, column_title in enumerate(list_data):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            if i == 0:
                renderer.props.weight_set = True
                renderer.props.weight = Pango.Weight.BOLD
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            renderer.colnr = i
            self.tree.append_column(column)
            renderer.connect("edited", self.text_edited)
        
        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.add(self.tree)
        self.hbox.add(self.scrollable_treelist)
        
        self.tree.connect("button-press-event", self.on_pressed)
        
        ## the label selected
        self.widget_label = '@'
        
        ## selected row
        self.selected_row = None
        
        # the database has been modified
        self.is_modified = 0
        
        ####
        self.window.show_all()
    
    
    # exit the program
    def exit_program(self, *args):
        # the database has been modified
        if self.is_modified == 1:
            # dialog
            dialog = DialogYN(self.window, "Question", "Do you want to exit this program?\nThe database has been modified.")
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                dialog.destroy()
                Gtk.main_quit()
                sys.exit()
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
        else:
            Gtk.main_quit()
            sys.exit()
    
    
    # filter function
    def filter_func(self, model, iter, data):
        if (
            self.current_filter is None
            or self.current_filter == "None"
        ):
            return True
        else:
            return model[iter][0][0].upper() in self.current_filter
    
    
    # 
    def on_button_clicked(self, widget):
        self.widget_label = widget.get_label()
        #
        # all the records
        if self.widget_label == "@":
            self.current_filter = None
            self.data_filter.refilter()
            # only in this page a new record can be added
            self.add_record_button.set_sensitive(True)
            self.save_button.set_sensitive(True)
            self.export_button.set_sensitive(False)
            self.exportall_button.set_sensitive(True)
            self.import_button.set_sensitive(True)
            self.del_record_button.set_sensitive(False)
        # or the chosen ones
        else:
            # we set the current language filter to the button's label
            self.current_filter = widget.get_label()
            # update the filter
            self.data_filter.refilter()
            # disabled
            self.add_record_button.set_sensitive(False)
            self.del_record_button.set_sensitive(False)
            self.save_button.set_sensitive(False)
            self.export_button.set_sensitive(False)
            self.exportall_button.set_sensitive(False)
            self.import_button.set_sensitive(False)
        # unselect all
        self.tree.get_selection().unselect_all()
        # to top
        self.tree.scroll_to_cell(0, None)
        

    # 
    def text_edited(self, widget, path, text):
        # remove ";" and ":" from the text
        text = text.replace(";", "*").replace(":", "*")
        
        idx = widget.colnr
        # no empty text in the first column 
        if idx == 0:
            if text == "" or text == None or text == " ":
                return
        
        if idx != None:
            selection = self.tree.get_selection()
            (model, iter) = selection.get_selected()
            if iter is not None:
                old_text = self.data_filter[iter][idx]
                
                if text != old_text:
                    if idx == 0:
                        if text[0].isalpha() or text[0].isdecimal():
                            self.data_filter[path][idx] = text.replace(";;", ";").replace("\n", " ").upper()
                        else:
                            text2 = 'a'+text[1:]
                            self.data_filter[path][idx] = text2.replace(";;", ";").replace("\n", " ").upper()
                            
                            dialog = Gtk.MessageDialog(
                                transient_for=self.window,
                                flags=0,
                                message_type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.OK,
                                text="Wrong text",
                            )
                            dialog.format_secondary_text(
                                "You have typed: "+text+"\n"
                                "Corrected text: "+text2
                            )
                            dialog.run()
                            
                            dialog.destroy()
                            
                    else:
                        self.data_filter[path][idx] = text.replace("", " ").replace(";;", ";").replace("\n", " ")
                
                    # the database has been modified
                    self.is_modified = 1
    
    
    #  
    def on_pressed(self, tree_view, event):
        # LMB
        if event.button == 1:
            try:
                path, col, x, y = tree_view.get_path_at_pos(event.x, event.y)
            except:
                pass
            pthinfo = self.tree.get_path_at_pos(event.x, event.y)
            if pthinfo != None:
                path,col,cellx,celly = pthinfo
                
                # only in the first tab
                if self.widget_label == '@':
                    # buttons available
                    # only if more than one record is stored
                    if len(self.store) > 1:
                        self.del_record_button.set_sensitive(True)
                    self.export_button.set_sensitive(True)
                # the selected row
                self.selected_row = path
            

    # add a new empty row
    def on_add_record_button(self, w):
        # only in the first tab
        if self.widget_label == '@':
            # insert an empty row
            self.store.insert(0,row=("NEW RECORD", " ", " ", " ", " ", " "))
            # to top
            self.tree.scroll_to_cell(0, None)
    
    
    # delete a row
    def on_del_record_button(self, w):
        # only in the first tab
        if self.widget_label == '@':
            # cannot delete the only record
            if len(self.store) == 1:
                return
            
            # dialog
            dialog = DialogYN(self.window, "Question", "Do you want to delete the selected item?")
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                self.store.remove(self.store.get_iter(self.selected_row))
                # the database has been modified
                self.is_modified = 1
                #
                self.del_record_button.set_sensitive(False)

            dialog.destroy()
            
    
    # save the database
    def on_save_button(self, w):
        self.temp_list = []
        self.store.foreach(self.for_each, None)
        
        save_ret = SR.save_rubrica(self.temp_list)
        if save_ret == 1:
            self.temp_list = []
            # restore the variable
            self.is_modified = 0
            #
            dialog = DialogBox(self.window, "Done.")
            dialog.run()
            dialog.destroy()
        elif save_ret == 2:
            dialog = DialogBox(self.window, "Something went wrong.")
            dialog.run()
            dialog.destroy()
    
    
    # function for the above
    def for_each(self, model, path, iter, data=None):
        self.temp_list.append(model[path][0:])
        
    
    # export the single item
    def on_export_button(self, w):
        selection = self.tree.get_selection()
        (model, iter) = selection.get_selected()
        if iter is not None:
            single_record = model[iter][0:]
            ret = self.select_folder()
            if not ret:
                return
            exp_ret = EI.export_item(single_record, ret)
            if exp_ret == 1:
                dialog = DialogBox(self.window, "Done.")
                dialog.run()
                dialog.destroy()
            elif exp_ret == 2:
                dialog = DialogBox(self.window, "Something went wrong.")
                dialog.run()
                dialog.destroy()
    
    
    # export the database
    def on_exportall_button(self, w):
        #
        ret = self.select_folder()
        if not ret:
            return
        #
        self.temp_list = []
        self.store.foreach(self.for_each, None)
        
        all_ret = ED.export_all(self.temp_list, ret)
        if all_ret == 1:
            dialog = DialogBox(self.window, "Done.")
            dialog.run()
            dialog.destroy()
        elif all_ret == 2:
            dialog = DialogBox(self.window, "Something went wrong.")
            dialog.run()
            dialod.destroy()
        self.temp_list = []
    
    
    # import a vcf file
    def on_import_button(self, w):
        #
        ret = self.select_file()
        
        if not ret:
            return
        
        import_ret = IV.import_vcf(ret)
        if import_ret == 2 or import_ret == [] or import_ret == None:
            dialog = DialogBox(self.window, "Something went wrong with the file\nor the file is empty.")
            dialog.run()
            dialog.destroy()
        else:
            data_list = import_ret
            data_list.sort()
            for el in data_list:
                self.store.insert(0,row=el)
                # to top
                self.tree.scroll_to_cell(0, None)
                # the database has been modified
                self.is_modified = 1
            
            dialog = DialogBox(self.window, "Imported.")
            dialog.run()
            dialog.destroy()
    
    
    # select a folder
    def select_folder(self):
        #
        selected_folder = None
        #
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self.window,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)
        dialog.set_current_folder(HOME)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_folder = dialog.get_filename()
        
        dialog.destroy()
        
        return selected_folder
    
    
    # select file
    def select_file(self):
        #
        selected_file = None
        #
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)
        dialog.set_current_folder(HOME)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_file = dialog.get_filename()
        
        dialog.destroy()
        
        return selected_file


# dialog
class DialogYN(Gtk.Dialog):
    def __init__(self, parent, title, info):
        Gtk.Dialog.__init__(self, title=title, transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=info)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


#####################

if __name__ == "__main__":
    app = App()
    Gtk.main()
