"""Module for building the UI with tkinter

UI consists of 
    root - Base Tk
        content - Frame, main frame
            f_left - Frame, includes game control, timers, ball control and action buttons
            f_right - Frame, details of each action button
"""

from tkinter import *
from tkinter import ttk

import re

from classes import Game

root = Tk()
root.title("Tilastoseuranta")

# --- Button styles STARTS
white_style = ttk.Style()
white_style.configure("BW.TButton", foreground="white")
# --- Button styles ENDS

# --- Validation functions STARTS
def check_num(value):
    """Checks input of game total time entry field

    Args:
        value (Any): input entry from user
    """
    return re.match('^[0-9]*$', value) is not None and len(value) <= 3
check_num_wrapper = (root.register(check_num), '%P')
# --- Validation functions ENDS

# --- Main frame STARTS
content = ttk.Frame(root, width=600, height=600, borderwidth=5, relief='ridge')
content.grid(column=0, row=0)

## --- Left frame STARTS
f_left = ttk.Frame(content, width=200, height=600, borderwidth=5, relief='ridge')
f_left.grid(column=0, row=0)

### --- Game control STARTS
f_game_control = ttk.Frame(f_left, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_game_control.grid(column=0, row=0)

### --- Variables STARTS
game_total_time = IntVar()
### --- Variables ENDS

ttk.Label(f_game_control, text="Peliaika (min):").grid(row=0, column=0)
e_game_total_time = ttk.Entry(f_game_control, textvariable=game_total_time, validate='key', validatecommand=check_num_wrapper, width=3)
e_game_total_time.grid(row=0, column=1)

b_game_start = ttk.Button(f_game_control, text="Aloita")
#b_game_pause = ttk.Button(f_game_control, text="Tauko")
b_game_start.grid(column=0, row=1)
#b_game_pause.grid(column=0, row=1)
### --- Game control ENDS

#### --- Teams, clock and score STARTS
f_teams_clock_score = ttk.Frame(f_left, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_teams_clock_score.grid(column=1, row=0)

##### --- Variables STARTS
game_timer = StringVar()
game_timer_remaining = StringVar()
##### --- Variables ENDS

##### --- Timers STARTS
l_game_timer = ttk.Label(f_teams_clock_score, text="Pelikello", textvariable=game_timer)
l_game_timer_remaining = ttk.Label(f_teams_clock_score, text="Peliaikaa jäljellä", textvariable=game_timer_remaining)

l_game_timer.grid(column=1, row=0)
l_game_timer_remaining.grid(column=2, row=0, sticky=W)
##### --- Timers ENDS

##### --- Teams STARTS
l_home_team = ttk.Label(f_teams_clock_score, text="Kotijoukkue")
l_away_team = ttk.Label(f_teams_clock_score, text="Vierasjoukkue")
l_home_team.grid(column=0, row=1)
l_away_team.grid(column=2, row=1)

ttk.Label(f_teams_clock_score, text="-").grid(column=1, row=1)
##### --- Teams ENDS
#### --- Teams, clock and score ENDS

#### --- Ball control frame STARTS
f_ball_control = ttk.Frame(f_left, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_ball_control.grid(column=0, row=1, columnspan=2)

##### --- Variables STARTS
ball_control_check = StringVar()
##### --- Variables ENDS

ttk.Label(f_ball_control, text="Pallonhallinta").grid(column=0, row=0)

##### Radio buttons
rb_ball_control_home = ttk.Radiobutton(
    master=f_ball_control,
    text="Kotijoukkue",
    variable=ball_control_check,
    value='home')
rb_ball_control_out = ttk.Radiobutton(
    master=f_ball_control,
    text="Ei pelissä",
    variable=ball_control_check,
    value='neither')
rb_ball_control_away = ttk.Radiobutton(
    master=f_ball_control,
    text="Vierasjoukkue",
    variable=ball_control_check,
    value='away')

rb_ball_control_home.grid(column=0, row=1)
rb_ball_control_out.grid(column=1, row=1)
rb_ball_control_away.grid(column=2, row=1)
#### --- Ball control frame ENDS

#### --- Action buttons frame STARTS
f_action_buttons = ttk.Frame(master=f_left, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_action_buttons.grid(column=0, row=2, columnspan=2)

##### --- Action buttons STARTS
b_pass = ttk.Button(f_action_buttons, text="Syöttö (sy)")
#b_shoot = ttk.Button(f_action_buttons, text="Laukaus (la)")
#b_goal = ttk.Button(f_action_buttons, text='Maali (mm)')
#b_goalkick = ttk.Button(f_action_buttons, text="Maalipotku (mp)")
#b_throw_in = ttk.Button(f_action_buttons, text="Sivurajaheitto (srh)")
#b_free_kick = ttk.Button(f_action_buttons, text="Vapaapotku (vp)")
#b_remove = ttk.Button(f_action_buttons, text="Poista edellinen (po)")

b_pass.grid(column=0, row=0)
#b_shoot.grid(column=1, row=0)
#b_goal.grid(column=2, row=0)
#b_throw_in.grid(column=0, row=1)
#b_free_kick.grid(column=1, row=1)
#b_remove.grid(column=0, row=2, columnspan=3, pady=10)

# TODO: Check if could be binded only to left frame
root.bind('<KeyPress-s><KeyPress-y>') # Pass
#root.bind('<KeyPress-l><KeyPress-a>') # Shhot
#root.bind('<KeyPress-m><KeyPress-m>') # Goal
#root.bind('<KeyPress-m><KeyPress-p>') # Goalkick
#root.bind('<KeyPress-s><KeyPress-r><KeyPress-h>') # Throw-in
#root.bind('<KeyPress-v><KeyPress-p>') # Free kick
#root.bind('<KeyPress-k><KeyPress-p>') # Corner kick
#root.bind('<KeyPress-p><KeyPress-o>') # Remove
##### --- Action buttons ENDS

## --- Left frame ENDS

## --- Right frame STARTS
f_right = ttk.Frame(content, width=400, height=600, borderwidth=5, relief='ridge')
f_right.grid(column=1, row=0)

### --- Players STARTS
f_pass_players = ttk.Frame(master=f_right, borderwidth=5, relief='ridge')
f_pass_players.grid(column=0, row=0)

l_players_text_home = ttk.Label(f_pass_players, text="Home team players")
l_players_text_away = ttk.Label(f_pass_players, text="Away team players")

l_players_text_home.grid(column=0, row=0)
l_players_text_away.grid(column=0, row=2)

for child in f_right.winfo_children():
    child.grid_configure(padx=5, pady=5)
## --- Right frame ENDS

## --- Frame bottom STARTS
f_bottom = ttk.Frame(master=content, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_bottom.grid(column=0, row=1, columnspan=2)

f_stats = ttk.Frame(master=f_bottom, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_stats.grid(column=0, row=0)

### --- Pass stats STARTS
f_pass_stats = ttk.Frame(f_stats, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_pass_stats.grid(column=0, row=0)

#### --- Variables STARTS
pass_stats_own_home = StringVar() # passes to own team
pass_stats_own_away = StringVar()
pass_stats_not_own_home = StringVar() # passes to opponent team/out of field
pass_stats_not_own_away = StringVar()
pass_stats_percentage_home = StringVar()
pass_stats_percentage_away = StringVar()
pass_stats_longest_pass_chain_home = StringVar()
pass_stats_longest_pass_chain_away = StringVar()
#### --- Variables ENDS

#### --- Pass stats texts STARTS
ttk.Label(f_pass_stats, text="Kotijoukkue").grid(column=1, row=0, sticky=W)
ttk.Label(f_pass_stats, text="Vierasjoukkue").grid(column=2, row=0, sticky=W)

ttk.Label(f_pass_stats, text="Syötöt omille").grid(column=0, row=1, sticky=W)
ttk.Label(f_pass_stats, text="Syötöt vastustajalle").grid(column=0, row=2, sticky=W)
ttk.Label(f_pass_stats, text="Syöttö-%").grid(column=0, row=3, sticky=W)
ttk.Label(f_pass_stats, text="Pisin syöttöketju").grid(column=0, row=4, sticky=W)
#### --- Pass stats texts ENDS

#### --- Pass stats values STARTS
l_pass_stats_own_home = ttk.Label(f_pass_stats, textvariable=pass_stats_own_home)
l_pass_stats_own_home.grid(column=1, row=1, sticky=W)
l_pass_stats_own_away = ttk.Label(f_pass_stats, textvariable=pass_stats_own_away)
l_pass_stats_own_away.grid(column=2, row=1, sticky=W)

l_pass_stats_not_own_home = ttk.Label(f_pass_stats, textvariable=pass_stats_not_own_home)
l_pass_stats_not_own_home.grid(column=1, row=2, sticky=W)
l_pass_stats_not_own_away = ttk.Label(f_pass_stats, textvariable=pass_stats_not_own_away)
l_pass_stats_not_own_away.grid(column=2, row=2, sticky=W)

l_pass_stats_percentage_home = ttk.Label(f_pass_stats, textvariable=pass_stats_percentage_home)
l_pass_stats_percentage_home.grid(column=1, row=3, sticky=W)
l_pass_stats_percentage_away = ttk.Label(f_pass_stats, textvariable=pass_stats_percentage_away)
l_pass_stats_percentage_away.grid(column=2, row=3, sticky=W)

l_pass_stats_longest_pass_chain_home = ttk.Label(f_pass_stats, textvariable=pass_stats_longest_pass_chain_home)
l_pass_stats_longest_pass_chain_home.grid(column=1, row=4, sticky=W)
l_pass_stats_longest_pass_chain_away = ttk.Label(f_pass_stats, textvariable=pass_stats_longest_pass_chain_away)
l_pass_stats_longest_pass_chain_away.grid(column=2, row=4, sticky=W)
#### --- Pass stats values ENDS
### --- Pass stats ENDS

### --- Ball control stats STARTS
f_ball_control_stats = ttk.Frame(f_stats, padding="3 3 3 3", borderwidth=5, relief='ridge')
f_ball_control_stats.grid(column=1, row=0)

#### --- Variables STARTS
bc_timer_home_team = StringVar()
bc_timer_away_team = StringVar()
bc_timer_neither = StringVar()
bc_pc_home_team = StringVar()
bc_pc_away_team = StringVar()
#### --- Variables ENDS

ttk.Label(f_ball_control_stats, text="Pallonhallinta").grid(row=0, column=0, columnspan=4, sticky=W)
ttk.Label(f_ball_control_stats, text="Kotijoukkue").grid(row=1, column=1)
ttk.Label(f_ball_control_stats, text="Vierasjoukkue").grid(row=1, column=2)
ttk.Label(f_ball_control_stats, text="Ei kumpikaan").grid(row=1, column=3)

ttk.Label(f_ball_control_stats, text="Pallonhallinta-aika").grid(column=0, row=2, sticky=W)
ttk.Label(f_ball_control_stats, text="Pallonhallinta-%").grid(column=0, row=3, sticky=W)

#### --- Ball control timers STARTS
l_home_team_bc_timer = ttk.Label(f_ball_control_stats, textvariable=bc_timer_home_team)
l_away_team_bc_timer = ttk.Label(f_ball_control_stats, textvariable=bc_timer_away_team)
l_neather_bc_timer = ttk.Label(f_ball_control_stats, textvariable=bc_timer_neither)

l_home_team_bc_pc = ttk.Label(f_ball_control_stats, textvariable=bc_pc_home_team)
l_away_team_bc_pc = ttk.Label(f_ball_control_stats, textvariable=bc_pc_away_team)

l_home_team_bc_timer.grid(column=1, row=2)
l_away_team_bc_timer.grid(column=2, row=2)
l_neather_bc_timer.grid(column=3, row=2)

l_home_team_bc_pc.grid(column=1, row=3)
l_away_team_bc_pc.grid(column=2, row=3)
#### --- Ball control timers ENDS
### --- Ball control stats ENDS
## --- Frame bottom ENDS

def update_pass_transfer_stats(game:Game):
    """Updates pass stats frame in ui

    Args:
        game: game object
    """

    for team in [game.home_team, game.away_team]:
        
        pass_code_to_own = team.code() + "1"
        pass_code_to_opponent = team.code() + "0"
        pass_code_to_out = team.code() + "2"
        
        s, longest = game.passing_chains(pass_code_to_own)

        pass_codes = [p.code() for p in team.get_passes()]

        try:
            team.pass_transfer_pct = pass_codes.count(pass_code_to_own) / len(pass_codes)
        except ZeroDivisionError:
            team.pass_transfer_pct = 0
        
        if team == game.home_team:
            pass_stats_own_home.set(f"{pass_codes.count(pass_code_to_own)}")
            pass_stats_not_own_home.set(f"{pass_codes.count(pass_code_to_opponent) + pass_codes.count(pass_code_to_out)}")
            pass_stats_percentage_home.set(f"{team.pass_transfer_pct:.1%}")
            pass_stats_longest_pass_chain_home.set(f"{longest}")
        elif team == game.away_team:
            pass_stats_own_away.set(f"{pass_codes.count(pass_code_to_own)}")
            pass_stats_not_own_away.set(f"{pass_codes.count(pass_code_to_opponent) + pass_codes.count(pass_code_to_out)}")
            pass_stats_percentage_away.set(f"{team.pass_transfer_pct:.1%}")
            pass_stats_longest_pass_chain_away.set(f"{longest}")