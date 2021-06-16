from multiprocessing import cpu_count
from os import makedirs
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, Future
from functools import partial
from typing import Callable, List
import sys
import traceback

from .segmenter import Segmenter

def path_iterator(paths, output_path, paths_to_ignore):
    for search_path in paths:
        if any(x in str(search_path) for x in paths_to_ignore):
            continue

        if Path(search_path).is_file():
            just_name = str(Path(search_path).relative_to(
                Path(search_path).parent)).split('.')[0]
            
            if output_path is not None:
                makedirs(Path(output_path) /
                        Path(search_path).relative_to(search_path).parent, exist_ok=True)
            yield search_path, f'{output_path}/{just_name}.cleaned.wav'
            continue

        for path in filter(lambda p: p.is_file(), Path(search_path).rglob('*')):
            sub_output_path = output_path if output_path is None else f'{output_path}/{path.relative_to(search_path).parent}'
            generator = path_iterator([path], sub_output_path, paths_to_ignore)
            if generator is not None:
                yield from generator

def default_callback(file_path, future_result):
    if future_result.exception():
        print(''.join(traceback.format_exception(etype=type(future_result.exception()), value=future_result.exception(), tb=future_result.exception().__traceback__)))
        print(f'error processing {file_path}, exception={future_result.exception()}', file=sys.stderr)
    else:
        print(f'processed {future_result.result()}', file=sys.stderr)

def process_directory(
    in_dirs: List[str], 
    out_dir: str, 
    noise_suppressor: Segmenter,
    on_processed_callback: Callable[[str, Future], None] = default_callback, 
    paths_to_ignore: list = [],
) -> List[Future]:
    """
        Process a whole directory of audio files with the desired noise supressor.
        params:
        
        in_dir: 
            the directory to traverse, finding audios to suppress.
        
        out_dir:
            the directory to put the processed audios. The file hierarchy will look the same
            as the input directory, meaning that audios that are contained in subdirectories
            in the input will be contained in subdirectories with the same name in the output.
        
        noise_suppressor:
            an instance of the NoiseSuppressor class that contains how to process the audios.

        on_processed_callback:
            a function that receives two parameters: (file_path: string, future_result: concurrent.future.Future).
            You can use this to know when a file was processed, if a file was processed correctly, and more.
            See the default callback for a reference implementation.

        paths_to_ignore:
            list of paths or substrings to ignore when crawling to a directory. Example: ['log', '.avi', '.gitignore']
    """
    return process_directory_raw(in_dirs, out_dir, noise_suppressor.process_signal_file, on_processed_callback, paths_to_ignore)

def process_directory_raw(
    in_dirs: List[str], 
    out_dir: str, 
    f: Callable[[str, str], None], 
    on_processed_callback: Callable[[str, Future], None] = default_callback, 
    paths_to_ignore: list = [],
) -> List[Future]:
    """
        Process a whole directory of audio files with the desired function.
        params:
        
        in_dir: 
            the directory to traverse, finding audios to suppress.
        
        out_dir:
            the directory to put the processed audios. The file hierarchy will look the same
            as the input directory, meaning that audios that are contained in subdirectories
            in the input will be contained in subdirectories with the same name in the output.
        
        f:
            A function of type (str, str) -> None, that receives the source path and the destination path, and does
            whatever computation is necessary.

        on_processed_callback:
            a function that receives two parameters: (file_path: string, future_result: concurrent.future.Future).
            You can use this to know when a file was processed, if a file was processed correctly, and more.
            See the default callback for a reference implementation.

        paths_to_ignore:
            list of paths or substrings to ignore when crawling to a directory. Example: ['log', '.avi', '.gitignore']
    """
    if out_dir is not None:
        makedirs(out_dir, exist_ok=True)
    futures = []

    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        for source_path, dest_path in path_iterator(in_dirs, out_dir, paths_to_ignore):
            bound_callback = partial(on_processed_callback, source_path)
            future = pool.submit(f, source_path, dest_path)
            future.add_done_callback(bound_callback)
            futures.append(future)

    return futures

def count_directory(path):
    return path_iterator([path], None, [])