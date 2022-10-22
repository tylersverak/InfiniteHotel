# InfiniteHotel
The infinite hotel SMS based command line interface game
Project created by Tyler Sverak

The Infinite Hotel is a command line interface multiplayer SMS puzzle game. You play as a character that explores the infinite hotel, using your knowledge to solve mysteries and progress. The current implementation uses the command line of the machine it is ran on and not from SMS input.

# How to Play
As your character, you interact with the environment via commands. You are given a prompt with options you can choose from. You start in the hotel lobby, where you will be given the opportunity to read guide books to learn how to input commands. It is HIGHLY SUGGESTED you read the guides as the game may not be intuitive without understanding how the game works. The guides are also below for your convenience. You can read the books with input "inspect guide 1".

Welcome to the Infinite Hotel! Here are some books to help give you some idea of how to navigate the hotel. Everyone participating will be able to interact with each other, and any changes you make to the environment will be visible to other people. Feel free to explore as much as you want, and check out the other guides! [contact me if you have any questions you can't figure out]

The first thing to learn is how to provide input. You will receive messages containing all the actions you can do. Each action is indicated by a \">\" followed by a word in all caps. If you want to do that action, type the capitalized part of the message. For example, if you were given the option \"> PRESS the button\" you would need to only type \"press\" to do that action (don't worry about capitalization in the messages you send). Some actions have to be given in a specific manner, which is covered in book 3

Some actions need some additional info to be performed. For example, \"USE\" lets you use an item you have. But you also need to specify which item! If given the option \"> USE Shovel, Flashlight, Ty's Note, Match\" you would respond with \"use ty's note\" to use that item. Notice upper or lower case doesn't matter, but otherwise the name must match exactly. \"SPEAK\" is a unique action that requires you to enter what you will say, for example \"speak very cool\" would make your character say \"very cool\" out loud. If you use SPEAK, other people in the room will hear whatever you say (maybe you should say hi?)
Not all actions have an effect in every room. Try experimenting with where you do certain actions to see if something new happens. There are also a few hidden actions that can be revealed as you explore. If you mistype an action or the additional info, it will prompt you to try again

The GO action: GO is important because it allows you to move. The options GO lets you pick are usually compass directions to help give you an idea of how the space is laid out. Sometimes you may encounter a passage way that is locked or otherwise blocked

Items: items can be found in the hotel. You can DROP, PICKUP, or USE items. If you DROP an item, it will remain in that room and other players can find it and pick it up. You can PICKUP items left by other players or found in the hotel (if you are given the option of picking up an item and are told the item doesn't seem to be there, it usually someone grabbed it after you entered the room but before you tried to pick it up). While all items can be used with USE, some items have no functionality and are mean to be moved to another room or are decorative

The Infinite Elevator: the elevator in the hotel is, well, infinite and allows you to travel to any possible number floor. It's a magic elevator (duh) so once you are in the elevator, you only need to speak what floor you want to go to, for example \"speak 6\" would take you to floor 6 [hint: don't go to floor 6]. You're currently on the main floor (1). If you wait too long in the elevator, it will kick you out. If someone else is using the elevator, you won't be able to use it, so wait 10 seconds or so and try again
