from nipype.pipeline import engine as pe
from nipype.algorithms.modelgen import SpecifyModel
from nipype.interfaces import fsl, utility as niu, io as nio
from nipype.interfaces.fsl import SUSAN
from nipype.interfaces.io import DataSink
from niworkflows.interfaces.bids import DerivativesDataSink as BIDSDerivatives
from interfaces import PtoZ
from utils import _dict_ds
from nipype.interfaces.fsl import ApplyMask

class DerivativesDataSink(BIDSDerivatives):
    out_path_base = 'firstLevel'

DATA_ITEMS = ['bold', 'mask', 'events', 'regressors', 'tr']

def first_level_wf(in_files, output_dir, fwhm=6.0, brightness_threshold=1000):
    workflow = pe.Workflow(name='wf_1st_level')
    workflow.config['execution']['use_relative_paths'] = True
    workflow.config['execution']['remove_unnecessary_outputs'] = False

    datasource = pe.Node(niu.Function(function=_dict_ds, output_names=DATA_ITEMS),
                         name='datasource')
    datasource.inputs.in_dict = in_files
    datasource.iterables = ('sub', sorted(in_files.keys()))

    # Extract motion parameters from regressors file
    runinfo = pe.Node(niu.Function(
        input_names=['in_file', 'events_file', 'regressors_file', 'regressors_names'],
        function=_bids2nipypeinfo, output_names=['info', 'realign_file']),
        name='runinfo')

    # Set the column names to be used from the confounds file
    runinfo.inputs.regressors_names = ['dvars', 'framewise_displacement'] + \
                                      ['a_comp_cor_%02d' % i for i in range(6)] + \
                                      ['cosine%02d' % i for i in range(4)]

    # Mask
    apply_mask = pe.Node(ApplyMask(), name='apply_mask')
    # SUSAN smoothing
    susan = pe.Node(SUSAN(), name='susan')
    susan.inputs.fwhm = fwhm
    susan.inputs.brightness_threshold = brightness_threshold

    l1_spec = pe.Node(SpecifyModel(
        parameter_source='FSL',
        input_units='secs',
        high_pass_filter_cutoff=100
    ), name='l1_spec')

    # l1_model creates a first-level model design
    l1_model = pe.Node(fsl.Level1Design(
        bases={'dgamma': {'derivs': True}},
        model_serial_correlations=True,
        contrasts=[('CS+_safe>CS-', 'T', ['CSS_first_half', 'CSS_second_half', 'CS-_first_half', 'CS-_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('CS+_safe<CS-', 'T', ['CSS_first_half', 'CSS_second_half', 'CS-_first_half', 'CS-_second_half'], [-0.5, -0.5, 0.5, 0.5]),
                   ('CS+_reinf>CS-', 'T', ['CSR_first_half', 'CSR_second_half', 'CS-_first_half', 'CS-_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('CS+_reinf<CS-', 'T', ['CSR_first_half', 'CSR_second_half', 'CS-_first_half', 'CS-_second_half'], [-0.5, -0.5, 0.5, 0.5]),
                   ('CS+_safe>CS+_reinf', 'T', ['CSS_first_half', 'CSS_second_half', 'CSR_first_half', 'CSR_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('CS+_safe<CS+_reinf', 'T', ['CSS_first_half', 'CSS_second_half', 'CSR_first_half', 'CSR_second_half'], [-0.5, -0.5, 0.5, 0.5]),
                   ('CS->FIXATION', 'T', ['CS-_first_half', 'CS-_second_half', 'FIXATION_second_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('CS+_safe>FIXATION', 'T', ['CSS_first_half', 'CSS_second_half', 'FIXATION_first_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('CS+_reinf>FIXATION', 'T', ['CSR_first_half', 'CSR_second_half', 'FIXATION_first_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
                   ('first_half_CS+_safe>first_half_CS+_reinf', 'T', ['CSS_first_half', 'CSR_first_half'], [1, -1]),
                   ('first_half_CS+_safe<first_half_CS+_reinf', 'T', ['CSS_first_half', 'CSR_first_half'], [-1, 1]),
                   ('first_half_CS+_safe>CS-', 'T', ['CSS_first_half', 'CS-_first_half'], [1, -1]),
                   ('first_half_CS+_safe<CS-', 'T', ['CSS_first_half', 'CS-_first_half'], [-1, 1]),
                   ('first_half_CS+_reinf>CS-', 'T', ['CSR_first_half', 'CS-_first_half'], [1, -1]),
                   ('first_half_CS+_reinf<CS-', 'T', ['CSR_first_half', 'CS-_first_half'], [-1, 1]),
                   ('first_half_CS+_safe>FIXATION', 'T', ['CSS_first_half', 'FIXATION_first_half'], [1, -1]),
                   ('first_half_CS+_reinf>FIXATION', 'T', ['CSR_first_half', 'FIXATION_first_half'], [1, -1]),
                   ('second_half_CS+_safe>second_half_CS+_reinf', 'T', ['CSS_second_half', 'CSR_second_half'], [1, -1]),
                   ('second_half_CS+_safe<second_half_CS+_reinf', 'T', ['CSS_second_half', 'CSR_second_half'], [-1, 1]),
                   ('second_half_CS+_safe>CS-', 'T', ['CSS_second_half', 'CS-_second_half'], [1, -1]),
                   ('second_half_CS+_safe<CS-', 'T', ['CSS_second_half', 'CS-_second_half'], [-1, 1]),
                   ('second_half_CS+_reinf>CS-', 'T', ['CSR_second_half', 'CS-_second_half'], [1, -1]),
                   ('second_half_CS+_reinf<CS-', 'T', ['CSR_second_half', 'CS-_second_half'], [-1, 1]),
                   ('second_half_CS+_safe>FIXATION', 'T', ['CSS_second_half', 'FIXATION_second_half'], [1, -1]),
                   ('second_half_CS+_reinf>FIXATION', 'T', ['CSR_second_half', 'FIXATION_second_half'], [1, -1]),
                   ('first_half_CS+_safe>second_half_CS+_safe', 'T', ['CSS_first_half', 'CSS_second_half'], [1, -1]),
                   ('first_half_CS+_safe<second_half_CS+_safe', 'T', ['CSS_first_half', 'CSS_second_half'], [-1, 1]),
                   ('first_half_CS+_reinf>second_half_CS+_reinf', 'T', ['CSR_first_half', 'CSR_second_half'], [1, -1]),
                   ('first_half_CS+_reinf<second_half_CS+_reinf', 'T', ['CSR_first_half', 'CSR_second_half'], [-1, 1])
                   ],
    ), name='l1_model')

    # feat_spec generates an fsf model specification file
    feat_spec = pe.Node(fsl.FEATModel(), name='feat_spec')
    # feat_fit actually runs FEAT
    feat_fit = pe.Node(fsl.FEAT(), name='feat_fit', mem_gb=12)
    feat_select = pe.Node(nio.SelectFiles({
        **{f'cope{i}': f'stats/cope{i}.nii.gz' for i in range(1, 26)},
        **{f'varcope{i}': f'stats/varcope{i}.nii.gz' for i in range(1, 26)}
    }), name='feat_select')

    ds_copes = [
        pe.Node(DerivativesDataSink(
            base_directory=str(output_dir), keep_dtype=False, desc=f'cope{i}'),
            name=f'ds_cope{i}', run_without_submitting=True)
        for i in range(1, 26)
    ]

    ds_varcopes = [
        pe.Node(DerivativesDataSink(
            base_directory=str(output_dir), keep_dtype=False, desc=f'varcope{i}'),
            name=f'ds_varcope{i}', run_without_submitting=True)
        for i in range(1, 26)
    ]

    workflow.connect([
        (datasource, apply_mask, [('bold', 'in_file'),
                                  ('mask', 'mask_file')]),
        (apply_mask, susan, [('out_file', 'in_file')]),
        (datasource, runinfo, [
            ('events', 'events_file'),
            ('regressors', 'regressors_file')]),
        *[
            (datasource, ds_copes[i - 1], [('bold', 'source_file')])
            for i in range(1, 26)
        ],
        *[
            (datasource, ds_varcopes[i - 1], [('bold', 'source_file')])
            for i in range(1, 26)
        ],
        (susan, l1_spec, [('smoothed_file', 'functional_runs')]),
        (datasource, l1_spec, [('tr', 'time_repetition')]),
        (datasource, l1_model, [('tr', 'interscan_interval')]),
        (susan, runinfo, [('smoothed_file', 'in_file')]),
        (runinfo, l1_spec, [
            ('info', 'subject_info'),
            ('realign_file', 'realignment_parameters')]),
        (l1_spec, l1_model, [('session_info', 'session_info')]),
        (l1_model, feat_spec, [
            ('fsf_files', 'fsf_file'),
            ('ev_files', 'ev_files')]),
        (l1_model, feat_fit, [('fsf_files', 'fsf_file')]),
        # Added connection to ensure feat_select runs after feat_fit
        (feat_fit, feat_select, [('feat_dir', 'base_directory')]),
        *[
            (feat_select, ds_copes[i - 1], [(f'cope{i}', 'in_file')])
            for i in range(1, 26)
        ],
        *[
            (feat_select, ds_varcopes[i - 1], [(f'varcope{i}', 'in_file')])
            for i in range(1, 26)
        ],
    ])
    return workflow


def SVC_wf(output_dir, name="SVC_wf"):
    wf = pe.Workflow(name=name, base_dir=output_dir)
    inputnode = Node(IdentityInterface(fields=['roi', 'cope_file', 'var_cope_file',
                                               'design_file', 'grp_file', 'con_file', 'result_dir']),
                     name='inputnode')

    roi_node = Node(Function(input_names=['roi'], output_names=['roi_files'],
                             function=get_roi_files),
                    name='roi_node')

    flameo = MapNode(FLAMEO(run_mode='flame1'),
                     iterfield=['cope_file', 'var_cope_file', 'mask_file'],  # Add mask_file to iterfield
                     name='flameo')

    fdr_ztop = MapNode(ImageMaths(op_string='-ztop', suffix='_pval'),
                       iterfield=['in_file'],
                       name='fdr_ztop')

    smoothness = MapNode(SmoothEstimate(),
                         iterfield=['zstat_file', 'mask_file'],  # Add mask_file to iterfield
                         name='smoothness')

    clustering = MapNode(Cluster(threshold=2.3,  # Z-threshold (e.g., 2.3 or 3.1)
                                 connectivity=26,  # 3D connectivity
                                 out_threshold_file=True,
                                 out_index_file=True,
                                 out_localmax_txt_file=True,  # Local maxima text file
                                 pthreshold=0.05),  # Cluster-level FWE threshold
                         iterfield=['in_file', 'dlh'],
                         name='clustering')

    outputnode = Node(IdentityInterface(fields=['zstats', 'cluster_thresh', 'cluster_index', 'cluster_peaks']),
                      name='outputnode')

    datasink = Node(DataSink(base_directory=output_dir), name='datasink')

    wf.connect([
        (inputnode, roi_node, [('roi', 'roi')]),
        # ROI files from roi_node
        (roi_node, flameo, [('roi_files', 'mask_file')]),
        (roi_node, smoothness, [('roi_files', 'mask_file')]),
        # Inputs to flameo
        (inputnode, flameo, [('cope_file', 'cope_file')]),  # Cope file as in_file
        (inputnode, flameo, [('var_cope_file', 'var_cope_file')]),  # Varcope file as in_file
        (inputnode, flameo, [('design_file', 'design_file'),
                             ('grp_file', 'cov_split_file'),
                             ('con_file', 't_con_file')]),

        # Clustering with dlh
        (flameo, clustering, [(('zstats', flatten_stats), 'in_file')]),
        (smoothness, clustering, [('volume', 'volume')]),
        (smoothness, clustering, [('dlh', 'dlh')]),

        # Outputs to outputnode
        (flameo, outputnode, [('zstats', 'zstats')]),
        (clustering, outputnode, [('threshold_file', 'cluster_thresh'),
                                  ('index_file', 'cluster_index'),
                                  ('localmax_txt_file', 'cluster_peaks')]),

        # Outputs to DataSink
        (outputnode, datasink, [('zstats', 'stats.@zstats'),
                                ('cluster_thresh', 'cluster_results.@thresh'),
                                ('cluster_index', 'cluster_results.@index'),
                                ('cluster_peaks', 'cluster_results.@peaks')])
    ])
    return wf


def _bids2nipypeinfo(in_file, events_file, regressors_file,
                     regressors_names=None,
                     motion_columns=None,
                     decimals=3, amplitude=1.0):
    from pathlib import Path
    import numpy as np
    import pandas as pd
    from nipype.interfaces.base.support import Bunch

    # Process the events file with tab separator (fix for BIDS TSV files)
    events = pd.read_csv(events_file, sep='\t')  # Changed from sep=',' to sep='\t'

    bunch_fields = ['onsets', 'durations', 'amplitudes']

    if not motion_columns:
        from itertools import product
        motion_columns = ['_'.join(v) for v in product(('trans', 'rot'), 'xyz')]

    out_motion = Path('motion.par').resolve()

    regress_data = pd.read_csv(regressors_file, sep='\t')
    np.savetxt(out_motion, regress_data[motion_columns].values, '%g')
    if regressors_names is None:
        regressors_names = sorted(set(regress_data.columns) - set(motion_columns))

    if regressors_names:
        bunch_fields += ['regressor_names']
        bunch_fields += ['regressors']

    runinfo = Bunch(
        scans=in_file,
        conditions=list(set(events.trial_type.values)),
        **{k: [] for k in bunch_fields})

    for condition in runinfo.conditions:
        event = events[events.trial_type.str.match(condition)]

        runinfo.onsets.append(np.round(event.onset.values, 3).tolist())
        runinfo.durations.append(np.round(event.duration.values, 3).tolist())
        if 'amplitudes' in events.columns:
            runinfo.amplitudes.append(np.round(event.amplitudes.values, 3).tolist())
        else:
            runinfo.amplitudes.append([amplitude] * len(event))

    if 'regressor_names' in bunch_fields:
        runinfo.regressor_names = regressors_names
        try:
            runinfo.regressors = regress_data[regressors_names]
        except KeyError:
            regressors_names = list(set(regressors_names).intersection(
                set(regress_data.columns)))
            runinfo.regressors = regress_data[regressors_names]
        runinfo.regressors = runinfo.regressors.fillna(0.0).values.T.tolist()

    return [runinfo], str(out_motion)

def _get_tr(in_dict):
    return in_dict.get('RepetitionTime')

def _len(inlist):
    return len(inlist)

def _dof(inlist):
    return len(inlist) - 1

def _neg(val):
    return -val

def _dict_ds(in_dict, sub, order=['bold', 'mask', 'events', 'regressors', 'tr']):
    return tuple([in_dict[sub][k] for k in order])

def get_roi_files(roi):
    import glob
    import os
    roi_dir = "/Users/xiaoqianxiao/tool/parcellation/ROIs"
    roi_pattern = os.path.join(roi_dir, f'*{roi}*_resampled.nii*')  # Use *roi* to match variations
    roi_files = glob.glob(roi_pattern)  # Expand wildcard into list of files
    if not roi_files:
        raise ValueError(f"No ROI files found matching pattern '{roi_pattern}' in {roi_dir}")
    return roi_files

def flatten_stats(stats):
    """Flatten a potentially nested list of stat file paths into a single list."""
    if not stats:
        return []
    if isinstance(stats, str):
        return [stats]
    if isinstance(stats[0], list):
        return [item for sublist in stats for item in sublist]
    return stats