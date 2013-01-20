import soundcloud
import argparse

client = soundcloud.Client(client_id='f1f354c01efa3a43d6c7c01d8f6d455e')

parser = argparse.ArgumentParser(description='Perform a search on soundcloud & download the results')
parser.add_argument('-searchString', dest="search_string",
                   help='a folder containing audio files to analyse')
parser.add_argument('-destination', dest="dest_folder",
                   help='a folder where the audio files are output')

args = parser.parse_args()

search_results = client.get('/tracks', q='bass')

print search_results