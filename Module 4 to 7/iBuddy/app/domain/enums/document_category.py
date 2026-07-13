from enum import Enum


class DocumentCategory(str, Enum):

    # HR

    LEAVE = "leave"

    WFH = "wfh"

    BENEFITS = "benefits"

    CERTIFICATION = "certification"

    REWARDS = "rewards"

    STAFF_LOAN = "staff_loan"

    TEAM_OUTING = "team_outing"

    HOLIDAY = "holiday"

    # Corporate Governance

    CODE_OF_CONDUCT = (
        "code_of_conduct"
    )

    WHISTLE_BLOWER = (
        "whistle_blower"
    )

    VENDOR_MANAGEMENT = (
        "vendor_management"
    )

    # IT Security

    ACCESS_MANAGEMENT = (
        "access_management"
    )

    ASSET_MANAGEMENT = (
        "asset_management"
    )

    ENDPOINT_SECURITY = (
        "endpoint_security"
    )

    PHYSICAL_SECURITY = (
        "physical_security"
    )

    DATA_SECURITY = (
        "data_security"
    )

    SECURE_DEVELOPMENT = (
        "secure_development"
    )

    VULNERABILITY_MANAGEMENT = (
        "vulnerability_management"
    )

    INCIDENT_MANAGEMENT = (
        "incident_management"
    )

    DISASTER_RECOVERY = (
        "disaster_recovery"
    )

    CHANGE_MANAGEMENT = (
        "change_management"
    )

    COMPLIANCE = (
        "compliance"
    )