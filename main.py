from common import NoiseSuppressor, process_directory

def main():
    from multiprocessing import cpu_count
    from concurrent.futures import ProcessPoolExecutor
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='A tool to reduce noise, clip, and mark Praat\'s TextGrids of voice audios.\n' +
                    'This tool is/was used for the SPIRA project.',
        usage='%(prog)s [options] DEST_DIR SOURCE_DIR [SOURCE_DIR ...]',
    )
    parser.set_defaults(noise_suppress=False, generate_textgrid=False, workers=2 * cpu_count())

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--noise-suppress', help='activates noise suppression for the audio processing', action='store_true')
    parser.add_argument('--generate-textgrid', help='generate a noise-signal textgrid for each audio', action='store_true')
    parser.add_argument('--workers', help='parallelize up to max amount of workers', type=int)

    parser.add_argument('dest_dir', help='directory to save all processed audio')
    parser.add_argument('source_dir', help='directories to search for audios to process', nargs='+')

    args = parser.parse_args()

    output_path = args.dest_dir.rstrip('/')
    noiseprocessor = NoiseSuppressor(noise_suppress=args.noise_suppress, generate_textgrid=args.generate_textgrid)

    process_directory(args.source_dir, output_path, noiseprocessor)
    return 0

if __name__ == '__main__':
    from sys import exit
    exit(main())
