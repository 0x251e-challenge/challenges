emoji_string = """
🍋🍊🍋🍋🍋🍋🍊🍊🍋🍊🍋🍊🍋🍊🍋🍋🍋🍊🍋🍋🍋🍊🍊🍋🍋🍊🍊🍊🍊🍋🍊🍊🍋🍊🍊🍋🍊🍊🍋🍊🍋🍊🍋🍋🍊🍊🍊🍊🍋🍊🍊🍋🍊🍊🍋🍊🍋🍊🍋🍊🍊🍊🍊🍊🍋🍊🍊🍊🍋🍋🍊🍊🍋🍊🍊🍋🍋🍋🍊🍊🍋🍋🍊🍊🍋🍋🍋🍋🍋🍋🍊🍊🍋🍋🍋🍊🍋🍊🍊🍋🍋🍊🍋🍋🍋🍊🍊🍋🍋🍊🍋🍊🍋🍊🍊🍋🍋🍊🍋🍋🍋🍊🍋🍊🍊🍊🍊🍊🍋🍊🍊🍋🍊🍊🍋🍊🍋🍋🍊🍊🍋🍋🍊🍊🍋🍊🍋🍊🍊🍊🍊🍊🍋🍊🍊🍋🍋🍋🍊🍋🍋🍋🍊🍊🍋🍋🍊🍊🍋🍊🍋🍋🍊🍋🍋🍊🍋🍊🍊🍋🍊🍊🍊🍋🍋🍊🍋🍋🍋🍊🍊🍊🍋🍊🍋🍊🍊🍊🍊🍊🍋🍊🍊🍋🍋🍋🍋🍊🍋🍊🍋🍊🍊🍊🍊🍊🍋🍊🍋🍋🍋🍊🍋🍋🍋🍊🍋🍊🍋🍊🍋🍊🍋🍊🍋🍋🍊🍊🍋🍊🍋🍊🍋🍋🍋🍋🍊🍋🍋🍊🍋🍋🍋🍋🍋🍊🍋🍊🍋🍊🍊🍋🍊🍋🍋🍊🍋🍊🍊🍋🍊🍋🍋🍊🍊🍊🍊🍊🍋🍊
"""

def decode(emoji):
  emoji_map = {"🍊":"1","🍋":"0"}
  binary = ""
  for e in emoji:
    binary+=emoji_map.get(e,"")
  return binary

flag = decode(emoji_string)
print(flag)