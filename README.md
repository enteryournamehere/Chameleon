# The Chameleon - Telegram game bot

This bot lets you play the game The Chameleon in Telegram groups!
## Game rules
* After the game starts, one players gets to be the chameleon, the other one are simple players
* A topic and a belonging word list is presented, with a button attached to it
* If you are a player and press this button, one of the words of this list is presented to you (called the secret word) - everybody gets to see the same word. If you are the chameleon, you will be informed about this fact instead
* Now the bot asks one after another about a description of the secret word.
* If you are a player, try to describe the secret word in a way that the chameleon can't guess it; but other players know certainly that you are not the chameleon
* If you are the chameleon, you have to choose a description based on your very limited knowledge. Try to blend in with your choice!
* After everyone said a word, everybody gets to vote on who they think is the chameleon. The role of the one with the most votes gets unmasked
* If it is an ordinary player, the chameleon wins!
* If it is the chameleon, it will try to guess the secret word. If its guess is indeed correct, it still wins; otherwise the player do!

## Options
The bot supports a few settings for games. These can be changed by running `/settings` in a group. The bot will send you a private message.
The following settings are supported:
* Language - Change the language of the bot in your group
* Deck - Set the deck of cards used in your group
* Fewer - If only three players are playing (and this is activated), the chameleon, if caught, gets two guesses.
* More - If 7 or 8 players are playing (and this is activated), the words vanish once everyone has said their word, making it harder for the chameleon to guess the correct one.
* Tournament - If this mode is activated, a scoring system is introduced. If the chameleon escapes undetected, it gets two points. If it gets caught and guesses the correct word, it gets one point. If it doesn't, the player get two points each. The first player making it to 5 points wins.
* Pin - Once activated, the bot will silently pin the word list so players can find it easier once a game is started. It will pin the old pinned message (if existing) silently again when the game ends. In order to activate this setting, you need to make the bot an admin with pin privileges.
* Restrict - Once activated, the bot will restrict everyone from writing except the person whose turn it is during the word saying phase. Everyone can write again after this phase is over. In order for this to work, it will promote those users to admins with add member rights, since admins aren't restricted. The original chat permissions are restored after the phase. In order to activate this setting, you need to make the bot an admin with *add new admins*, *restrict members* and *add members* privileges. For more information, read the FAQ item below.

## Supported commands
### Groups
`/start` - start a game
`/settings` - [admins only in bigger groups] change the settings of the bot in the group
`/nextgame` - adds (or removes) you from the nextgame list of this group. If you are on it, the bot will notify you when a game starts.
`/abort_game` - [admins only in bigger groups] abort a game if there is one running right now
`/admins_reload` - since admins are cached for an hour, you might want to run this if the bot doesn't recognize you as an admin, or isn't supposed to do so anymore :O
`/id` - show the groups id

### Private chats
`/language` - change the language I speak to you in the private chat
`/settings_help` - helps you understand the group settings
`/translation` - show you a help message how to do translations
`/deck` - show you how to add your own deck

## Decks
Decks are collection of "cards". You can create new decks or change existing ones. They are simple json files. In case you create a new deck, keep in mind that you set the topic/name of the deck with the name of the json file. Please keep it short and capitalize the first letter, since it will appear as an InlineKeyboardButton and looks better this way. One word only. Inside the json file, you define keys, which are the topic of the words, and then create a list with fitting words. Only strings are allowed in the list. 16 words per topic are recommended, but not required. You can look at actual implementations [here](https://github.com/TheChameleonBot/Chameleon/tree/master/cards) and join us over [here](https://t.me/joinchat/DG7UjlZfggQcMH2TEDCMyQ) in case you have questions or want to submit a file.

## Translations
You can translate the whole bot! The files are .yaml files, they should be edible in every basic text program, but Notepad ++ is a recommendation from us :) If you actually take on this challenge, you can find existing translations [here](https://github.com/TheChameleonBot/Chameleon/tree/master/strings). Once you download the base file (en (English) is recommended, since its always the most updated file), rename it with the ISO 639-1 code of your language. The two letter one is recommended, but not enforced. Translate the parts in the quotation marks. In case you want to actually use quotation marks in your strings, escape them like that: `\"` . Let the curly brackets stay and don't change their number. Telegrams formatting is supported with html tags, they worked as described [here](https://core.telegram.org/bots/api#html-style). After you are finished, join us [here](https://t.me/joinchat/DG7UjlZfggQcMH2TEDCMyQ) to submit this file or to ask further questions.

## FAQ
### Why does the restricted mode need so many rights?
Lets go through the three one by one:
Restrict members: This is needed in order to change chat permissions. Apparently, telegram didnt want to add a specific right for that.
New Admins: This is because telegram doesn't allow to give single users restrictions, which elevates them over the restricted chat permission. So in order to allow single users to write, the bot needs to be able to promote them to admins, which are always excluded from chat permissions. They get demoted after they wrote their word(s)
Add new member: These temporary admins need to have one specific admin right, writing isn't one of them sadly. I figured this would be the right with the less potential harm.
