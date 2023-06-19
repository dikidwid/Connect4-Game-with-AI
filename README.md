
# Implementation of Minimax and Alpha-Beta Pruning on Connect4 
One problem in traditional Connect Four gameplay is that it can be difficult for human players to predict the best move to make in a given situation. This is because the game has a large number of possible board positions and the optimal move can depend on the future moves of both players.

![Picture1](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/2559210f-50bb-4013-993d-47b663a47666)

To overcome this problem, artificial intelligence techniques such as the Minimax algorithm and Alpha-Beta pruning can be used to help determine the best move to make in any given situation.

The main objective of implementing the Minimax algorithm and Alpha-Beta pruning is to develop efficient decision-making algorithms for two-player, zero-sum games, such as Connect Four. The algorithm is designed to help a computer program to play the game at a level comparable to, or even better than, human players. 

Specifically, the objectives of the Minimax algorithm are:

- To evaluate all possible moves that can be made by both players, up to a certain depth in the game tree.
- To assign a score to each possible outcome, based on how favorable it is for the player making the move.
- To choose the move that maximizes the score for the player making the move.

The objective of Alpha-Beta pruning is to optimize the Minimax algorithm by:
- Reducing the number of nodes that need to be evaluated, thus speeding up the algorithm.
- Pruning parts of the search tree that are guaranteed to lead to suboptimal outcomes, which further reduces the number of nodes to be evaluated.

# What's New?
I've made some changes and improvement with each having its own purpose:
- Timer For Player (User)
The timer feature was added into the code with the purpose of increasing the challenge for the player, by putting them under a time constraint of 5 seconds.

- First Turn Option
The choice on who should start was done to give the player more flexibility in gameplay by allowing them to choose if they would like  to start first or to let the AI start first. To do this we use Python’s TKinter module to create a selectable radio button  that will assign a value to the variable that sets the turn.

- Difficulty Options
With our new difficulty option, players can adjust the difficulty of the game to suit their playstyle. This was done by assigning values from the TKinter module to the “Depth” variable that will be used to define the depth of the tree search in the minimax algorithm. There will be three options for difficulty in this game: Easy,Medium,and Hard with each having their own integer value. The easy option will have the lowest integer (1), medium will have (3), and hard will have the largest integer among the three which is (5) this is because in minimax 

# Flowchart
![Blank diagram (11)](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/ca791dde-62b9-4c1c-9f8a-4f9e62f2f64a)

# Screenshots
![pasted image 0](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/afedab00-bc9e-4cf4-9e5e-d436f94e0f02)
![pasted image 0-2](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/6ddda60c-53eb-4096-82d1-a962b813a7b2)
![pasted image 0-3](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/d8c1d645-820e-4dac-bb71-2183c638e3a9)
![pasted image 0-4](https://github.com/dikidwid/Connect4-Game-with-AI/assets/92709211/7279d047-f3b1-4707-b74a-acb563563420)

# References
Video walkthrough on programming this game: https://youtu.be/UYgyRArKDEs
