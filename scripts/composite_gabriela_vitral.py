import bpy
import numpy as np

# Clear data
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load images
img_gabriela = bpy.data.images.load('/home/omarchy/Projects/pj-vibe-game/assets/textures/castle_grounds/stained_glass_gabriela.jpg')
img_top = bpy.data.images.load('/home/omarchy/Projects/RENDER96-HD-TEXTURE-PACK/gfx/levels/castle_grounds/2.rgba16.png')
img_bottom = bpy.data.images.load('/home/omarchy/Projects/RENDER96-HD-TEXTURE-PACK/gfx/levels/castle_grounds/1.rgba16.png')

W, H_half = img_top.size[0], img_top.size[1]
H = H_half * 2 # 1024 x 1024

# Extract pixels as numpy float arrays
pix_top = np.array(img_top.pixels[:], dtype=np.float32).reshape((H_half, W, 4))
pix_bottom = np.array(img_bottom.pixels[:], dtype=np.float32).reshape((H_half, W, 4))

# Stack vertically: bottom (Y: 0..H_half) and top (Y: H_half..H)
pix_castle = np.vstack([pix_bottom, pix_top]) # shape (1024, 1024, 4)

# Gabriela image dimensions
gw, gh = img_gabriela.size[0], img_gabriela.size[1]
g_pix = np.array(img_gabriela.pixels[:], dtype=np.float32).reshape((gh, gw, 4 if img_gabriela.channels == 4 else 3))
if g_pix.shape[2] == 3:
    alpha = np.ones((gh, gw, 1), dtype=np.float32)
    g_pix = np.concatenate([g_pix, alpha], axis=2)

crop_y0 = int(gh * 0.12)
crop_y1 = int(gh * 0.95)
cropped_g = g_pix[crop_y0:crop_y1, :, :]
cgh, cgw = cropped_g.shape[0], cropped_g.shape[1]

target_w = 760
target_h = 860
# Bilinear resampling
y_indices = np.linspace(0, cgh - 1, target_h).astype(np.float32)
x_indices = np.linspace(0, cgw - 1, target_w).astype(np.float32)

y0 = np.floor(y_indices).astype(int)
y1 = np.clip(y0 + 1, 0, cgh - 1)
dy = (y_indices - y0)[:, None, None]

x0 = np.floor(x_indices).astype(int)
x1 = np.clip(x0 + 1, 0, cgw - 1)
dx = (x_indices - x0)[None, :, None]

sampled_rows_y0 = cropped_g[y0, :, :]
sampled_rows_y1 = cropped_g[y1, :, :]
sampled = (1 - dy) * ((1 - dx) * sampled_rows_y0[:, x0, :] + dx * sampled_rows_y0[:, x1, :]) + \
          dy * ((1 - dx) * sampled_rows_y1[:, x0, :] + dx * sampled_rows_y1[:, x1, :])

cx, cy = 512, 510
gx0 = cx - target_w // 2
gx1 = gx0 + target_w
gy0 = cy - target_h // 2
gy1 = gy0 + target_h

# Inner oval mask for Gabriela inside the gold bezel
Y, X = np.ogrid[:H, :W]
rx = 345.0
ry = 405.0
dist = ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2
edge_width = 0.05
mask = np.clip((1.0 - dist) / edge_width, 0.0, 1.0)[:, :, None]

final_pix = pix_castle.copy()
g_full = np.zeros((H, W, 4), dtype=np.float32)
g_full[gy0:gy1, gx0:gx1, :] = sampled
final_pix = final_pix * (1.0 - mask) + g_full * mask

# Outer arch mask: make the black background outside the silver arch transparent!
# Arch equation: rounded top (above cy), vertical sides (below cy)
# Silver frame outer limit: radius ~440 horizontally
outer_dist = ((X - cx) / 440.0) ** 2 + (np.maximum(0, Y - cy) / 495.0) ** 2
outer_mask = np.clip((1.05 - outer_dist) / 0.05, 0.0, 1.0)
final_pix[:, :, 3] = np.minimum(final_pix[:, :, 3], outer_mask)

# Save image
out_full = bpy.data.images.new("stained_glass_gabriela", width=W, height=H, alpha=True)
out_full.pixels = final_pix.flatten().tolist()
out_full.filepath_raw = '/home/omarchy/Projects/pj-vibe-game/assets/textures/castle_grounds/stained_glass_gabriela.png'
out_full.file_format = 'PNG'
out_full.save()

print("Re-composited stained_glass_gabriela.png with transparent outer arch!")
