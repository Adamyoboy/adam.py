import random
from typing import Optional

import nextcord

popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "🟩",
        "b": "🟩",
        "c": "🟩",
        "d": "🟩",
        "e": "🟩",
        "f": "🟩",
        "g": "🟩",
        "h": "🟩",
        "i": "🟩",
        "j": "🟩",
        "k": "🟩",
        "l": "🟩",
        "m": "🟩",
        "n": "🟩",
        "o": "🟩",
        "p": "🟩",
        "q": "🟩",
        "r": "🟩",
        "s": "🟩",
        "t": "🟩",
        "u": "🟩",
        "v": "🟩",
        "w": "🟩",
        "x": "🟩",
        "y": "🟩",
        "z": "🟩",
    },
    "yellow": {
        "a": "🟨",
        "b": "🟨",
        "c": "🟨",
        "d": "🟨",
        "e": "🟨",
        "f": "🟨",
        "g": "🟨",
        "h": "🟨",
        "i": "🟨",
        "j": "🟨",
        "k": "🟨",
        "l": "🟨",
        "m": "🟨",
        "n": "🟨",
        "o": "🟨",
        "p": "🟨",
        "q": "🟨",
        "r": "🟨",
        "s": "🟨",
        "t": "🟨",
        "u": "🟨",
        "v": "🟨",
        "w": "🟨",
        "x": "🟨",
        "y": "🟨",
        "z": "🟨",
    },
    "gray": {
        "a": "⬛",
        "b": "⬛",
        "c": "⬛",
        "d": "⬛",
        "e": "⬛",
        "f": "⬛",
        "g": "⬛",
        "h": "⬛",
        "i": "⬛",
        "j": "⬛",
        "k": "⬛",
        "l": "⬛",
        "m": "⬛",
        "n": "⬛",
        "o": "⬛",
        "p": "⬛",
        "q": "⬛",
        "r": "⬛",
        "s": "⬛",
        "t": "⬛",
        "u": "⬛",
        "v": "⬛",
        "w": "⬛",
        "x": "⬛",
        "y": "⬛",
        "z": "⬛",
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(
    user: nextcord.User, puzzle_id: Optional[int] = None
) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user
    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        nextcord.Embed: The embed to be sent
    """
    puzzle_id = puzzle_id or random_puzzle_id()
    embed = nextcord.Embed(title="Wordle Clone")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user
    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID
    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (nextcord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    Generates an embed with information about the bot
    Returns:
        nextcord.Embed: The embed to be sent
    """
    discord_url = "https://discord.gg/UWkmQ5GR5Z"
    youtube_url = "https://www.youtube.com/channel/UC6Lj52K6xPqWhjTNTRo0C4Q"
    return nextcord.Embed(
        title="About Discord Wordle Clone",
        description=(
            "Discord Wordle Clone is a game of wordle-like puzzle solving.\n"
            "You can play it by typing `/play` or `/play <puzzle_id> or w?play`\n"
            "You can also play a random puzzle by leaving out the puzzle ID.\n\n"
            f"<:discord:942984508586725417> [Join my Discord server]({discord_url})\n"
            f"<:youtube:942984508976795669> [My youtube channel!]({youtube_url})\n"
        ),
    )


async def process_message_as_guess(
    bot: nextcord.Client, message: nextcord.Message
) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.
    Args:
        bot (nextcord.Client): The bot
        message (nextcord.Message): The new message to process
    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play"
        if embed.author:
            reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply(
            "The game is already over. Start a new game with /play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(message.content.split()) > 1:
        await message.reply(
            "Please respond with a single 5-letter word.", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
