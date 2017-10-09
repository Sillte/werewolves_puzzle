# Werewolves' Puzzle Auto-Generator

This is English explanation, 
if you are Japanese please refer to [this page.]()

## Introduction 
Here, consider the puzzle inspred by the party game, "Are you a werefolf?" 
Each **player** is given the **role**, either **wolf** or **villager**. 
The objective of this puzzle is to discern **wolves** from **players** on the basis 
of the players' statements.  

### Rule

+ **Villagers** do never tell a lie. 
+ **Wolves** may claim false statement. 

## Puzzle's example  

####  Problem

+ Roles:Villagers/Wolves=4/2, PL:A~F
#### Player's claims

+ A's claim:BÅú,DÅõ
+ B's claim:FÅú
+ C's claim:DÅú

##### Explanation of player's statements. 

+ *A* claims that *B* is **wolf**, and *D* is not **wolf**.
+ *B* claims that *F* is **wolf**. 
+ *C* claims that *D* is **wolf**.
+ Other players claim no statements. 

### Answer  
Wolves=B,C

#### Proof

##### *B* is **wolf**.
Suppose that *B* is a **villager**.
In this case, *A* and *F* become **wolf**.
Other players except *A* and *F* are **villagers**.
Nevertheless, *C* claims that *D* is a **wolf**. 
This is a contradiction, hence, *B* is **wolf**.

##### *C* is **wolf**.
Suppose that *C* is a **villager**.
In this case, *D* and *A* become **wolf**. 
Including *B*,  the number of wolves exceeds 2. 
This is contradiction, hence, *C* is **wolf**. 
 

This module is intended to generate automatically the pair of 
problems and answers. 

##  Caution

Currently, the code is yet experimental. 
