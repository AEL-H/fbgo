import go
from getpass import getpass
import fbchat

email = str(getpass("Facebook username:"))
password = str(getpass("Password:"))
target_id = "" #str(getpass("target id:"))


###########################################################################

class GoBot(fbchat.Client):

	def __init__(self,email, password, debug=True, user_agent=None):
		fbchat.Client.__init__(self,email, password, debug, user_agent)
		self.game = go.GoManager()

	def on_message(self, mid, author_id, author_name, message, metadata):
		self.markAsDelivered(author_id, mid)
		self.markAsRead(author_id)

		print("%s said: %s"%(author_id, message))

		if str(author_id) == str(self.uid):
			self.response = self.game.tell(str(message), 0)
		else:
			self.response = self.game.tell(str(message), 1)

		if self.response != None:
			self.send(target_id, self.response)


bot = GoBot(email, password)
bot.listen()







