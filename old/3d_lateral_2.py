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

# Ambil posisi awal Keypoint 1
fixed_x1 = keypoints.iloc[0]['pixelx']
fixed_y1 = keypoints.iloc[0]['pixely']

# Setup plot
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 1920)
ax.set_ylim(0, 1080)
ax.set_zlim(0, 200)
ax.set_facecolor("white")
ax.set_xlabel("Pixel X")
ax.set_ylabel("Pixel Y")
ax.set_zlabel("Pixel Z")

# Inisialisasi plot
point1, = ax.plot([], [], [], 'o', color='green', markersize=8, label="Keypoint 1 (Fixed)")
point2, = ax.plot([], [], [], 'o', color='red', markersize=8, label="Keypoint 2")
point3, = ax.plot([], [], [], 'o', color='blue', markersize=8, label="Keypoint 3")
line1, = ax.plot([], [], [], '-', color='cyan', linewidth=2)
line2, = ax.plot([], [], [], '-', color='cyan', linewidth=2)
horizontal_line, = ax.plot([], [], [], '-', color='magenta', linewidth=2, label="Body Line")

# Tambahkan garis imajiner 0 derajat dari Keypoint 2
zero_degree_line, = ax.plot([], [], [], '--', color='black', linewidth=1.5, label="0° Reference Line")

ax.legend()

# Tambahkan teks untuk sudut dan waktu dalam figure
angle_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, color="black")

# List untuk menyimpan semua frame
data_frames = []

def init():
    """Inisialisasi elemen plot sebelum animasi dimulai."""
    angle_text.set_text("")
    return point1, point2, point3, line1, line2, horizontal_line, zero_degree_line, angle_text

def update(frame):
    """Fungsi untuk memperbarui animasi setiap frame."""
    time_now = frame / 30  # Asumsi 30 FPS
    line_length = 500  # Panjang garis horizontal
    
    # Ambil data terbaru berdasarkan timestamp
    try:
        kp1 = keypoints[keypoints['t'] <= time_now].iloc[-1]
        kp2 = keypoints2[keypoints2['t'] <= time_now].iloc[-1]
        kp3 = keypoints3[keypoints3['t'] <= time_now].iloc[-1]
        
        angle_data = angles_df[angles_df['t'] <= time_now].iloc[-1]
    except IndexError:
        return point1, point2, point3, line1, line2, horizontal_line, zero_degree_line, angle_text

    # Hitung offset relatif
    current_x1 = kp1['pixelx']
    current_y1 = kp1['pixely']
    
    # Hitung posisi adjusted untuk Keypoint 2 dan 3
    adjusted_x2 = fixed_x1 + (kp2['pixelx'] - current_x1)
    adjusted_y2 = fixed_y1 + (kp2['pixely'] - current_y1)
    
    adjusted_x3 = fixed_x1 + (kp3['pixelx'] - current_x1)
    adjusted_y3 = fixed_y1 + (kp3['pixely'] - current_y1)
    
    z = 100  # Ketinggian tetap

    # Simpan data untuk ekspor
    data_frames.append({
        "time": time_now,
        "fixed_x1": fixed_x1,
        "fixed_y1": fixed_y1,
        "adjusted_x2": adjusted_x2,
        "adjusted_y2": adjusted_y2,
        "adjusted_x3": adjusted_x3,
        "adjusted_y3": adjusted_y3
    })

    # Ambil data sudut
    index_angle = angle_data.name
    angle1 = angle_data['angle1_deg']
    angle2 = angle_data['angle2_deg']

    # Perbarui teks dalam figure
    angle_text.set_text(f"Frame: {index_angle}\nTime: {time_now:.2f}s\nAngle1: {angle1:.2f}°\nAngle2: {angle2:.2f}°")

    # Update posisi plot
    point1.set_data_3d([fixed_x1], [fixed_y1], [z])
    point2.set_data_3d([adjusted_x2], [adjusted_y2], [z])
    point3.set_data_3d([adjusted_x3], [adjusted_y3], [z])
    
    line1.set_data_3d([fixed_x1, adjusted_x2], [fixed_y1, adjusted_y2], [z, z])
    line2.set_data_3d([adjusted_x2, adjusted_x3], [adjusted_y2, adjusted_y3], [z, z])
    
    horizontal_line.set_data_3d(
        [fixed_x1, fixed_x1 + line_length],
        [fixed_y1, fixed_y1],
        [z, z]
    )

    # Tambahkan garis imajiner 0 derajat dari Keypoint 2
    zero_degree_line.set_data_3d(
        [adjusted_x2, adjusted_x2 + 300],  # Garis sepanjang 300 px di sumbu X
        [adjusted_y2, adjusted_y2],  # Tetap sejajar dengan Keypoint 2
        [z, z]  # Tetap di sumbu Z yang sama
    )

    return point1, point2, point3, line1, line2, horizontal_line, zero_degree_line, angle_text

# Buat animasi
ani = FuncAnimation(
    fig,
    update,
    frames=300,
    init_func=init,
    interval=33,
    blit=False  # blit=False agar teks bisa diperbarui dengan lancar
)

plt.show()

# Simpan semua data ke CSV setelah animasi selesai
# pd.DataFrame(data_frames).to_csv("final_keypoints.csv", index=False)