# Werewolves' Puzzle Auto-Generator

For Japanese, please refer to [this page.](http://students.hatenablog.com/entry/2017/11/03/190643)

## Introduction 
This module generates the puzzle inspired by the party game, "Are you a werewolf?", also known as "Mafia". 
Each **player** is given the **role**, either **villager**, **wolf**, or **lunatic**. 
The objective of this puzzle is to discern **wolves** from **players** on the basis 
of the players' statements. 

## Requirements
My python version is 3.6.3. External library is not used for this repository. 

## Usage

```
python puzzle_generator.py
```

If you would like to specify the number of players, 

```
python puzzle_generator.py -v 4 -w 1 -l 1
```

Other options can be seen by the following command, 

```
python puzzle_generator.py -h 
```


## Puzzle's Rule
+ The objective of puzzle is to find **wolves**.
+ **Players** make claims that other playeres are **wolves** or not. 
+ **Villagers** do never tell lies. 
+ **Wolves** and **lunatics** may claim false statements.

## Puzzle's example 

### Problem1
+ Roles:Villager/Wolf=4/2, PL:A-F

#### Player's claims

+ A's claim:B●,D○
+ B's claim:F●
+ C's claim:D●

#### Explanation of player's statements. 

+ *A* claims that *B* is **wolf**, and *D* is not **wolf**.
+ *B* claims that *F* is **wolf**. 
+ *C* claims that *D* is **wolf**.
+ Other players claim no statements. 

### Answer 
Wolves=B,C

### Proof

#### *B* is **wolf**.
Suppose that *B* is a **villager**.
In this case, *A* and *F* become **wolf**.
Other players except *A* and *F* are **villagers**.
Nevertheless, *C* claims that *D* is a **wolf**. 
This is a contradiction, hence, *B* is **wolf**.

#### *C* is **wolf**.
Suppose that *C* is a **villager**.
In this case, *D* and *A* become **wolf**. 
Remembering that *B* is wolf, the number of wolves exceeds 2. 
This is contradiction, hence, *C* is **wolf**. 

#### Problem2
Roles:Villager/Wolf/Lunatic=4/1/2, PL:A-G

### Player's claims
+ A's claim:B○,C○,D○,E○,F○,G●
+ B's claim:D○,E○,F●,G○
+ C's claim:A○,B●,G○
+ D's claim:F●,G○
+ E's claim:B●

### Answer
Wolves:B 


## Design Outline
The process of generation is simple. 
The core function of generation is **strategy.generate_problem**. 

+ Check whether the uniqueness of coherent cases in which all players' statements do not contradict each other.
+ If the coherent cases are more than one, then add the claim of a player.
+ If the coherent cases do not exist, then delete the claim of a player. 

This function iterates the above until the unique coherent case is found. 

By overriding the functions of adding or deleting claims of players, 
the properties of the generated problem change. (see the derived classes of **Strategy**.)

When you create the subclass of **Strategy**, add the class to 
*_mode_dict* in **get_strategy_map**.
Then, the class used for generation of problems can be specified
via **strategy_mode** option at the command line. 
