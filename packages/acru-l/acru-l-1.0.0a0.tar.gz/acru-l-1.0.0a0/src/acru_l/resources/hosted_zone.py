from typing import Optional

from aws_cdk import (
    core,
    aws_route53 as route53,
)


class HostedZone(core.Construct):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        *,
        domain_name: str,
        export_name: str = "HostedZoneId",
        use_github_pages: bool = False,
        github_username: Optional[str] = None,
        github_cname: Optional[str] = None,
    ):
        super().__init__(scope, id)

        self.hosted_zone = route53.HostedZone(
            self, "HostedZone", zone_name=domain_name
        )
        # Usage: core.Fn.import_value(export_name)
        core.CfnOutput(
            self,
            "HostedZoneId",
            value=self.hosted_zone.hosted_zone_id,
            export_name=export_name,
        )

        if use_github_pages:
            if (
                github_username
                and github_cname
                and github_cname != domain_name
            ):
                # for subdomains of the apex
                route53.CnameRecord(
                    self,
                    "GithubPagesRecord",
                    zone=self.hosted_zone,
                    record_name=f"{github_cname}.",
                    domain_name=f"{github_username}.github.io.",
                )
            else:
                # for when you want to use the apex domain on github pages
                route53.ARecord(
                    self,
                    "GithubPagesRecord",
                    zone=self.hosted_zone,
                    record_name=f"{domain_name}.",
                    target=route53.RecordTarget.from_ip_addresses(
                        "185.199.108.153",
                        "185.199.109.153",
                        "185.199.110.153",
                        "185.199.111.153",
                    ),
                )
                route53.CnameRecord(
                    self,
                    "WWWRecord",
                    zone=self.hosted_zone,
                    record_name=f"www.{domain_name}.",
                    domain_name=f"{domain_name}.",
                )
