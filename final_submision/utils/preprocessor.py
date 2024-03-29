import time

from utils.histogram_extractor import histogram_extractor
from utils.noise_extractor import noise_extractor
from utils.transform_builder import transform_builder
from utils._2d_histograms import hist_builder
from utils._patchless_1d_hist import hist_builder_p
from utils.noiseprint_extractor_alt import noise_extractor as noise_extractor_alt

options = {
    'Histogram': histogram_extractor,
    'Noise':    noise_extractor,
    '2DHist': hist_builder,
    'Patchless': hist_builder_p,
    "DCT" : transform_builder,
    "Noise_alt" : noise_extractor_alt
}

# iterate over every subset of dataset and preprocess each subset
def builder(input, dset):
    for task, dset, in dset.items():
        start = time.process_time()
        # get preprocessing method based on domain
        options.get(input.domain)(input, task, dset[0], dset[1])
        end = time.process_time()
        # save preprocess time taken for subset
        with open(f"preprocess_times/{input.dset_name}_time.txt", "a") as f:
            f.write(f"{task}: Elapsed time: {end-start:.6f} seconds\n")

def builder_iplab(input, dset):
    options.get(input.domain)(input, 'full', dset[0], dset[1])






