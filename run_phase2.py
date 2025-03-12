# %%
# Import top-level modules (used throughout the script)
import os
import json
from bids.layout import BIDSLayout
from templateflow.api import get as tpl_get, templates as get_tpl_list
import pandas as pd
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as niu
import logging

# Set environment variables for FSL
os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'
os.environ['FSLDIR'] = '/Users/xiaoqianxiao/fsl'  # Adjust this according to your FSL installation
os.environ['PATH'] += os.pathsep + os.path.join(os.environ['FSLDIR'], 'bin')
#os.environ['OMP_NUM_THREADS'] = '4'  # Limit film_gls to 4 threads per process

# Resource management options
plugin_settings = {
    'plugin': 'MultiProc',
    'plugin_args': {
        'n_procs': 1,  # Start with 8, can increase to 12 later if memory allows
        'raise_insufficient': False,
        'maxtasksperchild': 1,
    }
}

# Set logging to DEBUG for detailed output
logging.getLogger().setLevel(logging.DEBUG)

# Define directories
root_dir = '/Users/xiaoqianxiao/projects'
project_name = 'NARSAD'
data_dir = os.path.join(root_dir, project_name, 'MRI')
bids_dir = data_dir
derivatives_dir = os.path.join(data_dir, 'derivatives')
fmriprep_folder = os.path.join(derivatives_dir, 'fmriprep')
behav_dir = os.path.join(data_dir, 'source_data/behav')
output_dir = os.path.join(derivatives_dir, 'fMRI_analysis')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# %%
# Define task and space for BIDS query
participant_label = []
run = []
task = ['phase2']
space = ['MNI152NLin2009cAsym']

#

work_dir = os.path.join(derivatives_dir, f'work_flows/firstLevel/{task[0]}')
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

# Get absolute path to BIDS directory
layout = BIDSLayout(str(bids_dir), validate=False, derivatives=str(derivatives_dir))
subjects = layout.get(target='subject', return_type='id')
sessions = layout.get(target='session', return_type='id')
runs = layout.get(target='run', return_type='id')

# Load onset files
onsets_phase2 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'), sheet_name=0)
onsets_phase3 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'), sheet_name=1)
onsets_phase3_sub202 = pd.read_excel(os.path.join(behav_dir, 'task-Narsad_events.xlsx'), sheet_name=2)

# Query for preprocessed BOLD files
query = {
    'desc': 'preproc',
    'suffix': 'bold',
    'extension': ['.nii', '.nii.gz']
}
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
    print(f'No preprocessed files found under the given derivatives folder: {derivatives_dir}.')
    exit()

# Collect inputs for all subjects
inputs = {}
base_entities = set(['subject', 'task'])
for part in prepped_bold:
    entities = part.entities
    sub = entities['subject']
    task = entities['task']
    session = entities['session']

    # Define events file based on subject and task
    if (sub == 'N202') & (task == 'phase3'):
        events_file = os.path.join(behav_dir, 'task-NARSAD_phase-3_sub-202_events.csv')
    else:
        events_file = os.path.join(behav_dir, 'task-Narsad_' + task + '_events.csv')

    if sub not in inputs:
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
    inputs[sub]['events'] = events_file


# Define a top-level workflow to parallelize across subjects
def create_subject_parallel_wf(subjects, inputs, output_dir, work_dir):
    # Import Nipype modules within the function
    import nipype.pipeline.engine as pe
    import nipype.interfaces.utility as niu

    # Top-level workflow
    parallel_wf = pe.Workflow(name='subject_parallel_wf')
    parallel_wf.base_dir = work_dir

    # Input node to iterate over subjects
    input_node = pe.Node(niu.IdentityInterface(fields=['subject']),
                         name='input_node')
    input_node.iterables = ('subject', subjects)

    # Define a function to run the first-level workflow for a subject
    def run_subject_wf(subject, inputs, output_dir, work_dir):
        # Import required modules within the function
        import os
        from workflows import first_level_wf

        # Create and run the first-level workflow
        sub_inputs = {subject: inputs[subject]}
        wf = first_level_wf(sub_inputs, output_dir)
        wf.base_dir = os.path.join(work_dir, f'sub_{subject}')
        result = wf.run()
        return result

    # Use MapNode to iterate over subjects and run first_level_wf
    subject_wf_node = pe.MapNode(
        niu.Function(
            input_names=['subject', 'inputs', 'output_dir', 'work_dir'],  # Add work_dir to inputs
            output_names=['result'],
            function=run_subject_wf
        ),
        name='subject_wf_node',
        iterfield=['subject']
    )
    subject_wf_node.inputs.inputs = inputs
    subject_wf_node.inputs.output_dir = output_dir
    subject_wf_node.inputs.work_dir = work_dir

    # Connect the input node to the subject workflow node
    parallel_wf.connect(input_node, 'subject', subject_wf_node, 'subject')

    return parallel_wf


if __name__ == "__main__":
    # Create the parallel workflow for all subjects
    subjects = list(inputs.keys())
    parallel_wf = create_subject_parallel_wf(subjects, inputs, output_dir, work_dir)

    # Run the workflow with MultiProc to parallelize across subjects
    parallel_wf.run(**plugin_settings)
