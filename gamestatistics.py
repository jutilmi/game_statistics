# tilastoseuranta/gamestatistics.py

"""Game statistics module

Attributes:
    g (classes.Game): basic game
    g.start_time (time): wall clock time when the game was started
    p (classes.GameEvent): global game event

Functions:
    - 'create_pass_event(team, event)': initialize a pass event from ui binded event
    - 'finalize_pass_event(game_event, team, event)': finalize a pass event from ui binded event
    - 'muotoile_peliaika(sekunnit)': modifies wall clock time based on seconds given to show minutes and seconds properly
    - 'update_time': updates game timer
"""

from time import time
from math import floor
from tkinter import Event, Tk

import ui

from classes import Game, GameEvent, Team, Pass

# Initialize new game instance and add details
g = Game('game.json')
ui.ball_control_check.set('home') # Setting home team as the default starting team user can change before starting the game

g.ball_control_team = g.home_team
g.ball_control_start_time = 0

# Game total time from json file, but time can be modified before period is started
ui.e_game_total_time.insert(0, str(g.total_game_time))
ui.e_game_total_time.delete(2, 'end')

ui.l_home_team['text'] = g.home_team.name
ui.l_away_team['text'] = g.away_team.name

def create_pass_event(team:Team, event:Event):
    """Initializes a game event based on ui event

    Args:
        team: team which passes the ball
        event: player number click event in ui

    Output:
        initialize new global p (classes.GameEvent) variable
        if game is not started, returns None
    """

    global p

    if not g.started:
        p = None
        return None

    passing_player = team.get_player(event.widget.cget('text'))
    
    p = GameEvent(ui.game_timer.get(), passing_player)

def finalize_pass_event(game_event:GameEvent, team:Team, event:Event):
    """Finalize pass event based in initialized game event
    
    Args:
        game_event: Previously created game_event
        team: pass receiving team
        event: player number click event in ui
    
    Return:
        if game_event.initialized_player.team == team -> None, Pass event not created
        and returns None
        if game.started = False, returns None
    
    Output:
        Appends pass event to g.events list and updates pass statistics
    """

    global p
    
    if not p:
        return None
    
    if team is not None:
        receiving_player = team.get_player(event.widget.cget('text'))
    else:
        receiving_player = 'out'

    # Return nothing if self pass
    if game_event.initialization_player == receiving_player:
        return None

    # Changed ball control if passed to opponent
    if receiving_player == 'out':
        ui.ball_control_check.set('neither')
    else:
        if receiving_player.team == g.home_team:
            ui.ball_control_check.set('home')
        else:
            ui.ball_control_check.set('away')

    pass_transfer = Pass(game_event=game_event, receiving_player=receiving_player)

    g.events.append(pass_transfer)

    p = None # Set global GameEvent variable to None
  
    ui.update_pass_transfer_stats(g)
    
def format_timer(seconds:int) -> str:
    """Formats game timer and ball control timer from seconds to minute and seconds
    
    Args:
        seconds: time elapsed
    
    Examples:
        >>> format_timer(300)
        '05:00'
        >>> format_timer(1274)
        '21:14'
    
    Return:
        timer in a a form minutes:seconds, i.e. 04:38
    """
    
    if seconds < 60:
        minutes = 0
    
    else:
        minutes = int(seconds // 60)
        seconds = seconds - minutes * 60
        
    return f"{minutes:02d}:{seconds:02d}"

def update_time():
    """Updates and formats game timer in 200 ms interval
    
    Output:
        modifies ui.game_timer and g.game_timer
    """
    
    g.game_timer = floor(time()) - g.start_time
    game_timer_left = g.total_game_time * 60 - g.game_timer
    ui.game_timer.set(format_timer(g.game_timer)) # + " : (" +  )
    ui.game_timer_remaining.set(
        '(' + format_timer(game_timer_left) + ')')

    update_ball_control_timers()

    ui.f_teams_clock_score.after(200, update_time)

def update_ball_control_timers(*args):
    """Updates ball control timers depending on a team who controls the ball
    """

    # Defining local ball control team
    if ui.ball_control_check.get() == 'home':
        ball_control_team = g.home_team
    elif ui.ball_control_check.get() == 'away':
        ball_control_team = g.away_team
    elif ui.ball_control_check.get() == 'neither':
        ball_control_team = None
    
    if g.ball_control_team is None:
        ball_control_timer_neither = g.game_timer - (g.home_team.ball_control_timer + g.away_team.ball_control_timer)
        ui.bc_timer_neither.set(format_timer(ball_control_timer_neither))
    else:
        g.ball_control_team.ball_control_timer += g.game_timer - g.ball_control_start_time
        
        try:
            ball_control_home_pc = g.home_team.ball_control_timer / (g.home_team.ball_control_timer + g.away_team.ball_control_timer)
        except ZeroDivisionError:
            ball_control_home_pc = 0
        
        try:
            ball_control_away_pc = g.away_team.ball_control_timer / (g.home_team.ball_control_timer + g.away_team.ball_control_timer)
        except ZeroDivisionError:
            ball_control_away_pc = 0

        # Update ui variables
        ui.bc_pc_home_team.set(f"{ball_control_home_pc:.0%}")
        ui.bc_pc_away_team.set(f"{ball_control_away_pc:.0%}")
    
    g.ball_control_start_time = g.game_timer
    g.ball_control_team = ball_control_team
    
    ui.bc_timer_home_team.set(format_timer(g.home_team.ball_control_timer))
    ui.bc_timer_away_team.set(format_timer(g.away_team.ball_control_timer))

# Add game control button actions
def start_game():
    """Method when Start-button is clicked."""

    g.started = True

    g.start_time = floor(time()) # start time of the game in seconds to update game timer
    g.total_game_time = int(ui.e_game_total_time.get())

    ui.e_game_total_time.state(['readonly'])

    update_time()

ui.b_game_start.configure(command=start_game)

# When ball_control is changed
ui.ball_control_check.trace_add(mode='write', callback=update_ball_control_timers)

col, row = 0, 1
# Binding home player buttons
for player in g.home_team.players:
    b_player = ui.ttk.Button(
        ui.f_pass_players,
        text=player.player_number)
    b_player.grid(column=col, row=row)

    b_player.bind('<ButtonPress-1>', lambda e: create_pass_event(team=g.home_team, event=e))
    b_player.bind('<ButtonPress-3>', lambda e: finalize_pass_event(game_event=p, team=g.home_team, event=e))
    col += 1

col = 0
row += 2

# Binding away player buttons
for player in g.away_team.players:
    b_player = ui.ttk.Button(
        ui.f_pass_players,
        text=player.player_number)
    b_player.grid(column=col, row=row)

    b_player.bind('<ButtonPress-1>', lambda e: create_pass_event(team=g.away_team, event=e))
    b_player.bind('<ButtonPress-3>', lambda e: finalize_pass_event(game_event=p, team=g.away_team, event=e))
    col += 1

b_out_of_sides = ui.ttk.Button(ui.f_pass_players, text="Sivurajalta\nulos")
b_out_of_sides.bind('<ButtonPress-3>', lambda e: finalize_pass_event(game_event=p, team=None, event=e))

b_out_of_ends = ui.ttk.Button(ui.f_pass_players, text="Päätyrajalta\nulos")
b_out_of_ends.bind('<ButtonPress-3>', lambda e: finalize_pass_event(game_event=p, team=None, event=e))

b_out_of_sides.grid(column=0, row=row+1)
b_out_of_ends.grid(column=1, row=row+1)

ui.l_players_text_home['text'] =  g.home_team.name
ui.l_players_text_away['text'] =  g.away_team.name

ui.l_players_text_home.grid(columnspan=len(g.home_team.players), sticky="W")
ui.l_players_text_away.grid(columnspan=len(g.away_team.players), sticky="W")

ui.root.mainloop()

pass_codes = [p.code() for p in g.get_passes()]

### --- THIS SECTION ONLY FOR TESTING ---
total_passes_home = pass_codes.count("o1") + pass_codes.count("o0")
# Longest passing chains
pass_counter_series_home, longest_pass_chain_home = g.passing_chains("o1")

try:
    pass_pct_home = pass_codes.count("o1") / total_passes_home
except ZeroDivisionError:
    pass_pct_home = 0

total_passes_away = pass_codes.count("v1") + pass_codes.count("v0")
pass_counter_series_away, longest_pass_chain_away = g.passing_chains("v1")
try:
    pass_pct_away = pass_codes.count("v1") / total_passes_away
except ZeroDivisionError:
    pass_pct_away = 0

print(f"Oranssit: Syötöt yhteensä: {total_passes_home}, joista omille {pass_codes.count('o1')}, syöttöprosentti {pass_pct_home:.1%}")

print(f"Valkoiset: Syötöt yhteensä: {total_passes_away}, joista omille {pass_codes.count('v1')}, syöttöprosentti {pass_pct_away:.1%}")

# Print passing chains
for k, v in sorted(pass_counter_series_home.items(), key=lambda x: x[1], reverse=True):
    print(f"Pituus: {k}, määrä: {v}")

# Print last pass game time
if len(g.events) > 0:
    print(f"Syöttöaika: {g.events[-1].gametime}")

# Print list of passing players
for team in [g.home_team, g.away_team]:
    print(f"Joukkue - {team.name}")
    for player in team.players:
        passes = player.get_passes()
        successful_passes = [p for p in passes if p.target == 1]
        try:
            s_pct = len(successful_passes) / len(passes)
        except ZeroDivisionError:
            s_pct = 0
        print(f"{player.player_number} - {player.name}: {len(passes)} syöttöä - {s_pct:.1%}")
### --- THIS SECTION ONLY FOR TESTING ---