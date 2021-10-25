from random import randint
import socket
import threading
import struct
import sys

TCP_PORT =int(sys.argv[1])  
TCP_IP = sys.argv[2]

winners = []
movements = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))

server.listen(5)
 
def show_chessboard(board):
    for i in board:
        print(i)

def horse_jump(row1,col1,row2,col2):
    #check if the positions are going in an L going 2 above or below 1 to the left or right
    if abs(row1 - row2 ) == 2:
        if abs(col1 -col2) ==1:
            return True

    #check if the positions are going in an L going 2 left or right 1 to the above or below
    if abs(row1 - row2 ) == 1:
        if abs(col1 -col2) ==2:
            return True

    return False    

def handle_client(conn, addr):
    print(f"Hello client {addr}")
    rows,cols = (8,8)
    board = [[0 for i in range(cols)] for j in range(rows)]
    # row_start = randint(0,7)
    # col_start = randint(0,7)
    # row_stop = randint(0,7)
    # col_stop = randint(0,7)

    doing_well = False
    row_start = 4
    col_start = 0
    row_stop = 1
    col_stop = 2
    board[row_start][col_start] = 'S'
    board[row_stop][col_stop] = 'F'
    show_chessboard(board)     #shows the initial chess board
   

    positions = struct.pack('>HHHH',row_start,col_start,row_stop,col_stop)
    conn.send(positions)

    nr = int.from_bytes(conn.recv(2), byteorder="big")

    row1 = int.from_bytes(conn.recv(2), byteorder="big")
    col1 = int.from_bytes(conn.recv(2), byteorder="big")

    #if the first jump is not valid
    if not horse_jump(row_start,col_start,row1,col1):
        print("The first jump is not good")

    movements.append([row1,col1,1])
    board[row1][col1] = 1
    moves = 1
    for i in range(0,nr-1):
        row2 = int.from_bytes(conn.recv(2), byteorder="big")
        col2 = int.from_bytes(conn.recv(2), byteorder="big")
        if not horse_jump(row1,col1,row2,col2):
            break
        row1 = row2
        col1 = col2
        moves +=1
        board[row1][col1] = moves
        movements.append([row1,col1,moves])

    if moves == nr:
        if horse_jump(row1,col1,row_stop,col_stop):
            doing_well = True
            print("Final board with the movement numbers")
            show_chessboard(board)

            winners.append([addr[0],nr])
            print("This guy won :)")
        else:
            print("Not all moves are correct :(")
    else:
        print("Not all moves are correct :(")

    

    if doing_well == True:
        msg = "Good job you won :)\n"
        conn.send(msg.encode())
        
    else:
        msg = "Sadly you lost :(\n"
        conn.send(msg.encode())

    ip_addr = str(addr[0])
    conn.send(ip_addr.encode())

    winners_no = len(winners)
    print(winners_no)
    no_winners = struct.pack('>H', winners_no)
    conn.send(no_winners)

    for i in range(0,winners_no):
        win = str("IP winner:" + winners[i][0]) + " Number of moves: " + str(winners[i][1])
        print(win)
        conn.send(win.encode())

    conn.close()

while True:
    conn, addr = server.accept()
    print(addr)
    thr = threading.Thread(target=handle_client, args=(conn, addr))
    thr.start()

server.close()