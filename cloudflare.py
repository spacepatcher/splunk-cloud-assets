import sys
import json
import argparse

import CloudFlare


cf = CloudFlare.CloudFlare(email="<CF_EMAIL>", token="<CF_TOKEN>")


def get_domains():
    zones = cf.zones.get()

    sys.stdout.buffer.write(json.dumps(zones).encode("utf8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domains", action="store_true")

    args = parser.parse_args()

    if args.domains:
        get_domains()
