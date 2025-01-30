
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Ambil data
angles_df = pd.read_csv('final_output_with_angles.csv')
keypoints = pd.read_csv('keypoints.csv', index_col=0)
keypoints2 = pd.read_csv('keypoints2.csv', index_col=0)
keypoints3 = pd.read_csv('keypoints3.csv', index_col=0)

# Ambil posisi awal Keypoint 1 (Body)
fixed_x1 = keypoints.iloc[0]['pixelx']
fixed_y1 = keypoints.iloc[0]['pixely']

# Hitung panjang awal vektor Keypoint 2 ke Keypoint 3
kp2_initial = keypoints2.iloc[0]
kp3_initial = keypoints3.iloc[0]
initial_vector_x = kp3_initial['pixelx'] - kp2_initial['pixelx']
initial_vector_y = kp3_initial['pixely'] - kp2_initial['pixely']
initial_vector_length = np.sqrt(initial_vector_x**2 + initial_vector_y**2)

# Setup plot
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.set_zlim(0, 200)
ax.set_xlabel("Pixel X")
ax.set_ylabel("Pixel Y")
ax.set_zlabel("Pixel Z")

# Inisialisasi plot
point1, = ax.plot([], [], [], 'o', color='green', markersize=8, label="Keypoint 1 (Fixed)")
point2, = ax.plot([], [], [], 'o', color='red', markersize=8, label="Keypoint 2")
point3, = ax.plot([], [], [], 'o', color='blue', markersize=8, label="Keypoint 3")
line1, = ax.plot([], [], [], '-', color='cyan', linewidth=2)
line2, = ax.plot([], [], [], '-', color='cyan', linewidth=2)
ax.legend()

# Tambahkan teks untuk sudut dan waktu dalam figure
angle_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, color="black")

def init():
    angle_text.set_text("")
    return point1, point2, point3, line1, line2, angle_text

def update(frame):
    time_now = frame / 30  # Asumsi 30 FPS
    
    try:
        kp1 = keypoints[keypoints['t'] <= time_now].iloc[-1]
        kp2 = keypoints2[keypoints2['t'] <= time_now].iloc[-1]
    except IndexError:
        return point1, point2, point3, line1, line2, angle_text

    # Hitung posisi adjusted untuk Keypoint 2
    adjusted_x2 = fixed_x1 + (kp2['pixelx'] - kp1['pixelx'])
    adjusted_y2 = fixed_y1
    
    # Gunakan vektor awal untuk menghitung posisi Keypoint 3
    vector_x = initial_vector_x
    vector_y = initial_vector_y
    adjusted_x3 = adjusted_x2 + vector_x
    adjusted_y3 = adjusted_y2 + vector_y
    
    # Tetapkan koordinat Z
    z1, z2, z3 = 100, 125, 125
    
    # Perbarui teks dalam figure
    angle_text.set_text(f"Frame: {frame}\nTime: {time_now:.2f}s")
    
    # Update posisi plot
    point1.set_data_3d([fixed_x1], [fixed_y1], [z1])
    point2.set_data_3d([adjusted_x2], [adjusted_y2], [z2])
    point3.set_data_3d([adjusted_x3], [adjusted_y3], [z3])
    
    line1.set_data_3d([fixed_x1, adjusted_x2], [fixed_y1, adjusted_y2], [z1, z2])
    line2.set_data_3d([adjusted_x2, adjusted_x3], [adjusted_y2, adjusted_y3], [z2, z3])
    
    return point1, point2, point3, line1, line2, angle_text

# Buat animasi
ani = FuncAnimation(
    fig,
    update,
    frames=300,
    init_func=init,
    interval=33,
    blit=False
)

plt.show()


# Simpan semua data ke CSV setelah animasi selesai
# pd.DataFrame(data_frames).to_csv("final_keypoints.csv", index=False)