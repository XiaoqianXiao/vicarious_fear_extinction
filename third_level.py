from nipype.pipeline.engine import Workflow, Node
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.fsl import FLAMEO, Randomise, Cluster, Merge
from nipype.interfaces.utility import Function


def create_mixed_design_files(group_info, output_dir):
    design_file = f"{output_dir}/design_files/design.mat"
    con_file = f"{output_dir}/design_files/contrast.con"
    # ... write files ...
    return design_file, con_file


def third_level_wf(output_dir, bids_ref, c, name="third_level"):
    wf = Workflow(name=name)

    inputnode = Node(IdentityInterface(fields=['in_copes', 'in_varcopes', 'group_info', 'group_mask']),
                     name='inputnode')

    design_gen = Node(Function(input_names=['group_info', 'output_dir'],
                               output_names=['design_file', 'con_file'],
                               function=create_mixed_design_files),
                      name='design_gen')
    design_gen.inputs.output_dir = output_dir

    merge_copes = Node(Merge(dimension='t'), name='merge_copes')
    merge_varcopes = Node(Merge(dimension='t'), name='merge_varcopes')

    flameo = Node(FLAMEO(run_mode='flame1'), name='flameo')

    cluster = Node(Cluster(threshold=2.3, pthreshold=0.05), name='cluster')

    randomise = Node(Randomise(), name='randomise')
    randomise.inputs.n_perm = 5000
    randomise.inputs.tfce = True
    randomise.inputs.vox_p_values = True

    outputnode = Node(IdentityInterface(fields=['zstats_raw', 'zstats_clust', 'clust_index_file',
                                                'clust_localmax_txt_file', 'zstats_fwe']),
                      name='outputnode')

    wf.connect([
        (inputnode, design_gen, [('group_info', 'group_info')]),
        (inputnode, merge_copes, [('in_copes', 'in_files')]),
        (inputnode, merge_varcopes, [('in_varcopes', 'in_files')]),
        (inputnode, flameo, [('group_mask', 'mask_file')]),
        (merge_copes, flameo, [('merged_file', 'cope_file')]),
        (merge_varcopes, flameo, [('merged_file', 'var_cope_file')]),
        (design_gen, flameo, [('design_file', 'design_file'),
                              ('con_file', 'tcon_file')]),
        (flameo, cluster, [('zstats', 'in_file')]),
        (merge_copes, cluster, [('merged_file', 'cope_file')]),
        (merge_copes, randomise, [('merged_file', 'in_file')]),
        (inputnode, randomise, [('group_mask', 'mask')]),
        (design_gen, randomise, [('design_file', 'design_mat'),
                                 ('con_file', 'tcon')]),
        (flameo, outputnode, [('zstats', 'zstats_raw')]),
        (cluster, outputnode, [('threshold_file', 'zstats_clust'),
                               ('index_file', 'clust_index_file'),
                               ('localmax_txt_file', 'clust_localmax_txt_file')]),
        (randomise, outputnode, [('tstat_files', 'zstats_fwe')]),
    ])

    return wf