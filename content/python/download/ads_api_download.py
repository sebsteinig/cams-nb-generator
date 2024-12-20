
dataset = "cams-global-atmospheric-composition-forecasts"
request = {
    'variable': ['${variable}'],
    'date': [f'{FORECAST_BASE_TIME}/{FORECAST_BASE_TIME}'],
    'time': ['12:00'],
    'leadtime_hour': ['0'],
    'type': ['forecast'],
    'data_format': 'netcdf_zip',
}

client = cdsapi.Client(url=URL, key=KEY)
client.retrieve(dataset, request).download(f'{DATA_DIR}/{FORECAST_BASE_TIME}_${variable}.zip')