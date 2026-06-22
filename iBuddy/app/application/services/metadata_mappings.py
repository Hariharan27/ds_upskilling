from app.domain.enums.department import (
    Department,
)

from app.domain.enums.document_category import (
    DocumentCategory,
)


DOCUMENT_METADATA_MAPPING = {

    # ==========================
    # HR
    # ==========================

    "leave policy": (
        Department.HR,
        DocumentCategory.LEAVE,
    ),

    "work from home": (
        Department.HR,
        DocumentCategory.WFH,
    ),

    "employee benefits": (
        Department.HR,
        DocumentCategory.BENEFITS,
    ),

    "certification": (
        Department.HR,
        DocumentCategory.CERTIFICATION,
    ),

    "rewards": (
        Department.HR,
        DocumentCategory.REWARDS,
    ),

    "staff loan": (
        Department.HR,
        DocumentCategory.STAFF_LOAN,
    ),

    "team outing": (
        Department.HR,
        DocumentCategory.TEAM_OUTING,
    ),

    "holiday": (
        Department.HR,
        DocumentCategory.HOLIDAY,
    ),

    # ==========================
    # Corporate Governance
    # ==========================

    "code of conduct": (
        Department.CORPORATE_GOVERNANCE,
        DocumentCategory.CODE_OF_CONDUCT,
    ),

    "whistle blower": (
        Department.CORPORATE_GOVERNANCE,
        DocumentCategory.WHISTLE_BLOWER,
    ),

    "vendor onboarding": (
        Department.CORPORATE_GOVERNANCE,
        DocumentCategory.VENDOR_MANAGEMENT,
    ),

    "vendor performance": (
        Department.CORPORATE_GOVERNANCE,
        DocumentCategory.VENDOR_MANAGEMENT,
    ),

    # ==========================
    # IT Security
    # ==========================

    "access allocation": (
        Department.IT_SECURITY,
        DocumentCategory.ACCESS_MANAGEMENT,
    ),

    "access card": (
        Department.IT_SECURITY,
        DocumentCategory.ACCESS_MANAGEMENT,
    ),

    "registration and de-registration": (
        Department.IT_SECURITY,
        DocumentCategory.ACCESS_MANAGEMENT,
    ),

    "asset management": (
        Department.IT_SECURITY,
        DocumentCategory.ASSET_MANAGEMENT,
    ),

    "it policy": (
        Department.IT_SECURITY,
        DocumentCategory.ASSET_MANAGEMENT,
    ),

    "laptop": (
        Department.IT_SECURITY,
        DocumentCategory.ENDPOINT_SECURITY,
    ),

    "malware": (
        Department.IT_SECURITY,
        DocumentCategory.ENDPOINT_SECURITY,
    ),

    "password": (
        Department.IT_SECURITY,
        DocumentCategory.ENDPOINT_SECURITY,
    ),

    "physical security": (
        Department.IT_SECURITY,
        DocumentCategory.PHYSICAL_SECURITY,
    ),

    "data backup": (
        Department.IT_SECURITY,
        DocumentCategory.DATA_SECURITY,
    ),

    "encryption": (
        Department.IT_SECURITY,
        DocumentCategory.DATA_SECURITY,
    ),

    "secure development": (
        Department.IT_SECURITY,
        DocumentCategory.SECURE_DEVELOPMENT,
    ),

    "vulnerability": (
        Department.IT_SECURITY,
        DocumentCategory.VULNERABILITY_MANAGEMENT,
    ),

    "incident reporting": (
        Department.IT_SECURITY,
        DocumentCategory.INCIDENT_MANAGEMENT,
    ),

    "disaster recovery": (
        Department.IT_SECURITY,
        DocumentCategory.DISASTER_RECOVERY,
    ),

    "change management": (
        Department.IT_SECURITY,
        DocumentCategory.CHANGE_MANAGEMENT,
    ),

    "copyright": (
        Department.IT_SECURITY,
        DocumentCategory.COMPLIANCE,
    ),

    "internal audit": (
        Department.IT_SECURITY,
        DocumentCategory.COMPLIANCE,
    ),
}