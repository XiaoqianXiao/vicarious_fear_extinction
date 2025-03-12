#%%
import os, json
from bids.layout import BIDSLayout
from templateflow.api import get as tpl_get, templates as get_tpl_list
import pandas as pd
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as niu
#%%
os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'
os.environ['FSLDIR'] = '/Users/xiaoqianxiao/fsl'  # Adjust this according to your FSL installation
os.environ['PATH'] += os.pathsep + os.path.join(os.environ['FSLDIR'], 'bin')
# Resource management options
plugin_settings = {
    'plugin': 'MultiProc',
    'plugin_args': {
        'n_procs': 4,
        'raise_insufficient': False,
        'maxtasksperchild': 1,
    }
}

#%%
root_dir = '/Users/xiaoqianxiao/projects'
project_name = 'NARSAD'
data_dir = os.path.join(root_dir, project_name, 'MRI')
bids_dir = data_dir
derivatives_dir = os.path.join(data_dir, 'derivatives')
fmriprep_folder = os.path.join(derivatives_dir, 'fmriprep')
behav_dir = os.path.join(data_dir, 'source_data/behav')
work_dir = os.path.join(derivatives_dir, 'work_flows_phase2')
if not os.path.exists(work_dir):
    os.makedirs(work_dir)
output_dir = os.path.join(derivatives_dir, 'fMRI_analysis')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
#%%
participant_label = []
run = []
task = ['phase2']
#task_label = "phase2"
#['phase2','phase3']
space = ['MNI152NLin2009cAsym']
# Get absolute path to BIDS directory
layout = BIDSLayout(str(bids_dir), validate=False, derivatives=str(derivatives_dir))
subjects = layout.get(target='subject', return_type='id')
sessions = layout.get(target='session', return_type='id')
runs = layout.get(target='run', return_type='id')
#%%
onsets_phase2 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'),sheet_name=0)
onsets_phase3 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'),sheet_name=1)
onsets_phase3_sub202 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'),sheet_name=2)
#%%
query = {'desc': 'preproc',
         'suffix': 'bold',
         #'subject': '2001LH',
         #'subject': '002',
         'extension': ['.nii', '.nii.gz']}
if participant_label:
    query['subject'] = '|'.join(participant_label)
if run:
    query['run'] = '|'.join(run)
if task:
    query['task'] = '|'.join(task)
if space:
    query['space'] = '|'.join(space)
prepped_bold = layout.get(**query)
if not prepped_bold:
    print(f'No preprocessed files found under the given derivatives '
          'folder: {derivatives_dir}.')
entities = prepped_bold[0].entities
#%%
for part in prepped_bold:
    from workflows import first_level_wf
    #base_entities = set(['subject', 'session', 'run', 'task'])
    #for test, not include session, since the file name were not consistent across behavioral and fMRI data
    #base_entities = set(['subject', 'run', 'task'])
    base_entities = set(['subject', 'task'])
    inputs = {}
    entities = part.entities
    sub = entities['subject']
    task = entities['task']
    if (sub == 'N202') & (task == 'phase3'):
        events_file = os.path.join(behav_dir, 'task-NARSAD_phase-3_sub-202_events.csv')
    else:
        events_file = os.path.join(behav_dir, 'task-Narsad_'+task+'_events.csv')
    session = entities['session']
    inputs[sub] = {}
    base = base_entities.intersection(entities)
    subquery = {k: v for k, v in entities.items() if k in base}
    inputs[sub]['bold'] = part.path
    inputs[sub]['mask'] = layout.get(suffix='mask',
                                        return_type='file',
                                        extension=['.nii', '.nii.gz'],
                                        space=query['space'],
                                        **subquery)[0]
    inputs[sub]['regressors'] = layout.get(desc='confounds',
                                            return_type='file',
                                            extension=['.tsv'],
                                            **subquery)[0]
    inputs[sub]['tr'] = entities['RepetitionTime']
    #inputs[sub]['events'] = layout.get(suffix='events',
    #                                   return_type='file', **subquery)[0]
    inputs[sub]['events'] = events_file
    workflow = first_level_wf(inputs, output_dir)
    workflow.base_dir = work_dir
    workflow.run(**plugin_settings)


