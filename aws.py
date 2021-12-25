import json
import argparse

import boto3


client = boto3.client(
    "route53",
    aws_access_key_id="<AWS_ID>",
    aws_secret_access_key="<AWS_KEY>",
)


def get_route53_zones():
    zones = client.list_hosted_zones().get("HostedZones")

    zones_id = []

    for item in zones:
        zones_id.append(item.get("Id").split("/")[2])

    return zones_id


def get_route53_records():
    zones_id = get_route53_zones()

    records = []

    for item in zones_id:
        zone_record = client.list_resource_record_sets(
            HostedZoneId=item, MaxItems="300"
        )

        records.extend(zone_record.get("ResourceRecordSets"))

    print(json.dumps(records))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--route53-records", action="store_true")

    args = parser.parse_args()

    if args.route53_records:
        get_route53_records()
