import sys
import json
import argparse
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdksas.request.v20181203 import DescribeAllEntityRequest
from aliyunsdksas.request.v20181203 import DescribeExposedInstanceListRequest
from aliyunsdksas.request.v20181203 import DescribeVulListRequest
from aliyunsdksas.request.v20181203 import DescribeDomainListRequest
from aliyunsdksas.request.v20181203 import DescribeDomainDetailRequest
from aliyunsdksas.request.v20181203 import DescribeGroupedContainerInstancesRequest
from aliyunsdksas.request.v20181203 import DescribeCloudCenterInstancesRequest


client = AcsClient(
    "<ALI_ID>",
    "<ALI_SECRET>",
    connect_timeout=60,
    timeout=60
)


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

    pages_num = (total_count // page_size) + 1 if (total_count %
                                                   page_size) > 0 else (total_count // page_size)

    for page in range(2, pages_num + 1):
        request.set_CurrentPage(page)

        yield client.do_action_with_exception(request).decode("utf-8")


def get_cloud_products(retries):
    if not retries:
        sys.exit()

    request = DescribeCloudCenterInstancesRequest.DescribeCloudCenterInstancesRequest()

    cloud_products = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        cloud_products.extend(response_page_obj.get("Instances"))

    if retries and not cloud_products:
        time.sleep(60)
        get_cloud_products(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(cloud_products).encode("utf8"))
        sys.exit()


def get_containers(retries):
    if not retries:
        sys.exit()

    request = DescribeGroupedContainerInstancesRequest.DescribeGroupedContainerInstancesRequest()

    request.set_GroupField("pod")

    containers = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        containers.extend(response_page_obj.get(
            "GroupedContainerInstanceList"))

    if retries and not containers:
        time.sleep(60)
        get_containers(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(containers).encode("utf8"))
        sys.exit()


def get_domains(retries):
    if not retries:
        sys.exit()

    request_list = DescribeDomainListRequest.DescribeDomainListRequest()

    domains_list = []

    for response_page in request_by_pages(request_list):
        response_page_obj = json.loads(response_page)

        domains_list.extend(response_page_obj.get(
            "DomainListResponseList"))

    domains_details = []

    for item in domains_list:
        for _, v in item.items():
            request_domain = DescribeDomainDetailRequest.DescribeDomainDetailRequest()

            request_domain.set_DomainName(v)

            response_domain = client.do_action_with_exception(
                request_domain).decode("utf-8")
            response_domain_obj = json.loads(response_domain)

            domains_details.append(response_domain_obj)

    if retries and not domains_details:
        time.sleep(60)
        get_domains(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(domains_details).encode("utf8"))
        sys.exit()


def get_exposed_instances(retries):
    if not retries:
        sys.exit()

    request = DescribeExposedInstanceListRequest.DescribeExposedInstanceListRequest()

    exposed = []

    for response_page in request_by_pages(request):
        response_page_obj = json.loads(response_page)

        exposed.extend(response_page_obj.get("ExposedInstances"))

    if retries and not exposed:
        time.sleep(60)
        get_exposed_instances(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(exposed).encode("utf8"))
        sys.exit()


def get_servers(retries):
    if not retries:
        sys.exit()

    request = DescribeAllEntityRequest.DescribeAllEntityRequest()

    response = client.do_action_with_exception(request).decode("utf-8")
    response_obj = json.loads(response)

    servers = response_obj.get("EntityList")

    if retries and not servers:
        time.sleep(60)
        get_servers(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(servers).encode("utf8"))
        sys.exit()


def get_vulns(retries):
    if not retries:
        sys.exit()

    vuln_types = ["cve", "sys", "cms", "app", "emg", "sca"]

    vulns = []

    for type in vuln_types:
        request = DescribeVulListRequest.DescribeVulListRequest()

        request.set_Type(type)

        for response_page in request_by_pages(request):
            response_page_obj = json.loads(response_page)

            vulns.extend(response_page_obj.get("VulRecords"))

    if retries and not vulns:
        time.sleep(60)
        get_vulns(retries-1)
    else:
        sys.stdout.buffer.write(json.dumps(vulns).encode("utf8"))
        sys.exit()


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
        get_cloud_products(retries=5)

    if args.containers:
        get_containers(retries=5)

    if args.domains:
        get_domains(retries=5)

    if args.exposed_instances:
        get_exposed_instances(retries=5)

    if args.servers:
        get_servers(retries=5)

    if args.vulns:
        get_vulns(retries=5)
