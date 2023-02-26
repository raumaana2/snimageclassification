import numpy as np
import h5py
import extract_dcts 
import io
from PIL import Image


# convert patch to bytes so jpeg2dct can load it
def im_to_bytes(patch, q):
    buf = io.BytesIO()
    patch.save(buf, format='JPEG', qtables=q)
    return buf.getvalue()

# from image, create a list of patches of defined size
def make_patches(image, patch_size, q=None, to_bytes=True):
    patches = []
    for i in range(0, image.width-patch_size+1, patch_size):
        for j in range(0, image.height-patch_size+1, patch_size):
            patch = image.crop((i, j, i+patch_size, j+patch_size))
            if to_bytes:
                patch = im_to_bytes(patch, q)
            patches.append(patch)
    return patches    


def builder(input, task, examples, labels):
    # initialise dataset 
    with h5py.File(f'processed/DCT_{task}_{input.dset_name}.h5', 'w') as f:
        _ = f.create_dataset('DCT', shape=(0, input.his_size), maxshape=(None, input.his_size))
        _ = f.create_dataset('labels', shape=(0, 2), maxshape=(None, 2))

        # generate patches from an image and extract the dcts from each patch and store in dataset
        for im_num, (path, label) in enumerate(zip(examples, labels)):

                # load image
                image = Image.open(path)
                # get q tables
                qtable = image.quantization

                # break down image to patches
                if input.patch_size:
                    patches = make_patches(image, input.patch_size, qtable, True)

                # extract dct histograms from each patch 
                patch_histograms = extract_dcts.process(patches, input)

                #iterate over all patches and save to dataset
                for patch_histogram in patch_histograms:

                    dct_dset = f['DCT']
                    dct_dset.resize((dct_dset.shape[0] + 1, input.his_size))
                    dct_dset[-1] = patch_histogram
                    
                    labels_dset = f['labels']
                    labels_dset.resize((labels_dset.shape[0] + 1, 2))
                    labels_dset[-1] = np.array([label, im_num])