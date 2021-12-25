import sys
import json
import argparse

from aliyunsdkcore.client import AcsClient
from aliyunsdksas.request.v20181203 import DescribeAllEntityRequest
from aliyunsdksas.request.v20181203 import DescribeExposedInstanceListRequest
from aliyunsdksas.request.v20181203 import DescribeVulListRequest
from aliyunsdksas.request.v20181203 import DescribeDomainListRequest
from aliyunsdksas.request.v20181203 import DescribeDomainDetailRequest
from aliyunsdksas.request.v20181203 import DescribeGroupedContainerInstancesRequest
from aliyunsdksas.request.v20181203 import DescribeCloudCenterInstancesRequest


client = AcsClient("<ALI_KEY>", "<ALI_SECRET>", connect_timeout=60, timeout=60)


def request_by_pages(request):
    response = client.do_action_with_exception(request).decode("utf-8")

    yield response

    response_obj = json.loads(response)

    if response_obj.get("PageInfo"):
        total_count = response_obj.get("PageInfo").get("TotalCount")
        page_size = response_obj.get("PageInfo").get("PageSize")
    else:
        total_count = response_obj.get("TotalCount")
        page_size = response_obj.get("PageSize")

    pages_num = (
        (total_count // page_size) + 1
        if (total_count % page_size) > 0
        else (total_count // page_size)
    )

    for page in range(2, pages_num + 1):
        request.set_CurrentPage(page)

        yield client.do_action_with_exception(request).decode("utf-8")


def get_cloud_products():
    request = DescribeCloudCenterInstancesRequest.DescribeCloudCenterInstancesRequest()

    cloud_products = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        cloud_products.extend(response_page_obj.get("Instances"))

    sys.stdout.buffer.write(json.dumps(cloud_products).encode("utf8"))


def get_containers():
    request = (
        DescribeGroupedContainerInstancesRequest.DescribeGroupedContainerInstancesRequest()
    )

    request.set_GroupField("pod")

    containers = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        containers.extend(response_page_obj.get("GroupedContainerInstanceList"))

    sys.stdout.buffer.write(json.dumps(containers).encode("utf8"))


def get_domains():
    request_list = DescribeDomainListRequest.DescribeDomainListRequest()

    domains_list = []

    for response_page in request_by_pages(request_list):
        response_page_obj = json.loads(response_page)

        domains_list.extend(response_page_obj.get("DomainListResponseList"))

    domains_details = []

    for item in domains_list:
        for _, v in item.items():
            request_domain = DescribeDomainDetailRequest.DescribeDomainDetailRequest()

            request_domain.set_DomainName(v)

            response_domain = client.do_action_with_exception(request_domain).decode(
                "utf-8"
            )
            response_domain_obj = json.loads(response_domain)

            domains_details.append(response_domain_obj)

    sys.stdout.buffer.write(json.dumps(domains_details).encode("utf8"))


def get_exposed_instances():
    request = DescribeExposedInstanceListRequest.DescribeExposedInstanceListRequest()

    exposed = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        exposed.extend(response_page_obj.get("ExposedInstances"))

    sys.stdout.buffer.write(json.dumps(exposed).encode("utf8"))


def get_servers():
    request = DescribeAllEntityRequest.DescribeAllEntityRequest()

    response = client.do_action_with_exception(request).decode("utf-8")
    response_obj = json.loads(response)

    servers = response_obj.get("EntityList")

    sys.stdout.buffer.write(json.dumps(servers).encode("utf8"))


def get_vulns():
    vuln_types = ["cve", "sys", "cms", "app", "emg", "sca"]

    vulns = []

    for type in vuln_types:
        request = DescribeVulListRequest.DescribeVulListRequest()

        request.set_Type(type)

        for response_page in request_by_pages(request):
            response_page_obj = json.loads(response_page)

            vulns.extend(response_page_obj.get("VulRecords"))

    sys.stdout.buffer.write(json.dumps(vulns).encode("utf8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cloud-products", action="store_true")
    parser.add_argument("--containers", action="store_true")
    parser.add_argument("--domains", action="store_true")
    parser.add_argument("--exposed-instances", action="store_true")
    parser.add_argument("--servers", action="store_true")
    parser.add_argument("--vulns", action="store_true")

    args = parser.parse_args()

    if args.cloud_products:
        get_cloud_products()

    if args.containers:
        get_containers()

    if args.domains:
        get_domains()

    if args.exposed_instances:
        get_exposed_instances()

    if args.servers:
        get_servers()

    if args.vulns:
        get_vulns()
