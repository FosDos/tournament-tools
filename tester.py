import tohelper

import time

bot = tohelper.chal_driver('FosDos', 'zVrnwoyiXiIwOokz0AvhURPG3vi3V3WONhkG4SnY')

x = bot.create_bracket('test1', 'PM')

bot.add(x, "fluzi")
bot.add(x, "parsec")
bot.add(x, "chapo")
bot.add(x,"fuji")
bot.add(x,"dickfart")
bot.add(x,"ionicbearcannon")
bot.add(x,"wormy")
bot.add(x, "sammy")
bot.add(x, "starlord")
bot.add(x, "peep")
bot.add(x, "blitz")
bot.add(x, "fuckface")
bot.add(x, "lolidk")
bot.add(x, "isaac")
bot.add(x, "foolio")
bot.add(x, "redio")
bot.add(x, "outof")
bot.add(x, "ideas")
bot.add(x, "but")
bot.add(x, "thats")
bot.add(x, "cool")
bot.start(x)

i =  bot.encode(x)

p = raw_input("\n")

bot.decode(x, i)

print i

print x
