import json
import argparse
import sys
import time

import boto3

CREDENTIALS = [{
    "id": "<AWS_ID>",
    "secret": "<AWS_KEY>",
}]


def get_route53_zones(client):
    response = client.list_hosted_zones().get("HostedZones")

    zones = []

    for zone in response:
        info = {}

        info.update(zone.get("Config"))
        info.update({"Id": zone.get("Id").split('/')[2]})

        zones.append(info)

    return zones


def get_route53_zone_records(client, zone, next_record=None):
    if next_record:
        response = client.list_resource_record_sets(
            HostedZoneId=zone.get("Id"),
            StartRecordName=next_record[0],
            StartRecordType=next_record[1])

    else:
        response = client.list_resource_record_sets(
            HostedZoneId=zone.get("Id"))

    resource_records_extended = []

    resource_records = response.get("ResourceRecordSets")

    for rr in resource_records:
        rr.update({"ZoneInfo": zone})

        resource_records_extended.append(rr)

    if response["IsTruncated"]:
        resource_records_extended += get_route53_zone_records(
            client, zone,
            (response['NextRecordName'], response['NextRecordType']))

    return resource_records_extended


def get_route53_records(retries):
    if not retries:
        sys.exit()

    records = []

    for item in CREDENTIALS:
        client = boto3.client(
            "route53",
            aws_access_key_id=item.get("id"),
            aws_secret_access_key=item.get("secret"),
        )

        zones = get_route53_zones(client)

        for zone in zones:
            records.extend(get_route53_zone_records(client, zone))

    if retries and not records:
        time.sleep(60)
        get_route53_records(retries-1)
    else:
        print(json.dumps(records))
        sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--route53-records", action="store_true")

    args = parser.parse_args()

    if args.route53_records:
        get_route53_records(retries=5)
