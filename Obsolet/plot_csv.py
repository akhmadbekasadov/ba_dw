import matplotlib.pyplot as plt
import numpy as np


y, y_fil_lo, y_fil_hi = np.loadtxt('live_data.csv', dtype=str, delimiter='; ', unpack=True)

y = y.astype(np.float)
y_fil_lo = y_fil_lo.astype(np.float)
y_fil_hi = y_fil_hi.astype(np.float)

n = y.size
T = n / 25
t = np.linspace(0, T, n, endpoint=False)

 

#Draw Plot
plt.subplot(3, 1, 1)
plt.plot(t, y, 'b-', label='Rawdata')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, y_fil_lo, 'g-', linewidth=2, label='Atmung')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, y_fil_hi, 'k-', linewidth=2, label='Herzschalg')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

