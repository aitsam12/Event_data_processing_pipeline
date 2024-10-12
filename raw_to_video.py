import argparse
import os
from metavision_hal import DeviceDiscovery
from metavision_designer_engine import Controller, KeyboardEvent
from metavision_designer_core import HalDeviceInterface, CdProducer, FrameGenerator, VideoWriter

def parse_arguments():
    """
    Parses input arguments to capture the input RAW file and the desired output video file path.
    """
    description = ("Generate an AVI video from a RAW file using the Metavision Designer Python API. "
                   "This script converts event-based RAW files into standard AVI format.")

    parser = argparse.ArgumentParser(description=description, 
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input', required=True, 
                        help='Path to the input RAW file.')
    parser.add_argument('-o', '--output', 
                        help='Path to the output AVI file. If not specified, the input file name will be used.')

    return parser.parse_args()

def verify_file(file_path):
    """
    Verifies that the provided file path exists and is a valid file.
    """
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        print(f"Error: The provided file '{file_path}' does not exist or is not a valid file.")
        return False
    return True

def setup_output_filename(input_file, output_file):
    """
    Sets up the output filename. If not provided, the base name of the input file is used.
    """
    if output_file:
        return output_file
    return f"{os.path.splitext(input_file)[0]}.avi"

def process_raw_to_video(input_file, output_file):
    """
    Main logic for processing the RAW file and converting it into an AVI video.
    """
    device = DeviceDiscovery.open_raw_file(input_file)
    if not device:
        print(f"Error: Could not open file '{input_file}'.")
        return False

    i_events_stream = device.get_i_events_stream()
    i_events_stream.start()

    controller = Controller()
    hal_device_interface = HalDeviceInterface(device)
    controller.add_device_interface(hal_device_interface)

    prod_cd = CdProducer(hal_device_interface)
    controller.add_component(prod_cd)

    frame_generator = FrameGenerator(prod_cd)
    frame_generator.set_name("Event Frame Generator")
    controller.add_component(frame_generator)

    video_writer = VideoWriter(frame_generator, output_file, fps=50.0)
    controller.add_component(video_writer)
    video_writer.enable(True)

    controller.add_renderer(video_writer, Controller.RenderingMode.SimulationClock, 50.0)
    controller.enable_rendering(True)
    controller.set_slice_duration(10000)
    controller.set_batch_duration(100000)

    print(f"Generating video: {output_file}")
    while not controller.is_done():
        last_key = controller.get_last_key_pressed()
        if last_key == ord('q') or last_key == KeyboardEvent.Symbol.Escape:
            break
        controller.run(False)

    return True

def main():
    """
    Main entry point for the script. Handles argument parsing, file validation, and starts the processing.
    """
    args = parse_arguments()

    if not verify_file(args.input):
        return 1

    output_video = setup_output_filename(args.input, args.output)

    if not process_raw_to_video(args.input, output_video):
        return 1

    print(f"Video generated successfully at {output_video}")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())

