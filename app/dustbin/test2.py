import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680801)

N = 2
x = ["chandan", "gaurav"]
y = [50, 7]
colors = np.random.rand(N)
area = [i**2 for i in y]  # 0 to 15 point radii

plt.scatter(x, y, s=area, c=colors, alpha=1.5, label=x)
plt.show()
