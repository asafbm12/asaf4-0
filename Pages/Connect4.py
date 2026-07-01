import streamlit as st
from PIL.ImageChops import offset

from Pages.chat import start

rows_number = 6
cols_number = 7

empty_cell = "⚪"
player_cell = "🔵"
comp_cell = "🔴"

def newBoard():
    board = []
    for row in range(rows_number):
        row = []
        for cell in range(cols_number):
            row.append(empty_cell)
        board.append(row)
    print(board)
    st.session_state.board = board

if not "board" in st.session_state:
    newBoard()

board = st.session_state.board

if "turn" not in st.session_state:
    st.session_state.turn = player_cell

turn = st.session_state.turn

def swichTurn():
    global turn
    if turn == player_cell:
        turn = comp_cell
    else:
        turn = player_cell
    st.session_state.turn = turn

def check(row,col,player):
    print(f"Checking row {row} col {col}")
    for cell in range(0, cols_number - 3):
        if board[row][cell] == empty_cell:
            continue
        if board[row][cell] != player:
            continue

        number = 0
        for i in range(cell,cell + 4):
            if board[row][i] == board[row][cell]:
                number+=1
            else:
                break
        if number == 4:
            print(player)
            st.session_state.winner = player
            return

    for cell in range(0, rows_number - 3):
        if board[cell][col] == empty_cell:
            continue
        if board[cell][col] != player:
            continue

        number = 0
        for i in range(cell,cell + 4):
            if board[i][col] == board[cell][col]:
                number+=1
            else:
                break
        if number == 4:
            print(player)
            st.session_state.winner = player
            return

    offset = min(row,col)
    start_row = row - offset
    start_col = col - offset

    for i in range(col):
        check_row = start_row + i
        check_col = start_col + i
        if check_col == cols_number or check_row == rows_number:
            print("")
            break

        print(f"player: {player} row: {check_row} col: {check_col}")
        if board[check_row][check_col] == player:
            number += 1
        else:
            number = 0
        if number == 4:
            print(player)
            st.session_state.winner = player
            return

    dist_left = col
    dist_bottom = rows_number - 1 - row
    offset = min(dist_left,dist_bottom)

    start_row = row + offset
    start_col = col - offset

    number = 0
    for i in range(cols_number):
        check_row = start_row - i
        check_col = start_col + i

        if check_col < 0 or check_col >= cols_number:
            break

        if board[check_row][check_col] == player:
            number += 1
        else:
            number = 0

        if number == 4:
            print(player)
            st.session_state.winner = player
            return

def click(col):
    if board[0][col] != empty_cell:
        st.rerun()
    for row in range(rows_number - 1, -1, -1):
        if board[row][col] == empty_cell:
            board[row][col] = turn
            check(row,col,turn)
            break

    swichTurn()
    st.session_state.board = board
    st.rerun()

def computer_play():
    import random,time
    time.sleep(1)
    coll = random.randint(0,cols_number - 1)
    click(coll)

if "winner" not in st.session_state:
    st.session_state.winner = ""

winner = st.session_state.winner

has_empty = False
for col in range(cols_number):
    if board[0][col] == empty_cell:
        has_empty = True
        break

if winner == comp_cell:
    st.info("המחשב ניצח")
elif winner == player_cell:
    st.info("ניצחת!!!")
elif not has_empty:
    st.info("תיקו")
else:
    if turn == player_cell:
        st.info("התור שלך")
    else:
        st.status("המחשב חושב...")

for row in range(rows_number):
    all_column = st.columns(cols_number)
    for col in range(cols_number):
        with all_column[col]:
            cell = board[row][col]
            if st.button(cell,
                         key=f"row_{row}_col{col}",
                         use_container_width=True,
                         disabled = turn==comp_cell or winner!=""):
                click(col)

if turn == comp_cell and winner=="" and has_empty:
    computer_play()