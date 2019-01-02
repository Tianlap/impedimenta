#!/usr/bin/env bash
# coding=utf-8
# Don't `set -e`. If one DDNS update can't be completed (that is, if one curl
# invocation fails), we still want to attempt the remaining DDNS updates.
set -uo pipefail

dynamic_dns_urls=(
    {% for dynamic_dns_url in dynamic_dns_urls %}
    '{{ dynamic_dns_url }}'
    {% endfor %}
)
for dynamic_dns_url in "${dynamic_dns_urls[@]}"; do
    curl --silent --show-error "$dynamic_dns_url" 1>/dev/null
done
