import sys
import json
import argparse
import time

import CloudFlare


cf = CloudFlare.CloudFlare(
    email="<CF_EMAIL>",
    token="<CF_TOKEN>"
)


def get_domains(retries):
    if not retries:
        sys.exit()

    zones = cf.zones.get(params = {"per_page":1000})

    domains = []

    for zone in zones:
        dns_records = cf.zones.dns_records.get(zone.get("id"))

        domains.extend(dns_records)

    if retries and not domains:
        time.sleep(60)
        get_domains(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(domains).encode("utf8"))
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domains", action="store_true")

    args = parser.parse_args()

    if args.domains:
        get_domains(retries=5)
