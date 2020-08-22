import tohelper
import sys
import keys
print "Time to C L E A N\n"

num = raw_input("How many brackets would you like to delete?\n")
try:
  num = int(num)
except:
  print "Sorry please try again but this time enter a number ya dingus"
  exit()

bot = tohelper.chal_driver(keys.get_user(), keys.get_key)

print "\nGetting bracket names..."
checker = ""
ids = bot.get_recent(num)
for x in range(len(ids)):
  checker = checker + bot.get_name(ids[x]) + "\n"

print checker
confirm = raw_input("Are you sure you want to delete these? (y)\n")
confirm = confirm.strip()
if confirm == "y":
  print "Deleting..."
  bot.bulk_delete(ids)
  print "Success!"
elif confirm == "Y":
  print "Deleting..."
  bot.bulk_delete(ids)
  print "Success!"
else:
  print "Alright cool just checking!"
