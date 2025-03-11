"""
Analysis workflows
"""

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


class secondDerivativesDataSink(BIDSDerivatives):
    out_path_base = 'secondLevel'


#%%
DATA_ITEMS = ['bold', 'mask', 'events', 'regressors', 'tr']


def first_level_wf(in_files, output_dir, fwhm=6.0, brightness_threshold=1000, name='wf_1st_level'):
    workflow = pe.Workflow(name=name)

    datasource = pe.Node(niu.Function(function=_dict_ds, output_names=DATA_ITEMS),
                         name='datasource')
    datasource.inputs.in_dict = in_files
    datasource.iterables = ('sub', sorted(in_files.keys()))
    print(datasource)

    # Extract motion parameters from regressors file
    runinfo = pe.Node(niu.Function(
        input_names=['in_file', 'events_file', 'regressors_file', 'regressors_names'],
        function=_bids2nipypeinfo, output_names=['info', 'realign_file']),
        name='runinfo')

    # Set the column names to be used from the confounds file
    runinfo.inputs.regressors_names = ['dvars', 'framewise_displacement'] + \
                                      ['a_comp_cor_%02d' % i for i in range(6)] + ['cosine%02d' % i for i in range(4)]

    #Mask
    apply_mask = pe.Node(ApplyMask(), name='apply_mask')
    # SUSAN smoothing
    susan = pe.Node(SUSAN(),
                    name='susan')
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
        contrasts=[('CS->FIXATION', 'T', ['CS-', 'FIXATION'], [1, -1]),
                   ('CS+_safe>FIXATION', 'T', ['CSS', 'FIXATION'], [1, -1]),
                   ('CS+_reinf>FIXATION', 'T', ['CSR', 'FIXATION'], [1, -1]),
                   ('CS+_safe>CS-', 'T', ['CSS', 'CS-'], [1, -1]),
                   ('CS+_safe<CS-', 'T', ['CSS', 'CS-'], [-1, 1]),
                   ('CS+_reinf>CS-', 'T', ['CSR', 'CS-'], [1, -1]),
                   ('CS+_reinf<CS-', 'T', ['CSR', 'CS-'], [-1, 1]),
                   ('CS+_safe>CS+_reinf', 'T', ['CSS', 'CSR'], [1, -1]),
                   ('CS+_safe<CS+_reinf', 'T', ['CSS', 'CSR'], [-1, 1])
                   ],
        # orthogonalization=orthogonality,
    ), name='l1_model')

    # feat_spec generates an fsf model specification file
    feat_spec = pe.Node(fsl.FEATModel(), name='feat_spec')
    # feat_fit actually runs FEAT
    feat_fit = pe.Node(fsl.FEAT(), name='feat_fit', mem_gb=12)
    feat_select = pe.Node(nio.SelectFiles({
        # 'cope1': 'stats/cope1.nii.gz',
        # 'varcope1': 'stats/varcope1.nii.gz',
        # 'cope2': 'stats/cope2.nii.gz',
        # 'varcope2': 'stats/varcope2.nii.gz',
        # 'cope3': 'stats/cope3.nii.gz',
        # 'varcope3': 'stats/varcope3.nii.gz',
        # 'cope4': 'stats/cope4.nii.gz',
        # 'varcope4': 'stats/varcope4.nii.gz',
        # 'cope5': 'stats/cope5.nii.gz',
        # 'varcope5': 'stats/varcope5.nii.gz',
        # 'cope6': 'stats/cope6.nii.gz',
        # 'varcope6': 'stats/varcope6.nii.gz',
        'cope7': 'stats/cope7.nii.gz',
        'varcope7': 'stats/varcope7.nii.gz',
        'cope8': 'stats/cope8.nii.gz',
        'varcope8': 'stats/varcope8.nii.gz',
        'cope9': 'stats/cope9.nii.gz',
        'varcope9': 'stats/varcope9.nii.gz',
    }), name='feat_select')

    # ds_cope1 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope1'),
    #     name='ds_cope1', run_without_submitting=True)
    # ds_cope2 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope2'),
    #     name='ds_cope2', run_without_submitting=True)
    # ds_cope3 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope3'),
    #     name='ds_cope3', run_without_submitting=True)
    # ds_cope4 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope4'),
    #     name='ds_cope4', run_without_submitting=True)
    # ds_cope5 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope5'),
    #     name='ds_cope5', run_without_submitting=True)
    # ds_cope6 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='cope6'),
    #     name='ds_cope6', run_without_submitting=True)
    ds_cope7 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='cope7'),
        name='ds_cope7', run_without_submitting=True)
    ds_cope8 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='cope8'),
        name='ds_cope8', run_without_submitting=True)
    ds_cope9 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='cope9'),
        name='ds_cope9', run_without_submitting=True)


    # ds_varcope1 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope1'),
    #     name='ds_varcope1', run_without_submitting=True)
    # ds_varcope2 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope2'),
    #     name='ds_varcope2', run_without_submitting=True)
    # ds_varcope3 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope3'),
    #     name='ds_varcope3', run_without_submitting=True)
    # ds_varcope4 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope4'),
    #     name='ds_varcope4', run_without_submitting=True)
    # ds_varcope5 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope5'),
    #     name='ds_varcope5', run_without_submitting=True)
    # ds_varcope6 = pe.Node(DerivativesDataSink(
    #     base_directory=str(output_dir), keep_dtype=False, desc='varcope6'),
    #     name='ds_varcope6', run_without_submitting=True)
    ds_varcope7 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='varcope7'),
        name='ds_varcope7', run_without_submitting=True)
    ds_varcope8 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='varcope8'),
        name='ds_varcope8', run_without_submitting=True)
    ds_varcope9 = pe.Node(DerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc='varcope9'),
        name='ds_varcope9', run_without_submitting=True)

    workflow.connect([
        (datasource, apply_mask, [('bold', 'in_file'),
                                  ('mask', 'mask_file')]),
        (apply_mask, susan, [('out_file', 'in_file')]),
        (datasource, runinfo, [
            ('events', 'events_file'),
            ('regressors', 'regressors_file')]),
        # (datasource, ds_cope1, [('bold', 'source_file')]),
        # (datasource, ds_cope2, [('bold', 'source_file')]),
        # (datasource, ds_cope3, [('bold', 'source_file')]),
        # (datasource, ds_cope4, [('bold', 'source_file')]),
        # (datasource, ds_cope5, [('bold', 'source_file')]),
        # (datasource, ds_cope6, [('bold', 'source_file')]),
        (datasource, ds_cope7, [('bold', 'source_file')]),
        (datasource, ds_cope8, [('bold', 'source_file')]),
        (datasource, ds_cope9, [('bold', 'source_file')]),
        # (datasource, ds_varcope1, [('bold', 'source_file')]),
        # (datasource, ds_varcope2, [('bold', 'source_file')]),
        # (datasource, ds_varcope3, [('bold', 'source_file')]),
        # (datasource, ds_varcope4, [('bold', 'source_file')]),
        # (datasource, ds_varcope5, [('bold', 'source_file')]),
        # (datasource, ds_varcope6, [('bold', 'source_file')]),
        (datasource, ds_varcope7, [('bold', 'source_file')]),
        (datasource, ds_varcope8, [('bold', 'source_file')]),
        (datasource, ds_varcope9, [('bold', 'source_file')]),
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
        (feat_fit, feat_select, [('feat_dir', 'base_directory')]),
        # (feat_select, ds_cope1, [('cope1', 'in_file')]),
        # (feat_select, ds_cope2, [('cope2', 'in_file')]),
        # (feat_select, ds_cope3, [('cope3', 'in_file')]),
        # (feat_select, ds_cope4, [('cope4', 'in_file')]),
        # (feat_select, ds_cope5, [('cope5', 'in_file')]),
        # (feat_select, ds_cope6, [('cope6', 'in_file')]),
        (feat_select, ds_cope7, [('cope7', 'in_file')]),
        (feat_select, ds_cope8, [('cope8', 'in_file')]),
        (feat_select, ds_cope9, [('cope9', 'in_file')]),
        # (feat_select, ds_varcope1, [('varcope1', 'in_file')]),
        # (feat_select, ds_varcope2, [('varcope2', 'in_file')]),
        # (feat_select, ds_varcope3, [('varcope3', 'in_file')]),
        # (feat_select, ds_varcope4, [('varcope4', 'in_file')]),
        # (feat_select, ds_varcope5, [('varcope5', 'in_file')]),
        # (feat_select, ds_varcope6, [('varcope6', 'in_file')]),
        (feat_select, ds_varcope7, [('varcope7', 'in_file')]),
        (feat_select, ds_varcope8, [('varcope8', 'in_file')]),
        (feat_select, ds_varcope9, [('varcope9', 'in_file')]),
    ])
    return workflow


def second_level_wf(output_dir, bids_ref, c, name='wf_2nd_level'):
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(niu.IdentityInterface(
        fields=['group_mask', 'in_copes', 'in_varcopes']),
        name='inputnode')

    # Configure FSL 2nd level analysis
    l2_model = pe.Node(fsl.L2Model(), name='l2_model')
    flameo_fe = pe.Node(fsl.FLAMEO(run_mode='fe'), name='flameo_fe')

    merge_copes = pe.Node(fsl.Merge(dimension='t'), name='merge_copes')
    merge_varcopes = pe.Node(fsl.Merge(dimension='t'), name='merge_varcopes')

    resample_copes = pe.Node(fsl.FLIRT(apply_isoxfm=2), name='resample_copes')
    resample_varcopes = pe.Node(fsl.FLIRT(apply_isoxfm=2), name='resample_varcopes')

    flameo_select = pe.Node(nio.SelectFiles({
        'cope': 'cope1.nii.gz',
        'varcope': 'varcope1.nii.gz',
    }), name='flameo_select')

    ds_cope = pe.Node(secondDerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc=f'cope{c}'),
        name='ds_cope', run_without_submitting=True)
    ds_cope.inputs.source_file = bids_ref

    ds_varcope = pe.Node(secondDerivativesDataSink(
        base_directory=str(output_dir), keep_dtype=False, desc=f'varcope{c}'),
        name='ds_varcope', run_without_submitting=True)
    ds_varcope.inputs.source_file = bids_ref

    workflow.connect([
        (inputnode, l2_model, [(('in_copes', _len), 'num_copes')]),
        (inputnode, flameo_fe, [('group_mask', 'mask_file')]),
        (inputnode, merge_copes, [('in_copes', 'in_files')]),
        (inputnode, merge_varcopes, [('in_varcopes', 'in_files')]),
        (inputnode, resample_copes, [('group_mask', 'reference')]),
        (inputnode, resample_varcopes, [('group_mask', 'reference')]),
        (merge_copes, resample_copes, [('merged_file', 'in_file')]),
        (merge_varcopes, resample_varcopes, [('merged_file', 'in_file')]),
        (l2_model, flameo_fe, [('design_mat', 'design_file'),
                               ('design_con', 't_con_file'),
                               ('design_grp', 'cov_split_file')]),
        (resample_copes, flameo_fe, [('out_file', 'cope_file')]),
        (resample_varcopes, flameo_fe, [('out_file', 'var_cope_file')]),
        (flameo_fe, flameo_select, [('stats_dir', 'base_directory')]),
        (flameo_select, ds_cope, [('cope', 'in_file')]),
        (flameo_select, ds_varcope, [('varcope', 'in_file')]),
    ])
    return workflow


def third_level_wf(output_dir, bids_ref, c, name='wf_3rd_level'):
    workflow = pe.Workflow(name=name)

    inputnode = pe.Node(niu.IdentityInterface(
        fields=['group_mask', 'in_copes', 'in_varcopes']),
        name='inputnode')

    outputnode = pe.Node(niu.IdentityInterface(
        fields=['zstats_raw', 'zstats_fwe', 'zstats_clust',
                'clust_index_file', 'clust_localmax_txt_file']),
        name='outputnode')

    # Configure FSL 2nd level analysis
    l2_model = pe.Node(fsl.L2Model(), name='l2_model')
    flameo_fe = pe.Node(fsl.FLAMEO(run_mode='fe'), name='flameo_fe')
    flameo_flame1 = pe.Node(fsl.FLAMEO(run_mode='flame1'), name='flameo_flame1')

    merge_copes = pe.Node(fsl.Merge(dimension='t'), name='merge_copes')
    merge_varcopes = pe.Node(fsl.Merge(dimension='t'), name='merge_varcopes')

    datasink = pe.Node(DataSink(base_directory=str(output_dir),
                                #container='thirdlevel',
                                strip_dir='stats',
                                substitutions=[(r'stats', f'cope-{c}')]
                                ),
                       name="datasink")

    flameo_select = pe.Node(nio.SelectFiles({
        'mask': 'mask.nii.gz',
    }), name='flameo_select')

    # Thresholding - FDR ################################################
    # Calculate pvalues with ztop
    fdr_ztop = pe.Node(fsl.ImageMaths(op_string='-ztop', suffix='_pval'),
                       name='fdr_ztop')
    # Find FDR threshold: fdr -i zstat1_pval -m <group_mask> -q 0.05
    # fdr_th = <write Nipype interface for fdr>
    # Apply threshold:
    # fslmaths zstat1_pval -mul -1 -add 1 -thr <fdr_th> -mas <group_mask> \
    #     zstat1_thresh_vox_fdr_pstat1

    # Thresholding - FWE ################################################
    # smoothest -r %s -d %i -m %s
    smoothness = pe.Node(fsl.SmoothEstimate(), name='smoothness')
    # ptoz 0.025 -g %f
    # p = 0.05 / 2 for 2-tailed test
    fwe_ptoz = pe.Node(PtoZ(pvalue=0.025), name='fwe_ptoz')
    # fslmaths %s -uthr %s -thr %s nonsignificant
    # fslmaths %s -sub nonsignificant zstat1_thresh
    fwe_nonsig0 = pe.Node(fsl.Threshold(direction='above'), name='fwe_nonsig0')
    fwe_nonsig1 = pe.Node(fsl.Threshold(direction='below'), name='fwe_nonsig1')
    fwe_thresh = pe.Node(fsl.BinaryMaths(operation='sub'), name='fwe_thresh')

    # Thresholding - Cluster ############################################
    # cluster -i %s -c %s -t 3.2 -p 0.025 -d %s --volume=%s  \
    #     --othresh=thresh_cluster_fwe_zstat1 --connectivity=26 --mm
    cluster_kwargs = {
        'threshold': 3.2,
        'pthreshold': 0.025,
        'out_threshold_file': True,
        'out_index_file': True,
        'out_localmax_txt_file': True
    }
    cluster_pos = pe.Node(fsl.Cluster(
        **cluster_kwargs),
        name='cluster_pos')
    cluster_neg = pe.Node(fsl.Cluster(
        **cluster_kwargs),
        name='cluster_neg')
    zstat_inv = pe.Node(fsl.BinaryMaths(operation='mul', operand_value=-1),
                        name='zstat_inv')
    cluster_inv = pe.Node(fsl.BinaryMaths(operation='mul', operand_value=-1),
                          name='cluster_inv')
    cluster_all = pe.Node(fsl.BinaryMaths(operation='add'), name='cluster_all')
    # Randomise
    randomise = pe.Node(fsl.Randomise(
        tfce=True,
        one_sample_group_mean=True,  # Adjust based on design
        num_perm=5000,
        vox_p_values=True),  # TFCE corrected p-value output
        name='randomise'
    )

    workflow.connect([
        (inputnode, l2_model, [(('in_copes', _len), 'num_copes')]),
        (inputnode, flameo_fe, [('group_mask', 'mask_file')]),
        #(inputnode, smoothness, [('group_mask', 'mask_file'),
        #                         (('in_copes', _dof), 'dof')]),
        (inputnode, merge_copes, [('in_copes', 'in_files')]),
        (inputnode, merge_varcopes, [('in_varcopes', 'in_files')]),

        (l2_model, flameo_fe, [('design_mat', 'design_file'),
                               ('design_con', 't_con_file'),
                               ('design_grp', 'cov_split_file')]),
        (merge_copes, flameo_fe, [('merged_file', 'cope_file')]),
        (merge_varcopes, flameo_fe, [('merged_file', 'var_cope_file')]),
        (flameo_fe, datasink, [('stats_dir', 'stats')]),
        #(flameo_fe, smoothness, [('res4d', 'residual_fit_file')]),

        #(flameo_fe, fwe_nonsig0, [('zstats', 'in_file')]),
        #(fwe_nonsig0, fwe_nonsig1, [('out_file', 'in_file')]),
        #(smoothness, fwe_ptoz, [('resels', 'resels')]),
        #(fwe_ptoz, fwe_nonsig0, [('zstat', 'thresh')]),
        #(fwe_ptoz, fwe_nonsig1, [(('zstat', _neg), 'thresh')]),
        #(flameo_fe, fwe_thresh, [('zstats', 'in_file')]),
        #(fwe_nonsig1, fwe_thresh, [('out_file', 'operand_file')]),

        #(flameo_fe, cluster_pos, [('zstats', 'in_file')]),
        #(merge_copes, cluster_pos, [('merged_file', 'cope_file')]),
        #(smoothness, cluster_pos, [('volume', 'volume'),
        #                           ('dlh', 'dlh')]),
        #(flameo_fe, zstat_inv, [('zstats', 'in_file')]),
        #(zstat_inv, cluster_neg, [('out_file', 'in_file')]),
        #(cluster_neg, cluster_inv, [('threshold_file', 'in_file')]),
        #(merge_copes, cluster_neg, [('merged_file', 'cope_file')]),
        #(smoothness, cluster_neg, [('volume', 'volume'),
        #                          ('dlh', 'dlh')]),
        #(cluster_pos, cluster_all, [('threshold_file', 'in_file')]),
        #(cluster_inv, cluster_all, [('out_file', 'operand_file')]),
        #(flameo_flame1, flameo_select, [('stats_dir', 'base_directory')]),
        #(flameo_flame1, randomise, [('copes', 'in_file')]),
        #(flameo_select, randomise, [('mask', 'mask')]),
    ])
    return workflow

def _bids2nipypeinfo(in_file, events_file, regressors_file,
                     regressors_names=None,
                     motion_columns=None,
                     decimals=3, amplitude=1.0):
    from pathlib import Path
    import numpy as np
    import pandas as pd
    from nipype.interfaces.base.support import Bunch

    # Process the events file
    #events = pd.read_csv(events_file, sep=r'\s+')
    events = pd.read_csv(events_file, sep=',')

    bunch_fields = ['onsets', 'durations', 'amplitudes']

    if not motion_columns:
        from itertools import product
        motion_columns = ['_'.join(v) for v in product(('trans', 'rot'), 'xyz')]

    out_motion = Path('motion.par').resolve()

    regress_data = pd.read_csv(regressors_file, sep=r'\s+')
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
