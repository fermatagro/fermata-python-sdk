from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import UUID

from fermata._call import call_async
from fermata._generated.pipelines.api.fires import create_fire as _create_fire
from fermata._generated.pipelines.api.schedules import (
    get_schedule as _get_schedule,
)
from fermata._generated.pipelines.api.schedules import (
    list_schedules as _list_schedules,
)
from fermata._generated.pipelines.models.create_or_update_fire import CreateOrUpdateFire
from fermata._generated.pipelines.models.create_or_update_fire_arguments import CreateOrUpdateFireArguments
from fermata._generated.pipelines.models.models_fire_status import ModelsFireStatus
from fermata._generated.pipelines.models.models_schedule import ModelsSchedule
from fermata._generated.pipelines.models.models_schedule_scope import ModelsScheduleScope


class AsyncPipelines:
    def __init__(self, client: Any) -> None:
        self._c = client

    async def list_schedules(self) -> list[ModelsSchedule]:
        page = await call_async(_list_schedules.asyncio_detailed(client=self._c))
        return page.items

    async def get_schedule(self, schedule_id: str) -> ModelsSchedule:
        return await call_async(_get_schedule.asyncio_detailed(UUID(schedule_id), client=self._c))

    async def create_fire(
        self,
        fire_id: str,
        *,
        template_id: str,
        scope: str,
        scope_id: str,
        trigger_id: str,
        arguments: dict[str, Any] | None = None,
    ) -> None:
        args = CreateOrUpdateFireArguments()
        if arguments:
            args.additional_properties = arguments
        body = CreateOrUpdateFire(
            organization_id="",
            pipeline_template_id=UUID(template_id),
            trigger_id=UUID(trigger_id),
            scope=ModelsScheduleScope(scope),
            scope_id=UUID(scope_id),
            status=ModelsFireStatus.PENDING,
            arguments=args,
        )
        await call_async(_create_fire.asyncio_detailed(UUID(fire_id), body=body, client=self._c))


class SyncPipelines:
    def __init__(self, async_ns: AsyncPipelines, run: Callable[..., Any]) -> None:
        self._a = async_ns
        self._run = run

    def list_schedules(self) -> list[ModelsSchedule]:
        return self._run(self._a.list_schedules())

    def get_schedule(self, schedule_id: str) -> ModelsSchedule:
        return self._run(self._a.get_schedule(schedule_id))

    def create_fire(self, fire_id: str, **kw: Any) -> None:
        self._run(self._a.create_fire(fire_id, **kw))
