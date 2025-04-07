from nipype.pipeline import engine as pe
from nipype.algorithms.modelgen import SpecifyModel
from nipype.interfaces import fsl, utility as niu, io as nio
from nipype.interfaces.fsl.utils import ImageMeants
from nipype.interfaces.fsl import SUSAN, ApplyMask, FLIRT, FILMGLS, Level1Design, FEATModel
from niworkflows.interfaces.bids import DerivativesDataSink as BIDSDerivatives
import numpy as np
import os
from utils import _dict_ds

class DerivativesDataSink(BIDSDerivatives):
    out_path_base = 'firstLevel'

DATA_ITEMS = ['bold', 'mask', 'events', 'regressors', 'tr']

def first_level_wf_roi(in_files, output_dir, roi_masks, fwhm=6.0, brightness_threshold=1000):
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    workflow = pe.Workflow(name='wf_1st_level')
    workflow.config['execution']['use_relative_paths'] = True
    workflow.config['execution']['remove_unnecessary_outputs'] = False

    def text_to_nifti(ts_file, out_file='roi_ts.nii.gz'):
        import numpy as np
        import nibabel as nib
        import os
        out_file = os.path.abspath(out_file)
        ts_data = np.loadtxt(ts_file)
        nifti_data = ts_data.reshape(1, 1, 1, -1)
        affine = np.eye(4)
        img = nib.Nifti1Image(nifti_data, affine)
        nib.save(img, out_file)
        return out_file

    def get_contrast_indices(n_contrasts):
        return list(range(1, n_contrasts + 1))

    def get_roi_label(roi_file):
        import os
        label = os.path.splitext(os.path.basename(roi_file))[0].replace('_flirt.nii', '')
        print(f"ROI Label: {label}")  # Debug print
        return label

    def get_subject_id(bold_file):
        import os
        filename = os.path.basename(bold_file)
        subject = filename.split('_')[0].replace('sub-', '')
        print(f"Subject ID: {subject}")  # Debug print
        return subject

    def get_session_id(bold_file):
        import os
        filename = os.path.basename(bold_file)
        for part in filename.split('_'):
            if part.startswith('ses-'):
                return part.replace('ses-', '')
        return 'nosession'

    def get_space_id(bold_file):
        import os
        filename = os.path.basename(bold_file)
        for part in filename.split('_'):
            if part.startswith('space-'):
                return part.replace('space-', '')
        return 'nospace'

    def get_base_directory(output_dir, roi_label):
        """Dynamically set base_directory to include ROI label."""
        import os
        return os.path.join(output_dir, roi_label)

    datasource = pe.Node(niu.Function(function=_dict_ds, output_names=DATA_ITEMS),
                         name='datasource')
    datasource.inputs.in_dict = in_files
    datasource.iterables = ('sub', sorted(in_files.keys()))

    runinfo = pe.Node(niu.Function(
        input_names=['in_file', 'events_file', 'regressors_file', 'regressors_names'],
        function=_bids2nipypeinfo, output_names=['info', 'realign_file']),
        name='runinfo')
    runinfo.inputs.regressors_names = ['dvars', 'framewise_displacement'] + \
                                      ['a_comp_cor_%02d' % i for i in range(6)] + \
                                      ['cosine%02d' % i for i in range(4)]

    apply_mask = pe.Node(ApplyMask(), name='apply_mask')
    susan = pe.Node(SUSAN(), name='susan')
    susan.inputs.fwhm = fwhm
    susan.inputs.brightness_threshold = brightness_threshold

    resample_rois = pe.Node(FLIRT(interp='nearestneighbour'), name='resample_rois')
    resample_rois.iterables = ('in_file', roi_masks)

    roi_means = pe.Node(ImageMeants(), name='roi_means')

    ts_to_nifti = pe.Node(niu.Function(
        input_names=['ts_file'],
        output_names=['out_file'],
        function=text_to_nifti), name='ts_to_nifti')

    l1_spec = pe.Node(SpecifyModel(
        parameter_source='FSL',
        input_units='secs',
        high_pass_filter_cutoff=100
    ), name='l1_spec')

    l1_model = pe.Node(Level1Design(
        bases={'dgamma': {'derivs': True}},
        model_serial_correlations=True,
        contrasts=[
            ('CS+_safe>CS-', 'T', ['CSS_first_half', 'CSS_second_half', 'CS-_first_half', 'CS-_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('CS+_reinf>CS-', 'T', ['CSR_first_half', 'CSR_second_half', 'CS-_first_half', 'CS-_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('CS+_safe>CS+_reinf', 'T', ['CSS_first_half', 'CSS_second_half', 'CSR_first_half', 'CSR_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('CS->FIXATION', 'T', ['CS-_first_half', 'CS-_second_half', 'FIXATION_first_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('CS+_safe>FIXATION', 'T', ['CSS_first_half', 'CSS_second_half', 'FIXATION_first_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('CS+_reinf>FIXATION', 'T', ['CSR_first_half', 'CSR_second_half', 'FIXATION_first_half', 'FIXATION_second_half'], [0.5, 0.5, -0.5, -0.5]),
            ('first_half_CS+_safe>first_half_CS+_reinf', 'T', ['CSS_first_half', 'CSR_first_half'], [1, -1]),
            ('first_half_CS+_safe>CS-', 'T', ['CSS_first_half', 'CS-_first_half'], [1, -1]),
            ('first_half_CS+_reinf>CS-', 'T', ['CSR_first_half', 'CS-_first_half'], [1, -1]),
            ('first_half_CS+_safe>FIXATION', 'T', ['CSS_first_half', 'FIXATION_first_half'], [1, -1]),
            ('first_half_CS+_reinf>FIXATION', 'T', ['CSR_first_half', 'FIXATION_first_half'], [1, -1]),
            ('second_half_CS+_safe>second_half_CS+_reinf', 'T', ['CSS_second_half', 'CSR_second_half'], [1, -1]),
            ('second_half_CS+_safe>CS-', 'T', ['CSS_second_half', 'CS-_second_half'], [1, -1]),
            ('second_half_CS+_reinf>CS-', 'T', ['CSR_second_half', 'CS-_second_half'], [1, -1]),
            ('second_half_CS+_safe>FIXATION', 'T', ['CSS_second_half', 'FIXATION_second_half'], [1, -1]),
            ('second_half_CS+_reinf>FIXATION', 'T', ['CSR_second_half', 'FIXATION_second_half'], [1, -1]),
            ('first_half_CS+_safe>second_half_CS+_safe', 'T', ['CSS_first_half', 'CSS_second_half'], [1, -1]),
            ('first_half_CS+_reinf>second_half_CS+_reinf', 'T', ['CSR_first_half', 'CSR_second_half'], [1, -1])
        ]
    ), name='l1_model')

    feat_model = pe.Node(FEATModel(), name='feat_model')

    film_gls = pe.Node(FILMGLS(
        threshold=0,
        smooth_autocorr=True,
        autocorr_noestimate=False
    ), name='film_gls')

    contrast_indices = pe.Node(niu.Function(
        input_names=['n_contrasts'],
        output_names=['contrast_indices'],
        function=get_contrast_indices),
        name='contrast_indices')
    contrast_indices.inputs.n_contrasts = 18

    roi_label = pe.Node(niu.Function(
        input_names=['roi_file'],
        output_names=['roi_label'],
        function=get_roi_label),
        name='roi_label')

    subject_id = pe.Node(niu.Function(
        input_names=['bold_file'],
        output_names=['subject_id'],
        function=get_subject_id),
        name='subject_id')

    session_id = pe.Node(niu.Function(
        input_names=['bold_file'],
        output_names=['session_id'],
        function=get_session_id),
        name='session_id')

    space_id = pe.Node(niu.Function(
        input_names=['bold_file'],
        output_names=['space_id'],
        function=get_space_id),
        name='space_id')

    # Function to dynamically set base_directory
    base_dir_node = pe.Node(niu.Function(
        input_names=['output_dir', 'roi_label'],
        output_names=['base_directory'],
        function=get_base_directory),
        name='base_dir_node')
    base_dir_node.inputs.output_dir = output_dir

    # DerivativesDataSink nodes for copes (one per contrast, per ROI)
    ds_copes = [pe.Node(DerivativesDataSink(
        keep_dtype=False,
        desc=f'cope{i}',
        extension='.nii.gz'),
        name=f'ds_cope{i}', run_without_submitting=True) for i in range(1, 19)]

    # Select nodes for each cope file
    cope_selects = [pe.Node(niu.Select(index=i-1), name=f'cope_select_{i}') for i in range(1, 19)]

    # DerivativesDataSink for source file (per ROI)
    ds_source = pe.Node(DerivativesDataSink(
        keep_dtype=False,
        desc='source',
        extension='.nii.gz'),
        name='ds_source', run_without_submitting=True)

    workflow.connect([
        (datasource, apply_mask, [('bold', 'in_file'), ('mask', 'mask_file')]),
        (apply_mask, susan, [('out_file', 'in_file')]),
        (datasource, runinfo, [('events', 'events_file'), ('regressors', 'regressors_file')]),
        (susan, resample_rois, [('smoothed_file', 'reference')]),
        (susan, roi_means, [('smoothed_file', 'in_file')]),
        (resample_rois, roi_means, [('out_file', 'mask')]),
        (susan, runinfo, [('smoothed_file', 'in_file')]),
        (roi_means, ts_to_nifti, [('out_file', 'ts_file')]),
        (ts_to_nifti, film_gls, [('out_file', 'in_file')]),
        (susan, l1_spec, [('smoothed_file', 'functional_runs')]),
        (datasource, l1_spec, [('tr', 'time_repetition')]),
        (runinfo, l1_spec, [('info', 'subject_info'),
                            ('realign_file', 'realignment_parameters')]),
        (l1_spec, l1_model, [('session_info', 'session_info')]),
        (datasource, l1_model, [('tr', 'interscan_interval')]),
        (l1_model, feat_model, [('fsf_files', 'fsf_file'),
                                ('ev_files', 'ev_files')]),
        (feat_model, film_gls, [('design_file', 'design_file'),
                                ('con_file', 'tcon_file')]),
        (datasource, subject_id, [('bold', 'bold_file')]),
        (datasource, session_id, [('bold', 'bold_file')]),
        (datasource, space_id, [('bold', 'bold_file')]),
        (resample_rois, roi_label, [('out_file', 'roi_file')]),
        # Connect ROI label to base_directory node
        (roi_label, base_dir_node, [('roi_label', 'roi_label')]),
        # Connect copes through Select nodes to DerivativesDataSink
        *[(film_gls, cope_selects[i-1], [('copes', 'inlist')]) for i in range(1, 19)],
        *[(cope_selects[i-1], ds_copes[i-1], [('out', 'in_file')]) for i in range(1, 19)],
        *[(datasource, ds_copes[i-1], [('bold', 'source_file')]) for i in range(1, 19)],
        *[(subject_id, ds_copes[i-1], [('subject_id', 'subject')]) for i in range(1, 19)],
        *[(session_id, ds_copes[i-1], [('session_id', 'session')]) for i in range(1, 19)],
        *[(space_id, ds_copes[i-1], [('space_id', 'space')]) for i in range(1, 19)],
        *[(base_dir_node, ds_copes[i-1], [('base_directory', 'base_directory')]) for i in range(1, 19)],
        # Connect source to DerivativesDataSink
        (susan, ds_source, [('smoothed_file', 'in_file')]),
        (datasource, ds_source, [('bold', 'source_file')]),
        (subject_id, ds_source, [('subject_id', 'subject')]),
        (session_id, ds_source, [('session_id', 'session')]),
        (space_id, ds_source, [('space_id', 'space')]),
        (base_dir_node, ds_source, [('base_directory', 'base_directory')]),
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
    import sys

    print(f"_bids2nipypeinfo: events_file={events_file}, type={type(events_file)}, regressors_file={regressors_file}, type={type(regressors_file)}", file=sys.stdout, flush=True)

    events = pd.read_csv(events_file, sep='\t')
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
            regressors_names = list(set(regressors_names).intersection(set(regress_data.columns)))
            runinfo.regressors = regress_data[regressors_names]
        runinfo.regressors = runinfo.regressors.fillna(0.0).values.T.tolist()

    return [runinfo], str(out_motion)