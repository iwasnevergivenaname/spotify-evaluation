class Alignment:
	def __init__(self, classification):
		self.classification = classification
		self.message = ""
	
	def moral_judgment(self, message):
		self.message = message
		return message


lawful_good = Alignment('lawful good').message("no offense but you're kind of boring")
lawful_neutral = Alignment('lawful neutral').message("like listening to a vine compilation")
lawful_evil = Alignment('lawful evil').message("i'm scared of you")
neutral_good = Alignment('neutral good').message("talented, brilliant, incredible, amazing, show stopping, spectacular")
true_neutral = Alignment('true neutral').message("stuck in the middle with you")
neutral_evil = Alignment('neutral evil').message("never the same, totally unique, completely not ever been done before")
chaotic_good = Alignment('chaotic good').message(
	"unafraid to reference or not reference, put it in a blender, shit on it, vomit on it, eat it, give birth to it")
chaotic_neutral = Alignment('chaotic neutral').message("just the best taste")
chaotic_evil = Alignment('chaotic evil').message("you cannot be tied down")
