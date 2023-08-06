from pydiator_core.interfaces import BaseRequest, BasePipeline, BaseCacheable, CacheType, BaseCacheProvider
from pydiator_core.serializer import SerializerFactory


class CachePipeline(BasePipeline):
    def __init__(self, cache_provider: BaseCacheProvider) -> None:
        self.cache_provider = cache_provider

    async def handle(self, req: BaseRequest) -> object:
        if self.next() is None:
            raise Exception("pydiator_cache_pipeline_has_no_next_pipeline")

        response = None

        if isinstance(req, BaseCacheable):
            if req.is_no_cache() is False:
                cache_key = req.get_cache_key()
                if cache_key is not None and cache_key != "":
                    cache_type = req.get_cache_type()
                    if cache_type == CacheType.DISTRIBUTED:
                        cached_obj = self.__get_from_cache(cache_key)
                        if cached_obj is not None:
                            return cached_obj

                    cache_duration = req.get_cache_duration()
                    response = await self.next().handle(req)
                    if response is not None and response != "" and cache_duration > 0:
                        self.__add_to_cache(response, cache_key, cache_duration)

        if response is None:
            response = await self.next().handle(req)

        return response

    def __get_from_cache(self, cache_key) -> object:
        cached_obj_str = self.cache_provider.get(cache_key)
        if cached_obj_str is not None:
            return self.__get_serializer().loads(cached_obj_str)

        return None

    def __add_to_cache(self, res: object, cache_key, cache_duration):
        res_value_obj = self.__get_serializer().dumps(res)
        if res_value_obj is not None:
            self.cache_provider.add(cache_key, res_value_obj, cache_duration)

    @staticmethod
    def __get_serializer():
        return SerializerFactory.get_serializer()
