#!/usr/bin/env python3
'''
App for request and show russian shares market and currency data,
for one share from app input or bunch of shares (portfolio) stored in config.py.
App also shows difference between share buy price and share price for input date.
If input date data not stored it'll be requested from internet
GUI using moex.py as main module for data manipulations
'''
import datetime as dt
import tkinter as tk
from threading import Thread

from moex import get_shares_info, update_market_history
from moex import export_data, get_last_workday
from config import boards, export_file, shares_pool, currency_pool


class SharesApp(tk.Tk):
    '''
    Main class for application
    '''
    def __init__(self):
        tk.Tk.__init__(self, className="Moex")

        main_bg = "#222"
        main_font = "roboto, 12"
        label_col = {"bg": "#222", "fg": "#b38600"}
        btn_green = {"bg": "#28a745", "fg": "#222", "hover": "#1e7b34"}
        btn_yellow = {"bg": "#ffc107", "fg": "#222", "hover": "#b38600"}
        btn_grey = {"bg": "#6c757d", "fg": "#eee", "hover": "#474d52"}
        but_hl = "#474d52"

        self.title("Moex")
        self.configure(background=main_bg)
        for column in range(4):
            self.grid_columnconfigure(column, minsize=180)
        for row in [0, 1, 5]:
            self.grid_rowconfigure(row, minsize=60)
        for row in [3, 4]:
            self.grid_rowconfigure(row, minsize=40)
        self.grid_rowconfigure(2, minsize=280)

        # Header
        # Date entry
        self.date_entry = tk.Entry(self, text = "date",
           bg=label_col["bg"], fg=label_col["fg"], font=main_font, width=10)
        self.source_date = tk.StringVar()
        # if today week day is sauturday, sunday or monday, date set to friday
        self.source_date.set(get_last_workday())

        self.date_entry["textvariable"] = self.source_date
        self.date_entry.grid(row=0, column=0)

        # Share entry
        self.share_entry = tk.Entry(self, text = "Share name",
            bg=label_col["bg"], fg=label_col["fg"], font=main_font, width=10)
        self.source_share = tk.StringVar()
        self.source_share.set("FXUS")
        self.share_entry["textvariable"] = self.source_share
        self.share_entry.grid(row=0, column=1)

        # Share type menu
        self.MenuBttn = tk.Menubutton(self, text = "Type",
            relief = "raised", width=10, bg=btn_yellow["bg"],
            fg=btn_yellow["fg"], highlightbackground=but_hl,
            activebackground=btn_yellow["hover"], activeforeground=btn_yellow["fg"],
            font=main_font)
        self.share_type = tk.StringVar()
        self.share_type.set = None
        self.Menu = tk.Menu(self.MenuBttn, tearoff = 0)
        for board in boards:
            self.Menu.add_radiobutton(
                label = board["name"], variable = self.share_type,
                value = board["board"], command=self.set_share_type,
                activebackground=btn_yellow["hover"], activeforeground=btn_yellow["fg"],
                font=main_font)
        self.MenuBttn["menu"] = self.Menu
        self.MenuBttn.grid(row=0, column=2)

        # Get share button
        self.get_share_button = tk.Button(self, text="Share info", command=show_share,
            width=8, bg=btn_green["bg"], fg=btn_green["fg"],
            highlightbackground=but_hl, activebackground=btn_green["hover"],
            activeforeground=btn_green["fg"], font=main_font)
        self.get_share_button.grid(row=0, column=3)
        # End of header

        # Main buttons
        self.update_button = tk.Button(self, text="Update", command=update_market,
            width=8, bg=btn_yellow["bg"], fg=btn_yellow["fg"],
            highlightbackground=but_hl, activebackground=btn_yellow["hover"],
            activeforeground=btn_yellow["fg"], font=main_font)
        self.update_button.grid(row=1, column=0)

        self.export_button = tk.Button(self, text="Export", command=export_to_file,
            width=8, bg=btn_yellow["bg"], fg=btn_yellow["fg"],
            highlightbackground=but_hl, activebackground=btn_yellow["hover"],
            activeforeground=btn_yellow["fg"], font=main_font)
        self.export_button.grid(row=1, column=1)

        self.portfolio_button = tk.Button(self, text="Portfolio",
            command=show_portfolio, width=8, bg=btn_green["bg"],
            fg=btn_green["fg"], highlightbackground=but_hl,
            activebackground=btn_green["hover"], activeforeground=btn_green["fg"],
            font=main_font)
        self.portfolio_button.grid(row=1, column=3)

        # Table frame
        self.table_frame = tk.Frame(self, bg=label_col["bg"], width=640, height=240)
        self.table_frame.grid(row=2, column=0, columnspan=4)
        # End of table frame

        self.warnings_label = tk.Label(self, text = " ",
            bg=label_col["bg"], fg=label_col["fg"], font=main_font)
        self.warnings_label.grid(row=3, column=0, columnspan=4)

        self.currency_label = tk.Label(self, text = " ",
            bg=label_col["bg"], fg=label_col["fg"], font=main_font)
        self.currency_label.grid(row=4, column=0, columnspan=4)

        self.quit_button = tk.Button(self, text="QUIT", command=quit, padx=30,
            bg=btn_grey["bg"], fg=btn_grey["fg"], highlightbackground=but_hl,
            activebackground=btn_grey["hover"], activeforeground=btn_grey["fg"],
            font=main_font)
        self.quit_button.grid(row=5, column=0, columnspan=4)

    def set_share_type(self):
        '''
        Set button name for selected share type
        '''
        board_attrs = [x for x in boards if x["board"] == self.share_type.get()][0]

        self.MenuBttn.configure(text=f"{board_attrs['name']}")


def gen_table(input_dict,shares_pool_gen):
    '''
    Function for generate table with shares data
    '''
    def set_share_buy(share):
        '''
        Return share attributes from saved pool in config.py
        for calculate "buy-sell" difference
        '''
        for one_share in shares_pool:
            if one_share["name"] in share[1]:
                return one_share
        return None


    label_bg = "white"
    label_fg = "black"
    main_font = "roboto, 12"
    title_bg = "gray"
    title_fg = "black"
    title_font = "roboto, 12 bold"

    try:
        for widget in app.table_title.winfo_children():
            widget.destroy()
        for widget in app.table.winfo_children():
            widget.destroy()
    except:
        pass

    # Table configuration
    app.table_title = tk.Frame(app.table_frame, bg=title_bg, height=40)
    app.table_title.grid(row=0, column=0)

    app.table = tk.Frame(app.table_frame, bg=label_bg, height=240)
    app.table.grid(row=1, column=0)


    for column in [0, 1]:
        app.table_title.grid_columnconfigure(column, minsize=150)
        app.table.grid_columnconfigure(column, minsize=150)
    for column in [2,3]:
        app.table_title.grid_columnconfigure(column, minsize=120)
        app.table.grid_columnconfigure(column, minsize=120)
    app.table_title.grid_columnconfigure(4, minsize=100)
    app.table.grid_columnconfigure(4, minsize=100)

    app.table_title.grid_rowconfigure(0, minsize=40)
    if len(input_dict) > 5:
        rows = len(input_dict)
    else:
        rows = 5
    for row in range(0,rows):
        app.table.grid_rowconfigure(row, minsize=40)

    # Table title
    app.share_name_label = tk.Label(app.table_title, text = "Name",
        bg=title_bg, fg=title_fg, font=title_font)
    app.share_name_label.grid(row=0, column=0)
    app.share_index_label = tk.Label(app.table_title, text = "Index",
        bg=title_bg, fg=title_fg, font=title_font)
    app.share_index_label.grid(row=0, column=1)
    app.share_buy_label = tk.Label(app.table_title, text = "Buy Price",
        bg=title_bg, fg=title_fg, font=title_font)
    app.share_buy_label.grid(row=0, column=2)
    app.share_close_label = tk.Label(app.table_title, text = "Date Price",
        bg=title_bg, fg=title_fg, font=title_font)
    app.share_close_label.grid(row=0, column=3)
    app.share_change_label = tk.Label(app.table_title, text = "Change %",
        bg=title_bg, fg=title_fg, font=title_font)
    app.share_change_label.grid(row=0, column=4)
    # End of table title

    # Table
    i = 0
    for share in input_dict:
        share_buy = set_share_buy(input_dict[share])
        if share_buy and share_buy['price'] != 0:
            diff_price = round(
                (input_dict[share][2] - share_buy['price']) /
                share_buy['price'] * 100, 2 )
            main_font_diff = "roboto, 12 bold"
            if diff_price > 0:
                label_diff = "green"
            elif diff_price < 0:
                label_diff = "red"
            else:
                label_diff = label_fg
                main_font_diff = main_font
        else:
            share_buy = {"price":0}
            diff_price = 0
            label_diff = label_fg
            main_font_diff = main_font

        app.table_name_label = tk.Label(app.table, text = f"{input_dict[share][0]}",
            wraplength=150, bg=label_bg, fg=label_fg, font=main_font + " bold")
        app.table_name_label.grid(row=i, column=0)
        app.table_index_label = tk.Label(app.table, text = f"{input_dict[share][1]}",
            bg=label_bg, fg=label_fg, font=main_font)
        app.table_index_label.grid(row=i, column=1)
        app.table_buy_label = tk.Label(app.table, text = f"{share_buy['price']}",
            bg=label_bg, fg=label_fg, font=main_font)
        app.table_buy_label.grid(row=i, column=2)
        app.table_close_label = tk.Label(app.table, text = f"{input_dict[share][2]}",
            bg=label_bg, fg=label_fg, font=main_font)
        app.table_close_label.grid(row=i, column=3)
        app.table_change_label = tk.Label(app.table, text = f"{diff_price}",
            bg=label_bg, fg=label_diff, font=main_font_diff)
        app.table_change_label.grid(row=i, column=4)
        i += 1
    # End of table

def check_date(date):
    '''
    Checking entry date format
    '''
    try:
        date = dt.date.fromisoformat(date)
    except:
        app.warnings_label.configure(text = str("Wrong date format." +
            "Should be ISO: 2021-05-18"))
        return None
    return date

def update_market():
    '''
    Button function to update market
    '''
    date = check_date(app.source_date.get())
    if not date:
        return
    buttons = [app.update_button, app.get_share_button,
               app.portfolio_button, app.export_button]
    app.warnings_label.configure(text = "Updating...")
    update_status = update_market_history(date)
    app.after(1000, lambda: app.warnings_label.configure(text = f"{update_status}"))
    show_currency()

def show_share():
    '''
    Button function for request one share
    '''
    app.warnings_label.configure(text = " ")
    date = check_date(app.source_date.get())
    if not date:
        return
    share_name = app.source_share.get()
    share_type = app.share_type.get()
    if not share_type:
        return app.warnings_label.configure(text = "Share type not set")
    if not share_name:
        return app.warnings_label.configure(text = "Share name not set")

    one_share = [ { "board": share_type, "name": share_name,
                    "buy_date": "None", "price": 0 } ]

    input_dict = get_shares_info(date, one_share)
    if not input_dict:
        return app.warnings_label.configure(text = "Share not found")
    th_gen = Thread(target=gen_table, args=(input_dict, shares_pool))
    th_gen.start()


def show_portfolio():
    '''
    Request and show portfolio shares stored in config.py
    '''
    app.warnings_label.configure(text = " ")
    date = check_date(app.source_date.get())
    if not date:
        return
    input_dict = get_shares_info(date, shares_pool)
    if not input_dict:
        return app.warnings_label.configure(text = "Shares not found")
    th_gen = Thread(target=gen_table, args=(input_dict, shares_pool))
    th_gen.start()

def show_currency():
    '''
    Request and show currency-rub and bitcoin-usd rates at bottom
    '''
    date = check_date(app.source_date.get())
    if not date:
        return
    input_dict = get_shares_info(date, currency_pool)
    if not input_dict:
        return app.currency_label.configure(text = "Currency not found")

    show_list = []
    for share in input_dict:
        cur_name, cur_rate = input_dict[share][1:3]
        cur_name = cur_name[:3] + "-" + cur_name[3:]
        show_list.append(f"{cur_name}: {cur_rate}")
    show_string = '    '.join(show_list)
    app.currency_label.configure(text = show_string)

def export_to_file():
    '''
    Export data for shares in config.py to a file
    '''
    app.warnings_label.configure(text = " ")
    date = check_date(app.source_date.get())
    if not date:
        return

    if not export_data(date):
        return app.warnings_label.configure(text = "Shares not found")

    app.warnings_label.configure(text = f"File exported: {export_file}")

def at_start():
    '''
    Threading for startup queries
    '''
    th1 = Thread(target=update_market, args=())
    th1.start()
    th1.join()
    th2 = Thread(target=show_currency, args=())
    th2.start()
    th3 = Thread(target=show_portfolio, args=())
    th3.start()

def quit():
    '''
    Button function for quit app
    '''
    app.destroy()

if __name__ == "__main__":
    app = SharesApp()
    th = Thread(target=at_start, args=())
    th.start()
    app.mainloop()
