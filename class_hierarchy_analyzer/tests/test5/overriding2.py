from overriding import FormalLanguage

class Colloquial(FormalLanguage):
    def speak(self):
        super().speak()
        print("That movie was fire. 10/10 peak cinema fr fr")

c = Colloquial()
