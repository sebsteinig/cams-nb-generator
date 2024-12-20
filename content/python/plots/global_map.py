# Create global map visualization
fig = plt.figure(figsize=(12, 8))
ekplots.geomap(
    data,
    projection='PlateCarree',
    colormap='viridis',
    title='Global Aerosol Optical Depth'
)
plt.show() 