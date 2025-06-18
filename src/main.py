import h5py
import argparse
import os

def copy_h5_without_empty_datasets(source_path, dest_path):
    def copy_items(name, obj):
        if isinstance(obj, h5py.Dataset):
            if 0 in obj.shape:
                print(f"Skipping empty dataset: {name} (shape={obj.shape})")
                return

            # Preserve compression, chunking, and filter options
            creation_args = {}
            for attr in ['compression', 'compression_opts', 'shuffle', 'fletcher32', 'chunks']:
                # Check both dataset attributes and properties
                if hasattr(obj, attr):
                    val = getattr(obj, attr)
                    if val is not None:
                        creation_args[attr] = val

            # Use creation_args and preserve dtype
            dest_dataset = dest_file.create_dataset(
                name,
                data=obj[:],
                dtype=obj.dtype,
                **creation_args
            )

            # Copy dataset attributes
            for key, val in obj.attrs.items():
                dest_dataset.attrs[key] = val

            print(f"Copied dataset: {name} (shape={obj.shape}, compression={creation_args.get('compression')})")

        elif isinstance(obj, h5py.Group):
            dest_file.require_group(name)
            for key, val in obj.attrs.items():
                dest_file[name].attrs[key] = val

    with h5py.File(source_path, 'r') as source_file:
        with h5py.File(dest_path, 'w') as dest_file:
            source_file.visititems(copy_items)

def main():
    parser = argparse.ArgumentParser(description="Copy HDF5 file without empty datasets.")
    parser.add_argument('--input', '-i', required=True, help="Path to source HDF5 file")
    parser.add_argument('--output', '-o', required=True, help="Path to output HDF5 file")
    
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print(f"Processing file: {args.input}")
    copy_h5_without_empty_datasets(args.input, args.output)
    print(f"Done. Output saved to: {args.output}")

if __name__ == '__main__':
    main()
