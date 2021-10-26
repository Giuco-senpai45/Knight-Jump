# Horse-Jump
# This project is an exercise for socket programming where the server and client communicate through a TCP/IP connection.

## The game is the following:
### The server generates a 2D array with the length of 8 representing a chess board and generates 2 random positions for Start and Finish
### The client has the 'knight' chess piece and his goal is to try to reach the finish with a list of moves he sends to the server.
<ul>
  <li> The client reads an integer representing the number of moves he is going to make and the pair of moves he is going to make (row,column) </li>
  <li> The server receives the moves and checks if the moves are valid knight moves (the knight moves in an L shape)  </li>
  <li> If the list of moves reaches the Finish spot in the array, then the server sends the client a status:
      <ul>
          <li>"Good job you won :)" if the movements list sent by the client reaches the Finish point starting from the Start point.</li>
          <li>"Sadly you lost :("  if the movements doesn't reach the Finish point</li>
      </ul>
  </li>
  <li> The client receives the status followed by his IP address and a list of the winners IP's and their number of moves. </li>
</ul>


The server is implemented using python and the client is implemented in C.
