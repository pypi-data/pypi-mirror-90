from vkwave.types.extension_responses import ExecuteResponse

from ._category import Category


class Execute(Category):
    async def __call__(self, code: str, return_raw_response: bool = False, **kwargs):
        params = {"code": code}
        params.update(**kwargs)

        raw_result = await self.api_request("", params=params)
        if return_raw_response:
            return raw_result

        result = ExecuteResponse(**raw_result)
        return result
