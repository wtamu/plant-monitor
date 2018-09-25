from dao import ArduinoDAO
from controllers import ArduinoController
from datetime import datetime
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, curdoc, figure


# establish arduino communication
arduinoEndpoint = ArduinoDAO("/dev/ttyACM1")
arduinoController = ArduinoController(arduinoEndpoint)

# Common Configuration Settings
COMMON_FIGURE_CONFIG = {'width': 700, 'plot_height': 200, 'x_axis_type': "datetime"}
COMMON_LINE_CONFIG = {'x': 'x', 'y': 'y', 'line_width': 3, 'line_join': 'bevel'}
COMMON_CIRCLE_CONFIG = {'x': 'x', 'y': 'y', 'line_width': 1, 'size': 4, 'line_color': 'black'}
COMMON_HOVER_CONFIG = {'formatters': {'x': 'datetime'}, 'mode': 'vline'}

# Light Plot
light_cds = ColumnDataSource({'x': [], 'y': []})
light_plot = figure(y_axis_label='Lumens', **COMMON_FIGURE_CONFIG)
light_plot.line(source=light_cds, line_color='khaki', **COMMON_LINE_CONFIG)
light_plot.circle(source=light_cds, fill_color='khaki', **COMMON_CIRCLE_CONFIG)
light_plot_hover = HoverTool(tooltips=[("value", "@y{0.00} lm"), ('date', '@x{%F %T}')], **COMMON_HOVER_CONFIG)
light_plot.add_tools(light_plot_hover)

# Add follow for streaming data
light_plot.x_range.follow = "end"
light_plot.x_range.follow_interval = 60000
light_plot.x_range.range_padding = 0

# Temperature Plot
temperature_cds = ColumnDataSource({'x': [], 'y': []})
temperature_plot = figure(y_axis_label='Fahrenheit', x_range=light_plot.x_range, **COMMON_FIGURE_CONFIG)
temperature_plot.line(source=temperature_cds, line_color='red', **COMMON_LINE_CONFIG)
temperature_plot.circle(source=temperature_cds, fill_color='red', **COMMON_CIRCLE_CONFIG)
temperature_plot_hover = HoverTool(tooltips=[("value", "@y{0.00}\u2109"), ('date', '@x{%F %T}')], **COMMON_HOVER_CONFIG)
temperature_plot.add_tools(temperature_plot_hover)

# Moisture Plot
moisture_cds = ColumnDataSource({'x': [], 'y': []})
moisture_plot = figure(y_axis_label='Humidity', x_range=light_plot.x_range, **COMMON_FIGURE_CONFIG)
moisture_plot.line(source=moisture_cds, line_color='blue', **COMMON_LINE_CONFIG)
moisture_plot.circle(source=moisture_cds, fill_color='blue', **COMMON_CIRCLE_CONFIG)
moisture_plot_hover = HoverTool(tooltips=[("value", "@y{0.00}"), ('date', '@x{%F %T}')], **COMMON_HOVER_CONFIG)
moisture_plot.add_tools(moisture_plot_hover)

plot = gridplot([[light_plot], [temperature_plot], [moisture_plot]], merge_tools=True, toolbar_location='right')


def update():
    now = datetime.now()
    now = now.replace(microsecond=0)
    x = next(iter(arduinoController.readArduino()))
    light_lvl = {'x': [now], 'y': [x.illuminance]}
    temperature_lvl = {'x': [now], 'y': [x.temperature['f']]}
    moisture_lvl = {'x': [now], 'y': [x.soilMoisture]}
    light_cds.stream(light_lvl)
    temperature_cds.stream(temperature_lvl)
    moisture_cds.stream(moisture_lvl)


# show the results
curdoc().add_periodic_callback(update, 3000)
curdoc().add_root(plot)