from Main import df
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource


df["Start_String"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_String"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds = ColumnDataSource(df)
output_file("Time Stamps.html")
f = figure(plot_width = 1660, plot_height = 875, x_axis_type="datetime", title="Motion Stamps")

hover = HoverTool(tooltips=[("Start", "@Start_String"), ("End", "@End_String")])
f.add_tools(hover)
f.quad(left = "Start", right = "End", bottom = 0, top = 1, color="green", source=cds)
f.yaxis.minor_tick_line_color = None
f.yaxis.ticker.desired_num_ticks = 1
show(f)
