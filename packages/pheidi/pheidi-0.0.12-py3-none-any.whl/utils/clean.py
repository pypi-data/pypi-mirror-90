from pheidi import Publisher, Consumer

con2 = Consumer("test", "a")
pub = Publisher("test")

con2.delete()
pub.delete()
