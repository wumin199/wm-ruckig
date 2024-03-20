from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import ipdb


class Plotter:
    @staticmethod
    def plot_trajectory(filename, otg, inp, out_list, show=False, plot_acceleration=True, plot_jerk=True, time_offsets=None, title=None):
        """
        filename: file to saved
        otg: Ruckig object
        inp: input parameter
        out_list: updated out list
        show:
        plot_acceleration:
        plot_jerk:
        time_offsets: []
        title:
        """
        print("---")
        print("Plotting trajectory")
        print("---")
        taxis = np.array(list(map(lambda x: x.time, out_list)))
        if time_offsets:
            taxis += np.array(time_offsets)
        qaxis = np.array(list(map(lambda x: x.new_position, out_list))) # s
        dqaxis = np.array(list(map(lambda x: x.new_velocity, out_list))) # v
        ddqaxis = np.array(list(map(lambda x: x.new_acceleration, out_list))) # a
        
        print("control_cycle", otg.delta_time)
        print("s:\n", qaxis)
        print("v:\n", ddqaxis)
        print("a:\n", ddqaxis)
        # otg.delta_time: control cycle
        # axis=0, row-wise
        # jerk
        dddqaxis = np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]) / otg.delta_time
        dddqaxis[0, :] = 0.0
        dddqaxis[-1, :] = 0.0

        # 这行代码的作用是创建一个新的图形窗口，其宽度为8.0英寸，高度为2.0 + 3.0 * inp.degrees_of_freedom英寸，分辨率为120 dpi。
        plt.figure(figsize=(8.0, 2.0 + 3.0 * inp.degrees_of_freedom), dpi=120)
        
        # (inp.degrees_of_freedom, 1)的第一个子图
        plt.subplot(inp.degrees_of_freedom, 1, 1)
        if title:
            plt.title(title)

        # j1~j6
        for dof in range(inp.degrees_of_freedom):
            # 每个自由度(关节)，都具有s，v，a，jerk   
            global_max = np.max([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])
            global_min = np.min([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])

            if plot_jerk:
                global_max = max(global_max, np.max(dddqaxis[:, dof]))
                global_min = min(global_min, np.min(dddqaxis[:, dof]))

            plt.subplot(inp.degrees_of_freedom, 1, dof + 1)
            plt.ylabel(f'DoF {dof + 1}')
            plt.plot(taxis, qaxis[:, dof], label=f'Position {dof + 1}')
            plt.plot(taxis, dqaxis[:, dof], label=f'Velocity {dof + 1}')
            if plot_acceleration:
                plt.plot(taxis, ddqaxis[:, dof], label=f'Acceleration {dof + 1}')
            if plot_jerk:
                plt.plot(taxis, dddqaxis[:, dof], label=f'Jerk {dof + 1}')

            # Plot sections
            if hasattr(out_list[-1], 'trajectory'):
                print("has trajectory")
                # ipdb.set_trace()

                linewidth = 1.0 if len(out_list[-1].trajectory.intermediate_durations) < 20 else 0.25
                for t in out_list[-1].trajectory.intermediate_durations:
                    plt.axvline(x=t, color='black', linestyle='--', linewidth=linewidth)

            # Plot limit lines
            if inp.min_position and inp.min_position[dof] > 1.4 * global_min:
                print("plot min_position limit lines")
                plt.axhline(y=inp.min_position[dof], color='grey', linestyle='--', linewidth=1.1)

            if inp.max_position and inp.max_position[dof] < 1.4 * global_max:
                print("plot max_position limit lines")
                plt.axhline(y=inp.max_position[dof], color='grey', linestyle='--', linewidth=1.1)

            if inp.max_velocity[dof] < 1.4 * global_max:
                print("plot max_velocity limit lines")
                plt.axhline(y=inp.max_velocity[dof], color='orange', linestyle='--', linewidth=3.1)

            min_velocity = inp.min_velocity[dof] if inp.min_velocity else -inp.max_velocity[dof]
            if min_velocity > 1.4 * global_min:
                plt.axhline(y=min_velocity, color='orange', linestyle='--', linewidth=1.1)

            if plot_acceleration and inp.max_acceleration[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_acceleration[dof], color='g', linestyle='--', linewidth=1.1)

            min_acceleration = inp.min_acceleration[dof] if inp.min_acceleration else -inp.max_acceleration[dof]
            if plot_acceleration and min_acceleration > 1.4 * global_min:
                plt.axhline(y=min_acceleration, color='g', linestyle='--', linewidth=1.1)

            if plot_jerk and inp.max_jerk[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            if plot_jerk and -inp.max_jerk[dof] > 1.4 * global_min:
                plt.axhline(y=-inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            plt.legend()
            plt.grid(True)
            print("\n================================")

        plt.xlabel('t')

        # c:\Users\xyz\repo\wm-ruckig\examples\01_test.pdf
        plt.savefig(Path(__file__).parent.parent / 'build' / filename)

        if show:
            plt.show()
