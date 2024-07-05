from pathlib import Path

from pywebio import start_server
from pywebio.output import put_text, put_table, put_collapse, put_row, put_column, use_scope, put_grid, put_scrollable, put_scope, put_button
from pywebio.input import input_group
from pywebio.pin import put_select, put_input, pin, pin_on_change, pin_update
from pywebio.session import run_js

class App:
    def __init__(self):
        self.selected_items = []
        self.workspaces = {
            "ws1": {
                "subfolder": ["file1", "file2"]
            },
            "ws2": {
                "subfolder": ["file3", "file3"]
            }
        }

    def update_selected_items(self, values: list):
        self.selected_items = list(set(self.selected_items + values))
        self.refresh_selected_items_display()

    def refresh_selected_items_display(self):
        '''A scope is a predefined area that can be modified later.'''
        with use_scope('selected_items_scope', clear=True):
            put_scrollable(put_column([
                put_text(item) for item in self.selected_items
            ]), height=300, keep_bottom=False)

    def clear_selections(self):
        for ws_name in self.workspaces.keys():
            pin_update(ws_name, value=[])
        self.selected_items = []
        self.refresh_selected_items_display()

    def main(self):

        put_row([
            put_column([ 
                put_select(name=ws_name, options=ws_files["subfolder"], multiple=True, label=ws_name)
                for ws_name, ws_files in self.workspaces.items()
            ], size='40%'),
            put_column(),
            put_column([
                put_text("Selected Items:"),
                put_scope(name='selected_items_scope')
            ], size='30%'),
        ])
        put_row([
            put_column(),
            put_column(),
            put_button("Clear all selections", onclick=self.clear_selections)
            ])

        # Set up pin callbacks for each workspace
        # This works because the workspace name is set as the pin name
        for ws_name in self.workspaces.keys():
            pin_on_change(ws_name, onchange=self.update_selected_items)


        # Initialize the display
        self.refresh_selected_items_display()

if __name__ == '__main__':
    app = App()
    start_server(app.main, port=8080, debug=True)
