#include <netinet/in.h>
#include <netinet/ip.h>
#include <string.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc,char* argv[]) {

    struct sockaddr_in server;
    uint16_t c;
    c = socket(AF_INET, SOCK_STREAM, 0);
    if (c < 0) {
        printf("Error creating client's socket\n");
        return 1;
    }

    memset(&server, 0, sizeof(server));
    server.sin_port = htons(atoi(argv[1]));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(argv[2]);

    if (connect(c, (struct sockaddr *) &server, sizeof(server)) < 0) {
            printf("Error connecting to the server\n");
            return 1;
    }

    uint16_t row_start,row_stop,col_start,col_stop;
    recv(c, &row_start, 2, 0);
    recv(c, &col_start, 2, 0);
    recv(c, &row_stop, 2, 0);
    recv(c, &col_stop, 2, 0);
    row_start = htons(row_start);
    row_stop = htons(row_stop);
    col_start = htons(col_start);
    col_stop = htons(col_stop);

    printf("Start position: %hu,%hu  Stop position:%hu,%hu\n",row_start,col_start,row_stop,col_stop);

    uint16_t nr,row,col;
    printf("Read the number of intermediare moves: ");
    scanf("%hu", &nr);

    //Trimit cate pozitii citesc
    uint16_t temp = nr;
    temp = htons(temp);
    send(c, &temp, sizeof(temp), 0);

    for(int i = 0 ;i < nr; i ++){
        printf("Row:\n");
        scanf("%hu", &row);
        printf("Col:\n");
        scanf("%hu", &col);
        row = htons(row);
        col = htons(col);
        send(c, &row, sizeof(row), 0);
        send(c, &col, sizeof(col), 0);
    }

    char status[30],addr[30];
    bzero(status, 30);
    recv(c, status, 30, 0);
    bzero(addr, 30);
    recv(c, addr, 30, 0);


    printf("For client %s\n",addr);
    printf("Your game status: %s",status);
    printf("\n");

    printf("Stats for other games: \n");
    uint16_t nr_winners;
    recv(c, &nr_winners, 2, 0);
    nr_winners = ntohs(nr_winners);
    printf("Number of winners %hu\n", nr_winners);

    printf("List of the winners and their number of moves\n");
    for(int i = 0 ; i < nr_winners; i++){
        char winner[80];
        bzero(winner, 80);
        recv(c, winner, 80, 0);
        printf("%s",winner);
    }

    close(c);
    return 0;
}