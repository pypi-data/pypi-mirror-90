import matplotlib
try:
    matplotlib.use('QT5Agg')  # Required for gui plotting
except Exception as e:
    try:
        matplotlib.use('PyQT5')  # Required for gui plotting
    except Exception as e:
        matplotlib.use('Agg')  # Permits running headless
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
import matplotlib.patheffects as pe
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from io import BytesIO as BIO
from PIL import Image
import warnings
warnings.filterwarnings("ignore")


class plotter(object):
    def __init__(self, data_instance):
        pl.close('all')
        self.__global_xlim = (-0.1, 0.1)
        self.__global_ylim = (-0.1, 0.1)
        self.__global_ylim_resid = (-0.1, 0.1)
        self.__resid_ax = False
        self.__scatter_ax = False
        self.__scatter_fig = False
        self.__plot = None
        self.__startplot = None
        self.inst = data_instance

    def __call__(self, pltarray, *args, **kwargs):
        print("Plotting...")
        pl.close('all')
        return_bytes = False
        scan = False
        auto = False
        delay = 0.5
        dpi = 50
        tight = True
        self.__global_xlim = (-0.1, 0.1)
        self.__global_ylim = (-0.1, 0.1)
        self.__global_ylim_resid = (-0.1, 0.1)
        self.__resid_ax = False
        self.__scatter_ax = False
        self.__scatter_fig = False
        self.__plot = None
        self.__startplot = None


        if 'get_bytes' in kwargs:
            return_bytes = bool(kwargs['get_bytes'])
        if 'scan' in kwargs:
            scan = kwargs['scan']
        if 'auto' in kwargs:
            auto = kwargs['auto']
        if 'delay' in kwargs:
            delay = kwargs['delay']
        if 'dpi' in kwargs:
            dpi = int(kwargs['dpi'])
        if 'tight' in kwargs:
            tight = int(kwargs['tight'])

        self.__set_plotting_backend(return_bytes)
        self.__get_global_lims(pltarray)

        if len(self.inst.matrix._Matrix__buffer_list) == 0:
            return "No data in matrix!"

        for i in range(len(pltarray)):
            buffer_number = pltarray[i]
            buffer = self.inst.matrix._Matrix__buffer_list[buffer_number-1]

            # determine plot type, and call correct routine
            plot_type = self.__get_plot_type(buffer)
            if plot_type == 'heatmap':
                self.__plot = self.__heatmap(buffer, *args, **kwargs)
            else:
                # scatter/line plots can be superimposed so plot has to be initialized outside of plotting method to permit stacking
                if i == 0:
                    self.__start_plot = pl.subplots(nrows=1, ncols=1, figsize=(8, 6), sharey=True, sharex=True)
                    # pl.close('all')
                self.__start_plot, self.__plot = self.__scatterline(buffer_number, plot_type, *args, **kwargs)
                if not auto:
                    print(f"Displaying Buffer {buffer_number}")

            # If scan mode, iterate through stack
            if scan:
                if auto:
                    print(f"Displaying Buffer {pltarray[i]} for {delay} seconds...")
                    matplotlib.pyplot.pause(delay)
                else:
                    userin = input("Press any key to continue, [q] to quit loop:  ")
                    if userin.lower() == 'q':
                        break
                if i < len(pltarray)-1:
                    pass
                    # pl.close('all')

        # if return bytes requested, return bytes
        if return_bytes:
            return self.__get_byte_png(self.__plot, dpi=dpi, tight=tight)
        return "Plotting Complete"

    def __get_plot_type(self, buffer):
        all_plots = ['scatter', 'line', 'heatmap']
        default = 'scatter'

        plot_type = buffer.plot.type.get()

        if plot_type.lower() in all_plots:
            return plot_type.lower()

        X = buffer.data.x.get()
        XE = buffer.data.xe.get()
        Y = buffer.data.y.get()
        YE = buffer.data.ye.get()
        Z = buffer.data.z.get()
        ZE = buffer.data.ze.get()
        X_model = buffer.model.x.get()
        Y_model = buffer.model.y.get()
        Z_model = buffer.model.z.get()
        X_cat = buffer.category.x.get()
        Y_cat = buffer.category.y.get()
        Z_cat = buffer.category.z.get()

        if len(X) > 1 and len(Y) > 1 and len(Z) == 0 and (len(X_model) == 0 or len(Y_model) == 0):
            return 'line'
        elif len(X_cat) > 1 and len(Y_cat) > 1 and len(Z) > 1:
            return 'heatmap'
        return default

    def __heatmap(self, buffer, *args, **kwargs):
        X = buffer.data.x.get()
        Y = buffer.data.y.get()
        Z = buffer.data.z.get()
        X_cat = buffer.category.x.get()
        Y_cat = buffer.category.y.get()
        X_title = buffer.plot.axis.x.title.get()
        X_title_size = buffer.plot.axis.x.label.size.get()
        Y_title = buffer.plot.axis.y.title.get()
        Y_title_size = buffer.plot.axis.y.label.size.get()
        Z_title = buffer.plot.axis.z.title.get()
        Z_title_size = buffer.plot.axis.z.label.size.get()
        plot_title = buffer.plot.title.get()

        X_axis = X if not X_cat else X_cat
        Y_axis = Y if not Y_cat else Y_cat

        data = Z.reshape((len(Y_axis), len(X_axis)))

        fig, ax = pl.subplots()
        pl.rcParams["font.size"] = min(X_title_size, Y_title_size)
        pl.gca().tick_params(axis='y', pad=8, labelsize=Y_title_size)
        pl.gca().tick_params(axis='x', pad=8, labelsize=X_title_size)

        # Plot the heatmap
        im = ax.imshow(data, cmap=matplotlib.cm.rainbow)

        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.set_xticklabels(X_axis)
        ax.set_yticklabels(Y_axis)
        pl.xlabel(X_title, size=X_title_size)
        pl.ylabel(Y_title, size=Y_title_size)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False)

        # Rotate the tick labels and set their alignment.
        pl.setp(ax.get_xticklabels(), rotation=-30, ha="right",
                rotation_mode="anchor")

        # Turn spines off and create white grid.
        for edge, spine in ax.spines.items():
            spine.set_visible(False)
        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
        ax.tick_params(which="minor", bottom=False, left=False)

        # Loop over data dimensions and create text annotations.
        for i in range(len(Y_axis)):
            for j in range(len(X_axis)):
                ax.text(j, i, data[i, j], ha="center", va="center", color='k')

        ax.set_title(plot_title)

        # Create colorbar
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.1 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = pl.colorbar(im, cax=cax)
        cbar.ax.set_ylabel(Z_title, rotation=-90, va="bottom", labelpad=5)

        fig.canvas.flush_events()
        return pl

    def __scatterline(self, buffer_number, plot_type, *args, **kwargs):
        buffer = self.inst.matrix._Matrix__buffer_list[buffer_number-1]
        black_models = False
        scan = False

        if 'black_models' in kwargs:
            black_models = kwargs['black_models']
        if 'scan' in kwargs:
            scan = kwargs['scan']

        #####################################
        # declare variables to tidy up code #
        # ___________________________________#
        X = buffer.data.x.get()
        XE = buffer.data.xe.get()
        Y = buffer.data.y.get()
        YE = buffer.data.ye.get()
        Z = buffer.data.z.get()
        ZE = buffer.data.ze.get()
        show_data = buffer.data.is_visible
        X_model = buffer.model.x.get()
        Y_model = buffer.model.y.get()
        Z_model = buffer.model.z.get()
        model_color = buffer.model.color.get()
        show_model = buffer.model.is_visible
        X_resid = buffer.residuals.x.get()
        Y_resid = buffer.residuals.y.get()
        Z_resid = buffer.residuals.z.get()
        show_residuals = buffer.residuals.is_visible
        series_color = matplotlib.colors.to_hex(buffer.plot.series.color.get() if buffer.plot.series.color.get() != '' else 'r', keep_alpha=True)
        data_weight = buffer.plot.series.weight.get() if buffer.data.weight.get() <= 0 else buffer.data.weight.get()
        model_weight = data_weight/5 if buffer.model.weight.get() <= 0 else buffer.model.weight.get() 
        x_axis_title = buffer.plot.axis.x.title.get()
        y_axis_title = buffer.plot.axis.y.title.get()
        z_axis_title = buffer.plot.axis.z.title.get()
        x_title_size = buffer.plot.axis.x.label.size.get()
        y_title_size = buffer.plot.axis.y.label.size.get()
        z_title_size = buffer.plot.axis.z.label.size.get()
        x_title_show = buffer.plot.axis.x.label.is_visible
        y_title_show = buffer.plot.axis.y.label.is_visible
        z_title_show = buffer.plot.axis.z.label.is_visible
        show_x_lines = buffer.plot.axis.x.lines.is_visible
        x_line_color = buffer.plot.axis.x.lines.color.get()
        x_line_weight = buffer.plot.axis.x.lines.weight.get()
        x_line_is_outlined = buffer.plot.axis.x.lines.outline.is_visible
        x_line_style = buffer.plot.axis.x.lines.line_style.get()
        x_lines = buffer.plot.axis.x.lines.get()
        show_y_lines = buffer.plot.axis.y.lines.is_visible
        y_line_color = buffer.plot.axis.y.lines.color.get()
        y_line_weight = buffer.plot.axis.y.lines.weight.get()
        y_line_is_outlined = buffer.plot.axis.y.lines.outline.is_visible
        y_line_style = buffer.plot.axis.y.lines.line_style.get()
        y_lines = buffer.plot.axis.y.lines.get()
        show_peaks = buffer.plot.axis.y.peaks.is_visible
        peak_indicies = buffer.plot.axis.y.peaks.get()
        peaks = [Y[p] for p in peak_indicies]
        show_peak_bounds = buffer.plot.axis.y.peak_bounds.is_visible
        peak_bounds_indicies = buffer.plot.axis.y.peak_bounds.get()
        show_integrals = buffer.plot.axis.x.integrals.is_visible
        integral_indicies_pairs = buffer.plot.axis.x.integrals.get()
        show_polygons = buffer.plot.polygons.is_visible
        polygon_verticies = buffer.plot.polygons.get()
        x_axis_type = buffer.plot.axis.x.axis_scale.get()
        y_axis_type = buffer.plot.axis.y.axis_scale.get()
        z_axis_type = buffer.plot.axis.z.axis_scale.get()
        x_axis_range = buffer.plot.axis.x.range.get() if len(buffer.plot.axis.x.range.get()) > 1 else buffer.data.x.range()
        y_axis_range = buffer.plot.axis.y.range.get() if len(buffer.plot.axis.y.range.get()) > 1 else buffer.data.y.range()
        z_axis_range = buffer.plot.axis.z.range.get() if len(buffer.plot.axis.z.range.get()) > 1 else buffer.data.z.range()
        # ___________________________________#
        # END Local Variable Definitions    #
        #####################################
        if scan: # if scan create new figure each iteration
            pass
            # self.__start_plot = pl.subplots(nrows=1, ncols=1, figsize=(8, 6), sharey=True, sharex=True)
        if not self.__scatter_ax:
            self.__scatter_fig, self.__scatter_ax = self.__start_plot
            self.__scatter_ax.plot(1, 1)
            self.__scatter_ax.set_xscale(x_axis_type)
            self.__scatter_ax.set_yscale(y_axis_type)
            self.__scatter_ax.grid()
            pl.rcParams["font.size"] = 10
            pl.gca().tick_params(axis='y', pad=8, labelsize=y_title_size)
            pl.gca().tick_params(axis='x', pad=8, labelsize=x_title_size)
            if x_title_show:
                pl.xlabel(x_axis_title, size=x_title_size)
            if y_title_show:
                pl.ylabel(y_axis_title, size=y_title_size)

        if not scan and len(x_axis_range) > 0:
            # do nothing
            pass
        elif scan:
            padding = (max(X)-min(X)) * 0.00
            x_axis_range = (min(X) - padding, max(X) + padding)
        else:
            padding = (max(self.__global_xlim) - min(self.__global_xlim)) * 0.00
            x_axis_range = (min(self.__global_xlim) - padding, max(self.__global_xlim) + padding)

        if scan:
            padding = (max(Y) - min(Y)) * 0.05
            y_axis_range = (min(Y) - padding, max(Y) + padding)
            if len(Y_model) > 0:
                padding_resid = (max(Y_model) - min(Y_model)) * 0.05
                y_resid_axis_range = (min(Y_model) - padding_resid, max(Y_model) + padding_resid)
            else:
                y_resid_axis_range = (0,0)
        else:
            if len(y_axis_range) == 0:
                padding = (max(self.__global_ylim) - min(self.__global_ylim)) * 0.05
                y_axis_range = (min(self.__global_ylim) - padding, max(self.__global_ylim) + padding)
            padding_resid = (max(self.__global_ylim_resid) - min(self.__global_ylim_resid)) * 0.05
            y_resid_axis_range = (min(self.__global_ylim_resid) - padding_resid, max(self.__global_ylim_resid) + padding_resid)

            # Set Plot ranges
            pl.xlim(min(x_axis_range), max(x_axis_range))
            pl.ylim(min(y_axis_range), max(y_axis_range))

        # If Z data, treat as heatmap scatter
        if len(Z) == 0 or len(set(Z)) == 1:
            if plot_type == 'scatter':
                self.__scatter_ax.scatter(X, Y, color=series_color, s=data_weight * 4, zorder=0)  # weight is by area, correct to height val
            else:
                self.__scatter_ax.plot(X, Y, color=series_color, linestyle='-', linewidth=data_weight, zorder=0)
        else:
            # color points by z value and sort to not obscure data in plot
            sorted_X, sorted_Y, sorted_Z = self.__sort_by_z(X, Y, Z)
            if plot_type == 'scatter':
                self.__scatter_ax.scatter(sorted_X, sorted_Y, c=sorted_Z, s=data_weight * 4, cmap=matplotlib.cm.rainbow, zorder=0)  # weight is by area, correct to height val
            else:
                self.__scatter_ax.plot(sorted_X, sorted_Y, c=sorted_Z, linestyle='-', linewidth=data_weight, cmap=matplotlib.cm.rainbow, zorder=0)

        #####################################
        #            Model Plot             #
        # __________________________________#
        if len(X_model) > 0 and show_model:
            if black_models:
                self.__scatter_ax.plot(X_model, Y_model, linestyle='-', color='#000000', linewidth=model_weight, zorder=1)
            elif model_color == series_color:
                self.__scatter_ax.plot(X_model, Y_model, linestyle='-', color=series_color, linewidth=model_weight,
                        path_effects=[pe.Stroke(linewidth=model_weight *2, foreground='#000000'), pe.Normal()],
                        zorder=1)
            else:
                self.__scatter_ax.plot(X_model, Y_model, linestyle='-', color=model_color, linewidth=model_weight,
                                       zorder=1)
        #___________________________________#
        #        END Model Plot             #
        #####################################

        #####################################
        #            Residual Plot          #
        # __________________________________#
        if len(X_resid) > 0 and None not in (min(y_resid_axis_range), max(y_resid_axis_range)) and show_residuals:
            if not self.__resid_ax:
                divider = make_axes_locatable(self.__scatter_ax)
                self.__resid_ax = divider.append_axes("bottom", size="20%", pad=0)
                self.__scatter_ax.figure.add_axes(self.__resid_ax)
                self.__resid_ax.set_xscale(x_axis_type)
                self.__resid_ax.set_yscale(y_axis_type)
                # end residuals plot
                self.__scatter_ax.set_xticklabels([])
                pl.gca().yaxis.set_major_locator(MaxNLocator(prune='upper'))
                # Set x bounds to match data plot
                pl.xlim(min(x_axis_range), max(x_axis_range))
                pl.xlabel(x_axis_title, size=x_title_size)
                self.__resid_ax.axhline(y=0, linestyle='-', color='#000000', linewidth=2, zorder=0)
                self.__resid_ax.grid()
                pl.ylabel('Residuals')
            centered_range = (-1*max(abs(y_resid_axis_range[0]), abs(y_resid_axis_range[1])),
                                max(abs(y_resid_axis_range[0]), abs(y_resid_axis_range[1])))
            self.__resid_ax.set_ylim(min(centered_range), max(centered_range))
            self.__resid_ax.plot(X_resid, Y_resid, linestyle='-', color=series_color, linewidth=model_weight)
        #___________________________________#
        #        END Residual Plot          #
        #####################################

        #####################################
        #     X-line and Y-line Plotting    #
        #___________________________________#
        if show_x_lines and len(x_lines) >= 1:
            for line in x_lines:
                if x_line_is_outlined:
                    self.__scatter_ax.axvline(x=line, linestyle=x_line_style, color=x_line_color,
                                              linewidth=x_line_weight, zorder=2,
                                              path_effects=[
                                                  pe.Stroke(linewidth=x_line_weight * 2, foreground='#000000'),
                                                  pe.Normal()])
                else:
                    self.__scatter_ax.axvline(x=line, linestyle=x_line_style, color=x_line_color,
                                              linewidth=x_line_weight, zorder=2)
        if show_y_lines and len(y_lines) >= 1:
            for line in y_lines:
                if y_line_is_outlined:
                    self.__scatter_ax.axhline(y=line, linestyle=y_line_style, color=y_line_color,
                                              linewidth=y_line_weight, zorder=2,
                                              path_effects=[
                                                  pe.Stroke(linewidth=y_line_weight * 2, foreground='#000000'),
                                                  pe.Normal()])
                else:
                    self.__scatter_ax.axhline(y=line, linestyle=y_line_style, color=y_line_color,
                                              linewidth=y_line_weight, zorder=2)
        # ___________________________________#
        #  END X-line and Y-line Plotting   #
        #####################################

        #####################################
        #           Peak Plotting           #
        # ___________________________________#
        if show_peaks and len(peak_indicies) >= 1:
            peak_x = []
            peak_y = []
            for p in peak_indicies:
                peak_x.append(X[p])
                peak_y.append(Y[p])
            self.__scatter_ax.plot(peak_x, peak_y, "d", markerfacecolor='#808080', markeredgecolor='#000000', zorder=3)
        if show_peak_bounds and len(peak_bounds_indicies) >= 1:
            peak_bound_x = []
            peak_bound_y = []
            for p in peak_bounds_indicies:
                p_start = p[0]
                p_end = p[1]
                peak_bound_x.append(X[p_start])
                peak_bound_y.append(Y[p_start])
                peak_bound_x.append(X[p_end])
                peak_bound_y.append(Y[p_end])
            self.__scatter_ax.plot(peak_bound_x, peak_bound_y, "d", markerfacecolor='#808080', markeredgecolor='#000000', zorder=3)
        # ___________________________________#
        #       END Peak Plotting           #
        #####################################

        #####################################
        #         Integral  Plotting        #
        # ___________________________________#
        if show_integrals and len(integral_indicies_pairs) >= 1:
            if not isinstance(series_color, tuple):
                series_color = matplotlib.colors.to_rgba(series_color)
            int_color = list(series_color)
            int_color[3] = 0.4
            int_color = tuple(int_color)
            int_x = []
            int_y = []
            xy_vals = list(zip(X, Y))
            for int_indx in integral_indicies_pairs:
                int_start = (X[int_indx[0]], Y[int_indx[0]])
                int_end = (X[int_indx[-1]], Y[int_indx[-1]])
                verts = [(int_start[0], 0)] + xy_vals[int_indx[0]:int_indx[1]] + [(int_end[0], 0)]
                poly = matplotlib.patches.Polygon(verts, facecolor=int_color, edgecolor='#808080', zorder=0)
                self.__scatter_ax.add_patch(poly)
        # ___________________________________#
        #     END  Integral  Plotting       #
        #####################################

        #####################################
        #        Polygon Plotting           #
        # ___________________________________#
        if show_polygons and len(polygon_verticies) >= 1:
            for polygon in polygon_verticies:
                poly_x, poly_y = zip(*polygon)
                self.__scatter_ax.plot(poly_x, poly_y, linestyle='-', color='#808080', linewidth=data_weight, zorder=4,
                        path_effects=[pe.Stroke(linewidth=data_weight * 2, foreground='k'), pe.Normal()])
        # ___________________________________#
        #       END  Polygon Plotting       #
        #####################################

        self.__scatter_fig.canvas.flush_events()
        return [self.__scatter_fig, self.__scatter_ax], pl

    def __get_byte_png(self, pl, dpi=50, tight=True):
        global is_savefig
        BIOstream = BIO()
        is_savefig = True
        pl.savefig(BIOstream, format='png', dpi=dpi, bbox_inches='tight')
        pl.close('all')
        is_savefig = False
        BIOstream.seek(0)
        im = Image.open(BIOstream)
        im2 = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im2 = im2.resize(im2.size, Image.ANTIALIAS)
        BIOstream = BIO()
        im2.save(BIOstream, format='PNG', quality=95)
        BIOstream.seek(0)
        byte_png = BIOstream.getvalue()
        pl.close('all')
        return byte_png

    def __sort_by_z(self, X, Y, Z):
        idx = Z.argsort()
        sorted_x, sorted_y, sorted_z = X[idx], Y[idx], Z[idx]
        return sorted_x, sorted_y, sorted_z

    def __get_global_lims(self, pltarray):
        xmin = np.inf
        xmax = -np.inf
        ymin = np.inf
        ymax = -np.inf
        ymin_res = np.inf
        ymax_res = -np.inf

        for num in pltarray:
            if int(num) > len(self.inst.matrix._Matrix__buffer_list):
                continue
            buffer = self.inst.matrix._Matrix__buffer_list[num-1]
            if self.inst.matrix.buffer(num).data.x.length() > 0:
                if np.isfinite(buffer.data.x.min()) and buffer.data.x.min() <= xmin:
                    xmin = buffer.data.x.min()
                if np.isfinite(buffer.data.x.max()) and buffer.data.x.max() >= xmax:
                    xmax = buffer.data.x.max()
            if buffer.data.y.length() > 0:
                if np.isfinite(buffer.data.y.min()) and buffer.data.y.min() <= ymin:
                    ymin = buffer.data.y.min()
                if np.isfinite(buffer.data.y.max()) and buffer.data.y.max() >= ymax:
                    ymax = buffer.data.y.max()
            if buffer.residuals.y.length() > 0:
                if np.isfinite(buffer.residuals.y.min()) and buffer.residuals.y.min() <= ymin_res:
                    ymin_res = buffer.residuals.y.min()
                if np.isfinite(buffer.residuals.y.max()) and buffer.residuals.y.max() >= ymax_res:
                    ymax_res = buffer.residuals.y.max()

        self.__global_xlim = (xmin, xmax)
        self.__global_ylim = (ymin, ymax)
        self.__global_ylim_resid = (ymin_res, ymax_res)
        return True

    def __set_plotting_backend(self, return_bytes):
        # Agg permits headless figure production
        init_backend = matplotlib.rcParams['backend']

        if init_backend.lower() not in ['agg', 'qt5agg']:
            raise ValueError(f'Current MatplotLib backend is not supported: {init_backend}')

        if not return_bytes and init_backend != 'qt5agg':
            try:
                # not returning bytes try to enforce gui if backend is available.  Turn interactive mode on
                matplotlib.use('qt5agg')
                pl.ion()
            except Exception as e:
                print('Using non-GUI backend: ' + str(e))
                matplotlib.use('agg')
                pl.ioff()
        elif return_bytes and init_backend != 'agg':
            try:
                # returning bytes try to enforce NO gui if backend is available.  Turn interactive mode off
                matplotlib.use('agg')
                pl.ioff()
            except Exception as e:
                print('Using GUI backend: ' + str(e))
                matplotlib.use('qt5agg')
                pl.ion()

        pl.close('all')
        print(f"Using MatPlotLib backend: {str(matplotlib.rcParams['backend'])}")
        return
