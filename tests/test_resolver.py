import json

import pytest

from handler import handle_request

test_payload = [
    {
        'event': 'default.json',
        'expected_result': {
            "order": "desc",
            "order_by": "risk_score",
            "total": 33,
            "start_from": 0,
            "size": 10,
            "results": [
                "KB4586823: Windows 8.1 and Windows Server 2012 R2 November 2020 Security Update",
                "Exposure of Application source code, config files and credentials",
                "Unsupported Cisco Operating System",
                "JBoss Java Object Deserialization RCE",
                "VMware ESX / ESXi Multiple Vulnerabilities (VMSA-2012-0005) (BEAST) (remote check)",
                "Insecure Kentico version 8.1 is running",
                "Docker remote API detection",
                "Mozilla Firefox ESR < 78.6",
                "Password Spraying Attack",
                "Google Chrome < 87.0.4280.88 Multiple Vulnerabilities"
            ]
        },
    },
    {
        'event': 'sorted.json',
        'expected_result': {
            "order": "asc",
            "order_by": "vulnerability",
            "total": 33,
            "start_from": 0,
            "size": 10,
            "results": [
                "Apache OpenOffice < 4.1.8 Arbitrary Code Execution",
                "Apache Struts2 Remote Command Execution",
                "Bind Shell Backdoor Detection",
                "Docker remote API detection",
                "Exposure of Application source code, config files and credentials",
                "Exposure of Application source code, config files and credentials",
                "File Content Disclosure /etc/passwd",
                "File Content Disclosure /etc/passwd",
                "Google Chrome < 87.0.4280.66 Multiple Vulnerabilities",
                "Google Chrome < 87.0.4280.88 Multiple Vulnerabilities"
            ]
        }
    },
    {
        'event': 'paginated.json',
        'expected_result': {
            "order": "desc",
            "order_by": "risk_score",
            "total": 33,
            "start_from": 20,
            "size": 5,
            "results": [
                "KB4586805: Windows 7 and Windows Server 2008 R2 November 2020 Security Update",
                "Oracle WebLogic Server Plug-in Remote Overflow (1166189)",
                "Oracle Error Log Found",
                "Unrestricted File Upload",
                "File Content Disclosure /etc/passwd"
            ]
        }
    }
]


@pytest.mark.parametrize('payload', test_payload)
def test_should_get_temporary_redirect(payload, json_loader, env_variables):
    event = json_loader(payload['event'])

    result = handle_request(event, {})
    assert result['statusCode'] == 200
    assert result['body'] == json.dumps(payload['expected_result'])
