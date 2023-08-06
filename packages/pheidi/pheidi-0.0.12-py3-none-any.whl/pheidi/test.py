from pheidi import Publisher, Consumer


pub = Publisher("test", 32, 10)

# for i in range(10):
# pub.publish(i)

# print(con.consume())

for i in range(100):
    pub.publish(i)
con2 = Consumer("test", "a", True)

print(con2.consume(minq=3, maxq=3))
print(con2.consume(minq=3, maxq=3))
# print(con2.consume(minq=4, maxq=5))

con2.delete()
pub.delete()
