# eventspec.py
# Copyright 2015 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Map ChessTab event names to tk(inter) event detail values."""

# Some cases need an object with a widget attribute, but the source of the
# event does not provide an event object, let alone the relevant widget.
# Fortunately the required widget is always known in these cases.
import collections
DummyEvent = collections.namedtuple('DummyEvent', 'widget')
del collections

# Mapped to widget focus setters and initialisers in all panels.
# Menu item label is same in all cases.
GAMES_PARTIAL_POSITION = 'Games Partial Position'
ACTIVE_PARTIAL_POSITION = 'Active Partial Position'
PARTIAL_POSITION_LIST = 'Partial Position List'
GAMES_REPERTOIRE = 'Games Repertoire'
ACTIVE_REPERTOIRE = 'Active Repertoire'
REPERTOIRE_GAME_LIST = 'Repertoire Game List'
GAMES_DATABASE = 'Games Database'
POSITION_GAME_LIST = 'Position Game List'
ACTIVE_GAME = 'Active Game'
SELECTION_RULE_LIST = 'Selection Rule List'
ACTIVE_SELECTION_RULE = 'Active Selection Rule'

# Mapped to widget focus setters and initialisers in relevant panels.
# Menu item label is same in all cases.
PREVIOUS_REPERTOIRE = 'Previous Repertoire'
NEXT_REPERTOIRE = 'Next Repertoire'
REPERTOIRE = 'Repertoire'
PREVIOUS_GAME = 'Previous Game'
NEXT_GAME = 'Next Game'
GAME = 'Game'
ANALYSIS = 'Analysis'
PREVIOUS_PARTIAL_POSITION = 'Previous Partial Position'
NEXT_PARTIAL_POSITION = 'Next Partial Position'
PREVIOUS_SELECTION_RULE = 'Previous Selection Rule'
NEXT_SELECTION_RULE = 'Next Selection Rule'


class EventSpec(object):
    """Event detail values for ChessTab keyboard and pointer actions."""

    # PartialPositionGames
    partial_game_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    partial_game_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    partial_game_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    partial_game_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    partial_game_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    partial_game_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'F9')
    partial_game_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    partial_game_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    partial_game_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    partial_game_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_game_from_partial_game_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_game_from_partial_game_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_archive_pgn_from_partial_game_grid = (
        '<Shift-Alt-KeyPress-Home>', 'Export Archive PGN', 'Shift Alt Home')
    export_rav_pgn_from_partial_game_grid = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_partial_game_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')

    # GamePositionGames
    position_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    position_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    position_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    position_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    position_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    position_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    position_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    position_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    position_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    position_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    display_game_from_position_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_game_from_position_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_archive_pgn_from_position_grid = (
        '<Shift-Alt-KeyPress-Home>', 'Export Archive PGN', 'Shift Alt Home')
    export_rav_pgn_from_position_grid = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_position_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')

    # TagRosterGrid
    game_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    game_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    game_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    game_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    game_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    game_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    game_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    game_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    game_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    game_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_game_from_game_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_game_from_game_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_archive_pgn_from_game_grid = (
        '<Shift-Alt-KeyPress-Home>', 'Export Archive PGN', 'Shift Alt Home')
    export_rav_pgn_from_game_grid = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_game_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')

    # RepertoireGrid
    repertoire_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    repertoire_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    repertoire_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    repertoire_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    repertoire_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    repertoire_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    repertoire_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    repertoire_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    repertoire_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    repertoire_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_game_from_repertoire_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_game_from_repertoire_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_rav_pgn_from_repertoire_grid = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_repertoire_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')

    # RepertoirePositionGames
    repertoire_game_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    repertoire_game_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    repertoire_game_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    repertoire_game_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    repertoire_game_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    repertoire_game_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    repertoire_game_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    repertoire_game_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    repertoire_game_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    repertoire_game_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_game_from_repertoire_game_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_game_from_repertoire_game_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_archive_pgn_from_repertoire_game_grid = (
        '<Shift-Alt-KeyPress-Home>', 'Export Archive PGN', 'Shift Alt Home')
    export_rav_pgn_from_repertoire_game_grid = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_repertoire_game_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')
    cycle_up_one_repeat_in_repertoire_game_grid = (
        '<Shift-KeyPress-Up>', 'Previous Transposition', 'Shift Up')
    cycle_down_one_repeat_in_repertoire_game_grid = (
        '<Shift-KeyPress-Down>', 'Next Transposition', 'Shift Down')

    # PartialGrid
    partial_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    partial_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    partial_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    partial_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    partial_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    partial_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    partial_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    partial_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    partial_grid_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    partial_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_partial_from_partial_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_partial_from_partial_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')
    export_from_partial_grid = (
        '<Control-Alt-KeyPress-Home>', 'Export', 'Ctrl Alt Home')

    # Score widget, common to Game and Repertoire widgets.
    # Default lambda in Score.__init__ ignored.
    score_show_previous_in_variation = (
        '<Shift-KeyPress-Up>', 'Previous Move Variation', 'Shift Up')
    score_show_previous_in_line = (
        '<KeyPress-Up>', 'Previous Move', 'Up')
    score_show_next_in_line = (
        '<Shift-KeyPress-Down>', 'Next Move', 'Shift Down')
    score_show_next_in_variation = (
        '<KeyPress-Down>', 'Next Move Select Variation', 'Down')
    score_show_first_in_line = (
        '<KeyPress-Prior>', 'Start of Variation', 'PageUp')
    score_show_last_in_line = (
        '<KeyPress-Next>', 'End of Variation', 'PageDn')
    score_show_first_in_game = (
        '<Shift-KeyPress-Prior>', 'Start of Game', 'Shift PageUp')
    score_show_last_in_game = (
        '<Shift-KeyPress-Next>', 'End of Game', 'Shift PageDn')
    score_show_selected_variation = (
        '<Shift-KeyPress-Down>', 'Enter Variation', 'Shift Down')
    score_cycle_selection_to_next_variation = (
        '<KeyPress-Down>', 'Next Variation', 'Down')
    score_cancel_selection_of_variation = (
        '<KeyPress-Up>', 'Cancel Variation', 'Up')
    score_disable_keypress = (
        '<KeyPress>', '', '') # No menu entry for this initialisation event.

    # Game widget analyse events.
    # Inherited by Repertoire, GameEdit, and RepertoireEdit, widgets.
    analyse_game = (
        '<Alt-KeyPress-a>', 'Analyse', 'Alt a')

    # Game widget PGN export events.
    # Inherited by Repertoire, GameEdit, and RepertoireEdit, widgets.
    export_archive_pgn_from_game = (
        '<Shift-Alt-KeyPress-Home>', 'Export Archive PGN', 'Shift Alt Home')
    export_rav_pgn_from_game = (
        '<Control-Shift-KeyPress-Home>', 'Export RAV PGN', 'Ctrl Shift Home')
    export_pgn_from_game = (
        '<Control-Alt-KeyPress-Home>', 'Export PGN', 'Ctrl Alt Home')

    # GameEdit widget editing events.
    # Inherited by RepertoireEdit widget.
    gameedit_insert_rav = (
        '<KeyPress>', '', '') # A menu entry would say type moves to insert.
    gameedit_insert_rav_castle_queenside = (
        '<Control-KeyPress-o>', 'O-O-O', 'Ctrl o')
    gameedit_insert_comment = (
        '<Control-KeyPress-braceleft>', 'Insert Comment', 'Ctrl {')
    gameedit_insert_reserved = (
        '<Control-KeyPress-less>', 'Insert Reserved', 'Ctrl <')
    gameedit_insert_comment_to_eol = (
        '<Control-KeyPress-semicolon>', 'Insert Comment to EOL', 'Ctrl ;')
    gameedit_insert_escape_to_eol = (
        '<Control-KeyPress-percent>', 'Insert Escape to EOL', 'Ctrl %')
    gameedit_insert_glyph = (
        '<Control-KeyPress-dollar>', 'Insert Glyph', 'Ctrl $')
    gameedit_insert_pgn_tag = (
        '<Control-KeyPress-bracketleft>', 'Insert PGN Tag', 'Ctrl [')
    gameedit_insert_pgn_seven_tag_roster = (
        '<Control-KeyPress-bracketright>',
        'Insert PGN Seven Tag Roster',
        'Ctrl ]')
    gameedit_insert_white_win = (
        '<Control-KeyPress-plus>', '1-0', 'Ctrl +')
    gameedit_insert_draw = (
        '<Control-KeyPress-equal>', '1/2-1/2', 'Ctrl =')
    gameedit_insert_black_win = (
        '<Control-KeyPress-minus>', '0-1', 'Ctrl -')
    gameedit_insert_other_result = (
        '<Control-KeyPress-asterisk>', 'Other Result', 'Ctrl *')
    gameedit_show_previous_token = (
        '<Shift-KeyPress-Left>', 'Previous Item', 'Shift Left')
    gameedit_show_next_token = (
        '<Shift-KeyPress-Right>', 'Next Item', 'Shift Right')
    gameedit_show_first_token = (
        '<Shift-KeyPress-Prior>', 'First Item', 'Shift PageUp')
    gameedit_show_last_token = (
        '<Shift-KeyPress-Next>', 'Last Item', 'Shift PageDn')
    gameedit_show_first_comment = (
        '<Control-KeyPress-Prior>', 'First Comment', 'Ctrl PageUp')
    gameedit_show_last_comment = (
        '<Control-KeyPress-Next>', 'Last Comment', 'Ctrl PageDn')
    gameedit_show_previous_comment = (
        '<Control-KeyPress-Up>', 'Previous Comment', 'Ctrl Up')
    gameedit_show_next_comment = (
        '<Control-KeyPress-Down>', 'Next Comment', 'Ctrl Down')
    gameedit_to_previous_pgn_tag = (
        '<Control-KeyPress-Left>', 'Previous PGN Tag', 'Ctrl Left')
    gameedit_to_next_pgn_tag = (
        '<Control-KeyPress-Right>', 'Next PGN Tag', 'Ctrl Right')
    gameedit_delete_empty_pgn_tag = (
        '<Control-KeyPress-Delete>', 'Delete empty PGN Tag', 'Ctrl Delete')
    gameedit_bind_and_show_previous_in_line = (
        '<KeyPress-Up>', 'Previous Move', 'Up')
    gameedit_bind_and_show_previous_in_variation = (
        '<Shift-KeyPress-Up>', 'Previous Move Variation', 'Shift Up')
    gameedit_bind_and_show_next_in_line = (
        '<Shift-KeyPress-Down>', 'Next Move', 'Shift Down')
    gameedit_bind_and_show_next_in_variation = (
        '<KeyPress-Down>', 'Next Move Select Variation', 'Down')
    gameedit_bind_and_show_first_in_line = (
        '<KeyPress-Prior>', 'Start of Variation', 'PageUp')
    gameedit_bind_and_show_last_in_line = (
        '<KeyPress-Next>', 'End of Variation', 'PageDn')
    gameedit_bind_and_show_first_in_game = (
        '<Shift-KeyPress-Prior>', 'Start of Game', 'Shift PageUp')
    gameedit_bind_and_show_last_in_game = (
        '<Shift-KeyPress-Next>', 'End of Game', 'Shift PageDn')
    gameedit_bind_and_to_previous_pgn_tag = (
        '<Control-KeyPress-Left>', 'Previous PGN Tag', 'Ctrl Left')
    gameedit_bind_and_to_next_pgn_tag = (
        '<Control-KeyPress-Right>', 'Next PGN Tag', 'Ctrl Right')
    gameedit_delete_token_char_left = (
        '<Shift-KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    gameedit_delete_token_char_right = (
        '<Shift-KeyPress-Delete>', '', '') # A menu entry would make sense.
    gameedit_delete_char_left = (
        '<KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    gameedit_delete_char_right = (
        '<KeyPress-Delete>', '', '') # A menu entry would make sense.
    gameedit_set_insert_previous_line_in_token = (
        '<Alt-KeyPress-Up>', '', '') # A menu entry would make sense.
    gameedit_set_insert_previous_char_in_token = (
        '<KeyPress-Left>', '', '') # A menu entry would make sense.
    gameedit_set_insert_next_char_in_token = (
        '<KeyPress-Right>', '', '') # A menu entry would make sense.
    gameedit_set_insert_next_line_in_token = (
        '<Alt-KeyPress-Down>', '', '') # A menu entry would make sense.
    gameedit_set_insert_first_char_in_token = (
        '<KeyPress-Home>', '', '') # A menu entry would make sense.
    gameedit_set_insert_last_char_in_token = (
        '<KeyPress-End>', '', '') # A menu entry would make sense.
    gameedit_add_char_to_token = (
        '<KeyPress>', '', '') # A menu entry would say type text to insert.
    gameedit_non_move_show_previous_in_variation = (
        '<Shift-KeyPress-Up>', 'Previous Move Variation', 'Shift Up')
    gameedit_non_move_show_previous_in_line = (
        '<KeyPress-Up>', 'Previous Move', 'Up')
    gameedit_non_move_show_next_in_line = (
        '<Shift-KeyPress-Down>', 'Next Move', 'Shift Down')
    gameedit_non_move_show_next_in_variation = (
        '<KeyPress-Down>', 'Next Move Select Variation', 'Down')
    gameedit_non_move_show_first_in_line = (
        '<KeyPress-Prior>', 'Start of Variation', 'PageUp')
    gameedit_non_move_show_last_in_line = (
        '<KeyPress-Next>', 'End of Variation', 'PageDn')
    gameedit_non_move_show_first_in_game = (
        '<Shift-KeyPress-Prior>', 'Start of Game', 'Shift PageUp')
    gameedit_non_move_show_last_in_game = (
        '<Shift-KeyPress-Next>', 'End of Game', 'Shift PageDn')

    # Why specific shift versions?
    gameedit_delete_move_char_left_shift = (
        '<Shift-KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    gameedit_delete_move_char_right_shift = (
        '<Shift-KeyPress-Delete>', '', '') # A menu entry would make sense.
    gameedit_delete_move_char_left = (
        '<KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    gameedit_delete_move_char_right = (
        '<KeyPress-Delete>', '', '') # A menu entry would make sense.
    
    gameedit_add_move_char_to_token = (
        '<KeyPress>', '', '') # A menu entry would say type moves to insert.
    gameedit_insert_move = (
        '<KeyPress>', '', '') # A menu entry would say type moves to insert.
    gameedit_edit_move = (
        '<KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    gameedit_insert_castle_queenside = (
        '<Control-KeyPress-o>', 'O-O-O', 'Ctrl o')

    # GameDisplay
    gamedisplay_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    gamedisplay_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    gamedisplay_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    gamedisplay_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    gamedisplay_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    gamedisplay_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    gamedisplay_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    gamedisplay_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    gamedisplay_to_previous_game = (
        '<KeyPress-F7>', PREVIOUS_GAME, 'F7')
    gamedisplay_to_next_game = (
        '<KeyPress-F8>', NEXT_GAME, 'F8')
    gamedisplay_game_to_analysis = (
        '<Alt-KeyPress-F8>', ANALYSIS, 'Alt F8')
    gamedisplay_analysis_to_game = (
        '<Alt-KeyPress-F8>', GAME, 'Alt F8')
    gamedisplay_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    gamedisplay_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')

    # DatabaseGameDisplay
    databasegamedisplay_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databasegamedisplay_delete = (
        '<KeyPress-Delete>', 'Delete', 'Delete')
    databasegamedisplay_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Game', 'Alt F12')
    databasegamedisplay_make_active = (
        '', 'Make Active', 'Left Click')
    databasegamedisplay_dismiss_inactive = (
        '', 'Close Game', '')

    # DatabaseGameEdit.
    databasegameedit_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databasegameedit_update = (
        '<Alt-KeyPress-Insert>', 'Update', 'Alt Insert')
    databasegameedit_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Game', 'Alt F12')
    databasegameedit_make_active = (
        '', 'Make Active', 'Left Click')
    databasegameedit_dismiss_inactive = (
        '', 'Close Game', '')

    # GameDialogue
    gamedialogue_game_to_analysis = (
        '<Alt-KeyPress-F8>', ANALYSIS, 'Alt F8')
    gamedialogue_analysis_to_game = (
        '<Alt-KeyPress-F8>', GAME, 'Alt F8')

    # PartialDisplay
    partialdisplay_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    partialdisplay_to_previous_partial = (
        '<KeyPress-F7>', PREVIOUS_PARTIAL_POSITION, 'F7')
    partialdisplay_to_next_partial = (
        '<KeyPress-F8>', NEXT_PARTIAL_POSITION, 'F8')
    partialdisplay_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    partialdisplay_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    partialdisplay_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    partialdisplay_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    partialdisplay_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    partialdisplay_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    partialdisplay_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    partialdisplay_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    partialdisplay_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    export_from_partialdisplay = (
        '<Control-Alt-KeyPress-Home>', 'Export', 'Ctrl Alt Home')

    # DatabasePartialDisplay
    databasepartialdisplay_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databasepartialdisplay_delete = (
        '<KeyPress-Delete>', 'Delete', 'Delete')
    databasepartialdisplay_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Partial', 'Alt F12')
    databasepartialdisplay_make_active = (
        '', 'Make Active', 'Left Click')
    databasepartialdisplay_dismiss_inactive = (
        '', 'Close Partial', '')

    # DatabasePartialEdit
    databasepartialedit_show_game_list = (
        '<Control-KeyPress-Return>', 'List Games', 'Ctrl Enter')
    databasepartialedit_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databasepartialedit_update = (
        '<Alt-KeyPress-Insert>', 'Edit', 'Alt Insert')
    databasepartialedit_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Partial', 'Alt F12')
    databasepartialedit_make_active = (
        '', 'Make Active', 'Left Click')
    databasepartialedit_dismiss_inactive = (
        '', 'Close Partial', '')

    # PartialEdit
    partialedit_insert_char_or_token = (
        '<KeyPress>', '', '') # No menu entry because character required.
    partialedit_delete_char_left = (
        '<KeyPress-BackSpace>', '', '') # A menu entry would make sense.
    partialedit_delete_char_right = (
        '<KeyPress-Delete>', '', '') # A menu entry would make sense.
    partialedit_show_previous_token = (
        '<KeyPress-Up>', 'Previous Piece', 'Up')
    partialedit_show_next_token = (
        '<KeyPress-Down>', 'Next Piece', 'Down')
    partialedit_show_first_token = (
        '<KeyPress-Prior>', 'First Piece', 'PageUp')
    partialedit_show_last_token = (
        '<KeyPress-Next>', 'Last Piece', 'PageDn')
    partialedit_insert_partial_name_left = (
        '<Control-KeyPress-bracketleft>', 'Name', 'Ctrl [')
    partialedit_insert_partial_name_right = (
        '<Control-KeyPress-bracketright>', 'Name', 'Ctrl ]')
    partialedit_set_insert_previous_char_in_token = (
        '<KeyPress-Left>', '', '') # A menu entry would make sense.
    partialedit_set_insert_next_char_in_token = (
        '<KeyPress-Right>', '', '') # A menu entry would make sense.
    partialedit_set_insert_first_char_in_token = (
        '<KeyPress-Home>', '', '') # A menu entry would make sense. 
    partialedit_set_insert_last_char_in_token = (
        '<KeyPress-End>', '', '') # A menu entry would make sense.

    # RepertoireDisplay
    repertoiredisplay_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    repertoiredisplay_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    repertoiredisplay_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    repertoiredisplay_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    repertoiredisplay_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    repertoiredisplay_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    repertoiredisplay_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    repertoiredisplay_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    repertoiredisplay_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    repertoiredisplay_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    repertoiredisplay_to_previous_repertoire = (
        '<KeyPress-F7>', PREVIOUS_REPERTOIRE, 'F7')
    repertoiredisplay_to_next_repertoire = (
        '<KeyPress-F8>', NEXT_REPERTOIRE, 'F8')
    repertoiredisplay_repertoire_to_analysis = (
        '<Alt-KeyPress-F8>', ANALYSIS, 'Alt F8')
    repertoiredisplay_analysis_to_repertoire = (
        '<Alt-KeyPress-F8>', REPERTOIRE, 'Alt F8')

    # DatabaseRepertoireDisplay
    databaserepertoiredisplay_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databaserepertoiredisplay_delete = (
        '<KeyPress-Delete>', 'Delete', 'Delete')
    databaserepertoiredisplay_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Repertoire', 'Alt F12')
    databaserepertoiredisplay_make_active = (
        '', 'Make Active', 'Left Click')
    databaserepertoiredisplay_dismiss_inactive = (
        '', 'Close Repertoire', '')

    # DatabaseRepertoireEdit
    databaserepertoireedit_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databaserepertoireedit_update = (
        '<Alt-KeyPress-Insert>', 'Update', 'Alt Insert')
    databaserepertoireedit_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Repertoire', 'Alt F12')
    databaserepertoireedit_make_active = (
        '', 'Make Active', 'Left Click')
    databaserepertoireedit_dismiss_inactive = (
        '', 'Close Repertoire', '')

    # RepertoireDialogue
    repertoiredialogue_repertoire_to_analysis = (
        '<Alt-KeyPress-F8>', ANALYSIS, 'Alt F8')
    repertoiredialogue_analysis_to_repertoire = (
        '<Alt-KeyPress-F8>', REPERTOIRE, 'Alt F8')

    # PartialScore
    partialscore_disable_keypress = (
        '<KeyPress>', '', '') # No menu entry because character required.

    # Partial widget partial position export events.
    # Inherited by PartialEdit widget.
    export_text_from_partial = (
        '<Control-Alt-KeyPress-Home>', 'Export', 'Ctrl Alt Home')

    # Keyboard traversal events (Control-F8 Control-F7): all relevant widgets.
    # tab_traverse_backward bindings behave differently to expectation given
    # tab_traverse_forward behaviour at Python3.3 with Tk8.6, although I do not
    # know what happens with Tk8.5 an so forth.  Similarely <Shift-Tab>.
    tab_traverse_forward = (
        '<Control-KeyPress-F8>', 'Focus Next', 'Ctrl F8')
    tab_traverse_backward = (
        '<Control-KeyPress-F7>', 'Focus Previous', 'Ctrl F7')
    tab_traverse_round = (
        '<Alt-KeyPress-F8>', 'Focus Round', 'Alt F8')

    # SelectionDisplay
    selectiondisplay_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    selectiondisplay_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    selectiondisplay_to_selection_rule_grid = (
        '<KeyPress-F3>', SELECTION_RULE_LIST, 'F3')
    selectiondisplay_to_previous_selection = (
        '<KeyPress-F7>', PREVIOUS_SELECTION_RULE, 'F7')
    selectiondisplay_to_next_selection = (
        '<KeyPress-F8>', NEXT_SELECTION_RULE, 'F8')
    selectiondisplay_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    selectiondisplay_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    selectiondisplay_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    selectiondisplay_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    selectiondisplay_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    selectiondisplay_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    selectiondisplay_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')

    # SelectionGrid
    selection_grid_to_active_partial = (
        '<Alt-KeyPress-F2>', ACTIVE_PARTIAL_POSITION, 'Alt F2')
    selection_grid_to_partial_game_grid = (
        '<Shift-KeyPress-F2>', GAMES_PARTIAL_POSITION, 'Shift F2')
    selection_grid_to_repertoire_grid = (
        '<KeyPress-F6>', REPERTOIRE_GAME_LIST, 'F6')
    selection_grid_to_active_repertoire = (
        '<Alt-KeyPress-F6>', ACTIVE_REPERTOIRE, 'Alt F6')
    selection_grid_to_repertoire_game_grid = (
        '<Shift-KeyPress-F6>', GAMES_REPERTOIRE, 'Shift F6')
    selection_grid_to_position_grid = (
        '<Shift-KeyPress-F9>', POSITION_GAME_LIST, 'Shift F9')
    selection_grid_to_active_game = (
        '<Alt-KeyPress-F9>', ACTIVE_GAME, 'Alt F9')
    selection_grid_to_game_grid = (
        '<KeyPress-F9>', GAMES_DATABASE, 'F9')
    selection_grid_to_partial_grid = (
        '<KeyPress-F2>', PARTIAL_POSITION_LIST, 'F2')
    selection_grid_to_active_selection_rule = (
        '<Alt-KeyPress-F3>', ACTIVE_SELECTION_RULE, 'Alt F3')
    display_selection_rule_from_selection_grid = (
        '<KeyPress-F11>', 'Display', 'F11')
    edit_selection_rule_from_selection_grid = (
        '<Control-KeyPress-F11>', 'Display allow edit', 'Ctrl F11')

    # SelectionText
    selectiontext_disable_keypress = (
        '<KeyPress>', '', '') # Keyboard actions do nothing by default.

    # DatabaseSelectionDisplay
    databaseselectiondisplay_show_game_list = (
        '<Control-KeyPress-Return>', 'List Games', 'Ctrl Enter')
    databaseselectiondisplay_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databaseselectiondisplay_delete = (
        '<KeyPress-Delete>', 'Delete', 'Delete')
    databaseselectiondisplay_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Selection', 'Alt F12')
    databaseselectiondisplay_make_active = (
        '', 'Make Active', 'Left Click')
    databaseselectiondisplay_dismiss_inactive = (
        '', 'Close Selection', '')

    # DatabaseSelectionEdit
    databaseselectionedit_show_game_list = (
        '<Control-KeyPress-Return>', 'List Games', 'Ctrl Enter')
    databaseselectionedit_insert = (
        '<KeyPress-Insert>', 'Insert', 'Insert')
    databaseselectionedit_update = (
        '<Alt-KeyPress-Insert>', 'Edit', 'Alt Insert')
    databaseselectionedit_dismiss = (
        '<Alt-KeyPress-F12>', 'Close Selection', 'Alt F12')
    databaseselectionedit_make_active = (
        '', 'Make Active', 'Left Click')
    databaseselectionedit_dismiss_inactive = (
        '', 'Close Selection', '')

    # EngineGrid
    engine_grid_run = (
        '<Alt-KeyPress-r>', 'Run Engine', 'Alt r')

    # EngineText
    enginetext_disable_keypress = (
        '<KeyPress>', '', '') # Keyboard actions do nothing by default.

    # DatabaseEngineDisplay
    databaseenginedisplay_run = (
        '<Alt-KeyPress-r>', 'Run Engine', 'Alt r')

    # DatabaseEngineEdit
    databaseengineedit_browse = (
        '<Alt-KeyPress-b>', 'Browse Engines', 'Alt b')
