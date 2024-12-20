# Create zonal mean plot
data.mean(dim='longitude').plot(
    figsize=(10, 6),
    title='Zonal Mean AOD'
)
plt.show() 