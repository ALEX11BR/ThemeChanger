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

    def selectTheme(self):
        for row in self.themesTreeViewModelFiltered:
            if self.selectedTheme == row[1]:
                self.themesTreeViewSelection.select_iter(row.iter)
                self.themesTreeView.scroll_to_cell(
                    self.themesTreeViewModelFiltered.get_path(row.iter),
                    None, False
                )
                return
        # Maybe the selectedTheme isn't in the model; we'll properly handle this case here
        firstRow = self.themesTreeViewModelFiltered[0]
        self.selectedTheme = firstRow[1]
        self.themesTreeViewSelection.select_iter(firstRow.iter)
        self.themesTreeView.scroll_to_point(0, 0)

    def setThemesTreeViewModel(self, themesTreeViewModel):
        self.themesTreeViewModelFiltered = themesTreeViewModel.filter_new()
        self.themesTreeViewModelFiltered.set_visible_func(self.filterFunc)
        self.themesTreeView.set_model(self.themesTreeViewModelFiltered)

        self.selectTheme()

    def setScrolledWindowOverlayScrolling(self, state):
        self.themesScrolledWindow.set_overlay_scrolling(state)
        
    def filterFunc(self, model, treeiter, data):
        return self.themesSearchEntry.get_text().lower() in model[treeiter][0].lower()

    @Gtk.Template.Callback()
    def onThemeSelected(self, selection):
        model, treeiter = selection.get_selected()
        # Sometimes the TreeSelection "changed" signal gets triggered when nothing has happened (as the docs say)
        # This makes this function run multiple times when searching stuff for some reason
        # In this case the selection is None, which breaks the theme name getting mechanism below; so we shield against this case
        if not treeiter:
            return
        self.selectedTheme = model[treeiter][1]
        self.onThemeSelectedCallback(self.selectedTheme)

    @Gtk.Template.Callback()
    def onChangeFilter(self, searchentry):
        self.themesTreeViewModelFiltered.refilter()
        # This handles the case in which the newly filtered model doen't have the selectedTheme anymore
        self.selectTheme()
        