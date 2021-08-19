from gi.repository import Gtk

@Gtk.Template(resource_path='/com/github/alex11br/themechanger/searchablethemelist.ui')
class SearchableThemeList(Gtk.Bin):
    __gtype_name__ = 'SearchableThemeList'

    themesSearchEntry = Gtk.Template.Child()
    themesScrolledWindow = Gtk.Template.Child()
    themesTreeView = Gtk.Template.Child()
    themesTreeViewSelection = Gtk.Template.Child()

    def __init__(self, themesTreeViewModel, selectedTheme, onThemeSelectedCallback, hasPixbuf=False, *args):
        Gtk.Bin.__init__(self, *args)

        self.selectedTheme = selectedTheme
        self.onThemeSelectedCallback = onThemeSelectedCallback
        self.setThemesTreeViewModel(themesTreeViewModel)

        themeColumn = Gtk.TreeViewColumn("Theme")

        if hasPixbuf:
            pixbufCell = Gtk.CellRendererPixbuf()
            themeColumn.pack_start(pixbufCell, False)
            themeColumn.add_attribute(pixbufCell, "pixbuf", 2)
            
        nameCell = Gtk.CellRendererText()
        themeColumn.pack_start(nameCell, True)
        themeColumn.add_attribute(nameCell, "text", 0)

        self.themesTreeView.append_column(themeColumn)

    def setThemesTreeViewModel(self, themesTreeViewModel):
        self.themesTreeViewModelFiltered = themesTreeViewModel.filter_new()
        self.themesTreeViewModelFiltered.set_visible_func(self.filterFunc)
        self.themesTreeView.set_model(self.themesTreeViewModelFiltered)

        for row in self.themesTreeViewModelFiltered:
            if self.selectedTheme == row[1]:
                self.themesTreeViewSelection.select_iter(row.iter)
                self.themesTreeView.scroll_to_cell(
                    self.themesTreeViewModelFiltered.get_path(row.iter),
                    None, False
                )
                break

    def setScrolledWindowOverlayScrolling(self, state):
        self.themesScrolledWindow.set_overlay_scrolling(state)
        
    def filterFunc(self, model, treeiter, data):
        return self.themesSearchEntry.get_text().lower() in model[treeiter][0].lower()

    @Gtk.Template.Callback()
    def onThemeSelected(self, selection):
        model, treeiter = selection.get_selected()
        self.selectedTheme = model[treeiter][1]
        self.onThemeSelectedCallback(self.selectedTheme)

    @Gtk.Template.Callback()
    def onChangeFilter(self, searchentry):
        self.themesTreeViewModelFiltered.refilter()
        