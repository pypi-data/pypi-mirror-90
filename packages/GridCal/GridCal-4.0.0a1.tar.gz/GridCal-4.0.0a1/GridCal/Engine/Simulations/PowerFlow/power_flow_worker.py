# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd
import numpy as np
import scipy.sparse as sp
from GridCal.Engine.basic_structures import BusMode, ReactivePowerControlMode, SolverType, TapsControlMode, Logger
from GridCal.Engine.Simulations.PowerFlow.linearized_power_flow import dcpf, lacpf
from GridCal.Engine.Simulations.PowerFlow.helm_power_flow import helm_josep
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import IwamotoNR
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import levenberg_marquardt_pf
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import NR_LS, NR_I_LS, NRD_LS
from GridCal.Engine.Simulations.PowerFlow.fast_decoupled_power_flow import FDPF
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_acdc_power_flow import NR_LS_ACDC, LM_ACDC
from GridCal.Engine.Simulations.PowerFlow.power_flow_results import PowerFlowResults
from GridCal.Engine.Simulations.PowerFlow.power_flow_options import PowerFlowOptions
from GridCal.Engine.Simulations.PowerFlow.power_flow_results import NumericPowerFlowResults
from GridCal.Engine.Core.snapshot_pf_data import SnapshotData
from GridCal.Engine.Core.multi_circuit import MultiCircuit
from GridCal.Engine.Core.common_functions import compile_types
from GridCal.Engine.Core.snapshot_pf_data import compile_snapshot_circuit


class ConvergenceReport:

    def __init__(self):
        self.methods_ = list()
        self.converged_ = list()
        self.error_ = list()
        self.elapsed_ = list()
        self.iterations_ = list()

    def add(self, method, converged, error, elapsed, iterations):
        self.methods_.append(method)
        self.converged_.append(converged)
        self.error_.append(error)
        self.elapsed_.append(elapsed)
        self.iterations_.append(iterations)

    def converged(self):
        if len(self.converged_) > 0:
            return self.converged_[-1]
        else:
            return False

    def error(self):
        if len(self.error_) > 0:
            return self.error_[-1]
        else:
            return 0

    def elapsed(self):
        if len(self.elapsed_) > 0:
            return self.elapsed_[-1]
        else:
            return 0

    def to_dataframe(self):
        data = {'Method': self.methods_,
                'Converged?': self.converged_,
                'Error': self.error_,
                'Elapsed (s)': self.elapsed_,
                'Iterations': self.iterations_}

        df = pd.DataFrame(data)

        return df


def solve(circuit: SnapshotData, options: PowerFlowOptions, report: ConvergenceReport, V0, Sbus, Ibus,
          pq, pv, ref, pqpv, logger=Logger()) -> NumericPowerFlowResults:
    """
    Run a power flow simulation using the selected method (no outer loop controls).
    :param circuit: SnapshotData circuit, this ensures on-demand admittances computation
    :param options: PowerFlow options
    :param report: Convergence report to fill in
    :param V0: Array of initial voltages
    :param Sbus: Array of power injections
    :param Ibus: Array of current injections
    :param pq: Array of pq nodes
    :param pv: Array of pv nodes
    :param ref: Array of slack nodes
    :param pqpv: Array of (sorted) pq and pv nodes
    :param logger: Logger
    :return: NumericPowerFlowResults 
    """

    if options.retry_with_other_methods:
        if circuit.any_control:
            solver_list = [SolverType.NR,
                           SolverType.LM,
                           SolverType.HELM,
                           SolverType.IWAMOTO,
                           SolverType.LACPF]
        else:
            solver_list = [SolverType.NR,
                           SolverType.HELM,
                           SolverType.IWAMOTO,
                           SolverType.LM,
                           SolverType.LACPF]

        if options.solver_type in solver_list:
            solver_list.remove(options.solver_type)

        solvers = [options.solver_type] + solver_list
    else:
        # No retry selected
        solvers = [options.solver_type]

    # set worked to false to enter in the loop
    solver_idx = 0

    # set the initial value

    final_solution = NumericPowerFlowResults(V=V0,
                                             converged=False,
                                             norm_f=1e200,
                                             Scalc=Sbus,
                                             ma=circuit.branch_data.m[:, 0],
                                             theta=circuit.branch_data.theta[:, 0],
                                             Beq=circuit.branch_data.Beq[:, 0],
                                             iterations=0,
                                             elapsed=0)

    while solver_idx < len(solvers) and not final_solution.converged:
        # get the solver
        solver_type = solvers[solver_idx]

        # type HELM
        if solver_type == SolverType.HELM:
            solution = helm_josep(Ybus=circuit.Ybus,
                                  Yseries=circuit.Yseries,
                                  V0=V0,  # take V0 instead of V
                                  S0=Sbus,
                                  Ysh0=circuit.Yshunt,
                                  pq=pq,
                                  pv=pv,
                                  sl=ref,
                                  pqpv=pqpv,
                                  tolerance=options.tolerance,
                                  max_coeff=options.max_iter,
                                  use_pade=True,
                                  verbose=False)

        # type DC
        elif solver_type == SolverType.DC:
            solution = dcpf(Ybus=circuit.Ybus,
                            Bpqpv=circuit.Bpqpv,
                            Bref=circuit.Bref,
                            Sbus=Sbus,
                            Ibus=Ibus,
                            V0=V0,
                            ref=ref,
                            pvpq=pqpv,
                            pq=pq,
                            pv=pv)

        # LAC PF
        elif solver_type == SolverType.LACPF:
            solution = lacpf(Y=circuit.Ybus,
                             Ys=circuit.Yseries,
                             S=Sbus,
                             I=Ibus,
                             Vset=V0,
                             pq=pq,
                             pv=pv)

        # Levenberg-Marquardt
        elif solver_type == SolverType.LM:
            if circuit.any_control:
                solution = LM_ACDC(nc=circuit,
                                   tolerance=options.tolerance,
                                   max_iter=options.max_iter)
            else:
                solution = levenberg_marquardt_pf(Ybus=circuit.Ybus,
                                                  Sbus=Sbus,
                                                  V0=final_solution.V,
                                                  Ibus=Ibus,
                                                  pv=pv,
                                                  pq=pq,
                                                  tol=options.tolerance,
                                                  max_it=options.max_iter)

        # Fast decoupled
        elif solver_type == SolverType.FASTDECOUPLED:
            solution = FDPF(Vbus=V0,
                            Sbus=Sbus,
                            Ibus=Ibus,
                            Ybus=circuit.Ybus,
                            B1=circuit.B1,
                            B2=circuit.B2,
                            pq=pq,
                            pv=pv,
                            pqpv=pqpv,
                            tol=options.tolerance,
                            max_it=options.max_iter)

        # Newton-Raphson (full)
        elif solver_type == SolverType.NR:

            if circuit.any_control:
                # Solve NR with the AC/DC algorithm
                solution = NR_LS_ACDC(nc=circuit,
                                      tolerance=options.tolerance,
                                      max_iter=options.max_iter,
                                      acceleration_parameter=options.backtracking_parameter,
                                      mu_0=options.mu)
            else:
                # Solve NR with the AC algorithm
                solution = NR_LS(Ybus=circuit.Ybus,
                                 Sbus=Sbus,
                                 V0=final_solution.V,
                                 Ibus=Ibus,
                                 pv=pv,
                                 pq=pq,
                                 tol=options.tolerance,
                                 max_it=options.max_iter,
                                 mu_0=options.mu,
                                 acceleration_parameter=options.backtracking_parameter)

        # Newton-Raphson-Decpupled
        elif solver_type == SolverType.NRD:
            # Solve NR with the linear AC solution
            solution = NRD_LS(Ybus=circuit.Ybus,
                              Sbus=Sbus,
                              V0=final_solution.V,
                              Ibus=Ibus,
                              pv=pv,
                              pq=pq,
                              tol=options.tolerance,
                              max_it=options.max_iter,
                              acceleration_parameter=options.backtracking_parameter)

        # Newton-Raphson-Iwamoto
        elif solver_type == SolverType.IWAMOTO:
            solution = IwamotoNR(Ybus=circuit.Ybus,
                                 Sbus=Sbus,
                                 V0=final_solution.V,
                                 Ibus=Ibus,
                                 pv=pv,
                                 pq=pq,
                                 tol=options.tolerance,
                                 max_it=options.max_iter,
                                 robust=True)

        # Newton-Raphson in current equations
        elif solver_type == SolverType.NRI:
            solution = NR_I_LS(Ybus=circuit.Ybus,
                               Sbus_sp=Sbus,
                               V0=final_solution.V,
                               Ibus_sp=Ibus,
                               pv=pv,
                               pq=pq,
                               tol=options.tolerance,
                               max_it=options.max_iter)

        else:
            # for any other method, raise exception
            raise Exception(solver_type + ' Not supported in power flow mode')

        # record the method used, if it improved the solution
        if solution.norm_f < final_solution.norm_f:
            report.add(method=solver_type,
                       converged=solution.converged,
                       error=solution.norm_f,
                       elapsed=solution.elapsed,
                       iterations=solution.iterations)
            final_solution = solution

        # record the solver steps
        solver_idx += 1

    if not final_solution.converged:
        logger.append('Did not converge, even after retry!, Error:' + str(final_solution.norm_f))

    if final_solution.ma is None:
        final_solution.ma = circuit.branch_data.m[:, 0]

    if final_solution.theta is None:
        final_solution.theta = circuit.branch_data.theta[:, 0]

    if final_solution.Beq is None:
        final_solution.Beq = circuit.branch_data.Beq[:, 0]

    return final_solution


def outer_loop_power_flow(circuit: SnapshotData, options: PowerFlowOptions,
                          voltage_solution, Sbus, Ibus, branch_rates, t=0, logger=Logger()) -> "PowerFlowResults":
    """
    Run a power flow simulation for a single circuit using the selected outer loop
    controls. This method shouldn't be called directly.

    Arguments:

        **circuit**: CalculationInputs instance

        **solver_type**: type of power flow to use first

        **voltage_solution**: vector of initial voltages

        **Sbus**: vector of power injections

        **Ibus**: vector of current injections

        **Ysh**: vector of admittance injections from the shunt devices (the legs of the PI branch are included already)

        **Sinstalled**: vector of installed power per bus in MVA

        **t**: (optional) time step

    Return:

        PowerFlowResults instance
    """

    # get the original types and compile this class' own lists of node types for thread independence
    original_types = circuit.bus_types.copy()
    bus_types = circuit.bus_types.copy()
    # vd, pq, pv, pqpv = compile_types(Sbus, original_types, logger)

    vd = circuit.vd.copy()
    pq = circuit.pq.copy()
    pv = circuit.pv.copy()
    pqpv = circuit.pqpv.copy()

    # copy the tap positions
    tap_positions = circuit.tr_tap_position.copy()
    tap_module = circuit.branch_data.m[:, t]

    # control flags
    any_q_control_issue = True
    any_tap_control_issue = True

    # outer loop max iterations
    control_max_iter = options.max_outer_loop_iter

    # The control iterations are either the number of tap_regulated transformers or 10, the larger of the two
    # if self.options.control_Q == ReactivePowerControlMode.Iterative:
    #     control_max_iter = 999  # TODO: Discuss what to do with these options
    # else:
    #     control_max_iter = 10
    #
    # # Alter the outer loop max iterations if the transformer tap control is active
    # for k in circuit.bus_to_regulated_idx:   # indices of the branches that are regulated at the bus "to"
    #     control_max_iter = max(control_max_iter, circuit.max_tap[k] + circuit.min_tap[k])

    # For the iterate_pv_control logic:
    Vset = voltage_solution.copy()  # Origin voltage set-points
    Scalc = Sbus

    report = ConvergenceReport()

    # modify the Ybus to include the shunts
    Ybus = circuit.Ybus  # + sp.diags(Ysh)

    solution = NumericPowerFlowResults(V=voltage_solution,
                                       converged=False,
                                       norm_f=1e200,
                                       Scalc=Sbus,
                                       ma=circuit.branch_data.m[:, 0],
                                       theta=circuit.branch_data.theta[:, 0],
                                       Beq=circuit.branch_data.Beq[:, 0],
                                       iterations=0,
                                       elapsed=0)

    # this the "outer-loop"
    outer_it = 0
    while (any_q_control_issue or any_tap_control_issue) and outer_it < control_max_iter:

        if len(circuit.vd) == 0:
            voltage_solution = np.zeros(len(Sbus), dtype=complex)
            normF = 0
            Scalc = Sbus.copy()
            any_q_control_issue = False
            converged = True
            logger.append('Not solving power flow because there is no slack bus')
        else:

            # run the power flow method that shall be run
            solution = solve(circuit=circuit,
                             options=options,
                             report=report,  # is modified here
                             V0=voltage_solution,
                             Sbus=Sbus,
                             Ibus=Ibus,
                             pq=pq,
                             pv=pv,
                             ref=vd,
                             pqpv=pqpv,
                             logger=logger)

            if options.distributed_slack:
                # Distribute the slack power
                slack_power = Scalc[vd].real.sum()
                total_installed_power = circuit.bus_installed_power.sum()

                if total_installed_power > 0.0:
                    delta = slack_power * circuit.bus_installed_power / total_installed_power

                    # repeat power flow with the redistributed power
                    solution = solve(circuit=circuit,
                                     options=options,
                                     report=report,  # is modified here
                                     V0=voltage_solution,
                                     Sbus=Sbus + delta,
                                     Ibus=Ibus,
                                     pq=pq,
                                     pv=pv,
                                     ref=vd,
                                     pqpv=pqpv,
                                     logger=logger)

                    # increase the metrics with the second run numbers
                    # it += it2
                    # el += el2

            if solution.converged:

                # Check controls
                if options.control_Q == ReactivePowerControlMode.Direct:

                    solution.V, \
                    Qnew, \
                    types_new, \
                    any_q_control_issue = control_q_direct(V=solution.V,
                                                           Vset=np.abs(solution.V),
                                                           Q=Scalc.imag,
                                                           Qmax=circuit.Qmax_bus[:, t],
                                                           Qmin=circuit.Qmin_bus[:, t],
                                                           types=bus_types,
                                                           original_types=original_types,
                                                           verbose=options.verbose)

                elif options.control_Q == ReactivePowerControlMode.Iterative:

                    Qnew, \
                    types_new, \
                    any_q_control_issue = control_q_iterative(V=solution.V,
                                                              Vset=Vset,
                                                              Q=Scalc.imag,
                                                              Qmax=circuit.Qmax_bus,
                                                              Qmin=circuit.Qmin_bus,
                                                              types=bus_types,
                                                              original_types=original_types,
                                                              verbose=options.verbose,
                                                              k=options.q_steepness_factor)

                else:
                    # did not check Q limits
                    any_q_control_issue = False
                    types_new = bus_types
                    Qnew = Scalc.imag

                # Check the actions of the Q-control
                if any_q_control_issue:
                    bus_types = types_new
                    Sbus = Sbus.real + 1j * Qnew
                    vd, pq, pv, pqpv = compile_types(Sbus, types_new, logger)
                else:
                    if options.verbose:
                        print('Q controls Ok')

                # control the transformer taps
                stable = True
                if options.control_taps == TapsControlMode.Direct:

                    stable, tap_module, \
                    tap_positions = control_taps_direct(voltage=solution.V,
                                                        T=circuit.T,
                                                        bus_to_regulated_idx=circuit.tr_bus_to_regulated_idx,
                                                        tap_position=tap_positions,
                                                        tap_module=tap_module,
                                                        min_tap=circuit.tr_min_tap,
                                                        max_tap=circuit.tr_max_tap,
                                                        tap_inc_reg_up=circuit.tr_tap_inc_reg_up,
                                                        tap_inc_reg_down=circuit.tr_tap_inc_reg_down,
                                                        vset=circuit.tr_vset,
                                                        tap_index_offset=circuit.nline,
                                                        verbose=options.verbose)

                elif options.control_taps == TapsControlMode.Iterative:

                    stable, tap_module, \
                    tap_positions = control_taps_iterative(voltage=solution.V,
                                                           T=circuit.T,
                                                           bus_to_regulated_idx=circuit.tr_bus_to_regulated_idx,
                                                           tap_position=tap_positions,
                                                           tap_module=tap_module,
                                                           min_tap=circuit.tr_min_tap,
                                                           max_tap=circuit.tr_max_tap,
                                                           tap_inc_reg_up=circuit.tr_tap_inc_reg_up,
                                                           tap_inc_reg_down=circuit.tr_tap_inc_reg_down,
                                                           vset=circuit.tr_vset,
                                                           verbose=options.verbose)

                if not stable:
                    # recompute the admittance matrices based on the tap changes
                    # the changes are stored internally, and passed o to the solvers
                    circuit.re_calc_admittance_matrices(tap_module, t=t)

                any_tap_control_issue = not stable

            else:
                any_q_control_issue = False
                any_tap_control_issue = False

        # increment the outer control iterations counter
        outer_it += 1

    if options.verbose:
        print("Stabilized in {} iteration(s) (outer control loop)".format(outer_it))

    # Compute the branches power and the slack buses power
    Sfb, Stb, If, It, Vbranch, loading, losses, \
     flow_direction, Sbus = power_flow_post_process(calculation_inputs=circuit,
                                                    Sbus=solution.Scalc,
                                                    V=solution.V,
                                                    branch_rates=branch_rates)

    # voltage, Sf, loading, losses, error, converged, Qpv
    results = PowerFlowResults(n=circuit.nbus,
                               m=circuit.nbr,
                               n_tr=circuit.ntr,
                               n_hvdc=circuit.nhvdc,
                               bus_names=circuit.bus_names,
                               branch_names=circuit.branch_names,
                               transformer_names=circuit.tr_names,
                               hvdc_names=circuit.hvdc_names,
                               bus_types=bus_types)
    results.Sbus = solution.Scalc
    results.voltage = solution.V
    results.Sf = Sfb  # in MVA already
    results.St = Stb  # in MVA already
    results.If = If  # in p.u.
    results.It = It  # in p.u.
    results.ma = solution.ma
    results.theta = solution.theta
    results.Beq = solution.Beq
    results.Vbranch = Vbranch
    results.loading = loading
    results.losses = losses
    results.flow_direction = flow_direction
    results.transformer_tap_module = solution.ma[circuit.transformer_idx]
    results.convergence_reports.append(report)
    results.Qpv = Sbus.imag[pv]

    # compile HVDC results
    results.hvdc_sent_power = circuit.hvdc_Pf
    results.hvdc_loading = circuit.hvdc_loading
    results.hvdc_losses = circuit.hvdc_losses

    return results


def get_q_increment(V1, V2, k):
    """
    Logistic function to get the Q increment gain using the difference
    between the current voltage (V1) and the target voltage (V2).

    The gain varies between 0 (at V1 = V2) and inf (at V2 - V1 = inf).

    The default steepness factor k was set through trial an error. Other values may
    be specified as a :ref:`PowerFlowOptions<pf_options>`.

    Arguments:

        **V1** (float): Current voltage

        **V2** (float): Target voltage

        **k** (float, 30): Steepness factor

    Returns:

        Q increment gain
    """

    return 2 * (1 / (1 + np.exp(-k * np.abs(V2 - V1))) - 0.5)


def control_q_iterative(V, Vset, Q, Qmax, Qmin, types, original_types, verbose, k):
    """
    Change the buses type in order to control the generators reactive power using
    iterative changes in Q to reach Vset.

    Arguments:

        **V** (list): array of voltages (all buses)

        **Vset** (list): Array of set points (all buses)

        **Q** (list): Array of reactive power (all buses)

        **Qmin** (list): Array of minimal reactive power (all buses)

        **Qmax** (list): Array of maximal reactive power (all buses)

        **types** (list): Array of types (all buses)

        **original_types** (list): Types as originally intended (all buses)

        **verbose** (list): output messages via the console

        **k** (float, 30): Steepness factor

    Return:

        **Qnew** (list): New reactive power values

        **types_new** (list): Modified types array

        **any_control_issue** (bool): Was there any control issue?
    """

    if verbose:
        print('Q control logic (iterative)')

    n = len(V)
    Vm = abs(V)
    Qnew = Q.copy()
    types_new = types.copy()
    any_control_issue = False
    precision = 4
    inc_prec = int(1.5 * precision)

    for i in range(n):

        if types[i] == BusMode.Slack.value:
            pass

        elif types[i] == BusMode.PQ.value and original_types[i] == BusMode.PV.value:

            gain = get_q_increment(Vm[i], abs(Vset[i]), k)

            if round(Vm[i], precision) < round(abs(Vset[i]), precision):
                increment = round(abs(Qmax[i] - Q[i]) * gain, inc_prec)

                if increment > 0 and Q[i] + increment < Qmax[i]:
                    # I can push more VAr, so let's do so
                    Qnew[i] = Q[i] + increment
                    if verbose:
                        print("Bus {} gain = {} (V = {}, Vset = {})".format(i,
                                                                            round(gain, precision),
                                                                            round(Vm[i], precision),
                                                                            abs(Vset[i])))
                        print("Bus {} increment = {} (Q = {}, Qmax = {})".format(i,
                                                                                 round(increment, inc_prec),
                                                                                 round(Q[i], precision),
                                                                                 round(abs(Qmax[i]), precision),
                                                                                 ))
                        print("Bus {} raising its Q from {} to {} (V = {}, Vset = {})".format(i,
                                                                                              round(Q[i], precision),
                                                                                              round(Qnew[i], precision),
                                                                                              round(Vm[i], precision),
                                                                                              abs(Vset[i]),
                                                                                              ))
                    any_control_issue = True

                else:
                    if verbose:
                        print("Bus {} stable enough (inc = {}, Q = {}, Qmax = {}, V = {}, Vset = {})".format(i,
                                                                                                             round(
                                                                                                                 increment,
                                                                                                                 inc_prec),
                                                                                                             round(Q[i],
                                                                                                                   precision),
                                                                                                             round(abs(
                                                                                                                 Qmax[
                                                                                                                     i]),
                                                                                                                   precision),
                                                                                                             round(
                                                                                                                 Vm[i],
                                                                                                                 precision),
                                                                                                             abs(Vset[
                                                                                                                     i]),
                                                                                                             )
                              )

            elif round(Vm[i], precision) > round(abs(Vset[i]), precision):
                increment = round(abs(Qmin[i] - Q[i]) * gain, inc_prec)

                if increment > 0 and Q[i] - increment > Qmin[i]:
                    # I can pull more VAr, so let's do so
                    Qnew[i] = Q[i] - increment
                    if verbose:
                        print("Bus {} increment = {} (Q = {}, Qmin = {})".format(i,
                                                                                 round(increment, inc_prec),
                                                                                 round(Q[i], precision),
                                                                                 round(abs(Qmin[i]), precision),
                                                                                 )
                              )
                        print("Bus {} gain = {} (V = {}, Vset = {})".format(i,
                                                                            round(gain, precision),
                                                                            round(Vm[i], precision),
                                                                            abs(Vset[i]),
                                                                            )
                              )
                        print("Bus {} lowering its Q from {} to {} (V = {}, Vset = {})".format(i,
                                                                                               round(Q[i], precision),
                                                                                               round(Qnew[i],
                                                                                                     precision),
                                                                                               round(Vm[i], precision),
                                                                                               abs(Vset[i]),
                                                                                               )
                              )
                    any_control_issue = True

                else:
                    if verbose:
                        print("Bus {} stable enough (inc = {}, Q = {}, Qmin = {}, V = {}, Vset = {})".format(i,
                                                                                                             round(
                                                                                                                 increment,
                                                                                                                 inc_prec),
                                                                                                             round(Q[i],
                                                                                                                   precision),
                                                                                                             round(abs(
                                                                                                                 Qmin[
                                                                                                                     i]),
                                                                                                                   precision),
                                                                                                             round(
                                                                                                                 Vm[i],
                                                                                                                 precision),
                                                                                                             abs(Vset[
                                                                                                                     i]),
                                                                                                             )
                              )

            else:
                if verbose:
                    print("Bus {} stable (V = {}, Vset = {})".format(i,
                                                                     round(Vm[i], precision),
                                                                     abs(Vset[i]),
                                                                     )
                          )

        elif types[i] == BusMode.PV.value:
            # If it's still in PV mode (first run), change it to PQ mode
            types_new[i] = BusMode.PQ.value
            Qnew[i] = 0
            if verbose:
                print("Bus {} switching to PQ control, with a Q of 0".format(i))
            any_control_issue = True

    return Qnew, types_new, any_control_issue


def power_flow_post_process(calculation_inputs: SnapshotData, Sbus, V, branch_rates):
    """
    Compute the power flows trough the branches.

    Arguments:

        **calculation_inputs**: instance of Circuit

        **V**: Voltage solution array for the circuit buses

        **only_power**: compute only the power injection

    Returns:

        Sf (MVA), If (p.u.), loading (p.u.), losses (MVA), Sbus(MVA)
    """
    # Compute the slack and pv buses power
    vd = calculation_inputs.vd
    pv = calculation_inputs.pv

    # power at the slack nodes
    Sbus[vd] = V[vd] * np.conj(calculation_inputs.Ybus[vd, :].dot(V))

    # Reactive power at the pv nodes
    P = Sbus[pv].real
    Q = (V[pv] * np.conj(calculation_inputs.Ybus[pv, :].dot(V))).imag
    Sbus[pv] = P + 1j * Q  # keep the original P injection and set the calculated reactive power

    # Branches current, loading, etc
    Vf = calculation_inputs.Cf * V
    Vt = calculation_inputs.Ct * V
    If = calculation_inputs.Yf * V
    It = calculation_inputs.Yt * V
    Sf = Vf * np.conj(If)
    St = Vt * np.conj(It)

    # Branch losses in MVA
    losses = (Sf + St) * calculation_inputs.Sbase

    flow_direction = Sf.real / np.abs(Sf + 1e-20)

    # branch voltage increment
    Vbranch = Vf - Vt

    # Branch power in MVA
    Sfb = Sf * calculation_inputs.Sbase
    Stb = St * calculation_inputs.Sbase

    # Branch loading in p.u.
    loading = Sfb / (branch_rates + 1e-9)

    return Sfb, Stb, If, It, Vbranch, loading, losses, flow_direction, Sbus


def control_q_direct(V, Vset, Q, Qmax, Qmin, types, original_types, verbose=False):
    """
    Change the buses type in order to control the generators reactive power.

    Arguments:

        **pq** (list): array of pq indices

        **pv** (list): array of pq indices

        **ref** (list): array of pq indices

        **V** (list): array of voltages (all buses)

        **Vset** (list): Array of set points (all buses)

        **Q** (list): Array of reactive power (all buses)

        **types** (list): Array of types (all buses)

        **original_types** (list): Types as originally intended (all buses)

        **verbose** (bool): output messages via the console

    Returns:

        **Vnew** (list): New voltage values

        **Qnew** (list): New reactive power values

        **types_new** (list): Modified types array

        **any_control_issue** (bool): Was there any control issue?

    ON PV-PQ BUS TYPE SWITCHING LOGIC IN POWER FLOW COMPUTATION
    Jinquan Zhao

    1) Bus i is a PQ bus in the previous iteration and its
       reactive power was fixed at its lower limit:

        If its voltage magnitude Vi ≥ Viset, then

            it is still a PQ bus at current iteration and set Qi = Qimin .

            If Vi < Viset , then

                compare Qi with the upper and lower limits.

                If Qi ≥ Qimax , then
                    it is still a PQ bus but set Qi = Qimax .
                If Qi ≤ Qimin , then
                    it is still a PQ bus and set Qi = Qimin .
                If Qimin < Qi < Qi max , then
                    it is switched to PV bus, set Vinew = Viset.

    2) Bus i is a PQ bus in the previous iteration and
       its reactive power was fixed at its upper limit:

        If its voltage magnitude Vi ≤ Viset , then:
            bus i still a PQ bus and set Q i = Q i max.

            If Vi > Viset , then

                Compare between Qi and its upper/lower limits

                If Qi ≥ Qimax , then
                    it is still a PQ bus and set Q i = Qimax .
                If Qi ≤ Qimin , then
                    it is still a PQ bus but let Qi = Qimin in current iteration.
                If Qimin < Qi < Qimax , then
                    it is switched to PV bus and set Vinew = Viset

    3) Bus i is a PV bus in the previous iteration.

        Compare Q i with its upper and lower limits.

        If Qi ≥ Qimax , then
            it is switched to PQ and set Qi = Qimax .
        If Qi ≤ Qimin , then
            it is switched to PQ and set Qi = Qimin .
        If Qi min < Qi < Qimax , then
            it is still a PV bus.
    """

    if verbose:
        print('Q control logic (fast)')

    n = len(V)
    Vm = abs(V)
    Qnew = Q.copy()
    Vnew = V.copy()
    types_new = types.copy()
    any_control_issue = False
    for i in range(n):

        if types[i] == BusMode.Slack.value:
            pass

        elif types[i] == BusMode.PQ.value and original_types[i] == BusMode.PV.value:

            if Vm[i] != Vset[i]:

                if Q[i] >= Qmax[i]:  # it is still a PQ bus but set Q = Qmax .
                    Qnew[i] = Qmax[i]

                elif Q[i] <= Qmin[i]:  # it is still a PQ bus and set Q = Qmin .
                    Qnew[i] = Qmin[i]

                else:  # switch back to PV, set Vnew = Vset.
                    if verbose:
                        print('Bus', i, 'switched back to PV')
                    types_new[i] = BusMode.PV.value
                    Vnew[i] = complex(Vset[i], 0)

                any_control_issue = True

            else:
                pass  # The voltages are equal

        elif types[i] == BusMode.PV.value:

            if Q[i] >= Qmax[i]:  # it is switched to PQ and set Q = Qmax .
                if verbose:
                    print('Bus', i, 'switched to PQ: Q', Q[i], ' Qmax:', Qmax[i])
                types_new[i] = BusMode.PQ.value
                Qnew[i] = Qmax[i]
                any_control_issue = True

            elif Q[i] <= Qmin[i]:  # it is switched to PQ and set Q = Qmin .
                if verbose:
                    print('Bus', i, 'switched to PQ: Q', Q[i], ' Qmin:', Qmin[i])
                types_new[i] = BusMode.PQ.value
                Qnew[i] = Qmin[i]
                any_control_issue = True

            else:  # it is still a PV bus.
                pass

        else:
            pass

    return Vnew, Qnew, types_new, any_control_issue


def tap_up(tap, max_tap):
    """
    Go to the next upper tap position
    """
    if tap + 1 <= max_tap:
        return tap + 1
    else:
        return tap


def tap_down(tap, min_tap):
    """
    Go to the next upper tap position
    """
    if tap - 1 >= min_tap:
        return tap - 1
    else:
        return tap


def control_taps_iterative(voltage, T, bus_to_regulated_idx, tap_position, tap_module, min_tap, max_tap,
                           tap_inc_reg_up, tap_inc_reg_down, vset, verbose=False):
    """
    Change the taps and compute the continuous tap magnitude.

    Arguments:

        **voltage** (list): array of bus voltages solution

        **T** (list): array of indices of the "to" buses of each branch

        **bus_to_regulated_idx** (list): array with the indices of the branches that regulate the bus "to"

        **tap_position** (list): array of branch tap positions

        **tap_module** (list): array of branch tap modules

        **min_tap** (list): array of minimum tap positions

        **max_tap** (list): array of maximum tap positions

        **tap_inc_reg_up** (list): array of tap increment when regulating up

        **tap_inc_reg_down** (list): array of tap increment when regulating down

        **vset** (list): array of set voltages to control

    Returns:

        **stable** (bool): Is the system stable (i.e.: are controllers stable)?

        **tap_magnitude** (list): Tap module at each bus in per unit

        **tap_position** (list): Tap position at each bus
    """

    stable = True
    for i in bus_to_regulated_idx:  # traverse the indices of the branches that are regulated at the "to" bus

        j = T[i]  # get the index of the "to" bus of the branch "i"
        v = np.abs(voltage[j])
        if verbose:
            print("Bus", j, "regulated by branch", i, ": U =", round(v, 4), "pu, U_set =", vset[i])

        if tap_position[i] > 0:

            if vset[i] > v + tap_inc_reg_up[i] / 2:
                if tap_position[i] == min_tap[i]:
                    if verbose:
                        print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_down(tap_position[i], min_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_up[i]
                    if verbose:
                        print("Branch", i, ": Lowering from tap ", tap_position[i])
                    stable = False

            elif vset[i] < v - tap_inc_reg_up[i] / 2:
                if tap_position[i] == max_tap[i]:
                    if verbose:
                        print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_up(tap_position[i], max_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_up[i]
                    if verbose:
                        print("Branch", i, ": Raising from tap ", tap_position[i])
                    stable = False

        elif tap_position[i] < 0:
            if vset[i] > v + tap_inc_reg_down[i] / 2:
                if tap_position[i] == min_tap[i]:
                    if verbose:
                        print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_down(tap_position[i], min_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_down[i]
                    if verbose:
                        print("Branch", i, ": Lowering from tap", tap_position[i])
                    stable = False

            elif vset[i] < v - tap_inc_reg_down[i] / 2:
                if tap_position[i] == max_tap[i]:
                    print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_up(tap_position[i], max_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_down[i]
                    if verbose:
                        print("Branch", i, ": Raising from tap", tap_position[i])
                    stable = False

        else:
            if vset[i] > v + tap_inc_reg_up[i] / 2:
                if tap_position[i] == min_tap[i]:
                    if verbose:
                        print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_down(tap_position[i], min_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_down[i]
                    if verbose:
                        print("Branch", i, ": Lowering from tap ", tap_position[i])
                    stable = False

            elif vset[i] < v - tap_inc_reg_down[i] / 2:
                if tap_position[i] == max_tap[i]:
                    if verbose:
                        print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                else:
                    tap_position[i] = tap_up(tap_position[i], max_tap[i])
                    tap_module[i] = 1.0 + tap_position[i] * tap_inc_reg_up[i]
                    if verbose:
                        print("Branch", i, ": Raising from tap ", tap_position[i])
                    stable = False

    return stable, tap_module, tap_position


def control_taps_direct(voltage, T, bus_to_regulated_idx, tap_position, tap_module, min_tap, max_tap,
                        tap_inc_reg_up, tap_inc_reg_down, vset, tap_index_offset, verbose=False):
    """
    Change the taps and compute the continuous tap magnitude.

    Arguments:

        **voltage** (list): array of bus voltages solution

        **T** (list): array of indices of the "to" buses of each branch

        **bus_to_regulated_idx** (list): array with the indices of the branches
        that regulate the bus "to"

        **tap_position** (list): array of branch tap positions

        **tap_module** (list): array of branch tap modules

        **min_tap** (list): array of minimum tap positions

        **max_tap** (list): array of maximum tap positions

        **tap_inc_reg_up** (list): array of tap increment when regulating up

        **tap_inc_reg_down** (list): array of tap increment when regulating down

        **vset** (list): array of set voltages to control

    Returns:

        **stable** (bool): Is the system stable (i.e.: are controllers stable)?

        **tap_magnitude** (list): Tap module at each bus in per unit

        **tap_position** (list): Tap position at each bus
    """
    stable = True

    # traverse the indices of the branches that are regulated at the "to" bus
    for k, bus_idx in enumerate(bus_to_regulated_idx):

        j = T[bus_idx]  # get the index of the "to" bus of the branch "i"
        v = np.abs(voltage[j])  # voltage at to "to" bus
        if verbose:
            print("Bus", j, "regulated by branch", bus_idx, ": U=", round(v, 4), "pu, U_set=", vset[k])

        tap_inc = tap_inc_reg_up
        if tap_inc_reg_up.all() != tap_inc_reg_down.all():
            print("Error: tap_inc_reg_up and down are not equal for branch {}".format(bus_idx))

        desired_module = v / vset[k] * tap_module[tap_index_offset + k]
        desired_pos = round((desired_module - 1) / tap_inc[k])

        if desired_pos == tap_position[k]:
            continue

        elif desired_pos > 0 and desired_pos > max_tap[k]:
            if verbose:
                print("Branch {}: Changing from tap {} to {} (module {} to {})".format(bus_idx,
                                                                                       tap_position[k],
                                                                                       max_tap[k],
                                                                                       tap_module[tap_index_offset + k],
                                                                                       1 + max_tap[k] * tap_inc[k]))
            tap_position[k] = max_tap[k]

        elif desired_pos < 0 and desired_pos < min_tap[k]:
            if verbose:
                print("Branch {}: Changing from tap {} to {} (module {} to {})".format(bus_idx,
                                                                                       tap_position[k],
                                                                                       min_tap[k],
                                                                                       tap_module[tap_index_offset + k],
                                                                                       1 + min_tap[k] * tap_inc[k]))
            tap_position[k] = min_tap[k]

        else:
            if verbose:
                print("Branch {}: Changing from tap {} to {} (module {} to {})".format(bus_idx,
                                                                                       tap_position[k],
                                                                                       desired_pos,
                                                                                       tap_module[tap_index_offset + k],
                                                                                       1 + desired_pos * tap_inc[k]))
            tap_position[k] = desired_pos

        tap_module[tap_index_offset + k] = 1 + tap_position[k] * tap_inc[k]
        stable = False

    return stable, tap_module, tap_position


def single_island_pf(circuit: SnapshotData, Vbus, Sbus, Ibus, branch_rates,
                     options: PowerFlowOptions, logger: Logger) -> "PowerFlowResults":
    """
    Run a power flow for a circuit. In most cases, the **run** method should be used instead.
    :param circuit: SnapshotData instance
    :param Vbus: Initial voltage at each bus in complex per unit
    :param Sbus: Power injection at each bus in complex MVA
    :param Ibus: Current injection at each bus in complex MVA
    :param branch_rates: array of branch rates
    :param options: PowerFlowOptions instance
    :param logger: Logger instance
    :return: PowerFlowResults instance
    """

    # solve the power flow
    results = outer_loop_power_flow(circuit=circuit,
                                    options=options,
                                    voltage_solution=Vbus,
                                    Sbus=Sbus,
                                    Ibus=Ibus,
                                    branch_rates=branch_rates,
                                    logger=logger)

    # did it worked?
    worked = np.all(results.converged)

    if not worked:
        logger.append('Did not converge, even after retry!, Error:' + str(results.error))

    return results


def multi_island_pf(multi_circuit: MultiCircuit, options: PowerFlowOptions, opf_results=None,
                    logger=Logger()) -> "PowerFlowResults":
    """
    Multiple islands power flow (this is the most generic power flow function)
    :param multi_circuit: MultiCircuit instance
    :param options: PowerFlowOptions instance
    :param opf_results: OPF results, to be used if not None
    :param logger: list of events to add to
    :return: PowerFlowResults instance
    """

    nc = compile_snapshot_circuit(circuit=multi_circuit,
                                  apply_temperature=options.apply_temperature_correction,
                                  branch_tolerance_mode=options.branch_impedance_tolerance_mode,
                                  opf_results=opf_results)

    calculation_inputs = nc.split_into_islands(ignore_single_node_islands=options.ignore_single_node_islands)

    results = PowerFlowResults(n=nc.nbus,
                               m=nc.nbr,
                               n_tr=nc.ntr,
                               n_hvdc=nc.nhvdc,
                               bus_names=nc.bus_data.bus_names,
                               branch_names=nc.branch_data.branch_names,
                               transformer_names=nc.transformer_data.tr_names,
                               hvdc_names=nc.hvdc_data.names,
                               bus_types=nc.bus_data.bus_types)

    if len(calculation_inputs) > 1:

        # simulate each island and merge the results
        for i, calculation_input in enumerate(calculation_inputs):

            if len(calculation_input.vd) > 0:

                # run circuit power flow
                res = single_island_pf(circuit=calculation_input,
                                       Vbus=calculation_input.Vbus,
                                       Sbus=calculation_input.Sbus,
                                       Ibus=calculation_input.Ibus,
                                       branch_rates=calculation_input.Rates,
                                       options=options,
                                       logger=logger)

                bus_original_idx = calculation_input.original_bus_idx
                branch_original_idx = calculation_input.original_branch_idx
                tr_original_idx = calculation_input.original_tr_idx

                # merge the results from this island
                results.apply_from_island(res, bus_original_idx, branch_original_idx, tr_original_idx)

            else:
                logger.append('There are no slack nodes in the island ' + str(i))
    else:

        if len(calculation_inputs[0].vd) > 0:
            # only one island
            # run circuit power flow
            res = single_island_pf(circuit=calculation_inputs[0],
                                   Vbus=calculation_inputs[0].Vbus,
                                   Sbus=calculation_inputs[0].Sbus,
                                   Ibus=calculation_inputs[0].Ibus,
                                   branch_rates=calculation_inputs[0].Rates,
                                   options=options,
                                   logger=logger)

            if calculation_inputs[0].nbus == nc.nbus:
                # we can confidently say that the island is the only one
                results = res
            else:
                # the island is the only valid subset, but does not contain all the buses
                bus_original_idx = calculation_inputs[0].original_bus_idx
                branch_original_idx = calculation_inputs[0].original_branch_idx
                tr_original_idx = calculation_inputs[0].original_tr_idx

                # merge the results from this island
                results.apply_from_island(res, bus_original_idx, branch_original_idx, tr_original_idx)

        else:
            logger.append('There are no slack nodes')

    return results


def power_flow_worker_args(args):
    """
    Power flow worker to schedule parallel power flows

    args -> t, options: PowerFlowOptions, circuit: Circuit, Vbus, Sbus, Ibus, return_dict


        **t: execution index
        **options: power flow options
        **circuit: circuit
        **Vbus: Voltages to initialize
        **Sbus: Power injections
        **Ibus: Current injections
        **return_dict: parallel module dictionary in which to return the values
    :return:
    """
    t, options, circuit, Vbus, Sbus, Ibus, branch_rates = args

    res = single_island_pf(circuit=circuit,
                           Vbus=Vbus,
                           Sbus=Sbus,
                           Ibus=Ibus,
                           branch_rates=branch_rates,
                           options=options,
                           logger=Logger())

    return t, res
