import argparse
import csv
import json
import sys

def load_input(input):
    with open(input, 'r') as f:
        return json.load(f)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-p', '--prefix', type=str, default='')
    args = parser.parse_args(argv)

    print(f'Converting {args.input} to {args.output}...')

    data = load_input(args.input)["data"]
    with open(args.output, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['url', 'type', 'username', 'password', 'hostname', 'extra', 'name', 'grouping'])
        for k, v in data.items():
            if not "url" in v and not "service" in v:
                print(f'Key {k} : no URL or service; skipping')
                continue

            # I'll import things without a URL into a 'no-url' group to help me fix
            # them up inside LastPass.
            has_url = len(v.get('url', '')) > 0
            csv_writer.writerow([
                # URL
                v.get('url', ''),

                # Type
                '',

                # Username
                v.get('username', ''),

                # Password
                v.get('password', ''),

                # Hostname
                '',

                # Extra
                # TODO : I'll add the notes here -- will this import decently?
                v.get('notes', ''),

                # Name
                v.get('service', v.get('url', '')),

                # Grouping
                args.prefix + ('no-url' if not has_url else v.get('style', 'other')),
            ])

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
