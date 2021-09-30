import matplotlib.pyplot as plt

names = ['Business', 'Entertainment', 'Politics','Sport','Tech']

values = [510, 417, 417,511,401]

plt.bar(names, values)
plt.suptitle('Instance of each class')
plt.ylabel('Number of instances')
plt.xlabel('Class names')
plt.savefig("BBC-distribution.pdf")
plt.show()
