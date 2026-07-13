from fastapi import Depends

from app.domain.services.date_provider import (
    DateProvider,
)
from app.domain.services.hrms_rest_client import (
    HRMSRestClient,
)
from app.infrastructure.rest.hrms_rest_client import (
    HRMSRestClientImpl,
)
from app.infrastructure.rest.mappers.apply_leave_request_mapper import ApplyLeaveRequestMapper
from app.infrastructure.rest.mappers.apply_leave_response_mapper import ApplyLeaveResponseMapper
from app.infrastructure.rest.mappers.leave_details_request_mapper import (
    LeaveDetailsRequestMapper,
)
from app.infrastructure.system.system_date_provider import (
    SystemDateProvider,
)


def get_date_provider() -> DateProvider:

    return SystemDateProvider()


def get_hrms_rest_client() -> HRMSRestClient:

    return HRMSRestClientImpl()


def get_leave_details_request_mapper(
    date_provider: DateProvider = Depends(
        get_date_provider,
    ),
) -> LeaveDetailsRequestMapper:

    return LeaveDetailsRequestMapper(
        date_provider=date_provider,
    )

def get_apply_leave_request_mapper() -> ApplyLeaveRequestMapper:
    return ApplyLeaveRequestMapper()

def get_apply_leave_response_mapper() -> ApplyLeaveResponseMapper:
    return ApplyLeaveResponseMapper()